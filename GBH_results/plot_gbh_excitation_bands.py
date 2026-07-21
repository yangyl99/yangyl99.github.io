#!/usr/bin/env python3
"""Plot selected excitation bands from GBH.out files.

The default command draws one sample figure.  The same parser and selector can
later be used for batch generation over every GBH.out in the tree.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv
import math
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache").resolve()))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(".cache").resolve()))

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.patches import FancyArrowPatch
from matplotlib.ticker import AutoMinorLocator, NullFormatter


State = tuple[int, int]


@dataclass(frozen=True)
class Level:
    spin: int
    index: int
    energy_mev: float


@dataclass(frozen=True)
class Band:
    name: str
    states: tuple[State, ...]
    edges: tuple[tuple[State, State, float], ...]


LEVEL_HEADER_RE = re.compile(r"^\s*I=\s*(\d+)\b")
LEVEL_RE = re.compile(r"^\s*(\d+)\s+(\d+)\s+([-+]?\d+(?:\.\d*)?(?:[Ee][-+]?\d+)?)\s*$")
E2_RE = re.compile(
    r"^\s*\(\s*(\d+)\s+(\d+)\)\s*<-->\s*"
    r"\(\s*(\d+)\s+(\d+)\)\s+"
    r"([-+]?\d+(?:\.\d*)?(?:[Ee][-+]?\d+)?)\s+"
    r"([-+]?\d+(?:\.\d*)?(?:[Ee][-+]?\d+)?)\s+"
    r"([-+]?\d+(?:\.\d*)?(?:[Ee][-+]?\d+)?)\s+WU\s+"
    r"([-+]?\d+(?:\.\d*)?(?:[Ee][-+]?\d+)?)\s+"
    r"([-+]?\d+(?:\.\d*)?(?:[Ee][-+]?\d+)?)\s*$"
)


def parse_gbh(path: Path) -> tuple[dict[State, Level], dict[tuple[State, State], float]]:
    """Parse levels and directional E2 strengths from one GBH.out."""
    text = path.read_text(errors="replace").splitlines()
    levels: dict[State, Level] = {}
    transitions: dict[tuple[State, State], float] = {}

    in_levels = False
    in_e2 = False
    current_spin: int | None = None

    for line in text:
        if "********* BEGIN LEVELS" in line:
            in_levels = True
            continue
        if "********* END LEVELS" in line:
            in_levels = False
            current_spin = None
            continue
        if "E2 transition" in line:
            in_e2 = True
            continue
        if in_e2 and line.strip().startswith("quadrupole shape invariant"):
            in_e2 = False

        if in_levels:
            header = LEVEL_HEADER_RE.match(line)
            if header:
                current_spin = int(header.group(1))
                continue
            match = LEVEL_RE.match(line)
            if match and current_spin is not None:
                spin = int(match.group(1))
                index = int(match.group(2))
                energy_mev = float(match.group(3))
                if spin == current_spin:
                    levels[(spin, index)] = Level(spin, index, energy_mev)

        if in_e2:
            match = E2_RE.match(line)
            if not match:
                continue
            spin1, index1, spin2, index2 = map(int, match.group(1, 2, 3, 4))
            state1 = (spin1, index1)
            state2 = (spin2, index2)
            transitions[(state1, state2)] = float(match.group(8))
            transitions[(state2, state1)] = float(match.group(9))

    return levels, transitions


def energy_kev(levels: dict[State, Level], state: State, reference: State = (0, 1)) -> float:
    return 1000.0 * (levels[state].energy_mev - levels[reference].energy_mev)


def transition_strength(
    transitions: dict[tuple[State, State], float],
    source: State,
    target: State,
) -> float | None:
    strength = transitions.get((source, target))
    if strength is None:
        return None
    return abs(strength)


def energy_ordered_transition(
    levels: dict[State, Level],
    transitions: dict[tuple[State, State], float],
    state_a: State,
    state_b: State,
) -> tuple[State, State, float] | None:
    """Return the high-energy to low-energy transition for a state pair."""
    energy_a = levels[state_a].energy_mev
    energy_b = levels[state_b].energy_mev
    if energy_a >= energy_b:
        source, target = state_a, state_b
    else:
        source, target = state_b, state_a
    strength = transition_strength(transitions, source=source, target=target)
    if strength is None:
        return None
    return source, target, strength


def require_energy_ordered_transition(
    levels: dict[State, Level],
    transitions: dict[tuple[State, State], float],
    state_a: State,
    state_b: State,
) -> tuple[State, State, float]:
    edge = energy_ordered_transition(levels, transitions, state_a, state_b)
    if edge is None:
        raise ValueError(f"No E2 transition found between {state_a} and {state_b}")
    return edge


def candidate_states(levels: dict[State, Level], spin: int, used: set[State]) -> list[State]:
    return [
        (spin, index)
        for index in range(1, 5)
        if (spin, index) in levels and (spin, index) not in used
    ]


def choose_max_be2(
    levels: dict[State, Level],
    transitions: dict[tuple[State, State], float],
    lower: State,
    target_spin: int,
    candidates: Iterable[State],
) -> tuple[State, tuple[State, State, float]]:
    scored: list[tuple[float, int, State, tuple[State, State, float]]] = []
    for state in candidates:
        if state[0] != target_spin:
            continue
        selection_strength = transition_strength(transitions, source=state, target=lower)
        if selection_strength is None:
            continue
        edge = energy_ordered_transition(levels, transitions, state, lower)
        if edge is None:
            continue
        # Stable tie break: larger B(E2), then lower state index.
        scored.append((selection_strength, -state[1], state, edge))
    if not scored:
        raise ValueError(f"No E2 transition found from candidates J={target_spin} to {lower}")
    _strength, _tie, state, edge = max(scored)
    return state, edge


def extends_upward_in_energy(levels: dict[State, Level], state: State, reference_state: State) -> bool:
    return levels[state].energy_mev > levels[reference_state].energy_mev


def select_bands(
    levels: dict[State, Level],
    transitions: dict[tuple[State, State], float],
) -> list[Band]:
    required_spins = (0, 2, 3, 4, 5, 6)
    required = [(spin, index) for spin in required_spins for index in range(1, 5)]
    missing = [state for state in required if state not in levels]
    if missing:
        raise ValueError(f"Missing required levels: {missing[:8]}")

    used: set[State] = set()
    bands: list[Band] = []

    for band_index, head in enumerate(((0, 1), (0, 2)), start=1):
        states = [head]
        edges: list[tuple[State, State, float]] = []
        used.add(head)
        lower = head
        for spin in (2, 4, 6):
            state, edge = choose_max_be2(
                levels,
                transitions,
                lower=lower,
                target_spin=spin,
                candidates=candidate_states(levels, spin, used),
            )
            if not extends_upward_in_energy(levels, state, lower):
                break
            states.append(state)
            edges.append(edge)
            used.add(state)
            lower = state
        bands.append(Band(name=f"band{band_index}", states=tuple(states), edges=tuple(edges)))

    remaining_2 = candidate_states(levels, 2, used)
    if len(remaining_2) < 1:
        raise ValueError("No unused 2+ state remains for band3")
    head3 = min(remaining_2, key=lambda state: (levels[state].energy_mev, state[1]))
    used.add(head3)

    states3 = [head3]
    edges3: list[tuple[State, State, float]] = []
    band3_reference = head3
    for spin in (3, 4):
        state, edge = choose_max_be2(
            levels,
            transitions,
            lower=head3,
            target_spin=spin,
            candidates=candidate_states(levels, spin, used),
        )
        if not extends_upward_in_energy(levels, state, band3_reference):
            break
        states3.append(state)
        edges3.append(edge)
        used.add(state)
        band3_reference = state

    selected_3 = next((state for state in states3 if state[0] == 3), None)
    selected_4 = next((state for state in states3 if state[0] == 4), None)
    if selected_4 is not None:
        band3_reference = selected_4
        for spin in (5, 6):
            state, edge = choose_max_be2(
                levels,
                transitions,
                lower=selected_4,
                target_spin=spin,
                candidates=candidate_states(levels, spin, used),
            )
            if not extends_upward_in_energy(levels, state, band3_reference):
                break
            states3.append(state)
            edges3.append(edge)
            used.add(state)
            band3_reference = state

    selected_5 = next((state for state in states3 if state[0] == 5), None)
    selected_6 = next((state for state in states3 if state[0] == 6), None)
    extra_edges = []
    if selected_3 is not None and selected_4 is not None:
        extra_edges.append((selected_4, selected_3))
    if selected_5 is not None and selected_6 is not None:
        extra_edges.append((selected_6, selected_5))
    if selected_3 is not None and selected_5 is not None:
        extra_edges.append((selected_5, selected_3))
    for state_a, state_b in extra_edges:
        edge = energy_ordered_transition(levels, transitions, state_a, state_b)
        if edge is not None:
            edges3.append(edge)

    bands.append(Band(name="band3", states=tuple(states3), edges=tuple(edges3)))
    return bands


def trim_bands_at_two_if_higher_spin_drops(levels: dict[State, Level], bands: list[Band]) -> list[Band]:
    trimmed_bands: list[Band] = []
    for band in bands:
        two_states = [state for state in band.states if state[0] == 2]
        if not two_states:
            trimmed_bands.append(band)
            continue
        two_state = two_states[0]
        two_energy = levels[two_state].energy_mev
        should_trim = any(
            state[0] in (4, 6) and levels[state].energy_mev < two_energy
            for state in band.states
        )
        if not should_trim:
            trimmed_bands.append(band)
            continue
        kept_states = tuple(state for state in band.states if state[0] <= 2)
        kept = set(kept_states)
        kept_edges = tuple(edge for edge in band.edges if edge[0] in kept and edge[1] in kept)
        trimmed_bands.append(Band(name=band.name, states=kept_states, edges=kept_edges))
    return trimmed_bands


def build_interband_edges(
    levels: dict[State, Level],
    transitions: dict[tuple[State, State], float],
    bands: list[Band],
) -> tuple[tuple[State, State, float], ...]:
    if len(bands) < 3:
        return ()
    band1_head = bands[0].states[0]
    band2_head = bands[1].states[0]
    band3_head = bands[2].states[0]
    band1_two = next((state for state in bands[0].states if state[0] == 2), None)
    if band1_two is None:
        return ()

    requested_pairs = (
        (band3_head, band1_head),
        (band3_head, band1_two),
        (band3_head, band2_head),
        (band2_head, band1_two),
    )
    edges: list[tuple[State, State, float]] = []
    seen: set[tuple[State, State]] = set()
    for state_a, state_b in requested_pairs:
        edge = energy_ordered_transition(levels, transitions, state_a, state_b)
        if edge is None:
            continue
        source, target, _strength = edge
        if source == target or (source, target) in seen:
            continue
        seen.add((source, target))
        edges.append(edge)
    return tuple(edges)


def style_axes(ax: plt.Axes) -> None:
    ax.tick_params(
        axis="both",
        which="major",
        direction="in",
        length=8,
        width=2,
        top=True,
        right=True,
        labelsize=14,
        pad=8,
    )
    ax.tick_params(axis="both", which="minor", direction="in", length=5, width=2, top=True, right=True)
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.yaxis.set_minor_formatter(NullFormatter())
    for spine in ax.spines.values():
        spine.set_linewidth(2)


def nice_y_limit(max_energy: float) -> float:
    if max_energy <= 0:
        return 100.0
    step = 500.0 if max_energy > 2500.0 else 250.0
    return math.ceil((max_energy + 180.0) / step) * step


def transition_text_path_effects(linewidth: float = 3.8) -> list[object]:
    return [path_effects.withStroke(linewidth=linewidth, foreground="white")]


def choose_transition_label_y(
    y_upper: float,
    y_lower: float,
    level_ys: list[float],
    occupied_ys: list[float] | None = None,
) -> float:
    """Place a B(E2) label on the arrow while avoiding nearby level lines."""
    occupied_ys = occupied_ys or []
    midpoint = 0.5 * (y_upper + y_lower)
    lower_bound = y_lower + 45.0
    upper_bound = y_upper - 45.0
    if lower_bound >= upper_bound:
        return midpoint

    for delta in (0.0, -70.0, 70.0, -120.0, 120.0):
        candidate = min(max(midpoint + delta, lower_bound), upper_bound)
        if all(abs(candidate - level_y) >= 60.0 for level_y in level_ys) and all(
            abs(candidate - label_y) >= 60.0 for label_y in occupied_ys
        ):
            return candidate
    return midpoint


def choose_short_transition_label_y(
    y_upper: float,
    y_lower: float,
    level_ys: list[float],
    occupied_ys: list[float] | None = None,
) -> float:
    occupied_ys = occupied_ys or []
    midpoint = 0.5 * (y_upper + y_lower)
    candidates = (
        midpoint,
        y_upper + 75.0,
        y_lower - 75.0,
        y_upper + 130.0,
        y_lower - 130.0,
    )
    for candidate in candidates:
        if all(abs(candidate - level_y) >= 58.0 for level_y in level_ys) and all(
            abs(candidate - label_y) >= 60.0 for label_y in occupied_ys
        ):
            return candidate
    return midpoint


def level_label_positions(states: Iterable[State], levels: dict[State, Level], reference: State) -> dict[State, float]:
    """Return y positions for level labels, spreading labels for near-degenerate levels."""
    min_gap = 120.0
    ordered = sorted(states, key=lambda state: energy_kev(levels, state, reference))
    positions: dict[State, float] = {}
    cluster: list[State] = []

    def flush_cluster(items: list[State]) -> None:
        if not items:
            return
        ys = [energy_kev(levels, state, reference) for state in items]
        if len(items) == 1:
            positions[items[0]] = ys[0]
            return
        center = sum(ys) / len(ys)
        start = center - min_gap * (len(items) - 1) / 2.0
        for index, state in enumerate(items):
            positions[state] = start + min_gap * index

    previous_y: float | None = None
    for state in ordered:
        y = energy_kev(levels, state, reference)
        if previous_y is None or y - previous_y < min_gap:
            cluster.append(state)
        else:
            flush_cluster(cluster)
            cluster = [state]
        previous_y = y
    flush_cluster(cluster)
    return positions


def arrow_x_offset(band: Band, lower: State, upper: State, fallback_offset: float) -> float:
    if band.name != "band3":
        return fallback_offset
    spin_pair = tuple(sorted((lower[0], upper[0])))
    if spin_pair in ((2, 3), (3, 4), (4, 5), (5, 6)):
        return -0.36
    if spin_pair in ((2, 4), (4, 6)):
        return 0.36
    if spin_pair == (3, 5):
        return 0.0
    return fallback_offset


def interband_source_x(
    source: State,
    target: State,
    bands: list[Band],
    state_x: dict[State, float],
    level_half_width: float,
) -> float:
    source_x = state_x[source]
    if len(bands) < 3 or not bands[0].states or not bands[1].states or not bands[2].states:
        return source_x

    band1_head = bands[0].states[0]
    band2_head = bands[1].states[0]
    band3_head = bands[2].states[0]
    band1_two = next((state for state in bands[0].states if state[0] == 2), None)

    offsets = {
        (band3_head, band2_head): -level_half_width,
        (band2_head, band3_head): level_half_width,
        (band3_head, band1_head): level_half_width,
    }
    if band1_two is not None:
        offsets[(band3_head, band1_two)] = 0.0
        offsets[(band2_head, band1_two)] = 0.0
    return source_x + offsets.get((source, target), 0.0)


def interband_guide_offset(count: int, rank: int, guide_length: float, label_gap: float) -> float:
    if count == 1:
        return max(label_gap + 0.16, 0.42 * guide_length)
    offset = label_gap + 0.18 * (guide_length - label_gap)
    offset += 0.76 * (guide_length - label_gap) * rank / max(count - 1, 1)
    return offset


def draw_bands(
    levels: dict[State, Level],
    bands: list[Band],
    interband_edges: tuple[tuple[State, State, float], ...],
    title: str,
    output_path: Path,
    reference: State = (0, 1),
) -> None:
    selected_states = sorted({state for band in bands for state in band.states})
    selected_edges = [edge for band in bands for edge in band.edges] + list(interband_edges)
    max_energy = max(energy_kev(levels, state, reference) for state in selected_states)
    max_be2 = max((edge[2] for edge in selected_edges), default=1.0)

    fig, ax = plt.subplots(figsize=(10.5, 7.0))
    band_x = [0.0, 2.65, 5.3]
    level_half_width = 0.48
    min_guide_length = 0.76
    right_spin_label_gap = 0.78
    colors = ["#111111", "#111111", "#111111"]

    state_x: dict[State, float] = {}
    for x, band in zip(band_x, bands):
        for state in band.states:
            state_x[state] = x

    interband_target_counts: dict[tuple[State, float], int] = {}
    interband_target_sides: dict[State, set[float]] = {}
    interband_guide_lengths: dict[tuple[State, float], float] = {}
    for source, target, _strength in interband_edges:
        if source not in state_x or target not in state_x:
            continue
        source_x = state_x[source]
        target_x = state_x[target]
        if source_x == target_x:
            continue
        toward_source = 1.0 if source_x > target_x else -1.0
        interband_target_counts[(target, toward_source)] = interband_target_counts.get((target, toward_source), 0) + 1
        interband_target_sides.setdefault(target, set()).add(toward_source)
        target_band_index = min(range(len(band_x)), key=lambda item: abs(band_x[item] - target_x))
        source_band_index = min(range(len(band_x)), key=lambda item: abs(band_x[item] - source_x))
        if abs(source_band_index - target_band_index) >= 2:
            inner_band_x = band_x[target_band_index + int(toward_source)]
            required_length = abs(inner_band_x - target_x) + level_half_width + 0.95
        else:
            required_length = min_guide_length
        if toward_source > 0:
            required_length = max(required_length, right_spin_label_gap + min_guide_length)
        key = (target, toward_source)
        interband_guide_lengths[key] = max(interband_guide_lengths.get(key, min_guide_length), required_length)

    edge_count_by_target: dict[State, int] = {}
    edge_seen_by_target: dict[State, int] = {}
    for _source, target, _strength in [edge for band in bands for edge in band.edges]:
        edge_count_by_target[target] = edge_count_by_target.get(target, 0) + 1

    for x, band, color in zip(band_x, bands, colors):
        band_level_ys = [energy_kev(levels, state, reference) for state in band.states]
        label_ys = level_label_positions(band.states, levels, reference)
        for state in sorted(band.states, key=lambda item: levels[item].energy_mev):
            state_x[state] = x
            y = energy_kev(levels, state, reference)
            label_y = label_ys[state]
            ax.plot(
                [x - level_half_width, x + level_half_width],
                [y, y],
                color=color,
                lw=3.6,
                solid_capstyle="round",
                zorder=3,
            )
            ax.text(
                x - level_half_width - 0.18,
                label_y,
                f"{y:.0f}",
                ha="right",
                va="center",
                fontsize=16,
                fontstyle="italic",
                fontweight="bold",
                zorder=5,
            )
            ax.text(
                x + level_half_width + 0.18,
                label_y,
                f"{state[0]}\N{SUPERSCRIPT PLUS SIGN}",
                ha="left",
                va="center",
                fontsize=23,
                fontfamily=["Times New Roman", "Times", "DejaVu Serif"],
                fontweight="bold",
                zorder=5,
            )

        transition_label_ys: list[float] = []
        for source, target, strength in band.edges:
            y_upper = energy_kev(levels, source, reference)
            y_lower = energy_kev(levels, target, reference)
            count = edge_count_by_target.get(target, 1)
            seen = edge_seen_by_target.get(target, 0)
            edge_seen_by_target[target] = seen + 1
            fallback_offset = 0.0 if count == 1 else (seen - (count - 1) / 2.0) * 0.62
            offset = arrow_x_offset(band, target, source, fallback_offset)
            x_arrow = x + offset
            lw = 0.8 + 5.0 * (strength / max_be2)
            transition_height = y_upper - y_lower
            if transition_height < 170.0:
                short_arrow = FancyArrowPatch(
                    (x_arrow, y_upper),
                    (x_arrow, y_lower),
                    arrowstyle="-|>",
                    mutation_scale=14.0 + 6.0 * (strength / max_be2),
                    linewidth=lw,
                    color=color,
                    shrinkA=0,
                    shrinkB=0,
                    joinstyle="miter",
                )
                ax.add_patch(short_arrow)
                label_y = 0.5 * (y_upper + y_lower)
                transition_label_ys.append(label_y)
                text_x = x_arrow - 0.12 if offset < 0 else x_arrow + 0.12
                text_ha = "right" if offset < 0 else "left"
                ax.text(
                    text_x,
                    label_y,
                    f"{strength:.1f}",
                    ha=text_ha,
                    va="center",
                    fontsize=16,
                    fontfamily=["Times New Roman", "Times", "DejaVu Serif"],
                    fontweight="semibold",
                    path_effects=transition_text_path_effects(),
                    zorder=6,
                )
            else:
                label_y = choose_transition_label_y(y_upper, y_lower, band_level_ys, transition_label_ys)
                transition_label_ys.append(label_y)
                text_gap = min(46.0, max(24.0, 0.18 * transition_height))
                ax.plot(
                    [x_arrow, x_arrow],
                    [y_upper, label_y + text_gap],
                    color=color,
                    lw=lw,
                    solid_capstyle="butt",
                )
                lower_arrow = FancyArrowPatch(
                    (x_arrow, label_y - text_gap),
                    (x_arrow, y_lower),
                    arrowstyle="-|>",
                    mutation_scale=16.0 + 8.0 * (strength / max_be2),
                    linewidth=lw,
                    color=color,
                    shrinkA=0,
                    shrinkB=0,
                    joinstyle="miter",
                )
                ax.add_patch(lower_arrow)
                ax.text(
                    x_arrow,
                    label_y,
                    f"{strength:.1f}",
                    ha="center",
                    va="center",
                    fontsize=16,
                    fontfamily=["Times New Roman", "Times", "DejaVu Serif"],
                    fontweight="semibold",
                    path_effects=transition_text_path_effects(),
                    zorder=6,
                )

    interband_target_groups: dict[tuple[State, float], list[tuple[float, State]]] = {}
    for source, target, _strength in interband_edges:
        if source not in state_x or target not in state_x:
            continue
        source_x = state_x[source]
        target_x = state_x[target]
        if source_x == target_x:
            continue
        toward_source = 1.0 if source_x > target_x else -1.0
        interband_target_groups.setdefault((target, toward_source), []).append((abs(source_x - target_x), source))

    interband_target_source_ranks: dict[tuple[State, State, float], int] = {}
    for (target, toward_source), items in interband_target_groups.items():
        for rank, (_distance, source) in enumerate(sorted(items)):
            interband_target_source_ranks[(source, target, toward_source)] = rank

    interband_guide_offsets: dict[tuple[State, State], float] = {}
    for source, target, _strength in interband_edges:
        if source not in state_x or target not in state_x:
            continue
        source_x = state_x[source]
        target_x = state_x[target]
        if source_x == target_x:
            continue
        toward_source = 1.0 if source_x > target_x else -1.0
        count = interband_target_counts.get((target, toward_source), 1)
        rank = interband_target_source_ranks.get((source, target, toward_source), 0)
        guide_length = interband_guide_lengths.get((target, toward_source), min_guide_length)
        label_gap = right_spin_label_gap if toward_source > 0 else 0.0
        interband_guide_offsets[(source, target)] = interband_guide_offset(count, rank, guide_length, label_gap)

    if len(bands) >= 3 and bands[0].states and bands[2].states:
        band1_head = bands[0].states[0]
        band3_head = bands[2].states[0]
        band1_two = next((state for state in bands[0].states if state[0] == 2), None)
        head_key = (band3_head, band1_head)
        two_key = (band3_head, band1_two) if band1_two is not None else None
        if (
            band1_two is not None
            and head_key in interband_guide_offsets
            and two_key in interband_guide_offsets
            and band3_head in state_x
            and band1_head in state_x
            and band1_two in state_x
        ):
            y_source = energy_kev(levels, band3_head, reference)
            y_head = energy_kev(levels, band1_head, reference)
            y_two = energy_kev(levels, band1_two, reference)
            if not math.isclose(y_two, y_source):
                toward_two = 1.0 if state_x[band3_head] > state_x[band1_two] else -1.0
                start_two_x = interband_source_x(band3_head, band1_two, bands, state_x, level_half_width)
                end_two_x = state_x[band1_two] + toward_two * (level_half_width + interband_guide_offsets[two_key])
                start_head_x = interband_source_x(band3_head, band1_head, bands, state_x, level_half_width)
                parallel_end_x = start_head_x + (y_head - y_source) * (end_two_x - start_two_x) / (y_two - y_source)
                toward_head = 1.0 if state_x[band3_head] > state_x[band1_head] else -1.0
                parallel_offset = toward_head * (parallel_end_x - state_x[band1_head]) - level_half_width
                min_offset = right_spin_label_gap + 0.16 if toward_head > 0 else 0.16
                if math.isfinite(parallel_offset) and parallel_offset > min_offset:
                    interband_guide_offsets[head_key] = parallel_offset
                    guide_key = (band1_head, toward_head)
                    interband_guide_lengths[guide_key] = max(
                        interband_guide_lengths.get(guide_key, min_guide_length),
                        parallel_offset + 0.24,
                    )

    for (target, toward_source), _count in interband_target_counts.items():
        target_x = state_x[target]
        y_target = energy_kev(levels, target, reference)
        guide_length = interband_guide_lengths.get((target, toward_source), min_guide_length)
        guide_start = target_x + toward_source * level_half_width
        guide_end = target_x + toward_source * (level_half_width + guide_length)
        ax.plot(
            [guide_start, guide_end],
            [y_target, y_target],
            color="#404040",
            lw=1.4,
            linestyle=(0, (4, 3)),
            solid_capstyle="butt",
            zorder=1,
        )

    for index, (source, target, strength) in enumerate(interband_edges):
        if source not in state_x or target not in state_x:
            continue
        source_x = state_x[source]
        target_x = state_x[target]
        if source_x == target_x:
            continue
        y_source = energy_kev(levels, source, reference)
        y_target = energy_kev(levels, target, reference)
        toward_source = 1.0 if source_x > target_x else -1.0
        guide_offset = interband_guide_offsets.get((source, target), min_guide_length)
        start = (interband_source_x(source, target, bands, state_x, level_half_width), y_source)
        end = (target_x + toward_source * (level_half_width + guide_offset), y_target)
        lw = 0.8 + 4.2 * (strength / max_be2)
        arrow = FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14.0 + 7.0 * (strength / max_be2),
            linewidth=lw,
            color="#404040",
            shrinkA=0,
            shrinkB=6,
            joinstyle="miter",
        )
        ax.add_patch(arrow)
        mid_x = 0.5 * (start[0] + end[0])
        mid_y = 0.5 * (start[1] + end[1])
        is_band3_head_to_band1_head = (
            len(bands) >= 3
            and bool(bands[0].states)
            and bool(bands[2].states)
            and source == bands[2].states[0]
            and target == bands[0].states[0]
        )
        label_shift = -70.0 if is_band3_head_to_band1_head else (70.0 if index % 2 == 0 else -70.0)
        ax.text(
            mid_x,
            mid_y + label_shift,
            f"{strength:.1f}",
            ha="center",
            va="center",
            fontsize=15,
            fontfamily=["Times New Roman", "Times", "DejaVu Serif"],
            fontweight="semibold",
            color="#404040",
            path_effects=transition_text_path_effects(),
            zorder=6,
        )

    ax.set_title(title, fontsize=34, pad=18)
    ax.set_xlim(-1.2, 6.55)
    ax.set_ylim(-80.0, nice_y_limit(max_energy))
    ax.axis("off")
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight", transparent=True)
    plt.close(fig)


def write_selection_csv(
    levels: dict[State, Level],
    bands: list[Band],
    interband_edges: tuple[tuple[State, State, float], ...],
    output_csv: Path,
    reference: State = (0, 1),
) -> None:
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["band", "kind", "spin", "index", "energy_keV", "upper", "lower", "be2_energy_down_WU"])
        for band in bands:
            for state in band.states:
                writer.writerow(
                    [
                        band.name,
                        "level",
                        state[0],
                        state[1],
                        f"{energy_kev(levels, state, reference):.6f}",
                        "",
                        "",
                        "",
                    ]
                )
            for upper, lower, strength in band.edges:
                writer.writerow(
                    [
                        band.name,
                        "transition",
                        "",
                        "",
                        "",
                        f"{upper[0]}_{upper[1]}",
                        f"{lower[0]}_{lower[1]}",
                        f"{strength:.6f}",
                    ]
                )
        for upper, lower, strength in interband_edges:
            writer.writerow(
                [
                    "interband",
                    "transition",
                    "",
                    "",
                    "",
                    f"{upper[0]}_{upper[1]}",
                    f"{lower[0]}_{lower[1]}",
                    f"{strength:.6f}",
                ]
            )


def nucleus_name_from_path(path: Path) -> str:
    if path.name == "GBH.out":
        return path.parent.name
    return path.stem


def format_nucleus_title(nucleus: str) -> str:
    """Format names such as Cd112 or _O28 as isotope math text."""
    clean = nucleus.strip("_")
    match = re.fullmatch(r"([A-Z][a-z]?)(\d+)", clean)
    if not match:
        return nucleus
    element, mass = match.groups()
    return rf"$^{{{mass}}}\mathrm{{{element}}}$"


def plot_one(
    input_path: Path,
    output_dir: Path,
    formats: tuple[str, ...] = ("svg", "png"),
    write_csv_output: bool = True,
) -> tuple[Path, ...]:
    levels, transitions = parse_gbh(input_path)
    bands = trim_bands_at_two_if_higher_spin_drops(levels, select_bands(levels, transitions))
    interband_edges = build_interband_edges(levels, transitions, bands)
    nucleus = nucleus_name_from_path(input_path)
    output_svg = output_dir / f"{nucleus}_excitation_bands.svg"
    output_png = output_dir / f"{nucleus}_excitation_bands.png"
    output_csv = output_dir / f"{nucleus}_selected_bands.csv"
    title = format_nucleus_title(nucleus)
    outputs: list[Path] = []
    if "svg" in formats:
        draw_bands(levels, bands, interband_edges, title=title, output_path=output_svg)
        outputs.append(output_svg)
    if "png" in formats:
        draw_bands(levels, bands, interband_edges, title=title, output_path=output_png)
        outputs.append(output_png)
    if write_csv_output:
        write_selection_csv(levels, bands, interband_edges, output_csv=output_csv)
        outputs.append(output_csv)
    return tuple(outputs)


def plot_in_place(
    input_path: Path,
    formats: tuple[str, ...] = ("svg", "png"),
    write_csv_output: bool = True,
) -> tuple[str, ...]:
    outputs = plot_one(input_path, input_path.parent, formats=formats, write_csv_output=write_csv_output)
    return (str(input_path), *(str(output) for output in outputs))


def find_gbh_files(root: Path) -> list[Path]:
    return sorted(root.glob("*_iso/*/GBH.out"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("Hf_iso/Hf164/GBH.out"), help="GBH.out to plot")
    parser.add_argument("--output-dir", type=Path, default=Path("excitation_band_plots"), help="Output directory")
    parser.add_argument("--batch", action="store_true", help="Plot every *_iso/*/GBH.out under --root")
    parser.add_argument("--root", type=Path, default=Path("."), help="Root directory for --batch")
    parser.add_argument("--workers", type=int, default=1, help="Parallel workers for --batch")
    parser.add_argument("--quiet", action="store_true", help="For --batch, print only failures and a summary")
    parser.add_argument(
        "--formats",
        default="svg,png",
        help="Comma-separated image formats to write: svg, png, or svg,png",
    )
    parser.add_argument("--no-csv", action="store_true", help="Do not write selected-bands CSV files")
    args = parser.parse_args()
    formats = tuple(part.strip().lower() for part in args.formats.split(",") if part.strip())
    invalid_formats = sorted(set(formats) - {"svg", "png"})
    if invalid_formats:
        raise SystemExit(f"Unsupported --formats value(s): {', '.join(invalid_formats)}")
    if not formats and args.no_csv:
        raise SystemExit("Nothing to write: --formats is empty and --no-csv was set")

    if args.batch:
        paths = find_gbh_files(args.root)
        if not paths:
            raise SystemExit(f"No GBH.out files found under {args.root}")
        ok_count = 0
        fail_count = 0
        if args.workers <= 1:
            for path in paths:
                try:
                    result = plot_in_place(path, formats=formats, write_csv_output=not args.no_csv)
                    ok_count += 1
                    if not args.quiet:
                        print(f"ok {path} -> {' '.join(result[1:])}")
                except Exception as exc:  # noqa: BLE001 - keep batch diagnostics going.
                    fail_count += 1
                    print(f"failed {path}: {exc}")
            print(f"summary total={len(paths)} ok={ok_count} failed={fail_count}")
            return
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(plot_in_place, path, formats, not args.no_csv): path
                for path in paths
            }
            for future in as_completed(futures):
                path = futures[future]
                try:
                    result = future.result()
                    ok_count += 1
                    if not args.quiet:
                        print(f"ok {path} -> {' '.join(result[1:])}")
                except Exception as exc:  # noqa: BLE001 - keep batch diagnostics going.
                    fail_count += 1
                    print(f"failed {path}: {exc}")
        print(f"summary total={len(paths)} ok={ok_count} failed={fail_count}")
        return

    for output_path in plot_one(args.input, args.output_dir, formats=formats, write_csv_output=not args.no_csv):
        print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
