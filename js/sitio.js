/* Avisos de exposición: "Ahora" durante las fechas, "Próximamente" antes, y
   desaparecen al terminar. La fecha que cuenta es la de Bergen. */
(function () {
  var hoy = new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Oslo" }).format(new Date());
  document.querySelectorAll("[data-desde][data-hasta]").forEach(function (el) {
    var desde = el.getAttribute("data-desde"), hasta = el.getAttribute("data-hasta");
    if (hoy > hasta) { el.remove(); return; }
    var ahora = hoy >= desde;
    el.querySelectorAll("[data-estado]").forEach(function (s) {
      s.hidden = (s.getAttribute("data-estado") === "ahora") !== ahora;
    });
  });
})();

/* Selector de idioma: se cierra al pulsar fuera o con Escape. */
(function () {
  var sel = document.querySelectorAll(".idioma-sel");
  if (!sel.length) return;
  document.addEventListener("click", function (e) {
    sel.forEach(function (d) { if (d.open && !d.contains(e.target)) d.open = false; });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    sel.forEach(function (d) { if (d.open) { d.open = false; d.querySelector("summary").focus(); } });
  });
})();
