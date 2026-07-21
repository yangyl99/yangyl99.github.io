var currentResultView = "ground";

function findPos(el) {
    var x = y = 0;
    if(el.offsetParent) {
		  x = el.offsetLeft;
		  y = el.offsetTop;
		  while(el = el.offsetParent) {
        x += el.offsetLeft;
        y += el.offsetTop;
		  }
    }
    return {'x':x, 'y':y};
  }
					   
function getScrollCursor(evt){
   evt = evt || window.event;
   var curScrollX = (evt.pageX)? evt.pageX : evt.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
   var curScrollY = (evt.pageY)? evt.pageY : evt.clientY + document.body.scrollTop + document.documentElement.scrollTop;
   return {'x': curScrollX, 'y': curScrollY};
}
  
function clientProperty(){
  document.onmousemove = function(evt){
    var myImg = document.getElementById('nuclear_chart')
    var currHeight = myImg.clientHeight;
    var currWidth = myImg.clientWidth;
    scrollCursor = getScrollCursor(evt);
    imagePos = findPos(document.getElementById('nuclear_chart'));
    var elementName= new Array("Neutron","Hydrogen","Helium","Lithium","Beryllium","Boron","Carbon","Nitrogen","Oxygen","Fluorine","Neon","Sodium","Magnesium","Aluminum","Silicon","Phosphorus","Sulfur","Chlorine","Argon","Potassium","Calcium","Scandium","Titanium","Vanadium","Chromium","Manganese","Iron","Cobalt","Nickel","Copper","Zinc","Gallium","Germanium","Arsenic","Selenium","Bromine","Krypton","Rubidium","Strontium","Yttrium","Zirconium","Niobium","Molybdenum","Technetium","Ruthenium","Rhodium","Palladium","Silver","Cadmium","Indium","Tin","Antimony","Tellurium","Iodine","Xenon","Cesium","Barium","Lanthanum","Cerium","Praseodymium","Neodymium","Promethium","Samarium","Europium","Gadolinium","Terbium","Dysprosium","Holmium","Erbium","Thulium","Ytterbium","Lutetium","Hafnium","Tantalum","Tungsten","Rhenium","Osmium","Iridium","Platinum","Gold","Mercury","Thallium","Lead","Bismuth","Polonium","Astatine","Radon","Francium","Radium","Actinium","Thorium","Protactinium","Uranium","Neptunium","Plutonium","Americium","Curium","Berkelium","Californium","Einsteinium","Fermium","MEndelevium","Nobelium","Lawrencium","Rutherfordium","Dubnium","Seaborgium");
    var elementSymbol= new Array("N","H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg");
  var drip=new Array(106);
  for (var i=1;i<107;i++)
  {
  drip[i]=new Array(2);
  }
  for (var i=1;i<107;i++)
  {
  	drip[i][1]="-1000";
  	drip[i][2]="-1000";
  }
  drip[8][1]="6";drip[8][2]="20";
  drip[10][1]="8";drip[10][2]="26";
  drip[12][1]="8";drip[12][2]="34";
  drip[14][1]="10";drip[14][2]="38";
  drip[16][1]="12";drip[16][2]="40";
  drip[18][1]="14";drip[18][2]="46";
  drip[20][1]="16";drip[20][2]="58";
  drip[22][1]="18";drip[22][2]="62";
  drip[24][1]="20";drip[24][2]="66";
  drip[26][1]="22";drip[26][2]="68";
  drip[28][1]="24";drip[28][2]="70";
  drip[30][1]="28";drip[30][2]="78";
  drip[32][1]="30";drip[32][2]="82";
  drip[34][1]="32";drip[34][2]="90";
  drip[36][1]="34";drip[36][2]="96";
  drip[38][1]="36";drip[38][2]="98";
  drip[40][1]="38";drip[40][2]="110";
  drip[42][1]="40";drip[42][2]="110";
  drip[44][1]="42";drip[44][2]="112";
  drip[46][1]="44";drip[46][2]="118";
  drip[48][1]="46";drip[48][2]="124";
  drip[50][1]="50";drip[50][2]="126";
  drip[52][1]="56";drip[52][2]="126";
  drip[54][1]="58";drip[54][2]="126";
  drip[56][1]="60";drip[56][2]="126";
  drip[58][1]="60";drip[58][2]="150";
  drip[60][1]="64";drip[60][2]="154";
  drip[62][1]="68";drip[62][2]="160";
  drip[64][1]="70";drip[64][2]="168";
  drip[66][1]="74";drip[66][2]="180";
  drip[68][1]="76";drip[68][2]="182";
  drip[70][1]="78";drip[70][2]="182";
  drip[72][1]="82";drip[72][2]="184";
  drip[74][1]="84";drip[74][2]="184";
  drip[76][1]="88";drip[76][2]="184";
  drip[78][1]="92";drip[78][2]="184";
  drip[80][1]="92";drip[80][2]="184";
  drip[82][1]="100";drip[82][2]="186";
  drip[84][1]="104";drip[84][2]="222";
  drip[86][1]="108";drip[86][2]="228";
  drip[88][1]="112";drip[88][2]="236";
  drip[90][1]="118";drip[90][2]="254";
  drip[92][1]="122";drip[92][2]="258";
  drip[94][1]="126";drip[94][2]="258";
  drip[96][1]="130";drip[96][2]="258";
  drip[98][1]="132";drip[98][2]="258";
  drip[100][1]="132";drip[100][2]="258";
  drip[102][1]="138";drip[102][2]="258";
  drip[104][1]="142";drip[104][2]="258";
  xReturn = scrollCursor.x-imagePos.x;
  yReturn = scrollCursor.y-imagePos.y;
  zNum=2*parseInt(0.238*(415.-yReturn/currHeight*513.)/2+4);
  nNum=2*parseInt(0.239*(xReturn/currWidth*1309. -131.)/2+3);
  aNum=nNum+zNum;
  var div1 = document.getElementById('result');
  div1.innerHTML = "<div class='row'>Click on a nuclide below</div>";
  if ((xReturn<=0) || (yReturn<=0) || (zNum>104) || (zNum<8) || (!drip[zNum])) {
  return;
  }
  d1=nNum-drip[zNum][1]+1;
  d2=nNum-drip[zNum][2]-1;
  d3=zNum%2-1;
  d4=nNum%2-1;
  flag=d1*d2*d3*d4;
  if (flag>0) flag=1;
  if (flag<=0) flag=-1;
  if ((xReturn>0) && (yReturn>0) && (flag<0) && (zNum<=104) && (zNum>=8)) {
  div1.innerHTML = "<div class='row'><sup><sup>"+aNum+"</sup></sup>"+elementSymbol[zNum]+' (Z='+zNum+', N='+nNum+')'+"</div>";
  }
  }
}
  
  
function nzNum(){
    //window.location.href=mapZN(zNum,nNum,flag);
	mapZN(zNum,nNum,flag);
}


function mapZN(Z,N,flag){
var m="./index.html";
if ((!(isNaN(N))) && (!(isNaN(Z)))) { 
var iz=parseInt(Z);
var jn=parseInt(N);
var aNum=parseInt(Z+N);
var zDir="Z0"+iz;
var zNum="Z0"+iz;
if (iz<10) {var zDir="Z00"+iz};
if (iz<10) {var zNum="Z00"+iz};
if (iz>99) {var zDir="Z"+iz};
if (iz>99) {var zNum="Z"+iz};
var nNum="N0"+jn;
if (jn<10) {var nNum="N00"+jn};
if (jn>99) {var nNum="N"+jn};

if (flag==-1) {
	var m="./index.html#detailedResults";
	var m2="./nuclides/"+zDir+"/"+zNum+nNum+"_pes.png";
      document.getElementById('detail').src = m2;
	
	var elementName= new Array("Neutron","Hydrogen","Helium","Lithium","Beryllium","Boron","Carbon","Nitrogen","Oxygen","Fluorine","Neon","Sodium","Magnesium","Aluminum","Silicon","Phosphorus","Sulfur","Chlorine","Argon","Potassium","Calcium","Scandium","Titanium","Vanadium","Chromium","Manganese","Iron","Cobalt","Nickel","Copper","Zinc","Gallium","Germanium","Arsenic","Selenium","Bromine","Krypton","Rubidium","Strontium","Yttrium","Zirconium","Niobium","Molybdenum","Technetium","Ruthenium","Rhodium","Palladium","Silver","Cadmium","Indium","Tin","Antimony","Tellurium","Iodine","Xenon","Cesium","Barium","Lanthanum","Cerium","Praseodymium","Neodymium","Promethium","Samarium","Europium","Gadolinium","Terbium","Dysprosium","Holmium","Erbium","Thulium","Ytterbium","Lutetium","Hafnium","Tantalum","Tungsten","Rhenium","Osmium","Iridium","Platinum","Gold","Mercury","Thallium","Lead","Bismuth","Polonium","Astatine","Radon","Francium","Radium","Actinium","Thorium","Protactinium","Uranium","Neptunium","Plutonium","Americium","Curium","Berkelium","Californium","Einsteinium","Fermium","MEndelevium","Nobelium","Lawrencium","Rutherfordium","Dubnium","Seaborgium");
    var elementSymbol= new Array("N","H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg");
	
	aNum=iz+jn;
	var div1 = document.getElementById('detail_title');
	div1.innerText = "Results for "+elementName[iz]+" "+aNum+" (Z="+iz+", N="+jn+")";
	
	aNum=iz+jn+2;
	var div2 = document.getElementById('up-Z');
	div2.innerHTML = "<h5>&nbsp;&nbsp;<sup><sup>"+aNum+"</sup></sup><big>"+elementSymbol[iz+2]+"</big></h5>";
	
	var div3 = document.getElementById('right-N');
	div3.innerHTML = "<h5>&nbsp;&nbsp;<sup><sup>"+aNum+"</sup></sup><big>"+elementSymbol[iz]+"</big></h5>";
	
	aNum=iz+jn-2;
	var div4 = document.getElementById('down-Z');
	div4.innerHTML = "<h5>&nbsp;&nbsp;<sup><sup>"+aNum+"</sup></sup><big>"+elementSymbol[iz-2]+"</big></h5>";
	
	var div5 = document.getElementById('left-N');
	div5.innerHTML = "<h5><sup><sup>"+aNum+"</sup></sup><big>"+elementSymbol[iz]+"</big></h5>";
	
	var new_element=document.createElement("script");
    new_element.setAttribute("type","text/javascript");
    new_element.setAttribute("src","./js/obs.js");
    document.body.appendChild(new_element);
	
	var obs=RHB(iz,jn)
	var div6 = document.getElementById('E_RHB');
	div6.innerHTML = "<h5>E<sub>RHB</sub> = -"+Number(obs[2]).toFixed(2)+" MeV</h5>";
	
	div6 = document.getElementById('E_5DCH');
	div6.innerHTML = "<h5>E<sub>5DCH</sub> = -"+Number(obs[3]).toFixed(2)+" MeV</h5>";
	
	div6 = document.getElementById('E_exp');
	if (isNaN(obs[4]))  {div6.innerHTML = "<h5>E<sub>exp</sub> = "+obs[4]+"</h5>";}
	if (!isNaN(obs[4])) {div6.innerHTML = "<h5>E<sub>exp</sub> = -"+Number(obs[4]).toFixed(2)+" MeV</h5>";}
	
	div6 = document.getElementById('beta');
	div6.innerHTML = "<h5>&beta; = "+Number(obs[0]).toFixed(2)+"</h5>";
	
	div6 = document.getElementById('gamma');
	div6.innerHTML = "<h5>&gamma; = "+obs[1]+"<sup>o</sup></h5>";
	
	updateSpectroscopyResult(iz, jn, elementSymbol);
	  }
}
return m;
}

function elementZN(name){
	var elementSymbol= new Array("N","H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og");
	var idx = -1;
	var idEl = -1;
	var cc = "cc";
	for (var i=0;i<name.length;i++){
		cc = name.charAt(i);
		if (!isNaN(cc) && idx == -1) {
		idx = i;
		}
		if (isNaN(cc) && idEl == -1) {
		idEl = i;
		}
	}
	var symbol = "sym";
	var aNum = "A";
	if (idx == 0) {
		symbol = name.slice(idEl, name.length);
		aNum = name.slice(0, idEl);
	}
	
	else {
		symbol = name.slice(0, idx);
		aNum = name.slice(idx, name.length);
	}
	if ((idx == -1) || (idEl == -1)) {
		return linkZN(999, 0);
	}
	else {
		var zNum = elementSymbol.indexOf(symbol);
		if (zNum == -1) {
		 	return linkZN(999, 0);
		}
		else {
			var m = linkZN(parseInt(zNum), parseInt(aNum)-parseInt(zNum));
			return m;
		}
	}
	
}

function linkZN(cZ, cN){
  if (parseInt(cZ) == 999) {alert("Please enter the nuclide name with right format, e.g., 'O16', '100Sn'");var m="./index.html";return m;}
  var m="./index.html";
  var drip=new Array(125);
  for (var i=1;i<124;i++)
    {
     drip[i]=new Array(2);
    }
  for (var i=1;i<124;i++)
    {
        drip[i][1]="-1000";
        drip[i][2]="-1000";
    }
  drip[8][1]="6";drip[8][2]="20";
  drip[10][1]="8";drip[10][2]="26";
  drip[12][1]="8";drip[12][2]="34";
  drip[14][1]="10";drip[14][2]="38";
  drip[16][1]="12";drip[16][2]="40";
  drip[18][1]="14";drip[18][2]="46";
  drip[20][1]="16";drip[20][2]="58";
  drip[22][1]="18";drip[22][2]="62";
  drip[24][1]="20";drip[24][2]="66";
  drip[26][1]="22";drip[26][2]="68";
  drip[28][1]="24";drip[28][2]="70";
  drip[30][1]="28";drip[30][2]="78";
  drip[32][1]="30";drip[32][2]="82";
  drip[34][1]="32";drip[34][2]="90";
  drip[36][1]="34";drip[36][2]="96";
  drip[38][1]="36";drip[38][2]="98";
  drip[40][1]="38";drip[40][2]="110";
  drip[42][1]="40";drip[42][2]="110";
  drip[44][1]="42";drip[44][2]="112";
  drip[46][1]="44";drip[46][2]="118";
  drip[48][1]="46";drip[48][2]="124";
  drip[50][1]="50";drip[50][2]="126";
  drip[52][1]="56";drip[52][2]="126";
  drip[54][1]="58";drip[54][2]="126";
  drip[56][1]="60";drip[56][2]="126";
  drip[58][1]="60";drip[58][2]="150";
  drip[60][1]="64";drip[60][2]="154";
  drip[62][1]="68";drip[62][2]="160";
  drip[64][1]="70";drip[64][2]="168";
  drip[66][1]="74";drip[66][2]="180";
  drip[68][1]="76";drip[68][2]="182";
  drip[70][1]="78";drip[70][2]="182";
  drip[72][1]="82";drip[72][2]="184";
  drip[74][1]="84";drip[74][2]="184";
  drip[76][1]="88";drip[76][2]="184";
  drip[78][1]="92";drip[78][2]="184";
  drip[80][1]="92";drip[80][2]="184";
  drip[82][1]="100";drip[82][2]="186";
  drip[84][1]="104";drip[84][2]="222";
  drip[86][1]="108";drip[86][2]="228";
  drip[88][1]="112";drip[88][2]="236";
  drip[90][1]="118";drip[90][2]="254";
  drip[92][1]="122";drip[92][2]="258";
  drip[94][1]="126";drip[94][2]="258";
  drip[96][1]="130";drip[96][2]="258";
  drip[98][1]="132";drip[98][2]="258";
  drip[100][1]="132";drip[100][2]="258";
  drip[102][1]="138";drip[102][2]="258";
  drip[104][1]="142";drip[104][2]="258";
  ix = parseInt(cN)
  iy = parseInt(cZ)
  d1=ix-drip[iy][1]+1;
  d2=ix-drip[iy][2]-1;
  d3=ix%2-1;
  d4=iy%2-1;
  flag=d1*d2*d3*d4;
  if (iy < 8) {alert("Proton number out of range 8<=Z<=104!");var m="./index.html#detailedResults";return m;}
  if (iy > 104) {alert("Proton number out of range 8<=Z<=104!");var m="./index.html#detailedResults";return m;}
  if (d3 == 0) {alert("Please search an even-even nuclide !");var m="./index.html#detailedResults";return m;}
  if (d4 == 0) {alert("Please search an even-even nuclide !");var m="./index.html#detailedResults";return m;}
  if (flag>0) flag=1;
  if (flag<=0) flag=-1;
  if (flag==1){
    var iz=parseFloat(cZ);
    var jn=parseFloat(cN);
    if ((iz+jn!=0)){
    if (d1<0){
        alert("Nuclide outside the proton driplines !");
        var m="./index.html#detailedResults";
		return m;
                     }
                     }
    if (d2>0){
        alert("Nuclide outside the neutron driplines !");
      var m="./index.html#detailedResults";
	  return m;
                   }
               }
  if (flag==-1) {
  var iz=parseInt(cZ);
  var jn=parseInt(cN);
  var zDir="Z0"+iz;
  var zNum="Z0"+iz;
  if (iz<10) {var zDir="Z00"+iz};
  if (iz<10) {var zNum="Z00"+iz};
  if (iz>99) {var zDir="Z"+iz};
  if (iz>99) {var zNum="Z"+iz};
  var nNum="N0"+jn;
  if (jn<10) {var nNum="N00"+jn};
  if (jn>99) {var nNum="N"+jn};
	var m="./index.html#detailedResults";
	var m2="./nuclides/"+zDir+"/"+zNum+nNum+"_pes.png";
      document.getElementById('detail').src = m2;
	  
	var elementName= new Array("Neutron","Hydrogen","Helium","Lithium","Beryllium","Boron","Carbon","Nitrogen","Oxygen","Fluorine","Neon","Sodium","Magnesium","Aluminum","Silicon","Phosphorus","Sulfur","Chlorine","Argon","Potassium","Calcium","Scandium","Titanium","Vanadium","Chromium","Manganese","Iron","Cobalt","Nickel","Copper","Zinc","Gallium","Germanium","Arsenic","Selenium","Bromine","Krypton","Rubidium","Strontium","Yttrium","Zirconium","Niobium","Molybdenum","Technetium","Ruthenium","Rhodium","Palladium","Silver","Cadmium","Indium","Tin","Antimony","Tellurium","Iodine","Xenon","Cesium","Barium","Lanthanum","Cerium","Praseodymium","Neodymium","Promethium","Samarium","Europium","Gadolinium","Terbium","Dysprosium","Holmium","Erbium","Thulium","Ytterbium","Lutetium","Hafnium","Tantalum","Tungsten","Rhenium","Osmium","Iridium","Platinum","Gold","Mercury","Thallium","Lead","Bismuth","Polonium","Astatine","Radon","Francium","Radium","Actinium","Thorium","Protactinium","Uranium","Neptunium","Plutonium","Americium","Curium","Berkelium","Californium","Einsteinium","Fermium","MEndelevium","Nobelium","Lawrencium","Rutherfordium","Dubnium","Seaborgium");
    var elementSymbol= new Array("N","H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg");
	
	aNum=iz+jn;
	var div1 = document.getElementById('detail_title');
	div1.innerText = "Results for "+elementName[iz]+" "+aNum+" (Z="+iz+", N="+jn+")";
	
	aNum=iz+jn+2;
	var div2 = document.getElementById('up-Z');
	div2.innerHTML = "<h5>&nbsp;&nbsp;<sup><sup>"+aNum+"</sup></sup><big>"+elementSymbol[iz+2]+"</big></h5>";
	
	var div3 = document.getElementById('right-N');
	div3.innerHTML = "<h5>&nbsp;&nbsp;<sup><sup>"+aNum+"</sup></sup><big>"+elementSymbol[iz]+"</big></h5>";
	
	aNum=iz+jn-2;
	var div4 = document.getElementById('down-Z');
	div4.innerHTML = "<h5>&nbsp;&nbsp;<sup><sup>"+aNum+"</sup></sup><big>"+elementSymbol[iz-2]+"</big></h5>";
	
	var div5 = document.getElementById('left-N');
	div5.innerHTML = "<h5><sup><sup>"+aNum+"</sup></sup><big>"+elementSymbol[iz]+"</big></h5>";
	
	//var fso = new ActiveXObject("Scripting.FileSystemObject");
	//var datafile=fso.OpenTextFile(".\files\isotopes\ERHB_Z008.txt",ForReading);
	//var datafile=document.location"./files/isotopes/ERHB_"+zNum+".txt"
	//var arr=datafile.innerText.split("\n")
	
	var new_element=document.createElement("script");
    new_element.setAttribute("type","text/javascript");
    new_element.setAttribute("src","./js/obs.js");
    document.body.appendChild(new_element);
	
	var obs=RHB(iz,jn)
	var div6 = document.getElementById('E_RHB');
	div6.innerHTML = "<h5>E<sub>RHB</sub> = -"+Number(obs[2]).toFixed(2)+" MeV</h5>";
	
	div6 = document.getElementById('E_5DCH');
	div6.innerHTML = "<h5>E<sub>5DCH</sub> = -"+Number(obs[3]).toFixed(2)+" MeV</h5>";
	
	div6 = document.getElementById('E_exp');
	if (isNaN(obs[4]))  {div6.innerHTML = "<h5>E<sub>exp</sub> = "+obs[4]+"</h5>";}
	if (!isNaN(obs[4])) {div6.innerHTML = "<h5>E<sub>exp</sub> = -"+Number(obs[4]).toFixed(2)+" MeV</h5>";}
	
	div6 = document.getElementById('beta');
	div6.innerHTML = "<h5>&beta; = "+Number(obs[0]).toFixed(2)+"</h5>";
	
	div6 = document.getElementById('gamma');
	div6.innerHTML = "<h5>&gamma; = "+obs[1]+"<sup>o</sup></h5>";
	
	updateSpectroscopyResult(iz, jn, elementSymbol);
  }
  
  return m;
}


function changeZN(a,b) {
	
    var Z1 = a.lastIndexOf("Z");
    var N1 = a.lastIndexOf("N");
    var D = a.lastIndexOf("_");
    var Z = a.slice(Z1+1,N1);
    var N = a.slice(N1+1,D);
    var Z=parseInt(Z);
    var N=parseInt(N);
	if (b==0) {Z=Z+0; m=linkZN(Z,N); return m;}
    else if (b==1) {Z=Z+2; m=linkZN(Z,N); return m;}
    else if (b==2) {N=N-2; m=linkZN(Z,N); return m;}
    else if (b==3) {N=N+2; m=linkZN(Z,N); return m;}
    else {Z=Z-2; m=linkZN(Z,N); return m;}
 
}

function saveFig(a) {
	
    var D = a.lastIndexOf(".");
    var name = a.slice(0,D);
	var m = name + ".pdf"
	return m
 
}

function setResultView(view) {
	currentResultView = (view == "spectroscopy") ? "spectroscopy" : "ground";
	var resultPanel = document.getElementById('result_panel');
	var groundView = document.getElementById('ground_result_view');
	var groundTitle = document.getElementById('ground_result_title');
	var groundPropertiesPanel = document.getElementById('ground_properties_panel');
	var spectroscopyView = document.getElementById('spectroscopy_result_view');
	var spectroscopyTitle = document.getElementById('spectroscopy_result_title');
	var groundButton = document.getElementById('ground_result_button');
	var spectroscopyButton = document.getElementById('spectroscopy_result_button');
	if (!resultPanel || !groundView || !groundTitle || !groundPropertiesPanel || !spectroscopyView || !spectroscopyTitle || !groundButton || !spectroscopyButton) {
		return;
	}
	if (currentResultView == "spectroscopy") {
		resultPanel.className = "col-lg-7";
		groundView.style.display = "none";
		groundTitle.style.display = "none";
		groundPropertiesPanel.style.display = "none";
		spectroscopyView.style.display = "";
		spectroscopyTitle.style.display = "";
		groundButton.className = "btn btn-default";
		spectroscopyButton.className = "btn btn-primary active";
	}
	else {
		resultPanel.className = "col-lg-5";
		groundView.style.display = "";
		groundTitle.style.display = "";
		groundPropertiesPanel.style.display = "";
		spectroscopyView.style.display = "none";
		spectroscopyTitle.style.display = "none";
		groundButton.className = "btn btn-primary active";
		spectroscopyButton.className = "btn btn-default";
	}
}

function updateSpectroscopyResult(iz, jn, elementSymbol) {
	var aNum = parseInt(iz) + parseInt(jn);
	var key = elementSymbol[parseInt(iz)] + aNum;
	var title = document.getElementById('spectroscopy_title');
	var status = document.getElementById('spectroscopy_status');
	var imageRow = document.getElementById('spectroscopy_image_row');
	var image = document.getElementById('spectroscopy_image');
	if (!title || !status || !imageRow || !image) {
		return;
	}
	title.innerText = "Spectroscopy for " + key;
	var results = window.GBH_RESULTS || {};
	var result = results[key];
	if (!result) {
		status.innerHTML = "<div class='alert alert-warning' role='alert'><h5>Spectroscopy result is not available for " + key + ".</h5></div>";
		imageRow.style.display = "none";
		setResultView(currentResultView);
		return;
	}
	status.innerHTML = "";
	image.src = result.image;
	image.alt = key + " excitation bands";
	imageRow.style.display = "";
	setResultView(currentResultView);
}
  
  

  
