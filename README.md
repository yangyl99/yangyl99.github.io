================================================================================
  Triaxial Relativistic Hartree-Bogoliubov (RHB) Results Website
  with the PC-PK1 Density Functional
================================================================================

Domain: nuclearmap.jcnp.org
Publication: Y. L. Yang, Y. K. Wang, P. W. Zhao, and Z. P. Li,
             Phys. Rev. C 104, 054312 (2021)
Authors: Yilong Yang, Pengwei Zhao (Peking University / Southwest University)


1. PROJECT OVERVIEW
================================================================================

A static website (hosted via GitHub Pages) that presents the ground-state
properties and potential energy surfaces (PES) of even-even nuclei calculated
by triaxial RHB theory using the PC-PK1 density functional, with dynamical
correlation energies from a five-dimensional collective Hamiltonian (5DCH).

Coverage: even-even nuclei with 8 <= Z <= 104, from proton drip line to
neutron drip line (~2021 PES images in total, across 49 isotopic chains).


2. FILE ARCHITECTURE
================================================================================

yangyl99.github.io-main/
|
|-- CNAME                       # Custom domain: nuclearmap.jcnp.org
|-- LICENSE
|-- index.html                  # Main page: nuclear chart, search, PES viewer
|-- theory.html                 # Theoretical framework (MathJax-rendered)
|
|-- css/
|   |-- bootstrap.min.css       # Bootstrap 4 framework
|   |-- bootstrap-theme.css     # Bootstrap theme
|   |-- justified-nav.css       # Navigation styling
|   |-- pwzhao.css              # Custom styles + Glyphicon definitions
|
|-- js/
|   |-- bootstrap.min.js        # Bootstrap JS
|   |-- npm.js                  # npm module loader (Bootstrap dependency)
|   |-- search.js               # Core logic: nuclide search, chart interaction,
|   |                             navigation between neighboring nuclei
|   |-- obs.js                  # Observable data: RHB(Z,N) function returning
|                                 [beta, gamma, E_RHB, E_5DCH, E_exp] for each
|                                 nuclide, hardcoded as JS conditionals
|
|-- files/
|   |-- data_web.txt            # Tabulated results (all nuclides), columns:
|                                 Elt, Z, N, beta, gamma, B_RHB, B_5DCH,
|                                 E_corr, S_2n, S_2p, lamb_n, lamb_p,
|                                 R_m, R_n, R_p, R_c
|
|-- img/
|   |-- nucl_chart.png          # Clickable nuclear chart image (main map)
|   |-- Empty_pes.png           # Placeholder PES image
|   |-- PKU.jpeg / SWU.jpeg     # University logos
|   |-- (other variants)
|
|-- fonts/
|   |-- glyphicons-halflings-*  # Glyphicon font files (eot/svg/ttf/woff/woff2)
|
|-- nuclides/
    |-- Z008/                   # Z=8 (Oxygen) isotopes
    |   |-- Z008N006_pes.png    # PES for Z=8, N=6 (14-O)
    |   |-- Z008N008_pes.png    # PES for Z=8, N=8 (16-O)
    |   |-- ...
    |-- Z010/                   # Z=10 (Neon) isotopes
    |-- ...
    |-- Z104/                   # Z=104 (Rutherfordium) isotopes
    (49 directories, ~2021 PES images total)


3. FUNCTIONALITY
================================================================================

3.1 Interactive Nuclear Chart (index.html)
    - A nuclear chart image (nucl_chart.png) serves as a clickable map.
    - Mouse hover: JS tracks cursor position, converts pixel coordinates
      to (Z, N) using linear mapping, and displays the nuclide name in
      real-time (e.g., "16-O (Z=8, N=8)").
    - Click: loads the corresponding PES image and ground-state observables.
    - Only even-even nuclei within the drip lines are selectable; drip line
      boundaries are hardcoded in the JS drip[] arrays.

3.2 Nuclide Search
    - Text input accepts formats like "O16" or "100Sn".
    - elementZN() in search.js parses the input, resolves the element symbol
      to Z via lookup array, computes N = A - Z, and calls linkZN().

3.3 Nuclide Detail View
    - Displays the PES contour plot from nuclides/Z{ZZZ}/Z{ZZZ}N{NNN}_pes.png.
    - Shows ground-state properties: E_RHB, E_5DCH, E_exp (AME2020),
      quadrupole deformation beta, triaxial deformation gamma.
    - Data is fetched from the RHB(Z,N) function in obs.js (hardcoded values).
    - Arrow buttons allow navigation to neighboring even-even nuclei
      (Z+/-2, N+/-2) via changeZN().

3.4 Tabulated Results (data_web.txt)
    - Plain-text table of all calculated observables for all nuclides.
    - Columns: element, Z, N, beta, gamma, B_RHB, B_5DCH, E_corr,
      S_2n, S_2p, lambda_n, lambda_p, R_m, R_n, R_p, R_c.

3.5 Theoretical Framework (theory.html)
    - Description of the RHB + 5DCH method, rendered with MathJax.


4. TECHNICAL NOTES
================================================================================

- Pure static site: no server-side code, no database. All nuclear data is
  embedded in obs.js (per-nuclide observables) and data_web.txt (full table).
- Frontend: Bootstrap 4 + jQuery + Glyphicons.
- Math rendering: MathJax (used on theory.html).
- Analytics: Baidu tongji (hm.baidu.com).
- The nuclear chart interaction uses pixel-to-(Z,N) coordinate conversion
  calibrated to the specific nucl_chart.png image dimensions.
- PES image naming convention: Z{ZZZ}N{NNN}_pes.png (zero-padded to 3 digits).


5. REFERENCES
================================================================================

[1] Y. L. Yang, Y. K. Wang, P. W. Zhao, and Z. P. Li,
    Phys. Rev. C 104, 054312 (2021)
[2] Y. L. Yang, P. W. Zhao, and Z. P. Li,
    Phys. Rev. C 107, 024308 (2023)
