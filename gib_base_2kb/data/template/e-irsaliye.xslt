<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ccts="urn:un:unece:uncefact:documentation:2" xmlns:clm54217="urn:un:unece:uncefact:codelist:specification:54217:2001" xmlns:clm5639="urn:un:unece:uncefact:codelist:specification:5639:1988" xmlns:clm66411="urn:un:unece:uncefact:codelist:specification:66411:2001" xmlns:clmIANAMIMEMediaType="urn:un:unece:uncefact:codelist:specification:IANAMIMEMediaType:2003" xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:link="http://www.xbrl.org/2003/linkbase" xmlns:n1="urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2" xmlns:qdt="urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2" xmlns:udt="urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2" xmlns:xbrldi="http://xbrl.org/2006/xbrldi" xmlns:xbrli="http://www.xbrl.org/2003/instance" xmlns:xdt="http://www.w3.org/2005/xpath-datatypes" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" exclude-result-prefixes="cac cbc ccts clm54217 clm5639 clm66411 clmIANAMIMEMediaType fn link n1 qdt udt xbrldi xbrli xdt xlink xs xsd xsi">
	<xsl:character-map name="a">
		<xsl:output-character character="&#128;" string="" />
		<xsl:output-character character="&#129;" string="" />
		<xsl:output-character character="&#130;" string="" />
		<xsl:output-character character="&#131;" string="" />
		<xsl:output-character character="&#132;" string="" />
		<xsl:output-character character="&#133;" string="" />
		<xsl:output-character character="&#134;" string="" />
		<xsl:output-character character="&#135;" string="" />
		<xsl:output-character character="&#136;" string="" />
		<xsl:output-character character="&#137;" string="" />
		<xsl:output-character character="&#138;" string="" />
		<xsl:output-character character="&#139;" string="" />
		<xsl:output-character character="&#140;" string="" />
		<xsl:output-character character="&#141;" string="" />
		<xsl:output-character character="&#142;" string="" />
		<xsl:output-character character="&#143;" string="" />
		<xsl:output-character character="&#144;" string="" />
		<xsl:output-character character="&#145;" string="" />
		<xsl:output-character character="&#146;" string="" />
		<xsl:output-character character="&#147;" string="" />
		<xsl:output-character character="&#148;" string="" />
		<xsl:output-character character="&#149;" string="" />
		<xsl:output-character character="&#150;" string="" />
		<xsl:output-character character="&#151;" string="" />
		<xsl:output-character character="&#152;" string="" />
		<xsl:output-character character="&#153;" string="" />
		<xsl:output-character character="&#154;" string="" />
		<xsl:output-character character="&#155;" string="" />
		<xsl:output-character character="&#156;" string="" />
		<xsl:output-character character="&#157;" string="" />
		<xsl:output-character character="&#158;" string="" />
		<xsl:output-character character="&#159;" string="" />
	</xsl:character-map>
	<xsl:decimal-format name="european" decimal-separator="," grouping-separator="." NaN="" />
	<xsl:output version="4.0" method="html" indent="no" encoding="UTF-8" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" doctype-system="http://www.w3.org/TR/html4/loose.dtd" use-character-maps="a" />
	<xsl:param name="SV_OutputFormat" select="'HTML'" />
	<xsl:variable name="XML" select="/" />


	<xsl:template match="/">
		<html>
			<head>

                <script type="text/javascript">
                    <![CDATA[var QRCode;!function(){function a(a){this.mode=c.MODE_8BIT_BYTE,this.data=a,this.parsedData=[];for(var b=[],d=0,e=this.data.length;e>d;d++){var f=this.data.charCodeAt(d);f>65536?(b[0]=240|(1835008&f)>>>18,b[1]=128|(258048&f)>>>12,b[2]=128|(4032&f)>>>6,b[3]=128|63&f):f>2048?(b[0]=224|(61440&f)>>>12,b[1]=128|(4032&f)>>>6,b[2]=128|63&f):f>128?(b[0]=192|(1984&f)>>>6,b[1]=128|63&f):b[0]=f,this.parsedData=this.parsedData.concat(b)}this.parsedData.length!=this.data.length&&(this.parsedData.unshift(191),this.parsedData.unshift(187),this.parsedData.unshift(239))}function b(a,b){this.typeNumber=a,this.errorCorrectLevel=b,this.modules=null,this.moduleCount=0,this.dataCache=null,this.dataList=[]}function i(a,b){if(void 0==a.length)throw new Error(a.length+"/"+b);for(var c=0;c<a.length&&0==a[c];)c++;this.num=new Array(a.length-c+b);for(var d=0;d<a.length-c;d++)this.num[d]=a[d+c]}function j(a,b){this.totalCount=a,this.dataCount=b}function k(){this.buffer=[],this.length=0}function m(){return"undefined"!=typeof CanvasRenderingContext2D}function n(){var a=!1,b=navigator.userAgent;return/android/i.test(b)&&(a=!0,aMat=b.toString().match(/android ([0-9]\.[0-9])/i),aMat&&aMat[1]&&(a=parseFloat(aMat[1]))),a}function r(a,b){for(var c=1,e=s(a),f=0,g=l.length;g>=f;f++){var h=0;switch(b){case d.L:h=l[f][0];break;case d.M:h=l[f][1];break;case d.Q:h=l[f][2];break;case d.H:h=l[f][3]}if(h>=e)break;c++}if(c>l.length)throw new Error("Too long data");return c}function s(a){var b=encodeURI(a).toString().replace(/\%[0-9a-fA-F]{2}/g,"a");return b.length+(b.length!=a?3:0)}a.prototype={getLength:function(){return this.parsedData.length},write:function(a){for(var b=0,c=this.parsedData.length;c>b;b++)a.put(this.parsedData[b],8)}},b.prototype={addData:function(b){var c=new a(b);this.dataList.push(c),this.dataCache=null},isDark:function(a,b){if(0>a||this.moduleCount<=a||0>b||this.moduleCount<=b)throw new Error(a+","+b);return this.modules[a][b]},getModuleCount:function(){return this.moduleCount},make:function(){this.makeImpl(!1,this.getBestMaskPattern())},makeImpl:function(a,c){this.moduleCount=4*this.typeNumber+17,this.modules=new Array(this.moduleCount);for(var d=0;d<this.moduleCount;d++){this.modules[d]=new Array(this.moduleCount);for(var e=0;e<this.moduleCount;e++)this.modules[d][e]=null}this.setupPositionProbePattern(0,0),this.setupPositionProbePattern(this.moduleCount-7,0),this.setupPositionProbePattern(0,this.moduleCount-7),this.setupPositionAdjustPattern(),this.setupTimingPattern(),this.setupTypeInfo(a,c),this.typeNumber>=7&&this.setupTypeNumber(a),null==this.dataCache&&(this.dataCache=b.createData(this.typeNumber,this.errorCorrectLevel,this.dataList)),this.mapData(this.dataCache,c)},setupPositionProbePattern:function(a,b){for(var c=-1;7>=c;c++)if(!(-1>=a+c||this.moduleCount<=a+c))for(var d=-1;7>=d;d++)-1>=b+d||this.moduleCount<=b+d||(this.modules[a+c][b+d]=c>=0&&6>=c&&(0==d||6==d)||d>=0&&6>=d&&(0==c||6==c)||c>=2&&4>=c&&d>=2&&4>=d?!0:!1)},getBestMaskPattern:function(){for(var a=0,b=0,c=0;8>c;c++){this.makeImpl(!0,c);var d=f.getLostPoint(this);(0==c||a>d)&&(a=d,b=c)}return b},createMovieClip:function(a,b,c){var d=a.createEmptyMovieClip(b,c),e=1;this.make();for(var f=0;f<this.modules.length;f++)for(var g=f*e,h=0;h<this.modules[f].length;h++){var i=h*e,j=this.modules[f][h];j&&(d.beginFill(0,100),d.moveTo(i,g),d.lineTo(i+e,g),d.lineTo(i+e,g+e),d.lineTo(i,g+e),d.endFill())}return d},setupTimingPattern:function(){for(var a=8;a<this.moduleCount-8;a++)null==this.modules[a][6]&&(this.modules[a][6]=0==a%2);for(var b=8;b<this.moduleCount-8;b++)null==this.modules[6][b]&&(this.modules[6][b]=0==b%2)},setupPositionAdjustPattern:function(){for(var a=f.getPatternPosition(this.typeNumber),b=0;b<a.length;b++)for(var c=0;c<a.length;c++){var d=a[b],e=a[c];if(null==this.modules[d][e])for(var g=-2;2>=g;g++)for(var h=-2;2>=h;h++)this.modules[d+g][e+h]=-2==g||2==g||-2==h||2==h||0==g&&0==h?!0:!1}},setupTypeNumber:function(a){for(var b=f.getBCHTypeNumber(this.typeNumber),c=0;18>c;c++){var d=!a&&1==(1&b>>c);this.modules[Math.floor(c/3)][c%3+this.moduleCount-8-3]=d}for(var c=0;18>c;c++){var d=!a&&1==(1&b>>c);this.modules[c%3+this.moduleCount-8-3][Math.floor(c/3)]=d}},setupTypeInfo:function(a,b){for(var c=this.errorCorrectLevel<<3|b,d=f.getBCHTypeInfo(c),e=0;15>e;e++){var g=!a&&1==(1&d>>e);6>e?this.modules[e][8]=g:8>e?this.modules[e+1][8]=g:this.modules[this.moduleCount-15+e][8]=g}for(var e=0;15>e;e++){var g=!a&&1==(1&d>>e);8>e?this.modules[8][this.moduleCount-e-1]=g:9>e?this.modules[8][15-e-1+1]=g:this.modules[8][15-e-1]=g}this.modules[this.moduleCount-8][8]=!a},mapData:function(a,b){for(var c=-1,d=this.moduleCount-1,e=7,g=0,h=this.moduleCount-1;h>0;h-=2)for(6==h&&h--;;){for(var i=0;2>i;i++)if(null==this.modules[d][h-i]){var j=!1;g<a.length&&(j=1==(1&a[g]>>>e));var k=f.getMask(b,d,h-i);k&&(j=!j),this.modules[d][h-i]=j,e--,-1==e&&(g++,e=7)}if(d+=c,0>d||this.moduleCount<=d){d-=c,c=-c;break}}}},b.PAD0=236,b.PAD1=17,b.createData=function(a,c,d){for(var e=j.getRSBlocks(a,c),g=new k,h=0;h<d.length;h++){var i=d[h];g.put(i.mode,4),g.put(i.getLength(),f.getLengthInBits(i.mode,a)),i.write(g)}for(var l=0,h=0;h<e.length;h++)l+=e[h].dataCount;if(g.getLengthInBits()>8*l)throw new Error("code length overflow. ("+g.getLengthInBits()+">"+8*l+")");for(g.getLengthInBits()+4<=8*l&&g.put(0,4);0!=g.getLengthInBits()%8;)g.putBit(!1);for(;;){if(g.getLengthInBits()>=8*l)break;if(g.put(b.PAD0,8),g.getLengthInBits()>=8*l)break;g.put(b.PAD1,8)}return b.createBytes(g,e)},b.createBytes=function(a,b){for(var c=0,d=0,e=0,g=new Array(b.length),h=new Array(b.length),j=0;j<b.length;j++){var k=b[j].dataCount,l=b[j].totalCount-k;d=Math.max(d,k),e=Math.max(e,l),g[j]=new Array(k);for(var m=0;m<g[j].length;m++)g[j][m]=255&a.buffer[m+c];c+=k;var n=f.getErrorCorrectPolynomial(l),o=new i(g[j],n.getLength()-1),p=o.mod(n);h[j]=new Array(n.getLength()-1);for(var m=0;m<h[j].length;m++){var q=m+p.getLength()-h[j].length;h[j][m]=q>=0?p.get(q):0}}for(var r=0,m=0;m<b.length;m++)r+=b[m].totalCount;for(var s=new Array(r),t=0,m=0;d>m;m++)for(var j=0;j<b.length;j++)m<g[j].length&&(s[t++]=g[j][m]);for(var m=0;e>m;m++)for(var j=0;j<b.length;j++)m<h[j].length&&(s[t++]=h[j][m]);return s};for(var c={MODE_NUMBER:1,MODE_ALPHA_NUM:2,MODE_8BIT_BYTE:4,MODE_KANJI:8},d={L:1,M:0,Q:3,H:2},e={PATTERN000:0,PATTERN001:1,PATTERN010:2,PATTERN011:3,PATTERN100:4,PATTERN101:5,PATTERN110:6,PATTERN111:7},f={PATTERN_POSITION_TABLE:[[],[6,18],[6,22],[6,26],[6,30],[6,34],[6,22,38],[6,24,42],[6,26,46],[6,28,50],[6,30,54],[6,32,58],[6,34,62],[6,26,46,66],[6,26,48,70],[6,26,50,74],[6,30,54,78],[6,30,56,82],[6,30,58,86],[6,34,62,90],[6,28,50,72,94],[6,26,50,74,98],[6,30,54,78,102],[6,28,54,80,106],[6,32,58,84,110],[6,30,58,86,114],[6,34,62,90,118],[6,26,50,74,98,122],[6,30,54,78,102,126],[6,26,52,78,104,130],[6,30,56,82,108,134],[6,34,60,86,112,138],[6,30,58,86,114,142],[6,34,62,90,118,146],[6,30,54,78,102,126,150],[6,24,50,76,102,128,154],[6,28,54,80,106,132,158],[6,32,58,84,110,136,162],[6,26,54,82,110,138,166],[6,30,58,86,114,142,170]],G15:1335,G18:7973,G15_MASK:21522,getBCHTypeInfo:function(a){for(var b=a<<10;f.getBCHDigit(b)-f.getBCHDigit(f.G15)>=0;)b^=f.G15<<f.getBCHDigit(b)-f.getBCHDigit(f.G15);return(a<<10|b)^f.G15_MASK},getBCHTypeNumber:function(a){for(var b=a<<12;f.getBCHDigit(b)-f.getBCHDigit(f.G18)>=0;)b^=f.G18<<f.getBCHDigit(b)-f.getBCHDigit(f.G18);return a<<12|b},getBCHDigit:function(a){for(var b=0;0!=a;)b++,a>>>=1;return b},getPatternPosition:function(a){return f.PATTERN_POSITION_TABLE[a-1]},getMask:function(a,b,c){switch(a){case e.PATTERN000:return 0==(b+c)%2;case e.PATTERN001:return 0==b%2;case e.PATTERN010:return 0==c%3;case e.PATTERN011:return 0==(b+c)%3;case e.PATTERN100:return 0==(Math.floor(b/2)+Math.floor(c/3))%2;case e.PATTERN101:return 0==b*c%2+b*c%3;case e.PATTERN110:return 0==(b*c%2+b*c%3)%2;case e.PATTERN111:return 0==(b*c%3+(b+c)%2)%2;default:throw new Error("bad maskPattern:"+a)}},getErrorCorrectPolynomial:function(a){for(var b=new i([1],0),c=0;a>c;c++)b=b.multiply(new i([1,g.gexp(c)],0));return b},getLengthInBits:function(a,b){if(b>=1&&10>b)switch(a){case c.MODE_NUMBER:return 10;case c.MODE_ALPHA_NUM:return 9;case c.MODE_8BIT_BYTE:return 8;case c.MODE_KANJI:return 8;default:throw new Error("mode:"+a)}else if(27>b)switch(a){case c.MODE_NUMBER:return 12;case c.MODE_ALPHA_NUM:return 11;case c.MODE_8BIT_BYTE:return 16;case c.MODE_KANJI:return 10;default:throw new Error("mode:"+a)}else{if(!(41>b))throw new Error("type:"+b);switch(a){case c.MODE_NUMBER:return 14;case c.MODE_ALPHA_NUM:return 13;case c.MODE_8BIT_BYTE:return 16;case c.MODE_KANJI:return 12;default:throw new Error("mode:"+a)}}},getLostPoint:function(a){for(var b=a.getModuleCount(),c=0,d=0;b>d;d++)for(var e=0;b>e;e++){for(var f=0,g=a.isDark(d,e),h=-1;1>=h;h++)if(!(0>d+h||d+h>=b))for(var i=-1;1>=i;i++)0>e+i||e+i>=b||(0!=h||0!=i)&&g==a.isDark(d+h,e+i)&&f++;f>5&&(c+=3+f-5)}for(var d=0;b-1>d;d++)for(var e=0;b-1>e;e++){var j=0;a.isDark(d,e)&&j++,a.isDark(d+1,e)&&j++,a.isDark(d,e+1)&&j++,a.isDark(d+1,e+1)&&j++,(0==j||4==j)&&(c+=3)}for(var d=0;b>d;d++)for(var e=0;b-6>e;e++)a.isDark(d,e)&&!a.isDark(d,e+1)&&a.isDark(d,e+2)&&a.isDark(d,e+3)&&a.isDark(d,e+4)&&!a.isDark(d,e+5)&&a.isDark(d,e+6)&&(c+=40);for(var e=0;b>e;e++)for(var d=0;b-6>d;d++)a.isDark(d,e)&&!a.isDark(d+1,e)&&a.isDark(d+2,e)&&a.isDark(d+3,e)&&a.isDark(d+4,e)&&!a.isDark(d+5,e)&&a.isDark(d+6,e)&&(c+=40);for(var k=0,e=0;b>e;e++)for(var d=0;b>d;d++)a.isDark(d,e)&&k++;var l=Math.abs(100*k/b/b-50)/5;return c+=10*l}},g={glog:function(a){if(1>a)throw new Error("glog("+a+")");return g.LOG_TABLE[a]},gexp:function(a){for(;0>a;)a+=255;for(;a>=256;)a-=255;return g.EXP_TABLE[a]},EXP_TABLE:new Array(256),LOG_TABLE:new Array(256)},h=0;8>h;h++)g.EXP_TABLE[h]=1<<h;for(var h=8;256>h;h++)g.EXP_TABLE[h]=g.EXP_TABLE[h-4]^g.EXP_TABLE[h-5]^g.EXP_TABLE[h-6]^g.EXP_TABLE[h-8];for(var h=0;255>h;h++)g.LOG_TABLE[g.EXP_TABLE[h]]=h;i.prototype={get:function(a){return this.num[a]},getLength:function(){return this.num.length},multiply:function(a){for(var b=new Array(this.getLength()+a.getLength()-1),c=0;c<this.getLength();c++)for(var d=0;d<a.getLength();d++)b[c+d]^=g.gexp(g.glog(this.get(c))+g.glog(a.get(d)));return new i(b,0)},mod:function(a){if(this.getLength()-a.getLength()<0)return this;for(var b=g.glog(this.get(0))-g.glog(a.get(0)),c=new Array(this.getLength()),d=0;d<this.getLength();d++)c[d]=this.get(d);for(var d=0;d<a.getLength();d++)c[d]^=g.gexp(g.glog(a.get(d))+b);return new i(c,0).mod(a)}},j.RS_BLOCK_TABLE=[[1,26,19],[1,26,16],[1,26,13],[1,26,9],[1,44,34],[1,44,28],[1,44,22],[1,44,16],[1,70,55],[1,70,44],[2,35,17],[2,35,13],[1,100,80],[2,50,32],[2,50,24],[4,25,9],[1,134,108],[2,67,43],[2,33,15,2,34,16],[2,33,11,2,34,12],[2,86,68],[4,43,27],[4,43,19],[4,43,15],[2,98,78],[4,49,31],[2,32,14,4,33,15],[4,39,13,1,40,14],[2,121,97],[2,60,38,2,61,39],[4,40,18,2,41,19],[4,40,14,2,41,15],[2,146,116],[3,58,36,2,59,37],[4,36,16,4,37,17],[4,36,12,4,37,13],[2,86,68,2,87,69],[4,69,43,1,70,44],[6,43,19,2,44,20],[6,43,15,2,44,16],[4,101,81],[1,80,50,4,81,51],[4,50,22,4,51,23],[3,36,12,8,37,13],[2,116,92,2,117,93],[6,58,36,2,59,37],[4,46,20,6,47,21],[7,42,14,4,43,15],[4,133,107],[8,59,37,1,60,38],[8,44,20,4,45,21],[12,33,11,4,34,12],[3,145,115,1,146,116],[4,64,40,5,65,41],[11,36,16,5,37,17],[11,36,12,5,37,13],[5,109,87,1,110,88],[5,65,41,5,66,42],[5,54,24,7,55,25],[11,36,12],[5,122,98,1,123,99],[7,73,45,3,74,46],[15,43,19,2,44,20],[3,45,15,13,46,16],[1,135,107,5,136,108],[10,74,46,1,75,47],[1,50,22,15,51,23],[2,42,14,17,43,15],[5,150,120,1,151,121],[9,69,43,4,70,44],[17,50,22,1,51,23],[2,42,14,19,43,15],[3,141,113,4,142,114],[3,70,44,11,71,45],[17,47,21,4,48,22],[9,39,13,16,40,14],[3,135,107,5,136,108],[3,67,41,13,68,42],[15,54,24,5,55,25],[15,43,15,10,44,16],[4,144,116,4,145,117],[17,68,42],[17,50,22,6,51,23],[19,46,16,6,47,17],[2,139,111,7,140,112],[17,74,46],[7,54,24,16,55,25],[34,37,13],[4,151,121,5,152,122],[4,75,47,14,76,48],[11,54,24,14,55,25],[16,45,15,14,46,16],[6,147,117,4,148,118],[6,73,45,14,74,46],[11,54,24,16,55,25],[30,46,16,2,47,17],[8,132,106,4,133,107],[8,75,47,13,76,48],[7,54,24,22,55,25],[22,45,15,13,46,16],[10,142,114,2,143,115],[19,74,46,4,75,47],[28,50,22,6,51,23],[33,46,16,4,47,17],[8,152,122,4,153,123],[22,73,45,3,74,46],[8,53,23,26,54,24],[12,45,15,28,46,16],[3,147,117,10,148,118],[3,73,45,23,74,46],[4,54,24,31,55,25],[11,45,15,31,46,16],[7,146,116,7,147,117],[21,73,45,7,74,46],[1,53,23,37,54,24],[19,45,15,26,46,16],[5,145,115,10,146,116],[19,75,47,10,76,48],[15,54,24,25,55,25],[23,45,15,25,46,16],[13,145,115,3,146,116],[2,74,46,29,75,47],[42,54,24,1,55,25],[23,45,15,28,46,16],[17,145,115],[10,74,46,23,75,47],[10,54,24,35,55,25],[19,45,15,35,46,16],[17,145,115,1,146,116],[14,74,46,21,75,47],[29,54,24,19,55,25],[11,45,15,46,46,16],[13,145,115,6,146,116],[14,74,46,23,75,47],[44,54,24,7,55,25],[59,46,16,1,47,17],[12,151,121,7,152,122],[12,75,47,26,76,48],[39,54,24,14,55,25],[22,45,15,41,46,16],[6,151,121,14,152,122],[6,75,47,34,76,48],[46,54,24,10,55,25],[2,45,15,64,46,16],[17,152,122,4,153,123],[29,74,46,14,75,47],[49,54,24,10,55,25],[24,45,15,46,46,16],[4,152,122,18,153,123],[13,74,46,32,75,47],[48,54,24,14,55,25],[42,45,15,32,46,16],[20,147,117,4,148,118],[40,75,47,7,76,48],[43,54,24,22,55,25],[10,45,15,67,46,16],[19,148,118,6,149,119],[18,75,47,31,76,48],[34,54,24,34,55,25],[20,45,15,61,46,16]],j.getRSBlocks=function(a,b){var c=j.getRsBlockTable(a,b);if(void 0==c)throw new Error("bad rs block @ typeNumber:"+a+"/errorCorrectLevel:"+b);for(var d=c.length/3,e=[],f=0;d>f;f++)for(var g=c[3*f+0],h=c[3*f+1],i=c[3*f+2],k=0;g>k;k++)e.push(new j(h,i));return e},j.getRsBlockTable=function(a,b){switch(b){case d.L:return j.RS_BLOCK_TABLE[4*(a-1)+0];case d.M:return j.RS_BLOCK_TABLE[4*(a-1)+1];case d.Q:return j.RS_BLOCK_TABLE[4*(a-1)+2];case d.H:return j.RS_BLOCK_TABLE[4*(a-1)+3];default:return void 0}},k.prototype={get:function(a){var b=Math.floor(a/8);return 1==(1&this.buffer[b]>>>7-a%8)},put:function(a,b){for(var c=0;b>c;c++)this.putBit(1==(1&a>>>b-c-1))},getLengthInBits:function(){return this.length},putBit:function(a){var b=Math.floor(this.length/8);this.buffer.length<=b&&this.buffer.push(0),a&&(this.buffer[b]|=128>>>this.length%8),this.length++}};var l=[[17,14,11,7],[32,26,20,14],[53,42,32,24],[78,62,46,34],[106,84,60,44],[134,106,74,58],[154,122,86,64],[192,152,108,84],[230,180,130,98],[271,213,151,119],[321,251,177,137],[367,287,203,155],[425,331,241,177],[458,362,258,194],[520,412,292,220],[586,450,322,250],[644,504,364,280],[718,560,394,310],[792,624,442,338],[858,666,482,382],[929,711,509,403],[1003,779,565,439],[1091,857,611,461],[1171,911,661,511],[1273,997,715,535],[1367,1059,751,593],[1465,1125,805,625],[1528,1190,868,658],[1628,1264,908,698],[1732,1370,982,742],[1840,1452,1030,790],[1952,1538,1112,842],[2068,1628,1168,898],[2188,1722,1228,958],[2303,1809,1283,983],[2431,1911,1351,1051],[2563,1989,1423,1093],[2699,2099,1499,1139],[2809,2213,1579,1219],[2953,2331,1663,1273]],o=function(){var a=function(a,b){this._el=a,this._htOption=b};return a.prototype.draw=function(a){function g(a,b){var c=document.createElementNS("http://www.w3.org/2000/svg",a);for(var d in b)b.hasOwnProperty(d)&&c.setAttribute(d,b[d]);return c}var b=this._htOption,c=this._el,d=a.getModuleCount();Math.floor(b.width/d),Math.floor(b.height/d),this.clear();var h=g("svg",{viewBox:"0 0 "+String(d)+" "+String(d),width:"100%",height:"100%",fill:b.colorLight});h.setAttributeNS("http://www.w3.org/2000/xmlns/","xmlns:xlink","http://www.w3.org/1999/xlink"),c.appendChild(h),h.appendChild(g("rect",{fill:b.colorDark,width:"1",height:"1",id:"template"}));for(var i=0;d>i;i++)for(var j=0;d>j;j++)if(a.isDark(i,j)){var k=g("use",{x:String(i),y:String(j)});k.setAttributeNS("http://www.w3.org/1999/xlink","href","#template"),h.appendChild(k)}},a.prototype.clear=function(){for(;this._el.hasChildNodes();)this._el.removeChild(this._el.lastChild)},a}(),p="svg"===document.documentElement.tagName.toLowerCase(),q=p?o:m()?function(){function a(){this._elImage.src=this._elCanvas.toDataURL("image/png"),this._elImage.style.display="block",this._elCanvas.style.display="none"}function d(a,b){var c=this;if(c._fFail=b,c._fSuccess=a,null===c._bSupportDataURI){var d=document.createElement("img"),e=function(){c._bSupportDataURI=!1,c._fFail&&_fFail.call(c)},f=function(){c._bSupportDataURI=!0,c._fSuccess&&c._fSuccess.call(c)};return d.onabort=e,d.onerror=e,d.onload=f,d.src="data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",void 0}c._bSupportDataURI===!0&&c._fSuccess?c._fSuccess.call(c):c._bSupportDataURI===!1&&c._fFail&&c._fFail.call(c)}if(this._android&&this._android<=2.1){var b=1/window.devicePixelRatio,c=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(a,d,e,f,g,h,i,j){if("nodeName"in a&&/img/i.test(a.nodeName))for(var l=arguments.length-1;l>=1;l--)arguments[l]=arguments[l]*b;else"undefined"==typeof j&&(arguments[1]*=b,arguments[2]*=b,arguments[3]*=b,arguments[4]*=b);c.apply(this,arguments)}}var e=function(a,b){this._bIsPainted=!1,this._android=n(),this._htOption=b,this._elCanvas=document.createElement("canvas"),this._elCanvas.width=b.width,this._elCanvas.height=b.height,a.appendChild(this._elCanvas),this._el=a,this._oContext=this._elCanvas.getContext("2d"),this._bIsPainted=!1,this._elImage=document.createElement("img"),this._elImage.style.display="none",this._el.appendChild(this._elImage),this._bSupportDataURI=null};return e.prototype.draw=function(a){var b=this._elImage,c=this._oContext,d=this._htOption,e=a.getModuleCount(),f=d.width/e,g=d.height/e,h=Math.round(f),i=Math.round(g);b.style.display="none",this.clear();for(var j=0;e>j;j++)for(var k=0;e>k;k++){var l=a.isDark(j,k),m=k*f,n=j*g;c.strokeStyle=l?d.colorDark:d.colorLight,c.lineWidth=1,c.fillStyle=l?d.colorDark:d.colorLight,c.fillRect(m,n,f,g),c.strokeRect(Math.floor(m)+.5,Math.floor(n)+.5,h,i),c.strokeRect(Math.ceil(m)-.5,Math.ceil(n)-.5,h,i)}this._bIsPainted=!0},e.prototype.makeImage=function(){this._bIsPainted&&d.call(this,a)},e.prototype.isPainted=function(){return this._bIsPainted},e.prototype.clear=function(){this._oContext.clearRect(0,0,this._elCanvas.width,this._elCanvas.height),this._bIsPainted=!1},e.prototype.round=function(a){return a?Math.floor(1e3*a)/1e3:a},e}():function(){var a=function(a,b){this._el=a,this._htOption=b};return a.prototype.draw=function(a){for(var b=this._htOption,c=this._el,d=a.getModuleCount(),e=Math.floor(b.width/d),f=Math.floor(b.height/d),g=['<table style="border:0;border-collapse:collapse;">'],h=0;d>h;h++){g.push("<tr>");for(var i=0;d>i;i++)g.push('<td style="border:0;border-collapse:collapse;padding:0;margin:0;width:'+e+"px;height:"+f+"px;background-color:"+(a.isDark(h,i)?b.colorDark:b.colorLight)+';"></td>');g.push("</tr>")}g.push("</table>"),c.innerHTML=g.join("");var j=c.childNodes[0],k=(b.width-j.offsetWidth)/2,l=(b.height-j.offsetHeight)/2;k>0&&l>0&&(j.style.margin=l+"px "+k+"px")},a.prototype.clear=function(){this._el.innerHTML=""},a}();QRCode=function(a,b){if(this._htOption={width:256,height:256,typeNumber:4,colorDark:"#000000",colorLight:"#ffffff",correctLevel:d.H},"string"==typeof b&&(b={text:b}),b)for(var c in b)this._htOption[c]=b[c];"string"==typeof a&&(a=document.getElementById(a)),this._android=n(),this._el=a,this._oQRCode=null,this._oDrawing=new q(this._el,this._htOption),this._htOption.text&&this.makeCode(this._htOption.text)},QRCode.prototype.makeCode=function(a){this._oQRCode=new b(r(a,this._htOption.correctLevel),this._htOption.correctLevel),this._oQRCode.addData(a),this._oQRCode.make(),this._el.title=a,this._oDrawing.draw(this._oQRCode),this.makeImage()},QRCode.prototype.makeImage=function(){"function"==typeof this._oDrawing.makeImage&&(!this._android||this._android>=3)&&this._oDrawing.makeImage()},QRCode.prototype.clear=function(){this._oDrawing.clear()},QRCode.CorrectLevel=d}();]]>
                </script>
                
				<style type="text/css">
					body {
					background-color:#FFFFFF;
					font-family:'Tahoma', "Times New Roman", Times, serif;
					font-size:#FontSize#px;
					font-weight: #FontWeight#;
					color:#666666;
					}
					.table > tbody > tr > td,
					.table > thead > tr > th {
					padding:5px
					}
					.table > thead > tr > th {
					background-color:#eee;
					font-weight:700
					}

					h1,
					h2 {
					padding-bottom:3px;
					padding-top:3px;
					margin-bottom:5px;
					text-transform:uppercase;
					font-family:Arial, Helvetica, sans-serif;
					}
					h1 {
					font-size:1.4em;
					text-transform:none;
					}
					h2 {
					font-size:1em;
					color:brown;
					}
					h3 {
					font-size:1em;
					color:#333333;
					text-align:justify;
					margin:0;
					padding:0;
					}
					h4 {
					font-size:1.1em;
					font-style:bold;
					font-family:Arial, Helvetica, sans-serif;
					color:#000000;
					margin:0;
					padding:0;
					}
					hr {
					height:2px;
					color:#000000;
					background-color:#000000;
					border-bottom:1px solid #000000;
					}
					.hr {
					border-top:3px solid #ccc;
					}
					p,
					ul,
					ol {
					margin-top:1.5em;
					}
					ul,
					ol {
					margin-left:3em;
					}
					blockquote {
					margin-left:3em;
					margin-right:3em;
					font-style:italic;
					}
					a {
					text-decoration:none;
					color:#70A300;
					}
					a:hover {
					border:none;
					color:#70A300;
					}
					#despatchTable {
					border-collapse:collapse;
					font-size:11px;
					width:320px;
					float:right;
					border-color:gray;
					}
					#despatchTable > tbody tr td {
					padding:4px;
					border:1px solid #ccc
					}
					.sevk-adresi{
					padding: 7.5px;
					border: 2px dashed black;
					border-radius: 5px;
					margin-top: 10px; 
					}
					#ettnTable {
					border-collapse:collapse;
					font-size:11px;
					border-color:gray;
					}
					#customerPartyTable {
					border-width:0px;
					border-spacing:
					;
					border-style:inset;
					border-color:gray;
					border-collapse:collapse;
					background-color:
					
					}
					#customerIDTable {
					border-width:2px;
					border-spacing:
					;
					border-style:inset;
					border-color:gray;
					border-collapse:collapse;
					background-color:
					
					}
					#customerIDTableTd {
					border-width:2px;
					border-spacing:
					;
					border-style:inset;
					border-color:gray;
					border-collapse:collapse;
					background-color:
					
					}
					#lineTable {
					border-width:2px;
					border-spacing:
					;
					border-color:black;
					border-collapse:collapse;
					background-color:
					;
					}
					td.lineTableTd {
					border-width:1px;
					padding:1px;
					border-style:inset;
					border-color:black;
					background-color:white;
					}
					tr.lineTableTr {
					border-width:1px;
					padding:0px;
					border-style:inset;
					border-color:black;
					background-color:white;
					-moz-border-radius:
					;
					}
					#lineTableDummyTd {
					border-width:1px;
					border-color:white;
					padding:1px;
					border-style:inset;
					border-color:black;
					background-color:white;
					}
					td.lineTableBudgetTd {
					border-width:2px;
					border-spacing:0px;
					padding:1px;
					border-style:inset;
					border-color:black;
					background-color:white;
					-moz-border-radius:
					;
					}
					#notesTable {
					border-width:2px;
					border-spacing:
					;
					border-style:inset;
					border-color:black;
					border-collapse:collapse;
					background-color:
					
					}
					#notesTableTd {
					border-width:0px;
					border-spacing:
					;
					border-style:inset;
					border-color:black;
					border-collapse:collapse;
					background-color:
					;
					vertical-align:top;
					}
					table {
					border-spacing:0px;
					}
					#budgetContainerTable {
					border-width:0px;
					border-spacing:0px;
					float:right;
					border-style:inset;
					width:320px;
					border-color:black;
					border-collapse:collapse;
					background-color:
					;
					margin-top:10px;
					}
					#budgetContainerTable > tbody > tr > td:first-child {
					width:px
					}
					#budgetContainerTable > tbody > tr:last-child {
					background-color:#dfdfdf
					}
					#monetory-total > tbody > tr > td {
					text-align:right
					}
					#monetory-total > tbody > tr:last-child > td {
					background:#dfdfdf
					}
					#budgetContainerTable > tbody > tr > td {
					border:1px solid #ccc;
					padding:4px
					}
					td {
					border-color:gray;
					}
					.malHizmetTablosu {
					margin-bottom:10px
					}
					.malHizmetTablosu > table {
					font-family:Verdana;
					background:#fff;
					width:800px;
					border-collapse:collapse;
					text-align:left;
					}
					.malHizmetTablosu > table th {
					font-weight:normal;
					padding:2px 5px 2px 8px;
					text-align:right;
					min-width:30px;
					font-size:12px;
					color:black;
					border-bottom:1px solid #ccc;
					background-color:#DFDFDF;
					border-right:1px solid #ccc;
					border-top:1px solid #ccc;
					vertical-align:middle;
					height:35px;
					}
					.malHizmetTablosu > table th .thTopTitle {
					text-align:center;
					width:89px;
					}
					.malHizmetTablosu > table th .thSubTitle {
					width:47px;
					display:inline-block;
					text-align:right;
					}
					.malHizmetTablosu > table th .thSubTitle.HF {
					width:36px;
					}
					.malHizmetTablosu > table th.alignLeft {
					text-align:left;
					}
					.malHizmetTablosu > table th.alignCenter {
					text-align:center;
					}
					.malHizmetTablosu > table td {
					border-bottom:1px solid #ccc;
					color:#000;
					padding-top:6px;
					padding-bottom:6px;
					border-right:1px solid #ccc;
					padding-right:3px;
					white-space:nowrap;
					text-align:right;
					}
					.malHizmetTablosu > table td.wrap {
					white-space:normal;
					text-align:left;
					padding-left:8px;
					}
					.malHizmetTablosu > table td:first-child,
					.malHizmetTablosu > table th:first-child {
					padding:2px;
					border-left:1px solid #ccc;
					}
					.malHizmetTablosu > table td:last-child,
					.malHizmetTablosu > table th:last-child {
					padding-right:6px;
					}
					.malHizmetTablosu > table tbody tr:hover td {
					background-color:#E4E4E4;
					}
					.malHizmetTablosu > table tbody tr:nth-child(even) td {
					background:#FFF
					}
					.malHizmetTablosu > table tbody tr:nth-child(odd) td {
					background:#EEE
					}
					.malHizmetTablosu > table th.alignLeft {
					text-align:left;
					}
					#documanLines {
					border-collapse:collapse;
					border:1px solid #ccc;
					padding:3px;
					}
					#documanLines td,
					#documanLines th {
					text-align:left;
					border:1px solid #ccc;
					padding:3px
					}
					#documanLines tr:first-child th {
					border-top:0;
					}
					#documanLines tr:last-child td {
					border-bottom:0;
					}
					#documanLines tr td:first-child,
					#documanLines tr th:first-child {
					border-left:0;
					}
					#documanLines tr td:last-child,
					#documanLines tr th:last-child {
					border-right:0;
					}
					#carrierInformation {
					border-collapse:collapse;
					border:1px solid #ccc;
					padding:3px;
					}
					#carrierInformation td,
					#carrierInformation th {
					text-align:left;
					border:1px solid #ccc;
					padding:3px
					}
					.t-l {
					text-align:left;
					}
					.t-r {
					text-align:right;
					}
					.w-800 {
					width:800px;
					}
					.mb-5 {
					margin-bottom:5px;
					}
					.mt-5 {
					margin-top:5px;
					}
					.mt-10 {
					margin-top:10px;
					}
					.key-value-table {
					border-collapse:collapse;
					font-size:11px;
					width:320px;
					float:right;
					border-color:gray;
					vertical-align:bottom
					}
					.key-value-table > tbody tr > td {
					padding:4px;
					border:1px solid #ccc
					}
					.key-value-table > tbody tr > td:first-child {
					font-weight:700
					}
					.border > thead > tr:first-child > th {
					border-top:1px solid #ccc
					}
					.border > tbody > tr > td:first-child,
					.border > thead > tr > th:first-child {
					border-left:1px solid #ccc
					}
					.border > tbody > tr > td,
					.border > thead > tr > th {
					border-bottom:1px solid #ccc;
					border-right:1px solid #ccc
					}
					.invoice-line > tbody > tr > td {
					padding:5px;
					white-space:nowrap
					}
					.invoice-line > tbody tr:nth-child(even) td {
					background:#fff;
					}
					.invoice-line > tbody tr:nth-child(odd) td {
					background:#eee;
					}
					.invoice-line > thead > tr > th {
					background-color:#dfdfdf;
					padding:5px;
					height:30px
					}
					.t-c {
					text-align:center
					}</style>
				<title>e-İrsaliye</title>
			</head>
			<body style="margin-left=0.6in; margin-right=0.6in; margin-top=0.79in; margin-bottom=0.79in">
				<xsl:for-each select="$XML">
					<table class="w-800">
						<tbody>
							<tr>
								<td width="40%">
									<div class="hr mb-5" />
									<table>
										<tbody>
											<tr>
												<xsl:for-each select="n1:DespatchAdvice/cac:DespatchSupplierParty/cac:Party">
													<xsl:call-template name="Party_Title">
														<xsl:with-param name="PartyType">SUPPLIER</xsl:with-param>
													</xsl:call-template>
												</xsl:for-each>
											</tr>
											<tr>
												<xsl:for-each select="n1:DespatchAdvice/cac:DespatchSupplierParty/cac:Party">
													<td>
														<xsl:for-each select="cac:PostalAddress">
															<xsl:for-each select="cbc:StreetName">
																<xsl:apply-templates />
																<xsl:text>&#160;</xsl:text>
															</xsl:for-each>
															<xsl:for-each select="cbc:BuildingName">
																<xsl:apply-templates />
															</xsl:for-each>
															<xsl:if test="cbc:BuildingNumber">
																<xsl:text> No:</xsl:text>
																<xsl:for-each select="cbc:BuildingNumber">
																	<xsl:apply-templates />
																</xsl:for-each>
																<xsl:text>&#160;</xsl:text>
															</xsl:if>
															<br />
															<xsl:for-each select="cbc:PostalZone">
																<xsl:apply-templates />
																<xsl:text>&#160;</xsl:text>
															</xsl:for-each>
															<xsl:for-each select="cbc:CitySubdivisionName">
																<xsl:apply-templates />
															</xsl:for-each>
															<xsl:text>/ </xsl:text>
															<xsl:for-each select="cbc:CityName">
																<xsl:apply-templates />
																<xsl:text>&#160;</xsl:text>
															</xsl:for-each>
														</xsl:for-each>
													</td>
												</xsl:for-each>
											</tr>
											<xsl:if test="//n1:DespatchAdvice/cac:DespatchSupplierParty/cac:Party/cac:Contact/cbc:Telephone or //n1:DespatchAdvice/cac:DespatchSupplierParty/cac:Party/cac:Contact/cbc:Telefax">
												<tr>
													<xsl:for-each select="n1:DespatchAdvice/cac:DespatchSupplierParty/cac:Party">
														<td>
															<xsl:for-each select="cac:Contact">
																<xsl:if test="cbc:Telephone">
																	<xsl:text>Tel: </xsl:text>
																	<xsl:for-each select="cbc:Telephone">
																		<xsl:apply-templates />
																	</xsl:for-each>
																</xsl:if>
																<xsl:if test="cbc:Telefax">
																	<xsl:text> Fax: </xsl:text>
																	<xsl:for-each select="cbc:Telefax">
																		<xsl:apply-templates />
																	</xsl:for-each>
																</xsl:if>
																<xsl:text>&#160;</xsl:text>
															</xsl:for-each>
														</td>
													</xsl:for-each>
												</tr>
											</xsl:if>
											<xsl:for-each select="//n1:DespatchAdvice/cac:DespatchSupplierParty/cac:Party/cbc:WebsiteURI">
												<tr>
													<td>
														<xsl:text>Web Sitesi: </xsl:text>
														<xsl:value-of select="." />
													</td>
												</tr>
											</xsl:for-each>
											<xsl:for-each select="//n1:DespatchAdvice/cac:DespatchSupplierParty/cac:Party/cac:Contact/cbc:ElectronicMail">
												<tr>
													<td>
														<xsl:text>E-Posta: </xsl:text>
														<xsl:value-of select="." />
													</td>
												</tr>
											</xsl:for-each>
											<tr>
												<xsl:for-each select="n1:DespatchAdvice/cac:DespatchSupplierParty/cac:Party">
													<td>
														<xsl:text>Vergi Dairesi: </xsl:text>
														<xsl:for-each select="cac:PartyTaxScheme">
															<xsl:for-each select="cac:TaxScheme">
																<xsl:for-each select="cbc:Name">
																	<xsl:apply-templates />
																</xsl:for-each>
															</xsl:for-each>
															<xsl:text>&#160; </xsl:text>
														</xsl:for-each>
													</td>
												</xsl:for-each>
											</tr>
											<xsl:for-each select="//n1:DespatchAdvice/cac:DespatchSupplierParty/cac:Party/cac:PartyIdentification">
												<tr>
													<td>
														<xsl:value-of select="cbc:ID/@schemeID" />
														<xsl:text>: </xsl:text>
														<xsl:value-of select="cbc:ID" />
													</td>
												</tr>
											</xsl:for-each>
										</tbody>
									</table>

									<div class="hr mt-5" />
									<div class="hr mt-5 mb-5" />

									<table>
										<tbody>
											<tr style="height:71px; ">
												<td>
													<table align="center" border="0">
														<tbody>
															<tr>
																<xsl:for-each select="n1:DespatchAdvice/cac:DeliveryCustomerParty/cac:Party">
																	<td style="width:469px; ">
																		<span style="font-weight:bold; ">
																			<xsl:text>SAYIN</xsl:text>
																		</span>
																	</td>
																</xsl:for-each>
															</tr>
															<tr>
																<xsl:choose>
																	<xsl:when test="n1:DespatchAdvice/cac:BuyerCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID[@schemeID='PARTYTYPE' and text()='TAXFREE']">
																		<xsl:for-each select="n1:DespatchAdvice/cac:BuyerCustomerParty/cac:Party">
																			<xsl:call-template name="Party_Title">
																				<xsl:with-param name="PartyType">TAXFREE</xsl:with-param>
																			</xsl:call-template>
																		</xsl:for-each>
																	</xsl:when>
																	<xsl:otherwise>
																		<xsl:for-each select="n1:DespatchAdvice/cac:DeliveryCustomerParty/cac:Party">
																			<xsl:call-template name="Party_Title">
																				<xsl:with-param name="PartyType">OTHER</xsl:with-param>
																			</xsl:call-template>
																		</xsl:for-each>
																	</xsl:otherwise>
																</xsl:choose>
															</tr>
															<xsl:choose>
																<xsl:when test="n1:DespatchAdvice/cac:BuyerCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID[@schemeID='PARTYTYPE' and text()='TAXFREE']">
																	<xsl:for-each select="n1:DespatchAdvice/cac:BuyerCustomerParty/cac:Party">
																		<tr>
																			<xsl:call-template name="Party_Adress">
																				<xsl:with-param name="PartyType">TAXFREE</xsl:with-param>
																			</xsl:call-template>
																		</tr>
																		<xsl:call-template name="Party_Other">
																			<xsl:with-param name="PartyType">TAXFREE</xsl:with-param>
																		</xsl:call-template>
																	</xsl:for-each>
																</xsl:when>
																<xsl:otherwise>
																	<xsl:for-each select="n1:DespatchAdvice/cac:DeliveryCustomerParty/cac:Party">
																		<tr>
																			<xsl:call-template name="Party_Adress">
																				<xsl:with-param name="PartyType">OTHER</xsl:with-param>
																			</xsl:call-template>
																		</tr>
																		<xsl:call-template name="Party_Other">
																			<xsl:with-param name="PartyType">OTHER</xsl:with-param>
																		</xsl:call-template>
																	</xsl:for-each>
																</xsl:otherwise>
															</xsl:choose>
															<xsl:if test="//n1:DespatchAdvice/cac:Shipment/cac:Delivery/cac:DeliveryAddress/cbc:StreetName">
																<xsl:if test="//n1:DespatchAdvice/cac:DeliveryCustomerParty/cac:Party/cac:PostalAddress/cbc:StreetName != //n1:DespatchAdvice/cac:Shipment/cac:Delivery/cac:DeliveryAddress/cbc:StreetName">
																	<tr>
																		<td>
																			<div class="sevk-adresi">
																				<b>Sevk Adresi </b>
																				<xsl:value-of select="//n1:DespatchAdvice/cac:Shipment/cac:Delivery/cac:DeliveryAddress/cbc:StreetName" />
																				<br />
																				<xsl:value-of select="//n1:DespatchAdvice/cac:Shipment/cac:Delivery/cac:DeliveryAddress/cbc:CitySubdivisionName" />
																				<br />
																				<xsl:value-of select="//n1:DespatchAdvice/cac:Shipment/cac:Delivery/cac:DeliveryAddress/cbc:CityName" />
																				<br />
																				<xsl:value-of select="//n1:DespatchAdvice/cac:Shipment/cac:Delivery/cac:DeliveryAddress/cac:Country/cbc:Name" />
																			</div>
																		</td>
																	</tr>
																</xsl:if>
															</xsl:if>
														</tbody>
													</table>
												</td>
											</tr>
										</tbody>
									</table>
									<div class="hr mt-5" />
								</td>
								<td width="20%" align="center" valign="middle">
									<img style="width:91px;" align="middle" alt="E-Fatura Logo" src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/4QBoRXhpZgAASUkqAAgAAAADABIBAwABAAAAAQAAADEBAgAQAAAAMgAAAGmHBAABAAAAQgAAAAAAAABTaG90d2VsbCAwLjIyLjAAAgACoAkAAQAAAKYBAAADoAkAAQAAAKYBAAAAAAAA/+EJ9Gh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8APD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNC40LjAtRXhpdjIiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczpleGlmPSJodHRwOi8vbnMuYWRvYmUuY29tL2V4aWYvMS4wLyIgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iIGV4aWY6UGl4ZWxYRGltZW5zaW9uPSI0MjIiIGV4aWY6UGl4ZWxZRGltZW5zaW9uPSI0MjIiIHRpZmY6SW1hZ2VXaWR0aD0iNDIyIiB0aWZmOkltYWdlSGVpZ2h0PSI0MjIiIHRpZmY6T3JpZW50YXRpb249IjEiLz4gPC9yZGY6UkRGPiA8L3g6eG1wbWV0YT4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8P3hwYWNrZXQgZW5kPSJ3Ij8+/9sAQwADAgIDAgIDAwMDBAMDBAUIBQUE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" />
									<h1 align="center">
										<span style="font-weight:bold; ">
											<xsl:text>e-İrsaliye</xsl:text>
										</span>
									</h1>
								</td>
								<td width="40%">

                                    <div id="qrcode_container" style="float: right; margin-bottom: 5px;">
                                        <div id="qrcode"/>
                                        <div id="qrvalue" style="visibility: hidden; height: 20px;width: 20px; ; display:none" > {"vkntckn":"<xsl:value-of select="n1:DespatchAdvice/cac:DespatchSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID[@schemeID ='TCKN' or @schemeID = 'VKN']"/>", "avkntckn":"<xsl:value-of select="n1:DespatchAdvice/cac:DeliveryCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID[@schemeID ='TCKN' or @schemeID = 'VKN']"/>", "senaryo":"<xsl:value-of select="n1:DespatchAdvice/cbc:ProfileID"/>", "tip":"<xsl:value-of select="n1:DespatchAdvice/cbc:DespatchAdviceTypeCode"/>", "tarih":"<xsl:value-of select="n1:DespatchAdvice/cbc:IssueDate"/>", "no":"<xsl:value-of select="n1:DespatchAdvice/cbc:ID"/>", "ettn":"<xsl:value-of select="n1:DespatchAdvice/cbc:UUID"/>", "sevktarihi":"<xsl:value-of select="n1:DespatchAdvice/cac:Shipment/cac:Delivery/cac:Despatch/cbc:ActualDespatchDate"/>", "sevkzamani":"<xsl:value-of select="n1:DespatchAdvice/cac:Shipment/cac:Delivery/cac:Despatch/cbc:ActualDespatchTime"/>", "tasiyicivkn":"<xsl:value-of select="n1:DespatchAdvice/cac:Shipment/cac:Delivery/cac:CarrierParty/cac:PartyIdentification/cbc:ID"/>", "plaka":"<xsl:value-of select="n1:DespatchAdvice/cac:Shipment/cac:ShipmentStage/cac:TransportMeans/cac:RoadTransport/cbc:LicensePlateID"/>"} </div>
                                        <script type="text/javascript">
                                            var qrcode = new QRCode(document.getElementById("qrcode"), { width : 140, height : 140, correctLevel : QRCode.CorrectLevel.L });

                                            function makeCode (msg) {
                                            var elText = document.getElementById("text");
                                            qrcode.makeCode(msg);
                                            }

                                            makeCode(document.getElementById("qrvalue").innerHTML);
                                        </script>
                                    </div>
                                    
									<div style="width:100%" class="t-c mb-10">
                                        
                                        
                                    </div>
									<div>
										<table class="key-value-table">
											<tbody>
												<tr>
													<td style="width:115px;">Özelleştirme No</td>
													<td style="width:110px;">
														<xsl:for-each select="n1:DespatchAdvice/cbc:CustomizationID">
															<xsl:apply-templates />
														</xsl:for-each>
													</td>
												</tr>
												<tr>
													<td>Senaryo</td>
													<td>
														<xsl:for-each select="n1:DespatchAdvice/cbc:ProfileID">
															<xsl:apply-templates />
														</xsl:for-each>
													</td>
												</tr>
												<tr>
													<td>İrsaliye Tipi</td>
													<td>
														<xsl:for-each select="n1:DespatchAdvice/cbc:DespatchAdviceTypeCode">
															<xsl:apply-templates />
														</xsl:for-each>
													</td>
												</tr>
												<tr>
													<td>İrsaliye No</td>
													<td>
														<xsl:for-each select="n1:DespatchAdvice/cbc:ID">
															<xsl:apply-templates />
														</xsl:for-each>
													</td>
												</tr>
												<tr>
													<td>İrsaliye Tarihi / Zamanı</td>
													<td>
														<xsl:for-each select="n1:DespatchAdvice/cbc:IssueDate">
															<xsl:apply-templates select="." />
														</xsl:for-each>
														/
														<xsl:for-each select="n1:DespatchAdvice/cbc:IssueTime">
															<xsl:apply-templates select="." />
														</xsl:for-each>
													</td>
												</tr>
												<tr>
													<td>Sevk Tarihi / Zamanı</td>
													<td>
														<xsl:for-each select="n1:DespatchAdvice/cac:Shipment/cac:Delivery/cac:Despatch/cbc:ActualDespatchDate">
															<xsl:apply-templates select="." />
														</xsl:for-each>
														/
														<xsl:for-each select="n1:DespatchAdvice/cac:Shipment/cac:Delivery/cac:Despatch/cbc:ActualDespatchTime">
															<xsl:apply-templates select="." />
														</xsl:for-each>
													</td>
												</tr>


												<xsl:if test="n1:DespatchAdvice/cac:OrderReference">
													<tr>
														<td>Sipariş No</td>
														<td>
															<xsl:for-each select="n1:DespatchAdvice/cac:OrderReference/cbc:ID">
																<xsl:apply-templates />
															</xsl:for-each>
														</td>
													</tr>
												</xsl:if>
												<xsl:if test="n1:DespatchAdvice/cac:OrderReference/cbc:IssueDate">
													<tr>
														<td>Sipariş Tarihi</td>
														<td>
															<xsl:for-each select="n1:DespatchAdvice/cac:OrderReference/cbc:IssueDate">
																<xsl:apply-templates select="." />
															</xsl:for-each>
														</td>
													</tr>
												</xsl:if>
											</tbody>
										</table>
									</div>

								</td>
							</tr>

							<tr>
								<td>
									<b>ETTN: </b>
									<xsl:value-of select="n1:DespatchAdvice/cbc:UUID" />
								</td>
							</tr>
						</tbody>
					</table>
					<div style="clear:both" class="mt-10" />

					<table class="invoice-line border w-800">
						<thead>
							<tr>
								<th>Sıra No</th>
								<th class="t-l">Mal Hizmet</th>
								<th class="t-r">Miktar</th>


								<xsl:if test="//n1:DespatchAdvice/cac:DespatchLine/cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cac:Price/cbc:PriceAmount">
									<th class="t-r">Birim Fiyat</th>
								</xsl:if>


								<xsl:if test="//n1:DespatchAdvice/cac:DespatchLine/cbc:OutstandingQuantity">
									<th class="t-r"> Sonra Gönderilecek Miktar</th>
								</xsl:if>


								<xsl:if test="//n1:DespatchAdvice/cac:DespatchLine/cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cbc:LineExtensionAmount">


									<th class="t-r">Tutar</th>
								</xsl:if>
							</tr>
						</thead>
						<tbody>
							<xsl:for-each select="//n1:DespatchAdvice/cac:DespatchLine">
								<xsl:apply-templates select="." />
							</xsl:for-each>
						</tbody>
					</table>
				</xsl:for-each>

				<div style="clear: both" />

				<xsl:variable name="printAdditionalDocuments">
					<xsl:for-each select="//n1:DespatchAdvice/cac:AdditionalDocumentReference">
						<xsl:if test="not(./cac:Attachment) or (./cac:Attachment and not((./cac:Attachment/cbc:EmbeddedDocumentBinaryObject[contains(@filename,'.xslt')])))">
							<xsl:value-of select="true()" />
						</xsl:if>
					</xsl:for-each>
				</xsl:variable>

				<xsl:if test="$printAdditionalDocuments != ''">
					<table class="invoice-line border w-800 mt-10">
						<thead>
							<tr>
								<th colspan="4" style="text-align: center; height:15px">İlgili Dökümanlar</th>
							</tr>
							<tr>
								<th style="height:15px">Doküman No</th>
								<th style="height:15px">Tarih</th>
								<th style="height:15px">Doküman Tipi</th>
								<th style="height:15px">Açıklama</th>
							</tr>
						</thead>
						<tbody>
							<xsl:for-each select="//n1:DespatchAdvice/cac:AdditionalDocumentReference">
								<xsl:if test="not(./cac:Attachment) or (./cac:Attachment and not((./cac:Attachment/cbc:EmbeddedDocumentBinaryObject[contains(@filename,'.xslt')])))">
									<tr>
										<td>
											<xsl:value-of select="./cbc:ID" />
										</td>
										<td>
											<xsl:for-each select="./cbc:IssueDate">
												<xsl:apply-templates select="." />
											</xsl:for-each>
										</td>
										<td>
											<xsl:value-of select="./cbc:DocumentType" />
										</td>
										<td>
											<xsl:value-of select="./cbc:DocumentDescription" />
										</td>
									</tr>
								</xsl:if>
							</xsl:for-each>
						</tbody>
					</table>

					<br />
				</xsl:if>
				<table id="carrierInformation" class="w-800 mt-10">
					<thead>
						<tr>
							<th>
								<span style="font-weight:bold; " align="center">&#160;&#160;&#160;&#160;&#160;Açıklamalar</span>
							</th>
							<th>
								<span style="font-weight:bold; " align="center">&#160;&#160;&#160;&#160;&#160;Taşıyıcı Bilgileri</span>
							</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td id="notesTableTd" height="100">
								<xsl:for-each select="//n1:DespatchAdvice/cbc:Note">
									<b>&#160;&#160;&#160;&#160;&#160;&#160;Not: </b>
									<xsl:value-of select="." />
									<br />
								</xsl:for-each>
								<xsl:for-each select="//cac:SellerSupplierParty">
									<b>&#160;&#160;&#160;&#160;&#160;&#160;Asıl Satıcı VKN: </b>
									<xsl:value-of select="cac:Party/cac:PartyIdentification/cbc:ID" />
									<br />
									<b>&#160;&#160;&#160;&#160;&#160;&#160;Asıl Satıcı Ünvan: </b>
									<xsl:value-of select="cac:Party/cac:PartyName/cbc:Name" />
									<br />
								</xsl:for-each>
								<xsl:for-each select="//cac:BuyerCustomerParty">
									<b>&#160;&#160;&#160;&#160;&#160;&#160;Asıl Alıcı VKN: </b>
									<xsl:value-of select="cac:Party/cac:PartyIdentification/cbc:ID" />
									<br />
									<b>&#160;&#160;&#160;&#160;&#160;&#160;Asıl Alıcı Ünvan: </b>
									<xsl:value-of select="cac:Party/cac:PartyName/cbc:Name" />
									<br />
								</xsl:for-each>
								<xsl:for-each select="//cac:OriginatorCustomerParty">
									<b>&#160;&#160;&#160;&#160;&#160;&#160;İşlemleri Başlatan Alıcı VKN: </b>
									<xsl:value-of select="cac:Party/cac:PartyIdentification/cbc:ID" />
									<br />
									<b>&#160;&#160;&#160;&#160;&#160;&#160;İşlemleri Başlatan Alıcı Ünvan: </b>
									<xsl:value-of select="cac:Party/cac:PartyName/cbc:Name" />
									<br />
								</xsl:for-each>
								<xsl:for-each select="//cac:DespatchSupplierParty/cac:Party/cac:Person">
									<xsl:if test="cbc:FirstName">
										<b>&#160;&#160;&#160;&#160;&#160; Teslim Eden: </b>
										<xsl:for-each select="cbc:Title">
											<xsl:apply-templates />
											<xsl:text>&#160;</xsl:text>
										</xsl:for-each>
										<xsl:for-each select="cbc:FirstName">
											<xsl:apply-templates />
											<xsl:text>&#160;</xsl:text>
										</xsl:for-each>
										<xsl:for-each select="cbc:MiddleName">
											<xsl:apply-templates />
											<xsl:text>&#160;</xsl:text>
										</xsl:for-each>
										<xsl:for-each select="cbc:FamilyName">
											<xsl:apply-templates />
											<xsl:text>&#160;</xsl:text>
										</xsl:for-each>
										<xsl:for-each select="cbc:NameSuffix">
											<xsl:apply-templates />
										</xsl:for-each>
										<br />
									</xsl:if>
								</xsl:for-each>
							</td>
							<td id="notesTableTd" height="100">
								<xsl:for-each select="//cac:CarrierParty">
									<b>&#160;&#160;&#160;&#160;&#160;&#160; Taşıyıcı Firma: </b>
									VKN:
									<xsl:value-of select="./cac:PartyIdentification/cbc:ID" />
									,
									<xsl:value-of select="./cac:PartyName/cbc:Name" />
									<br />
								</xsl:for-each>
								<xsl:for-each select="//cac:ShipmentStage/cac:TransportMeans/cac:RoadTransport/cbc:LicensePlateID">
									<b>&#160;&#160;&#160;&#160;&#160;&#160; Araç plaka numarası: </b>
									<xsl:value-of select="." />
									<br />
								</xsl:for-each>
								<xsl:for-each select="//cac:TransportHandlingUnit/cac:TransportEquipment/cbc:ID[@schemeID = 'DORSEPLAKA']">
									<b>&#160;&#160;&#160;&#160;&#160;&#160; Dorse plaka numarası: </b>
									<xsl:value-of select="." />
									<br />
								</xsl:for-each>
								<xsl:for-each select="//cac:ShipmentStage/cac:DriverPerson">
									<xsl:if test="cbc:FirstName">
										<b>&#160;&#160;&#160;&#160;&#160;&#160; Şoför: </b>
										<xsl:for-each select="cbc:Title">
											<xsl:apply-templates />
											<xsl:text>&#160;</xsl:text>
										</xsl:for-each>
										<xsl:for-each select="cbc:FirstName">
											<xsl:apply-templates />
											<xsl:text>&#160;</xsl:text>
										</xsl:for-each>
										<xsl:for-each select="cbc:MiddleName">
											<xsl:apply-templates />
											<xsl:text>&#160;</xsl:text>
										</xsl:for-each>
										<xsl:for-each select="cbc:FamilyName">
											<xsl:apply-templates />
											<xsl:text>&#160;</xsl:text>
										</xsl:for-each>
										, TCKN:
										<xsl:for-each select="cbc:NationalityID">
											<xsl:apply-templates />
										</xsl:for-each>
										<br />
									</xsl:if>
								</xsl:for-each>
							</td>
						</tr>
					</tbody>
				</table>
			</body>
		</html>
	</xsl:template>


	<xsl:template name="UnitText">
		<xsl:param name="UnitCode" />
		<xsl:choose>
			<xsl:when test="$UnitCode='26'">ton</xsl:when>
			<xsl:when test="$UnitCode='BX'">Kutu</xsl:when>
			<xsl:when test="$UnitCode='LTR'">lt</xsl:when>
			<xsl:when test="$UnitCode='C62'">Adet</xsl:when>
			<xsl:when test="$UnitCode='NIU'">Adet</xsl:when>
			<xsl:when test="$UnitCode='KGM'">kg</xsl:when>
			<xsl:when test="$UnitCode='KJO'">kJ</xsl:when>
			<xsl:when test="$UnitCode='GRM'">g</xsl:when>
			<xsl:when test="$UnitCode='MGM'">mg</xsl:when>
			<xsl:when test="$UnitCode='NT'">Net Ton</xsl:when>
			<xsl:when test="$UnitCode='GT'">Gross Ton</xsl:when>
			<xsl:when test="$UnitCode='MTR'">m</xsl:when>
			<xsl:when test="$UnitCode='MMT'">mm</xsl:when>
			<xsl:when test="$UnitCode='KTM'">km</xsl:when>
			<xsl:when test="$UnitCode='MLT'">ml</xsl:when>
			<xsl:when test="$UnitCode='MMQ'">mm3</xsl:when>
			<xsl:when test="$UnitCode='CLT'">cl</xsl:when>
			<xsl:when test="$UnitCode='CMK'">cm2</xsl:when>
			<xsl:when test="$UnitCode='CMQ'">cm3</xsl:when>
			<xsl:when test="$UnitCode='CMT'">cm</xsl:when>
			<xsl:when test="$UnitCode='MTK'">m2</xsl:when>
			<xsl:when test="$UnitCode='MTQ'">m3</xsl:when>
			<xsl:when test="$UnitCode='DAY'">Gün</xsl:when>
			<xsl:when test="$UnitCode='MON'">Ay</xsl:when>
			<xsl:when test="$UnitCode='PA'">Paket</xsl:when>
			<xsl:when test="$UnitCode='KWH'">KWH</xsl:when>
			<xsl:when test="$UnitCode='ANN'">Yıl</xsl:when>
			<xsl:when test="$UnitCode='HUR'">Saat</xsl:when>
			<xsl:when test="$UnitCode='D61'">Dakika</xsl:when>
			<xsl:when test="$UnitCode='D62'">Saniye</xsl:when>
			<xsl:when test="$UnitCode='CCT'">Ton baş.taşıma kap.</xsl:when>
			<xsl:when test="$UnitCode='D30'">Brüt kalori</xsl:when>
			<xsl:when test="$UnitCode='D40'">1000 lt</xsl:when>
			<xsl:when test="$UnitCode='LPA'">saf alkol lt</xsl:when>
			<xsl:when test="$UnitCode='B32'">kg.m2</xsl:when>
			<xsl:when test="$UnitCode='NCL'">hücre adet</xsl:when>
			<xsl:when test="$UnitCode='PR'">Çift</xsl:when>
			<xsl:when test="$UnitCode='R9'">1000 m3</xsl:when>
			<xsl:when test="$UnitCode='SET'">Set</xsl:when>
			<xsl:when test="$UnitCode='T3'">1000 adet</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$UnitCode" />
			</xsl:otherwise>
		</xsl:choose>


	</xsl:template>


	<xsl:template match="//n1:DespatchAdvice/cac:DespatchLine">
		<tr>
			<td>
				<xsl:value-of select="./cbc:ID" />
			</td>
			<td class="wrap">
				<xsl:value-of select="./cac:Item/cbc:Name" />
			</td>
			<td class="t-r">
				<xsl:value-of select="format-number(./cbc:DeliveredQuantity, '###.###,####', 'european')" />
				<xsl:if test="./cbc:DeliveredQuantity/@unitCode">
					<xsl:for-each select="./cbc:DeliveredQuantity">
						<xsl:text></xsl:text>
						<xsl:call-template name="UnitText">
							<xsl:with-param name="UnitCode">
								<xsl:value-of select="@unitCode" />
							</xsl:with-param>
						</xsl:call-template>
					</xsl:for-each>
				</xsl:if>
			</td>

			<xsl:if test="//n1:DespatchAdvice/cac:DespatchLine/cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cac:Price/cbc:PriceAmount">
				<td class="t-r">
					<xsl:value-of select="format-number(./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cac:Price/cbc:PriceAmount, '###.##0,########', 'european')" />
					<xsl:if test="./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cac:Price/cbc:PriceAmount/@currencyID">
						<xsl:text></xsl:text>
						<xsl:if test="./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cac:Price/cbc:PriceAmount/@currencyID = &quot;TRL&quot; or ./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cac:Price/cbc:PriceAmount/@currencyID = &quot;TRY&quot;">
							<xsl:text>TL</xsl:text>
						</xsl:if>
						<xsl:if test="./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cac:Price/cbc:PriceAmount/@currencyID != &quot;TRL&quot; and ./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cac:Price/cbc:PriceAmount/@currencyID != &quot;TRY&quot;">
							<xsl:value-of select="./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cac:Price/cbc:PriceAmount/@currencyID" />
						</xsl:if>
					</xsl:if>
				</td>
			</xsl:if>


			<xsl:if test="//n1:DespatchAdvice/cac:DespatchLine/cbc:OutstandingQuantity">

				<td class="t-r">
					<xsl:value-of select="format-number(./cbc:OutstandingQuantity, '###.###,####', 'european')" />
					<xsl:if test="./cbc:OutstandingQuantity/@unitCode">
						<xsl:for-each select="./cbc:OutstandingQuantity">
							<xsl:text></xsl:text>
							<xsl:call-template name="UnitText">
								<xsl:with-param name="UnitCode">
									<xsl:value-of select="@unitCode" />
								</xsl:with-param>
							</xsl:call-template>
						</xsl:for-each>
					</xsl:if>
				</td>
			</xsl:if>


			<xsl:if test="//n1:DespatchAdvice/cac:DespatchLine/cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cbc:LineExtensionAmount">

				<td class="t-r">
					<xsl:value-of select="format-number(./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cbc:LineExtensionAmount, '###.##0,########', 'european')" />
					<xsl:if test="./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cbc:LineExtensionAmount/@currencyID">
						<xsl:text></xsl:text>
						<xsl:if test="./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cbc:LineExtensionAmount/@currencyID = &quot;TRL&quot; or ./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cbc:LineExtensionAmount/@currencyID = &quot;TRY&quot;">
							<xsl:text>TL</xsl:text>
						</xsl:if>
						<xsl:if test="./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cbc:LineExtensionAmount/@currencyID != &quot;TRL&quot; and ./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cbc:LineExtensionAmount/@currencyID != &quot;TRY&quot;">
							<xsl:value-of select="./cac:Shipment/cac:GoodsItem/cac:InvoiceLine/cbc:LineExtensionAmount/@currencyID" />
						</xsl:if>
					</xsl:if>
				</td>
			</xsl:if>
		</tr>
	</xsl:template>
	<xsl:template match="//cbc:IssueDate">
		<xsl:value-of select="substring(.,9,2)" />
		-
		<xsl:value-of select="substring(.,6,2)" />
		-
		<xsl:value-of select="substring(.,1,4)" />
	</xsl:template>
	<xsl:template match="//cbc:ActualDespatchDate">
		<xsl:value-of select="substring(.,9,2)" />
		-
		<xsl:value-of select="substring(.,6,2)" />
		-
		<xsl:value-of select="substring(.,1,4)" />
	</xsl:template>


	<xsl:template name="Party_Title">
		<xsl:param name="PartyType" />
		<td style="width:469px; ">
			<xsl:if test="cac:PartyName">
				<xsl:value-of select="cac:PartyName/cbc:Name" />
				<br />
			</xsl:if>
			<xsl:for-each select="cac:Person">
				<xsl:for-each select="cbc:Title">
					<xsl:apply-templates />
					<xsl:text>&#160;</xsl:text>
				</xsl:for-each>
				<xsl:for-each select="cbc:FirstName">
					<xsl:apply-templates />
					<xsl:text>&#160;</xsl:text>
				</xsl:for-each>
				<xsl:for-each select="cbc:MiddleName">
					<xsl:apply-templates />
					<xsl:text>&#160; </xsl:text>
				</xsl:for-each>
				<xsl:for-each select="cbc:FamilyName">
					<xsl:apply-templates />
					<xsl:text>&#160;</xsl:text>
				</xsl:for-each>
				<xsl:for-each select="cbc:NameSuffix">
					<xsl:apply-templates />
				</xsl:for-each>
				<xsl:if test="$PartyType='TAXFREE'">
					<br />
					<xsl:text>Pasaport No: </xsl:text>
					<xsl:value-of select="cac:IdentityDocumentReference/cbc:ID" />
					<br />
					<xsl:text>Ülkesi: </xsl:text>
					<xsl:value-of select="cbc:NationalityID" />
				</xsl:if>
			</xsl:for-each>
		</td>
	</xsl:template>
	<xsl:template name="Party_Adress">
		<xsl:param name="PartyType" />
		<td style="width:469px; ">
			<xsl:for-each select="cac:PostalAddress">
				<xsl:for-each select="cbc:StreetName">
					<xsl:apply-templates />
					<xsl:text>&#160;</xsl:text>
				</xsl:for-each>
				<xsl:for-each select="cbc:BuildingName">
					<xsl:apply-templates />
				</xsl:for-each>
				<xsl:for-each select="cbc:BuildingNumber">
					<xsl:text> No:</xsl:text>
					<xsl:apply-templates />
					<xsl:text>&#160;</xsl:text>
				</xsl:for-each>
				<br />
				<xsl:for-each select="cbc:Room">
					<xsl:text>Kapı No:</xsl:text>
					<xsl:apply-templates />
					<xsl:text>&#160;</xsl:text>
				</xsl:for-each>
				<br />
				<xsl:for-each select="cbc:PostalZone">
					<xsl:apply-templates />
					<xsl:text>&#160;</xsl:text>
				</xsl:for-each>
				<xsl:for-each select="cbc:CitySubdivisionName">
					<xsl:apply-templates />
					<xsl:text>/ </xsl:text>
				</xsl:for-each>
				<xsl:for-each select="cbc:CityName">
					<xsl:apply-templates />
					<xsl:text>&#160;</xsl:text>
				</xsl:for-each>
				<xsl:if test="$PartyType='TAXFREE'">
					<br />
					<xsl:value-of select="cac:Country/cbc:Name" />
					<br />
				</xsl:if>
			</xsl:for-each>
		</td>
	</xsl:template>
	<xsl:template name='Party_Other'>
		<xsl:param name="PartyType" />
		<xsl:for-each select="cbc:WebsiteURI">
			<tr>
				<td>
					<xsl:text>Web Sitesi: </xsl:text>
					<xsl:value-of select="." />
				</td>
			</tr>
		</xsl:for-each>
		<xsl:for-each select="cac:Contact/cbc:ElectronicMail">
			<tr>
				<td>
					<xsl:text>E-Posta: </xsl:text>
					<xsl:value-of select="." />
				</td>
			</tr>
		</xsl:for-each>
		<xsl:for-each select="cac:Contact">
			<xsl:if test="cbc:Telephone or cbc:Telefax">
				<tr>
					<td style="width:469px; ">
						<xsl:for-each select="cbc:Telephone">
							<xsl:text>Tel: </xsl:text>
							<xsl:apply-templates />
						</xsl:for-each>
						<xsl:for-each select="cbc:Telefax">
							<xsl:text> Fax: </xsl:text>
							<xsl:apply-templates />
						</xsl:for-each>
						<xsl:text>&#160;</xsl:text>
					</td>
				</tr>
			</xsl:if>
		</xsl:for-each>
		<xsl:if test="$PartyType!='TAXFREE'">
			<xsl:for-each select="cac:PartyTaxScheme/cac:TaxScheme/cbc:Name">
				<tr>
					<td>
						<xsl:text>Vergi Dairesi: </xsl:text>
						<xsl:apply-templates />
					</td>
				</tr>
			</xsl:for-each>
			<xsl:for-each select="cac:PartyIdentification">
				<tr>
					<td>
						<xsl:value-of select="cbc:ID/@schemeID" />
						<xsl:text>: </xsl:text>
						<xsl:value-of select="cbc:ID" />
					</td>
				</tr>
			</xsl:for-each>
		</xsl:if>
	</xsl:template>
	<xsl:template name="Curr_Type">
		<xsl:value-of select="format-number(., '###.##0,00', 'european')" />
		<xsl:if test="@currencyID">
			<xsl:text></xsl:text>
			<xsl:choose>
				<xsl:when test="@currencyID = 'TRL' or @currencyID = 'TRY'">
					<xsl:text>TL</xsl:text>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="@currencyID" />
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>