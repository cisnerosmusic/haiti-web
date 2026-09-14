/* La luz de la página es la de Bergen, ahora.
   Calcula la altura del sol en Bergen (60,39° N, 5,32° E) y pinta el cielo de la
   portada y el fondo de las demás páginas. Se carga en <head>, sin defer, para que
   la primera imagen ya salga con la luz correcta. Sin peticiones externas.
   Vista previa de una hora concreta: ?luz=HH:MM (hora de Bergen, día de hoy). */
(function () {
  var LAT = 60.3913, LON = 5.3221, R = Math.PI / 180, raiz = document.documentElement;

  function elev(ms) {
    var d = (ms - Date.UTC(2000, 0, 1, 12)) / 864e5, g = (357.529 + 0.98560028 * d) * R, q = 280.459 + 0.98564736 * d;
    var L = (q + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) * R, e = (23.439 - 0.00000036 * d) * R;
    var ra = Math.atan2(Math.cos(e) * Math.sin(L), Math.cos(L)), dec = Math.asin(Math.sin(e) * Math.sin(L));
    var gmst = ((18.697374558 + 24.06570982441908 * d) % 24 + 24) % 24, H = (gmst * 15 + LON) * R - ra;
    return Math.asin(Math.sin(LAT * R) * Math.sin(dec) + Math.cos(LAT * R) * Math.cos(dec) * Math.cos(H)) / R;
  }

  /* Color en OKLab: las mezclas entre paradas no se enturbian */
  function cl(v) { return Math.max(0, Math.min(1, v)); }
  function lin(c) { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); }
  function gam(c) { c = cl(c); return Math.round((c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - 0.055) * 255); }
  function lab(h) {
    var r = lin(parseInt(h.slice(1, 3), 16)), g = lin(parseInt(h.slice(3, 5), 16)), b = lin(parseInt(h.slice(5, 7), 16));
    var l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b),
        m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b),
        s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
    return [0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s];
  }
  function rgbLin(L) {
    var l = L[0] + 0.3963377774 * L[1] + 0.2158037573 * L[2],
        m = L[0] - 0.1055613458 * L[1] - 0.0638541728 * L[2],
        s = L[0] - 0.0894841775 * L[1] - 1.2914855480 * L[2];
    l = l * l * l; m = m * m * m; s = s * s * s;
    return [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s];
  }
  function css(L) { var c = rgbLin(L); return "rgb(" + gam(c[0]) + "," + gam(c[1]) + "," + gam(c[2]) + ")"; }
  function lum(L) { var c = rgbLin(L); return 0.2126 * cl(c[0]) + 0.7152 * cl(c[1]) + 0.0722 * cl(c[2]); }
  function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }

  /* Paradas por altura del sol: [grados, arriba, centro, abajo] */
  var PARADAS = [
    [-30, "#010207", "#02040B", "#050A17"],  // la hora más oscura: azul casi negro
    [-18, "#02050D", "#050B1C", "#0A1430"],  // noche astronómica
    [-12, "#050B1E", "#0B1735", "#16264C"],  // noche náutica
    [-6,  "#12204A", "#283B72", "#56568E"],  // hora azul
    [-2,  "#34457F", "#8C7BA8", "#E8A78F"],  // alba: violeta, malva, rosa melocotón
    [2,   "#7FA3C4", "#E9C3A6", "#F5D494"],  // salida del sol
    [10,  "#BFDCD6", "#EEE2B4", "#F4DE98"],  // mañana
    [30,  "#CDE7E0", "#F4EEBB", "#E9E7A6"]   // la hora más clara: amarillo con tintes verdeazules
  ].map(function (p) { return [p[0], lab(p[1]), lab(p[2]), lab(p[3])]; });

  function cielo(el) {
    var n = PARADAS.length;
    if (el <= PARADAS[0][0]) return PARADAS[0].slice(1);
    if (el >= PARADAS[n - 1][0]) return PARADAS[n - 1].slice(1);
    for (var i = 0; i < n - 1; i++) {
      var a = PARADAS[i], b = PARADAS[i + 1];
      if (el <= b[0]) { var t = (el - a[0]) / (b[0] - a[0]); return [mix(a[1], b[1], t), mix(a[2], b[2], t), mix(a[3], b[3], t)]; }
    }
  }

  /* Legibilidad: ningún fondo con texto encima cae en la franja de luminancia media,
     donde ni la tinta clara ni la oscura contrastan bien. Así el peor caso supera 4,5:1. */
  function conLum(c, meta) {
    var lo = 0, hi = 1, x = c.slice();
    for (var k = 0; k < 20; k++) { x[0] = (lo + hi) / 2; if (lum(x) < meta) lo = x[0]; else hi = x[0]; }
    return x;
  }
  function legible(c) { var y = lum(c); return (y <= 0.12 || y >= 0.27) ? c : conLum(c, y < 0.18 ? 0.12 : 0.27); }

  var OSCURA = "#0B0D12", CLARA = "#F6F4ED";
  var LO = lum(lab(OSCURA)), LC = lum(lab(CLARA));
  function cr(a, b) { return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); }
  function tinta(fondo) {
    var y = lum(fondo);
    return cr(y, LO) >= cr(y, LC)
      ? { i: OSCURA, s: "rgba(11,13,18,.8)", l: "rgba(11,13,18,.2)" }
      : { i: CLARA, s: "rgba(246,244,237,.82)", l: "rgba(246,244,237,.22)" };
  }

  function momento() {
    var m = /[?&]luz=(\d{1,2}):(\d{2})/.exec(location.search);
    if (!m) return Date.now();
    var p = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Oslo", year: "numeric", month: "2-digit", day: "2-digit", timeZoneName: "shortOffset" }).formatToParts(new Date());
    var g = function (t) { var x = p.find(function (y) { return y.type === t; }); return x ? x.value : ""; };
    var off = /GMT([+-]\d+)?/.exec(g("timeZoneName")), h = off && off[1] ? +off[1] : 0;
    return Date.UTC(+g("year"), +g("month") - 1, +g("day"), +m[1] - h, +m[2]);
  }

  var meta = document.querySelector('meta[name="theme-color"]');
  function aplicar() {
    var el = elev(momento()), c = cielo(el), s = raiz.style;
    var c1 = legible(c[0]), c3 = legible(c[2]);
    var fondo = legible([c[1][0], c[1][1] * 0.22, c[1][2] * 0.22]);
    var t1 = tinta(c1), t3 = tinta(c3), tf = tinta(fondo);
    s.setProperty("--c1", css(c1)); s.setProperty("--c2", css(c[1])); s.setProperty("--c3", css(c3));
    s.setProperty("--t1", t1.i); s.setProperty("--t1-2", t1.s);
    s.setProperty("--t3", t3.i); s.setProperty("--t3-2", t3.s); s.setProperty("--t3-l", t3.l);
    s.setProperty("--fondo", css(fondo)); s.setProperty("--tinta", tf.i); s.setProperty("--tinta-2", tf.s); s.setProperty("--linea", tf.l);
    s.setProperty("--aur", (cl((-14 - el) / 10) * 0.22).toFixed(3));
    raiz.setAttribute("data-luz", el >= 2 ? "dia" : el >= -6 ? "alba" : "noche");
    if (meta) meta.setAttribute("content", css(fondo));
  }
  aplicar();
  setInterval(aplicar, 60000);
})();
