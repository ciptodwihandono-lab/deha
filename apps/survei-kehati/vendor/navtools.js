/* Survei: Kompas & Navigasi. Berisi pustaka pihak ketiga (dibundel dengan esbuild):
   - magvar 2.2.0 (World Magnetic Model 2025), MIT, (c) Darren Yeates
   - mgrs 2.2.0, MIT, (c) proj4js contributors
   - suncalc 2.1.1, BSD-2-Clause, (c) Volodymyr Agafonkin
   Lisensi lengkap: vendor/LICENSE-navtools.txt */
(()=>{var st=Object.create;var c0=Object.defineProperty;var at=Object.getOwnPropertyDescriptor;var ct=Object.getOwnPropertyNames;var it=Object.getPrototypeOf,ut=Object.prototype.hasOwnProperty;var i0=(t,n)=>()=>(n||t((n={exports:{}}).exports,n),n.exports),N0=(t,n)=>{for(var e in n)c0(t,e,{get:n[e],enumerable:!0})},lt=(t,n,e,o)=>{if(n&&typeof n=="object"||typeof n=="function")for(let s of ct(n))!ut.call(t,s)&&s!==e&&c0(t,s,{get:()=>n[s],enumerable:!(o=at(n,s))||o.enumerable});return t};var ft=(t,n,e)=>(e=t!=null?st(it(t)):{},lt(n||!t||!t.__esModule?c0(e,"default",{value:t,enumerable:!0}):e,t));var k0=i0((Xt,L0)=>{var ht=[[0,0,0,0,0,0,0,0,0,0,0,0,0],[-29351.8,-1410.8,0,0,0,0,0,0,0,0,0,0,0],[-2556.6,2951.1,1649.3,0,0,0,0,0,0,0,0,0,0],[1361,-2404.1,1243.8,453.6,0,0,0,0,0,0,0,0,0],[895,799.5,55.7,-281.1,12.1,0,0,0,0,0,0,0,0],[-233.2,368.9,187.2,-138.7,-142,20.9,0,0,0,0,0,0,0],[64.4,63.8,76.9,-115.7,-40.9,14.9,-60.7,0,0,0,0,0,0],[79.5,-77,-8.8,59.3,15.8,2.5,-11.1,14.2,0,0,0,0,0],[23.2,10.8,-17.5,2,-21.7,16.9,15,-16.8,.9,0,0,0,0],[4.6,7.8,3,-.2,-2.5,-13.1,2.4,8.6,-8.7,-12.9,0,0,0],[-1.3,-6.4,.2,2,-1,-.6,-.9,1.5,.9,-2.7,-3.9,0,0],[2.9,-1.5,-2.5,2.4,-.6,-.1,-.6,-.1,1.1,-1,-.2,2.6,0],[-2,-.2,.3,1.2,-1.3,.6,.6,.5,-.1,-.4,-.2,-1.3,-.7]],dt=[[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,4545.4,0,0,0,0,0,0,0,0,0,0,0],[0,-3133.6,-815.1,0,0,0,0,0,0,0,0,0,0],[0,-56.6,237.5,-549.5,0,0,0,0,0,0,0,0,0],[0,278.6,-133.9,212,-375.6,0,0,0,0,0,0,0,0],[0,45.4,220.2,-122.9,43,106.1,0,0,0,0,0,0,0],[0,-18.4,16.8,48.8,-59.8,10.9,72.7,0,0,0,0,0,0],[0,-48.9,-14.4,-1,23.4,-7.4,-25.1,-2.3,0,0,0,0,0],[0,7.1,-12.6,11.4,-9.7,12.7,.7,-5.2,3.9,0,0,0,0],[0,-24.8,12.2,8.3,-3.3,-5.2,7.2,-.6,.8,10,0,0,0],[0,3.3,0,2.4,5.3,-9.1,.4,-4.2,-3.8,.9,-9.1,0,0],[0,0,2.9,-.6,.2,.5,-.3,-1.2,-1.7,-2.9,-1.8,-2.3,0],[0,-1.3,.7,1,-1.4,0,.6,-.1,.8,.1,-1,.1,.2]],mt=[[0,0,0,0,0,0,0,0,0,0,0,0,0],[12,9.7,0,0,0,0,0,0,0,0,0,0,0],[-11.6,-5.2,-8,0,0,0,0,0,0,0,0,0,0],[-1.3,-4.2,.4,-15.6,0,0,0,0,0,0,0,0,0],[-1.6,-2.4,-6,5.6,-7,0,0,0,0,0,0,0,0],[.6,1.4,0,.6,2.2,.9,0,0,0,0,0,0,0],[-.2,-.4,.9,1.2,-.9,.3,.9,0,0,0,0,0,0],[-0,-.1,-.1,.5,-.1,-.8,-.8,.8,0,0,0,0,0],[-.1,.2,0,.5,-.1,.3,.2,-0,.2,0,0,0,0],[-0,-.1,.1,.3,-.3,0,.3,-.1,.1,-.1,0,0,0],[.1,0,.1,.1,-0,-.3,0,-.1,-.1,-0,-0,0,0],[0,-0,0,0,0,-.1,0,-0,-.1,-.1,-.1,-.1,0],[0,0,-0,-0,-0,-0,.1,-0,0,0,-.1,-0,-.1]],Mt=[[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,-21.5,0,0,0,0,0,0,0,0,0,0,0],[0,-27.7,-12.1,0,0,0,0,0,0,0,0,0,0],[0,4,-.3,-4.1,0,0,0,0,0,0,0,0,0],[0,-1.1,4.1,1.6,-4.4,0,0,0,0,0,0,0,0],[0,-.5,2.2,.4,1.7,1.9,0,0,0,0,0,0,0],[0,.3,-1.6,-.4,.9,.7,.9,0,0,0,0,0,0],[0,.6,.5,-.8,0,-1,.6,-.2,0,0,0,0,0],[0,-.2,.5,-.4,.4,-.5,-.6,.3,.2,0,0,0,0],[0,-.3,.3,-.3,.3,.2,-.1,-.2,.4,.1,0,0,0],[0,0,-0,-.2,.1,-.1,.1,0,-.1,.2,-0,0,0],[0,-0,.1,-0,.1,-0,-0,.1,-0,0,0,0,0],[0,-0,0,-.1,.1,-0,-0,-0,0,-0,-0,0,-.1]],gt=2460677;L0.exports={gnmWmm:ht,hnmWmm:dt,gtnmWmm:mt,htnmWmm:Mt,julianDaysCOF:gt,MODEL_EPOCH:2025,MODEL_VALID_UNTIL:2030}});var x0=i0((Zt,P0)=>{var pt=.017453292519943295,wt=57.29577951308232,bt=(t,n)=>{let e=10**n;return Math.round(t*e)/e},yt=(t,n,e)=>Date.UTC(t,n,e)/864e5+24405875e-1,u0=(t=new Date)=>{let n=t.getUTCFullYear(),e=Date.UTC(n,0,1),o=Date.UTC(n+1,0,1),s=Date.UTC(n,t.getUTCMonth(),t.getUTCDate(),t.getUTCHours(),t.getUTCMinutes(),t.getUTCSeconds(),t.getUTCMilliseconds());return n+(s-e)/(o-e)},Dt=t=>{if(t==null)return u0(new Date);if(t instanceof Date)return u0(t);if(typeof t=="number"&&Number.isFinite(t))return t;throw new TypeError("when must be a decimal year number or Date")},At=(t,n)=>Array.from({length:t},()=>Array(n).fill(0));P0.exports={deg2rad:t=>t*pt,rad2deg:t=>t*wt,roundToDecimalPlace:bt,gregorianToJulian:yt,dateToDecimalYear:u0,resolveDecimalYear:Dt,zeroArray2D:At}});var R0=i0((Kt,I0)=>{var{gnmWmm:Tt,gtnmWmm:vt,hnmWmm:Ct,htnmWmm:Et,julianDaysCOF:Nt,MODEL_EPOCH:X,MODEL_VALID_UNTIL:h0}=k0(),{deg2rad:z0,rad2deg:S0,zeroArray2D:Z,roundToDecimalPlace:q,resolveDecimalYear:U0}=x0(),U=12,x=U+1,F={a:6378.137,b:6356.7523142,r0:6371.2},z=Z(x,x),I=Z(x,x),d0=Z(x,x),m0=Z(x,x),l0=new Array(x).fill(0),f0=new Array(x).fill(0),M0=new Array(x).fill(0),W=Z(x,x).map(t=>t.map(()=>[0,0]));for(let t=2;t<=U;t++)M0[t]=Math.sqrt((2*t-1)/(2*t));for(let t=0;t<=U;t++){let n=t*t;for(let e=Math.max(t+1,2);e<=U;e++)W[t][e][0]=Math.sqrt((e-1)*(e-1)-n),W[t][e][1]=1/Math.sqrt(e*e-n)}var O0=Number.NaN,F0=!1,Lt=t=>{!F0&&(t<X||t>=h0)&&(F0=!0,console.warn(`magvar: decimal year ${t} is outside the WMM ${X}-${h0} validity period; results may be inaccurate.`))},kt=t=>{if(t===O0)return;O0=t;let n=t-X;for(let e=1;e<=U;e++)for(let o=0;o<=e;o++)d0[e][o]=Tt[e][o]+n*vt[e][o],m0[e][o]=Ct[e][o]+n*Et[e][o]},g0=(t,n,e,o=0)=>{Lt(t),kt(t);let s=z0(n),a=z0(e),r=Math.sin(s),i=Math.cos(s),c=Math.sqrt(F.a**2*i**2+F.b**2*r**2),w=Math.atan2(i*(o*c+F.a**2),r*(o*c+F.b**2)),h=Math.sqrt(o**2+2*o*c+(F.a**4-(F.a**4-F.b**4)*r**2)/(F.a**2-(F.a**2-F.b**2)*r**2)),b=Math.cos(w),D=Math.sin(w),M=1/(D+(D===0?1e-8:0));z[0][0]=1,z[1][1]=D,I[0][0]=0,I[1][1]=b,z[1][0]=b,I[1][0]=-D;for(let l=2;l<=U;l++)z[l][l]=z[l-1][l-1]*D*M0[l],I[l][l]=(I[l-1][l-1]*D+z[l-1][l-1]*b)*M0[l];for(let l=0;l<=U;l++)for(let L=Math.max(l+1,2);L<=U;L++)z[L][l]=(z[L-1][l]*b*(2*L-1)-z[L-2][l]*W[l][L][0])*W[l][L][1],I[L][l]=((I[L-1][l]*b-z[L-1][l]*D)*(2*L-1)-I[L-2][l]*W[l][L][0])*W[l][L][1];for(let l=0;l<=U;l++)l0[l]=Math.sin(l*a),f0[l]=Math.cos(l*a);let g=0,f=0,u=0,v=F.r0/h,d=v**2;for(let l=1;l<=U;l++){let L=0,v0=0,C0=0;for(let P=0;P<=l;P++){let E0=d0[l][P]*f0[P]+m0[l][P]*l0[P];L+=E0*z[l][P],v0+=E0*I[l][P],C0+=P*(d0[l][P]*l0[P]-m0[l][P]*f0[P])*z[l][P]}d*=v,g+=(l+1)*L*d,f-=v0*d,u+=C0*d*M}let C=w-(Math.PI/2-s),y=Math.sin(C),A=Math.cos(C),N=-f*A-g*y,O=u,E=f*y-g*A,k=Math.hypot(N,O),G=Math.hypot(k,E),V=N!==0||O!==0?S0(Math.atan2(O,N)):0,rt=k!==0||E!==0?S0(Math.atan2(E,k)):0;return{declination:q(V,2),inclination:q(rt,2),x:q(N,1),y:q(O,1),z:q(E,1),h:q(k,1),f:q(G,1),decimalYear:t}},p0=(t,n,e,o=0)=>g0(t,n,e,o).declination,Pt=(t,n,e,o=0)=>{let s=X+(t-Nt)/365.25;return p0(s,n,e,o)},xt=(t,n,e=0,o)=>p0(U0(o),t,n,e),zt=(t,n,e=0,o)=>g0(U0(o),t,n,e);I0.exports={magvar:xt,magneticField:zt,calculateMagVar:Pt,calculateMagVarForDecimalYear:p0,calculateMagneticField:g0,MODEL_EPOCH:X,MODEL_VALID_UNTIL:h0}});var $t=ft(R0());var y0={};N0(y0,{forward:()=>St,getLetterDesignator:()=>H0,inverse:()=>Ot,toPoint:()=>Ft});function St(t,n){if(n=typeof n=="number"?n:5,!Array.isArray(t))throw new TypeError("forward did not receive an array");if(typeof t[0]=="string"||typeof t[1]=="string")throw new TypeError("forward received an array of strings, but it only accepts an array of numbers.");let[e,o]=t;if(e<-180||e>180)throw new TypeError("forward received an invalid longitude of "+e);if(o<-90||o>90)throw new TypeError("forward received an invalid latitude of "+o);if(o<-80||o>84)throw new TypeError(`forward received a latitude of ${o}, but this library does not support conversions of points in polar regions below 80\xB0S and above 84\xB0N`);return function(s,a){let r="00000"+s.easting,i="00000"+s.northing;return s.zoneNumber+s.zoneLetter+function(c,w,h){let b=J0(h),D=Math.floor(c/1e5),M=Math.floor(w/1e5)%20;return function(g,f,u){let v=u-1,d="AJSAJS".charCodeAt(v),C="AFAFAF".charCodeAt(v),y=d+g-1,A=C+f,N=!1;return y>90&&(y=y-90+65-1,N=!0),(y===73||d<73&&y>73||(y>73||d<73)&&N)&&y++,(y===79||d<79&&y>79||(y>79||d<79)&&N)&&(y++,y===73&&y++),y>90&&(y=y-90+65-1),A>86?(A=A-86+65-1,N=!0):N=!1,(A===73||C<73&&A>73||(A>73||C<73)&&N)&&A++,(A===79||C<79&&A>79||(A>79||C<79)&&N)&&(A++,A===73&&A++),A>86&&(A=A-86+65-1),String.fromCharCode(y)+String.fromCharCode(A)}(D,M,b)}(s.easting,s.northing,s.zoneNumber)+r.substr(r.length-5,a)+i.substr(i.length-5,a)}(function(s){let a=s.lat,r=s.lon,i=6378137,c=w0(a),w=w0(r),h;h=Math.floor((r+180)/6)+1,r===180&&(h=60),a>=56&&a<64&&r>=3&&r<12&&(h=32),a>=72&&a<84&&(r>=0&&r<9?h=31:r>=9&&r<21?h=33:r>=21&&r<33?h=35:r>=33&&r<42&&(h=37));let b=w0(6*(h-1)-180+3),D=i/Math.sqrt(1-.00669438*Math.sin(c)*Math.sin(c)),M=Math.tan(c)*Math.tan(c),g=.006739496752268451*Math.cos(c)*Math.cos(c),f=Math.cos(c)*(w-b),u=i*(.9983242984503243*c-.002514607064228144*Math.sin(2*c)+2639046602129982e-21*Math.sin(4*c)-3418046101696858e-24*Math.sin(6*c)),v=.9996*D*(f+(1-M+g)*f*f*f/6+(5-18*M+M*M+72*g-.39089081163157013)*f*f*f*f*f/120)+5e5,d=.9996*(u+D*Math.tan(c)*(f*f/2+(5-M+9*g+4*g*g)*f*f*f*f/24+(61-58*M+M*M+600*g-2.2240339282485886)*f*f*f*f*f*f/720));return a<0&&(d+=1e7),{northing:Math.trunc(d),easting:Math.trunc(v),zoneNumber:h,zoneLetter:H0(a)}}({lat:o,lon:e}),n)}function Ot(t){let n=b0(G0(t.toUpperCase()));return typeof n.lat=="number"&&typeof n.lon=="number"?[n.lon,n.lat,n.lon,n.lat]:[n.left,n.bottom,n.right,n.top]}function Ft(t){if(t==="")throw new TypeError("toPoint received a blank string");let n=b0(G0(t.toUpperCase()));return typeof n.lat=="number"&&typeof n.lon=="number"?[n.lon,n.lat]:[(n.left+n.right)/2,(n.top+n.bottom)/2]}function w0(t){return t*(Math.PI/180)}function q0(t){return t/Math.PI*180}function b0(t){let n=t.northing,e=t.easting,{zoneLetter:o,zoneNumber:s}=t;if(s<0||s>60)return null;let a=6378137,r=(1-Math.sqrt(.99330562))/(1+Math.sqrt(.99330562)),i=e-5e5,c=n;o<"N"&&(c-=1e7);let w=6*(s-1)-180+3,h=c/.9996/6367449145945056e-9,b=h+(3*r/2-27*r*r*r/32)*Math.sin(2*h)+(21*r*r/16-55*r*r*r*r/32)*Math.sin(4*h)+151*r*r*r/96*Math.sin(6*h),D=a/Math.sqrt(1-.00669438*Math.sin(b)*Math.sin(b)),M=Math.tan(b)*Math.tan(b),g=.006739496752268451*Math.cos(b)*Math.cos(b),f=.99330562*a/Math.pow(1-.00669438*Math.sin(b)*Math.sin(b),1.5),u=i/(.9996*D),v=b-D*Math.tan(b)/f*(u*u/2-(5+3*M+10*g-4*g*g-.06065547077041606)*u*u*u*u/24+(61+90*M+298*g+45*M*M-1.6983531815716497-3*g*g)*u*u*u*u*u*u/720);v=q0(v);let d,C=(u-(1+2*M+g)*u*u*u/6+(5-2*g+28*M-3*g*g+.05391597401814761+24*M*M)*u*u*u*u*u/120)/Math.cos(b);if(C=w+q0(C),typeof t.accuracy=="number"){let y=b0({northing:t.northing+t.accuracy,easting:t.easting+t.accuracy,zoneLetter:t.zoneLetter,zoneNumber:t.zoneNumber});d={top:y.lat,right:y.lon,bottom:v,left:C}}else d={lat:v,lon:C};return d}function H0(t){return t<=84&&t>=72?"X":t<72&&t>=-80?"CDEFGHJKLMNPQRSTUVWX"[Math.floor((t- -80)/8)]:t>84||t<-80?"Z":void 0}function J0(t){let n=t%6;return n===0&&(n=6),n}function G0(t){if(t&&t.length===0)throw new TypeError("MGRSPoint coverting from nothing");t=t.replace(/ /g,"");let{length:n}=t,e,o=null,s="",a=0;for(;!/[A-Z]/.test(e=t.charAt(a));){if(a>=2)throw new Error("MGRSPoint bad conversion from: "+t);s+=e,a++}let r=parseInt(s,10);if(a===0||a+3>n)throw new Error("MGRSPoint bad conversion from "+t);let i=t.charAt(a++);if(i<="A"||i==="B"||i==="Y"||i>="Z"||i==="I"||i==="O")throw new Error(`MGRSPoint zone letter ${i} not handled: ${t}`);o=t.substring(a,a+=2);let c=J0(r),w=function(u,v){let d="AJSAJS".charCodeAt(v-1),C=1e5,y=!1;for(;d!==u.charCodeAt(0);){if(d++,d===73&&d++,d===79&&d++,d>90){if(y)throw new Error("Bad character: "+u);d=65,y=!0}C+=1e5}return C}(o.charAt(0),c),h=function(u,v){if(u>"V")throw new TypeError("MGRSPoint given invalid Northing "+u);let d="AFAFAF".charCodeAt(v-1),C=0,y=!1;for(;d!==u.charCodeAt(0);){if(d++,d===73&&d++,d===79&&d++,d>86){if(y)throw new Error("Bad character: "+u);d=65,y=!0}C+=1e5}return C}(o.charAt(1),c);for(;h<Ut(i);)h+=2e6;let b=n-a;if(b%2!=0)throw new Error(`MGRSPoint has to have an even number
of digits after the zone letter and two 100km letters - front
half for easting meters, second half for
northing meters `+t);let D=b/2,M=0,g=0,f=1e5/Math.pow(10,D);if(D>0){let u=t.substring(a,a+D);M=parseFloat(u)*f;let v=t.substring(a+D);g=parseFloat(v)*f}return{easting:M+w,northing:g+h,zoneLetter:i,zoneNumber:r,accuracy:f}}function Ut(t){let n;switch(t){case"C":n=11e5;break;case"D":n=2e6;break;case"E":n=28e5;break;case"F":n=37e5;break;case"G":n=46e5;break;case"H":n=55e5;break;case"J":n=64e5;break;case"K":n=73e5;break;case"L":n=82e5;break;case"M":n=91e5;break;case"N":n=0;break;case"P":n=8e5;break;case"Q":n=17e5;break;case"R":n=26e5;break;case"S":n=35e5;break;case"T":n=44e5;break;case"U":n=53e5;break;case"V":n=62e5;break;case"W":n=7e6;break;case"X":n=79e5;break;default:n=-1}if(n>=0)return n;throw new TypeError("Invalid zone letter: "+t)}var T0={};N0(T0,{addTime:()=>qt,getMoonIllumination:()=>_t,getMoonPosition:()=>ot,getMoonTimes:()=>Bt,getPosition:()=>Rt,getTimes:()=>Vt,times:()=>r0});var{PI:S,sin:m,cos:T,tan:s0,asin:Q,atan2:j,acos:$0,sqrt:j0,abs:o0,round:X0,floor:Z0}=Math,p=S/180,R=1e3*60*60*24,K0=2440588,B=2451545,Q0=6378.14;function K(t){return new Date((t+.5-K0)*R)}function Y(t){return t.valueOf()/R-.5+K0-B}function It(t){let n=2e3+t/365.2425,e;return n<1920?(e=n-1900,-2.79+e*(1.494119+e*(-.0598939+e*(.0061966-e*197e-6)))):n<1941?(e=n-1920,21.2+e*(.84493+e*(-.0761+e*.0020936))):n<1961?(e=n-1950,29.07+e*(.407+e*(-1/233+e/2547))):n<1986?(e=n-1975,45.45+e*(1.067+e*(-1/260-e/718))):n<2005?(e=n-2e3,63.86+e*(.3345+e*(-.060374+e*(.0017275+e*(651814e-9+e*2373599e-11))))):n<2050?(e=n-2e3,62.92+e*(.32217+e*.005589)):(e=(n-1820)/100,-20+32*e*e-.5628*(2150-n))}function J(t){return t+It(t)/86400}function Y0(t,n,e){return(j(m(t),T(t)*m(n)-s0(e)*T(n))/p+540)%360}function a0(t,n,e){return Q(m(n)*m(e)+T(n)*T(e)*T(t))}function t0(t,n){return p*(280.46061837+360.98564736629*t)-n}function tt(t){return t<0&&(t=0),2967e-7/s0(t+.00312536/(t+.08901179))}function n0(t){let n=t/36525,e=p*(280.46646+n*(36000.76983+n*3032e-7)),o=p*(357.52911+n*(35999.05029-n*1537e-7)),s=m(o),a=T(o),r=p*((1.914602-n*(.004817+n*14e-6))*s+(.019993-101e-6*n)*2*s*a+289e-6*s*(3-4*s*s)),i=p*(125.04-1934.136*n),c=e+r-p*(.00569+.00478*m(i)),w=p*(23.439291-n*(.0130042+n*(16e-8-n*504e-9)))+p*.00256*T(i);return{ra:j(T(w)*m(c),T(c)),dec:Q(m(w)*m(c)),lon:c}}function Rt(t,n,e){let o=p*-e,s=p*n,a=Y(t),r=n0(J(a)),i=t0(a,o)-r.ra,c=a0(i,s,r.dec);return{azimuth:Y0(i,s,r.dec),altitude:(c+tt(c))/p}}var r0=[[-.833,"sunrise","sunset"],[-.3,"sunriseEnd","sunsetStart"],[-6,"dawn","dusk"],[-12,"nauticalDawn","nauticalDusk"],[-18,"nightEnd","night"],[6,"goldenHourEnd","goldenHour"]];function qt(t,n,e){r0.push([t,n,e])}var Ht=9e-4;function Jt(t){return-2.076*j0(t)/60}function D0(t){return t-2*S*X0(t/(2*S))}function Gt(t,n){for(let e=0;e<3;e++){let o=D0(t0(t,n)-n0(J(t)).ra);t-=o/(2*S)}return t}function V0(t,n,e,o,s,a){let r=(m(t)-m(s)*m(a))/(T(s)*T(a));if(r<-1||r>1)return NaN;let i=n+e*$0(r)/(2*S);for(let c=0;c<2;c++){let w=n0(J(i)),h=D0(t0(i,o)-w.ra),b=a0(h,s,w.dec),D=T(s)*T(w.dec)*m(h);if(o0(D)<1e-6)break;i+=(b-t)/(2*S*D)}return i}function nt(t,n){let e=n*6e4;return Z0((t.valueOf()+e)/R)*R-e}function et(t,n,e){let o=e===void 0?t.valueOf():nt(t,e)+R/2,s=Ht+n/(2*S);return Gt(X0(Y(o)-s)+s,n)}function Vt(t,n,e,o=0,s){let a=p*-e,r=p*n,i=Jt(o),c=et(t,a,s),w=n0(J(c)).dec,h={solarNoon:K(c+B),nadir:K(c+B-.5)};for(let[b,D,M]of r0){let g=(b+i)*p,f=V0(g,c,-1,a,r,w),u=V0(g,c,1,a,r,w);h[D]=Number.isNaN(f)?null:K(f+B),h[M]=Number.isNaN(u)?null:K(u+B)}if(h.sunrise===null){let b=a0(0,r,w),D=(r0[0][0]+i)*p;h.alwaysUp=b>D,h.alwaysDown=b<=D}return h}function Wt(t){let n=p*(125.04452-1934.136261*t),e=p*(280.4665+36000.7698*t),o=p*(218.3165+481267.8813*t),s=(-17.2*m(n)-1.32*m(2*e)-.23*m(2*o)+.21*m(2*n))/3600,a=(9.2*T(n)+.57*T(2*e)+.1*T(2*o)-.09*T(2*n))/3600,r=23.439291-t*(.0130042+t*(16e-8-t*504e-9));return{dpsi:s,eps:p*(r+a)}}var H=new Int32Array([0,0,1,0,6288774,-20905355,2,0,-1,0,1274027,-3699111,2,0,0,0,658314,-2955968,0,0,2,0,213618,-569925,0,1,0,0,-185116,48888,0,0,0,2,-114332,-3149,2,0,-2,0,58793,246158,2,-1,-1,0,57066,-152138,2,0,1,0,53322,-170733,2,-1,0,0,45758,-204586,0,1,-1,0,-40923,-129620,1,0,0,0,-34720,108743,0,1,1,0,-30383,104755,2,0,0,-2,15327,10321,0,0,1,2,-12528,0,0,0,1,-2,10980,79661,4,0,-1,0,10675,-34782,0,0,3,0,10034,-23210,4,0,-2,0,8548,-21636,2,1,-1,0,-7888,24208,2,1,0,0,-6766,30824,1,0,-1,0,-5163,-8379,1,1,0,0,4987,-16675,2,-1,1,0,4036,-12831,2,0,2,0,3994,-10445,4,0,0,0,3861,-11650,2,0,-3,0,3665,14403,0,1,-2,0,-2689,-7003,2,0,-1,2,-2602,0,2,-1,-2,0,2390,10056,1,0,1,0,-2348,6322,2,-2,0,0,2236,-9884,0,1,2,0,-2120,5751,0,2,0,0,-2069,0,2,-2,-1,0,2048,-4950,2,0,1,-2,-1773,4130,2,0,0,2,-1595,0,4,-1,-1,0,1215,-3958,0,0,2,2,-1110,0,3,0,-1,0,-892,3258,2,1,1,0,-810,2616,4,-1,-2,0,759,-1897,0,2,-1,0,-713,-2117,2,2,-1,0,-700,2354,2,1,-2,0,691,0,2,-1,0,-2,596,0,4,0,1,0,549,-1423,0,0,4,0,537,-1117,4,-1,0,0,520,-1571,1,0,-2,0,-487,-1739,2,1,0,-2,-399,0,0,0,2,-2,-381,-4421,1,1,1,0,351,0,3,0,-2,0,-340,0,4,0,-3,0,330,0,2,-1,2,0,327,0,0,2,1,0,-323,1165,1,1,-1,0,299,0,2,0,3,0,294,0,2,0,-1,-2,0,8752]),_=new Int32Array([0,0,0,1,5128122,0,0,1,1,280602,0,0,1,-1,277693,2,0,0,-1,173237,2,0,-1,1,55413,2,0,-1,-1,46271,2,0,0,1,32573,0,0,2,1,17198,2,0,1,-1,9266,0,0,2,-1,8822,2,-1,0,-1,8216,2,0,-2,-1,4324,2,0,1,1,4200,2,1,0,-1,-3359,2,-1,-1,1,2463,2,-1,0,1,2211,2,-1,-1,-1,2065,0,1,-1,-1,-1870,4,0,-1,-1,1828,0,1,0,1,-1794,0,0,0,3,-1749,0,1,-1,1,-1565,1,0,0,1,-1491,0,1,1,1,-1475,0,1,1,-1,-1410,0,1,0,-1,-1344,1,0,0,-1,-1335,0,0,3,1,1107,4,0,0,-1,1021,4,0,-1,1,833,0,0,1,-3,777,4,0,-2,1,671,2,0,0,-3,607,2,0,2,-1,596,2,-1,1,-1,491,2,0,-2,1,-451,0,0,3,-1,439,2,0,2,1,422,2,0,-3,-1,421,2,1,-1,1,-366,2,1,0,1,-351,4,0,0,1,331,2,-1,1,1,315,2,-2,0,-1,302,0,0,1,3,-283,2,1,1,-1,-229,1,1,0,-1,223,1,1,0,1,223,0,1,-2,-1,-220,2,1,-1,-1,-220,1,0,1,1,-185,2,-1,-2,-1,181,0,1,2,1,-177,4,0,-2,-1,176,4,-1,-1,-1,166,1,0,1,-1,-164,4,0,1,-1,132,1,0,-1,-1,-119,4,-1,0,-1,115,2,-2,0,1,107]);function A0(t){let n=t/36525,e=218.3164477+n*(481267.88123421+n*(-.0015786+n*(1/538841-n/65194e3))),o=297.8501921+n*(445267.1114034+n*(-.0018819+n*(1/545868-n/113065e3))),s=357.5291092+n*(35999.0502909+n*(-1536e-7+n/2449e4)),a=134.9633964+n*(477198.8675055+n*(.0087414+n*(1/69699-n/14712e3))),r=93.272095+n*(483202.0175233+n*(-.0036539+n*(-1/3526e3+n/86331e4))),i=119.75+131.849*n,c=53.09+479264.29*n,w=313.45+481266.484*n,h=1-n*(.002516+n*74e-7),b=p*o,D=p*s,M=p*a,g=p*r,f=0,u=0,v=0;for(let E=0;E<H.length;E+=6){let k=H[E+1],G=H[E]*b+k*D+H[E+2]*M+H[E+3]*g,V=k===1||k===-1?h:k===2||k===-2?h*h:1;f+=H[E+4]*V*m(G),u+=H[E+5]*V*T(G)}for(let E=0;E<_.length;E+=5){let k=_[E+1],G=_[E]*b+k*D+_[E+2]*M+_[E+3]*g,V=k===1||k===-1?h:k===2||k===-2?h*h:1;v+=_[E+4]*V*m(G)}let d=p*i,C=p*e;f+=3958*m(d)+1962*m(C-g)+318*m(p*c),v+=-2235*m(C)+382*m(p*w)+175*m(d-g)+175*m(d+g)+127*m(C-M)-115*m(C+M);let{dpsi:y,eps:A}=Wt(n),N=p*(e+f/1e6+y),O=p*(v/1e6);return{ra:j(m(N)*T(A)-s0(O)*m(A),T(N)),dec:Q(m(O)*T(A)+T(O)*m(A)*m(N)),dist:385000.56+u/1e3,lon:N}}function ot(t,n,e){let o=p*-e,s=p*n,a=Y(t),r=A0(J(a)),i=t0(a,o)-r.ra,c=a0(i,s,r.dec),w=c-Q(Q0/r.dist*T(c)),h=j(m(i),s0(s)*T(r.dec)-m(r.dec)*T(i));return{azimuth:Y0(i,s,r.dec),altitude:(w+tt(w))/p,distance:r.dist,parallacticAngle:h/p}}function _t(t=new Date){let n=J(Y(t)),e=n0(n),o=A0(n),s=149598e3,a=$0(m(e.dec)*m(o.dec)+T(e.dec)*T(o.dec)*T(e.ra-o.ra)),r=j(s*m(a),o.dist-s*T(a)),i=j(T(e.dec)*m(e.ra-o.ra),m(e.dec)*T(o.dec)-T(e.dec)*m(o.dec)*T(e.ra-o.ra)),c=((o.lon-e.lon)/(2*S)%1+1)%1,w=c<.5;return{fraction:(1+T(r))/2,phase:c,angle:i/p,waxing:w}}function e0(t,n){return new Date(t.valueOf()+n*R/24)}function $(t,n,e){let o=ot(t,n,e);return o.altitude+.2725*Q(Q0/o.distance)/p+.09}function W0(t,n,e){for(let o=0;o<2;o++){let s=$(new Date(t),n,e),a=($(new Date(t+3e4),n,e)-$(new Date(t-3e4),n,e))/6e4;t-=s/a}return t}function _0(t,n){let e=Y(t);return t0(e,n)-A0(J(e)).ra}function B0(t,n,e){let o=2*S*.96614/R,s=e-_0(t,n),a=t+(s-2*S*Z0(s/(2*S)))/o;for(let r=0;r<2;r++)a-=D0(_0(a,n)-e)/o;return a<t+R?a:void 0}function Bt(t,n,e,o){let s=o===void 0?K(et(t,p*-e)+B-.5):new Date(nt(t,o)),a=$(s,n,e),r,i,c=a;for(let M=1;M<=24;M+=2){let g=$(e0(s,M),n,e),f=$(e0(s,M+1),n,e);c=Math.max(c,g,f);let u=(a+f)/2-g,v=(f-a)/2,d=-v/(2*u),C=v*v-4*u*g,y=0,A=0,N=0,O=(u*d+v)*d+g;if(C>=0){let E=j0(C)/(o0(u)*2);A=d-E,N=d+E,o0(A)<=1&&y++,o0(N)<=1&&y++,A<-1&&(A=N)}if(y===1?a<0?r=M+A:i=M+A:y===2&&(r=M+(O<0?N:A),i=M+(O<0?A:N)),r!==void 0&&i!==void 0)break;a=f}let w={};r!==void 0&&(w.rise=new Date(W0(e0(s,r).valueOf(),n,e))),i!==void 0&&(w.set=new Date(W0(e0(s,i).valueOf(),n,e)));let h=p*-e,b=B0(s.valueOf(),h,0),D=B0(s.valueOf(),h,S);return b!==void 0&&(w.transit=new Date(b)),D!==void 0&&(w.lowerTransit=new Date(D)),r===void 0&&i===void 0&&(w.alwaysUp=c>0,w.alwaysDown=c<=0),w}window.NAVLIB={magvar:$t,mgrs:y0,SunCalc:T0};})();

/* ================= Kompas & Navigasi (dipakai Peta Survei dan Survei KEHATI) =================
   - Kompas (utara magnetik / sebenarnya) dengan inklinometer, arah & jarak ke titik tujuan.
   - Matahari terbit/terbenam, fajar/senja, fase bulan, terbit/terbenam bulan (SunCalc, MIT).
   - Deklinasi magnetik dari World Magnetic Model 2025 (magvar, MIT; berlaku 2025–2030).
   - Format koordinat DD, DMS, UTM, MGRS (mgrs, MIT) dan satuan sudut derajat / mils (6400 per putaran).
   - GPX 1.1: buat dan baca titik (wpt), jalur (trk), dan rute (rte).
   Pustaka pihak ketiga dibundel di bagian atas berkas ini sebagai window.NAVLIB. */
(function () {
  'use strict';
  const L = window.NAVLIB;
  const rad = Math.PI / 180;
  const pad = n => String(n).padStart(2, '0');
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const PREF = 'navtools-';
  const pref = (k, d) => { try { const v = localStorage.getItem(PREF + k); return v == null ? d : v; } catch (e) { return d; } };
  const setPref = (k, v) => { try { localStorage.setItem(PREF + k, v); } catch (e) {} };

  /* ---------- Koordinat & sudut ---------- */
  function toUTM(lat, lon) {
    let zone = Math.floor((lon + 180) / 6) + 1;
    if (lat >= 56 && lat < 64 && lon >= 3 && lon < 12) zone = 32;
    if (lat >= 72 && lat < 84) { if (lon >= 0 && lon < 9) zone = 31; else if (lon >= 9 && lon < 21) zone = 33; else if (lon >= 21 && lon < 33) zone = 35; else if (lon >= 33 && lon < 42) zone = 37; }
    const a = 6378137, f = 1 / 298.257223563, k0 = 0.9996, e2 = f * (2 - f), ep2 = e2 / (1 - e2);
    const lon0 = ((zone - 1) * 6 - 180 + 3) * rad, phi = lat * rad, lam = lon * rad;
    const N = a / Math.sqrt(1 - e2 * Math.sin(phi) ** 2), T = Math.tan(phi) ** 2, C = ep2 * Math.cos(phi) ** 2, A = Math.cos(phi) * (lam - lon0);
    const M = a * ((1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256) * phi - (3 * e2 / 8 + 3 * e2 ** 2 / 32 + 45 * e2 ** 3 / 1024) * Math.sin(2 * phi) + (15 * e2 ** 2 / 256 + 45 * e2 ** 3 / 1024) * Math.sin(4 * phi) - (35 * e2 ** 3 / 3072) * Math.sin(6 * phi));
    const e = k0 * N * (A + (1 - T + C) * A ** 3 / 6 + (5 - 18 * T + T ** 2 + 72 * C - 58 * ep2) * A ** 5 / 120) + 500000;
    let n = k0 * (M + N * Math.tan(phi) * (A ** 2 / 2 + (5 - T + 9 * C + 4 * C ** 2) * A ** 4 / 24 + (61 - 58 * T + T ** 2 + 600 * C - 330 * ep2) * A ** 6 / 720));
    if (lat < 0) n += 10000000;
    return { zone, hemi: lat < 0 ? 'S' : 'N', e, n };
  }
  function dms(v, pos, neg) {
    const s = v < 0 ? neg : pos; v = Math.abs(v);
    let d = Math.floor(v), m = Math.floor((v - d) * 60), sec = ((v - d) * 60 - m) * 60;
    if (sec >= 59.995) { sec = 0; m++; } if (m >= 60) { m = 0; d++; }
    return `${d}°${pad(m)}′${sec.toFixed(2).padStart(5, '0')}″${s}`;
  }
  const FORMATS = { dd: 'Desimal (DD)', dms: 'Derajat-menit-detik', utm: 'UTM', mgrs: 'MGRS' };
  function fmt(lat, lon, f) {
    if (lat == null || lon == null || !isFinite(lat) || !isFinite(lon)) return '-';
    f = f || pref('fmt', 'dd');
    if (f === 'dms') return `${dms(lat, 'U', 'S')} ${dms(lon, 'T', 'B')}`;
    if (f === 'utm') { const u = toUTM(lat, lon); return `${u.zone}${u.hemi} ${Math.round(u.e)} mT ${Math.round(u.n)} mU`; }
    if (f === 'mgrs') { try { const m = L.mgrs.forward([lon, lat], 5); return m.replace(/^(\d+[A-Z])([A-Z]{2})(\d{5})(\d{5})$/, '$1 $2 $3 $4'); } catch (e) { return '-'; } }
    return `${lat.toFixed(6)}, ${lon.toFixed(6)}`;
  }
  const angleUnit = () => pref('sudut', 'deg');
  function angle(deg, unit) {
    unit = unit || angleUnit(); deg = ((deg % 360) + 360) % 360;
    return unit === 'mil' ? `${Math.round(deg / 360 * 6400) % 6400} mil` : `${Math.round(deg) % 360}°`;
  }
  function hav(a1, o1, a2, o2) { const R = 6371008.8, dA = (a2 - a1) * rad, dO = (o2 - o1) * rad; const x = Math.sin(dA / 2) ** 2 + Math.cos(a1 * rad) * Math.cos(a2 * rad) * Math.sin(dO / 2) ** 2; return 2 * R * Math.asin(Math.sqrt(x)); }
  function bearing(a1, o1, a2, o2) { const y = Math.sin((o2 - o1) * rad) * Math.cos(a2 * rad), x = Math.cos(a1 * rad) * Math.sin(a2 * rad) - Math.sin(a1 * rad) * Math.cos(a2 * rad) * Math.cos((o2 - o1) * rad); return (Math.atan2(y, x) / rad + 360) % 360; }
  const fmtDist = m => m >= 1000 ? `${(m / 1000).toFixed(2).replace('.', ',')} km` : `${Math.round(m)} m`;
  function declination(lat, lon, date) { try { return L.magvar.magvar(lat, lon, 0, date || new Date()); } catch (e) { return null; } }
  const card = d => ['U', 'TL', 'T', 'TG', 'S', 'BD', 'B', 'BL'][Math.round((((d % 360) + 360) % 360) / 45) % 8];

  /* ---------- Matahari & bulan ---------- */
  const hm = d => d && !isNaN(d) ? `${pad(d.getHours())}.${pad(d.getMinutes())}` : '–';
  function moonName(p) {
    const n = ['Bulan baru', 'Sabit awal', 'Paruh awal', 'Cembung awal', 'Purnama', 'Cembung akhir', 'Paruh akhir', 'Sabit akhir'];
    return n[Math.round(p * 8) % 8];
  }
  function skyInfo(lat, lon, date) {
    date = date || new Date();
    const t = L.SunCalc.getTimes(date, lat, lon), mi = L.SunCalc.getMoonIllumination(date), mt = L.SunCalc.getMoonTimes(date, lat, lon);
    return { fajar: t.dawn, terbit: t.sunrise, tengah: t.solarNoon, terbenam: t.sunset, senja: t.dusk, emasPagi: t.goldenHourEnd, emasSore: t.goldenHour,
      bulan: { fase: moonName(mi.phase), terang: mi.fraction, naik: mi.phase < 0.5, terbit: mt.rise, terbenam: mt.set } };
  }
  function moonSVG(phase, frac) {
    // Lingkaran bulan; bagian gelap digambar dengan elips. phase 0..1 (0 = bulan baru, 0,5 = purnama).
    const r = 18, waxing = phase < 0.5, k = Math.cos(2 * Math.PI * phase);
    const rx = Math.abs(k) * r, lit = 'var(--nt-moon, #f3e7b0)', dark = 'var(--nt-moondark, #2b2b33)';
    const big = frac > 0.5;
    return `<svg viewBox="-20 -20 40 40" width="40" height="40" aria-hidden="true"><circle r="${r}" fill="${dark}"/>
      <path d="M0 ${-r} A ${r} ${r} 0 0 ${waxing ? 1 : 0} 0 ${r} A ${rx} ${r} 0 0 ${(waxing ? !big : big) ? 0 : 1} 0 ${-r} Z" fill="${lit}"/></svg>`;
  }

  /* ---------- GPX ---------- */
  const x = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' }[c]));
  const pt = (tag, p) => `<${tag} lat="${(+p.lat).toFixed(7)}" lon="${(+p.lon).toFixed(7)}">${p.ele != null && p.ele !== '' ? `<ele>${(+p.ele).toFixed(1)}</ele>` : ''}${p.time ? `<time>${new Date(p.time).toISOString()}</time>` : ''}${p.name ? `<name>${x(p.name)}</name>` : ''}${p.desc ? `<desc>${x(p.desc)}</desc>` : ''}${p.sym ? `<sym>${x(p.sym)}</sym>` : ''}</${tag}>`;
  function toGPX({ name = '', wpts = [], rtes = [], trks = [] }, creator = 'Survei') {
    return `<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.1" creator="${x(creator)}" xmlns="http://www.topografix.com/GPX/1/1">\n<metadata>${name ? `<name>${x(name)}</name>` : ''}<time>${new Date().toISOString()}</time></metadata>\n`
      + wpts.filter(p => p.lat != null).map(p => pt('wpt', p)).join('\n') + '\n'
      + rtes.map(r => `<rte>${r.name ? `<name>${x(r.name)}</name>` : ''}${r.desc ? `<desc>${x(r.desc)}</desc>` : ''}\n${r.pts.map(p => pt('rtept', p)).join('\n')}\n</rte>`).join('\n') + '\n'
      + trks.map(t => `<trk>${t.name ? `<name>${x(t.name)}</name>` : ''}${t.desc ? `<desc>${x(t.desc)}</desc>` : ''}\n${(t.segs || [t.pts]).map(s => `<trkseg>\n${s.map(p => pt('trkpt', p)).join('\n')}\n</trkseg>`).join('\n')}\n</trk>`).join('\n')
      + '\n</gpx>\n';
  }
  function parseGPX(text) {
    const doc = new DOMParser().parseFromString(text, 'application/xml');
    if (doc.getElementsByTagName('parsererror').length) throw new Error('Berkas GPX tidak terbaca');
    const kid = (el, n) => { for (const c of el.children) if (c.localName === n) return c.textContent.trim(); return ''; };
    const P = el => ({ lat: +el.getAttribute('lat'), lon: +el.getAttribute('lon'), ele: kid(el, 'ele') === '' ? null : +kid(el, 'ele'), time: kid(el, 'time') || null, name: kid(el, 'name'), desc: kid(el, 'desc') || kid(el, 'cmt') });
    const all = n => [...doc.getElementsByTagNameNS('*', n)];
    const ok = p => isFinite(p.lat) && isFinite(p.lon) && Math.abs(p.lat) <= 90 && Math.abs(p.lon) <= 180;
    return {
      wpts: all('wpt').map(P).filter(ok),
      rtes: all('rte').map(r => ({ name: kid(r, 'name'), desc: kid(r, 'desc'), pts: [...r.getElementsByTagNameNS('*', 'rtept')].map(P).filter(ok) })).filter(r => r.pts.length),
      trks: all('trk').map(t => ({ name: kid(t, 'name'), desc: kid(t, 'desc'), segs: [...t.getElementsByTagNameNS('*', 'trkseg')].map(s => [...s.getElementsByTagNameNS('*', 'trkpt')].map(P).filter(ok)).filter(s => s.length) })).filter(t => t.segs.length),
    };
  }

  /* ---------- Sensor orientasi ---------- */
  const S = { heading: null, abs: false, beta: null, gamma: null, listening: false, lastEvt: 0 };
  function screenAngle() { return (screen.orientation && screen.orientation.angle) || window.orientation || 0; }
  function onOrient(e) {
    if (e.webkitCompassHeading != null) { S.heading = (e.webkitCompassHeading + screenAngle()) % 360; S.abs = true; }
    else if (e.alpha != null && (e.absolute || e.type === 'deviceorientationabsolute')) { S.heading = (360 - e.alpha + screenAngle()) % 360; S.abs = true; }
    if (e.beta != null) { S.beta = e.beta; S.gamma = e.gamma; }
    S.lastEvt = Date.now();
    if (P.open) draw();
  }
  async function startSensors() {
    if (S.listening) return true;
    try { if (window.DeviceOrientationEvent && typeof DeviceOrientationEvent.requestPermission === 'function') { const r = await DeviceOrientationEvent.requestPermission(); if (r !== 'granted') return false; } } catch (e) { return false; }
    if ('ondeviceorientationabsolute' in window) window.addEventListener('deviceorientationabsolute', onOrient);
    window.addEventListener('deviceorientation', onOrient);
    S.listening = true; return true;
  }
  function stopSensors() { window.removeEventListener('deviceorientationabsolute', onOrient); window.removeEventListener('deviceorientation', onOrient); S.listening = false; }

  /* ---------- Panel ---------- */
  const P = { open: false, el: null, opt: null, north: pref('utara', 'true'), lockTilt: null, raf: 0 };
  const CSS = `
  .nt-wrap { position: fixed; inset: 0; z-index: 3000; background: rgba(0,0,0,.5); display: flex; align-items: flex-end; justify-content: center; }
  .nt { background: var(--surface, #fff); color: var(--fg, #17221c); width: min(560px, 100%); max-height: 92vh; overflow-y: auto; border-radius: 16px 16px 0 0; padding: 14px 16px calc(16px + env(safe-area-inset-bottom, 0px)); display: flex; flex-direction: column; gap: 12px; font-family: inherit; }
  .nt h3 { margin: 0; font-size: 17px; flex: 1; } .nt-top { display: flex; align-items: center; gap: 8px; }
  .nt button { font: inherit; cursor: pointer; } .nt-x { border: 1px solid var(--line, #ccc); background: none; color: inherit; border-radius: 8px; padding: 6px 12px; font-weight: 650; }
  .nt-seg { display: inline-flex; border: 1px solid var(--line, #ccc); border-radius: 8px; overflow: hidden; } .nt-seg button { border: 0; background: var(--surface-2, #f3f3f3); color: inherit; padding: 6px 10px; font-size: 13px; }
  .nt-seg button[aria-pressed="true"] { background: var(--accent, #2b6a4f); color: var(--accent-fg, #fff); }
  .nt-row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; justify-content: space-between; }
  .nt-comp { display: flex; gap: 14px; align-items: center; }
  .nt-dial { width: 190px; height: 190px; flex: none; position: relative; }
  .nt-dial svg { width: 100%; height: 100%; }
  .nt-big { font-size: 34px; font-weight: 800; font-variant-numeric: tabular-nums; line-height: 1.1; }
  .nt-muted { font-size: 13px; color: var(--muted, #666); }
  .nt-box { background: var(--surface-2, #f4f6f1); border: 1px solid var(--line, #ddd); border-radius: 10px; padding: 10px 12px; display: flex; flex-direction: column; gap: 4px; }
  .nt-box b.k { font-size: 12px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted, #666); }
  .nt-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .nt-kv { display: flex; justify-content: space-between; gap: 8px; font-size: 14px; } .nt-kv span:last-child { font-weight: 650; font-variant-numeric: tabular-nums; text-align: right; }
  .nt-coord { display: grid; grid-template-columns: auto 1fr auto; gap: 4px 10px; align-items: center; font-size: 14px; }
  .nt-coord code { font-family: ui-monospace, Menlo, monospace; font-size: 13px; overflow-wrap: anywhere; }
  .nt-coord button { border: 1px solid var(--line, #ccc); background: none; color: inherit; border-radius: 6px; padding: 3px 8px; font-size: 12px; }
  .nt-coord .on { color: var(--accent, #2b6a4f); font-weight: 700; }
  .nt-tilt { display: flex; gap: 14px; align-items: center; }
  .nt-bubble { width: 92px; height: 92px; border-radius: 50%; border: 2px solid var(--line, #bbb); position: relative; flex: none; background: radial-gradient(circle, transparent 14px, var(--line, #ccc) 15px, transparent 16px); }
  .nt-bubble i { position: absolute; width: 22px; height: 22px; border-radius: 50%; background: #3fa34d; left: 35px; top: 35px; box-shadow: 0 0 0 2px #fff; }
  .nt-warn { color: #a8670f; font-size: 13px; font-weight: 600; }
  .nt-wrap[hidden] { display: none !important; }
  @media (prefers-color-scheme: dark) { .nt { --nt-moondark: #555; } }`;
  function ensure() {
    if (P.el) return;
    const st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
    const w = document.createElement('div'); w.className = 'nt-wrap'; w.hidden = true;
    w.innerHTML = '<div class="nt" role="dialog" aria-label="Kompas dan navigasi"></div>';
    document.body.appendChild(w); P.el = w;
    w.addEventListener('click', ev => {
      if (ev.target === w) return close();
      const b = ev.target.closest('button'); if (!b) return;
      if (b.dataset.nt === 'close') close();
      else if (b.dataset.nt === 'start') startSensors().then(okk => { if (!okk) toastNT('Izin sensor ditolak. Aktifkan sensor gerak/orientasi untuk browser ini.'); render(); });
      else if (b.dataset.north) { P.north = b.dataset.north; setPref('utara', P.north); render(); }
      else if (b.dataset.unit) { setPref('sudut', b.dataset.unit); render(); }
      else if (b.dataset.fmt) { setPref('fmt', b.dataset.fmt); render(); if (P.opt && P.opt.onFormat) P.opt.onFormat(b.dataset.fmt); }
      else if (b.dataset.copy) { const t = b.dataset.copy; (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(() => toastNT('Disalin: ' + t), () => toastNT(t)); }
      else if (b.dataset.nt === 'lock') { P.lockTilt = P.lockTilt ? null : tiltNow(); render(); }
    });
  }
  function toastNT(m) { if (P.opt && P.opt.toast) P.opt.toast(m); }
  function tiltNow() {
    if (S.beta == null) return null;
    const b = S.beta * rad, g = S.gamma * rad;
    const tilt = Math.acos(Math.max(-1, Math.min(1, Math.cos(b) * Math.cos(g)))) / rad;
    return { tilt, pitch: S.beta, roll: S.gamma };
  }
  function pos() { try { return P.opt && P.opt.getPos ? P.opt.getPos() : null; } catch (e) { return null; } }
  function render() {
    if (!P.el) return;
    const p = pos(), unit = angleUnit(), f = pref('fmt', 'dd');
    const dec = p ? declination(p.lat, p.lon) : null;
    const sky = p ? skyInfo(p.lat, p.lon) : null;
    const tgt = P.opt && P.opt.target ? P.opt.target() : null;
    const needBtn = !S.listening;
    P.el.firstElementChild.innerHTML = `
      <div class="nt-top"><h3>Kompas & navigasi</h3><button type="button" class="nt-x" data-nt="close">Tutup</button></div>
      <div class="nt-row"><div class="nt-seg"><button type="button" data-north="true" aria-pressed="${P.north === 'true'}">Utara sebenarnya</button><button type="button" data-north="mag" aria-pressed="${P.north === 'mag'}">Utara magnetik</button></div>
        <div class="nt-seg"><button type="button" data-unit="deg" aria-pressed="${unit === 'deg'}">Derajat</button><button type="button" data-unit="mil" aria-pressed="${unit === 'mil'}">Mils</button></div></div>
      <div class="nt-comp"><div class="nt-dial" id="ntDial">${dialSVG()}</div>
        <div><div class="nt-big" id="ntHead">–</div><div class="nt-muted" id="ntHeadSub">${needBtn ? 'Kompas belum aktif' : 'Menunggu sensor…'}</div>
        ${needBtn ? '<button type="button" class="nt-x" data-nt="start" style="margin-top:8px">Aktifkan kompas</button>' : ''}
        <div class="nt-muted" style="margin-top:6px">Deklinasi magnetik: <b>${dec == null ? '–' : `${Math.abs(dec).toFixed(1).replace('.', ',')}° ${dec >= 0 ? 'Timur' : 'Barat'}`}</b><br><span style="font-size:11px">WMM 2025${p ? '' : ' · butuh posisi GPS'}</span></div>
        ${tgt ? `<div class="nt-muted" style="margin-top:6px" id="ntTgt"></div>` : ''}</div></div>
      <p class="nt-muted" style="margin:0">Pegang HP mendatar, jauh dari logam/magnet. Bila arah meleset, gerakkan HP membentuk angka 8 untuk kalibrasi.</p>
      <div class="nt-box"><b class="k">Inklinometer</b><div class="nt-tilt"><div class="nt-bubble"><i id="ntBub"></i></div>
        <div style="flex:1"><div class="nt-kv"><span>Kemiringan bidang</span><span id="ntTilt">–</span></div><div class="nt-kv"><span>Pitch (depan-belakang)</span><span id="ntPitch">–</span></div><div class="nt-kv"><span>Roll (kiri-kanan)</span><span id="ntRoll">–</span></div>
        <div class="nt-muted" style="margin-top:4px">Taruh HP di permukaan lereng untuk mengukur kemiringan; atau bidik sepanjang sisi panjang HP (pitch) untuk sudut ke puncak pohon.</div>
        <button type="button" class="nt-x" data-nt="lock" style="margin-top:6px">${P.lockTilt ? 'Lepas kunci' : 'Kunci angka'}</button></div></div></div>
      <div class="nt-box"><b class="k">Posisi${p && p.acc ? ` · ±${Math.round(p.acc)} m` : ''}${p && p.alt != null ? ` · tinggi ${Math.round(p.alt)} m` : ''}</b>
        ${p ? `<div class="nt-coord">${Object.entries(FORMATS).map(([k, l]) => { const v = fmt(p.lat, p.lon, k); return `<span class="${k === f ? 'on' : ''}">${l}</span><code>${esc(v)}</code><button type="button" data-copy="${esc(v)}">Salin</button>`; }).join('')}</div>
        <div class="nt-row" style="margin-top:6px"><span class="nt-muted">Format utama di aplikasi:</span><div class="nt-seg">${Object.keys(FORMATS).map(k => `<button type="button" data-fmt="${k}" aria-pressed="${k === f}">${k.toUpperCase()}</button>`).join('')}</div></div>` : '<span class="nt-muted">Menunggu GPS…</span>'}</div>
      ${sky ? `<div class="nt-grid">
        <div class="nt-box"><b class="k">Matahari (hari ini)</b>
          <div class="nt-kv"><span>Fajar</span><span>${hm(sky.fajar)}</span></div><div class="nt-kv"><span>Terbit</span><span>${hm(sky.terbit)}</span></div>
          <div class="nt-kv"><span>Tengah hari</span><span>${hm(sky.tengah)}</span></div><div class="nt-kv"><span>Terbenam</span><span>${hm(sky.terbenam)}</span></div><div class="nt-kv"><span>Senja</span><span>${hm(sky.senja)}</span></div></div>
        <div class="nt-box"><b class="k">Bulan</b><div style="display:flex;gap:10px;align-items:center">${moonSVG(L.SunCalc.getMoonIllumination(new Date()).phase, sky.bulan.terang)}<div><b>${sky.bulan.fase}</b><br><span class="nt-muted">${Math.round(sky.bulan.terang * 100)}% terang</span></div></div>
          <div class="nt-kv"><span>Terbit</span><span>${hm(sky.bulan.terbit)}</span></div><div class="nt-kv"><span>Terbenam</span><span>${hm(sky.bulan.terbenam)}</span></div></div></div>
        <p class="nt-muted" style="margin:0">Waktu sesuai jam HP (${esc(Intl.DateTimeFormat().resolvedOptions().timeZone || '')}).</p>` : ''}`;
    draw();
  }
  function dialSVG() {
    const ticks = []; for (let i = 0; i < 72; i++) { const a = i * 5, long = a % 30 === 0; ticks.push(`<line x1="0" y1="${long ? -78 : -82}" x2="0" y2="-88" transform="rotate(${a})" stroke="currentColor" stroke-width="${long ? 2 : 1}" opacity="${long ? .9 : .5}"/>`); }
    const lbl = [['U', 0], ['T', 90], ['S', 180], ['B', 270]].map(([t, a]) => `<text x="0" y="-62" transform="rotate(${a})" text-anchor="middle" font-size="16" font-weight="800" fill="${t === 'U' ? '#d33' : 'currentColor'}">${t}</text>`).join('');
    return `<svg viewBox="-100 -100 200 200"><circle r="92" fill="none" stroke="currentColor" stroke-width="2" opacity=".6"/>
      <g id="ntRose">${ticks.join('')}${lbl}</g>
      <g id="ntTarget" opacity="0"><path d="M0 -92 L7 -76 L-7 -76 Z" fill="#2a7fff"/></g>
      <path d="M0 -50 L9 0 L0 -8 L-9 0 Z" fill="#d33"/><path d="M0 50 L9 0 L0 8 L-9 0 Z" fill="currentColor" opacity=".5"/>
      <line x1="0" y1="-99" x2="0" y2="-86" stroke="#d33" stroke-width="4"/></svg>`;
  }
  function draw() {
    if (!P.open || !P.el) return;
    cancelAnimationFrame(P.raf);
    P.raf = requestAnimationFrame(() => {
      const p = pos(), dec = p ? declination(p.lat, p.lon) : 0;
      const rose = P.el.querySelector('#ntRose'), head = P.el.querySelector('#ntHead'), sub = P.el.querySelector('#ntHeadSub');
      if (S.heading != null && rose) {
        const h = P.north === 'true' ? (S.heading + (dec || 0) + 360) % 360 : S.heading;
        rose.setAttribute('transform', `rotate(${-h})`);
        head.textContent = `${angle(h)} ${card(h)}`;
        sub.textContent = `${P.north === 'true' ? 'Utara sebenarnya' : 'Utara magnetik'}${!S.abs ? ' · sensor belum mutlak' : ''}`;
        const tgt = P.opt && P.opt.target ? P.opt.target() : null, tEl = P.el.querySelector('#ntTarget'), tTxt = P.el.querySelector('#ntTgt');
        if (tgt && p && tEl) {
          const brT = bearing(p.lat, p.lon, tgt.lat, tgt.lon), br = P.north === 'true' ? brT : (brT - (dec || 0) + 360) % 360;
          tEl.setAttribute('transform', `rotate(${br - h})`); tEl.setAttribute('opacity', '1');
          if (tTxt) tTxt.innerHTML = `Ke <b>${esc(tgt.name || 'tujuan')}</b>: ${angle(br)} · ${fmtDist(hav(p.lat, p.lon, tgt.lat, tgt.lon))}`;
        }
      } else if (S.listening && head && Date.now() - S.lastEvt > 3000) { sub.textContent = 'HP ini tidak mengirim data kompas (sensor magnet tidak tersedia/terblokir).'; }
      const t = P.lockTilt || tiltNow();
      if (t) {
        const set = (id, v) => { const el = P.el.querySelector(id); if (el) el.textContent = v; };
        set('#ntTilt', `${t.tilt.toFixed(1).replace('.', ',')}° · ${Math.round(Math.tan(Math.min(t.tilt, 89.9) * rad) * 100)}%`);
        set('#ntPitch', `${t.pitch.toFixed(1).replace('.', ',')}°`); set('#ntRoll', `${t.roll.toFixed(1).replace('.', ',')}°`);
        const bub = P.el.querySelector('#ntBub');
        if (bub) { const dx = Math.max(-35, Math.min(35, -t.roll * 1.2)), dy = Math.max(-35, Math.min(35, -t.pitch * 1.2)); bub.style.transform = `translate(${dx}px, ${dy}px)`; bub.style.background = t.tilt < 1 ? '#3fa34d' : '#e0a23a'; }
      }
    });
  }
  function open(opt) {
    ensure(); P.opt = opt || {}; P.open = true; P.el.hidden = false; hadPos = false;
    // Android tidak perlu izin: langsung aktif. iPhone meminta izin lewat tombol "Aktifkan kompas".
    if (!(window.DeviceOrientationEvent && typeof DeviceOrientationEvent.requestPermission === 'function')) startSensors();
    render();
    clearInterval(P.tick); P.tick = setInterval(() => { if (P.open) render(); }, 15000);
  }
  function close() { P.open = false; if (P.el) P.el.hidden = true; clearInterval(P.tick); stopSensors(); if (P.opt && P.opt.onClose) P.opt.onClose(); }

  // Dipanggil aplikasi saat posisi GPS berubah: panel digambar ulang bila posisi pertama baru didapat, selebihnya cukup jarum/jarak.
  let hadPos = false;
  function refresh() { if (!P.open) return; const has = !!pos(); if (has && !hadPos) { hadPos = true; render(); } else draw(); }
  window.NavTools = { refresh, fmt, FORMATS, toUTM, dms, angle, angleUnit, bearing, distance: hav, declination, skyInfo, toGPX, parseGPX, open, close, pref, setPref,
    format: () => pref('fmt', 'dd'), setFormat: f => setPref('fmt', f) };
})();
