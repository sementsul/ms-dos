/* ms-dos.su — v86 MS-DOS emulator page.
 *
 * The page sets window.DOSTEST before loading this file:
 *   window.DOSTEST = {
 *     i18n: { loading, reading, readyHint, started, stopped, timeout, error,
 *             noFile, readError, stoppedMsg },
 *     assets: { wasm, bios, vgaBios, demo5, demo6 }
 *   }
 */
(function () {
  "use strict";

  var CFG = window.DOSTEST || {};
  var T = CFG.i18n || {};
  var ASSETS = CFG.assets || {};
  var emulator = null;
  var statusEl = document.getElementById("emu-status");
  var screenEl = document.getElementById("screen_container");

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text;
  }

  function fmt(template, value) {
    return String(template || "").replace("%s", value);
  }

  function destroy() {
    if (emulator) {
      try { emulator.stop(); } catch (e) {}
      try { if (emulator.destroy) emulator.destroy(); } catch (e) {}
      emulator = null;
    }
    if (screenEl) screenEl.innerHTML = "";
  }

  function boot(opts, label) {
    destroy();
    setStatus(fmt(T.loading, label));
    var cfg = {
      screen_container: screenEl,
      wasm_path: ASSETS.wasm,
      bios: { url: ASSETS.bios },
      vga_bios: { url: ASSETS.vgaBios },
      autostart: true,
      memory_size: 16 * 1024 * 1024,
      vga_memory_size: 2 * 1024 * 1024
    };
    if (opts.fda) cfg.fda = { buffer: opts.fda };
    if (opts.hda_url) cfg.hda = { url: opts.hda_url, async: true };
    try {
      emulator = new V86(cfg);
    } catch (e) {
      setStatus(fmt(T.error, e.message));
      return;
    }
    emulator.add_listener("download-progress", function (e) {
      if (e && e.total) {
        setStatus(fmt(T.loadingProgress, Math.round(e.loaded / e.total * 100)));
      }
    });
    emulator.add_listener("emulator-ready", function () {
      if (readyTimer) { clearTimeout(readyTimer); readyTimer = null; }
      setStatus(fmt(T.started, label));
    });
    emulator.add_listener("emulator-stopped", function () {
      setStatus(T.stopped);
    });
    var readyTimer = setTimeout(function () {
      readyTimer = null;
      setStatus(T.timeout);
    }, 60000);
  }

  window.addEventListener("error", function (e) {
    setStatus(fmt(T.pageError, (e && e.message) || (e && e.type) || ""));
  });

  function bootFromInput(inputId, label) {
    var input = document.getElementById(inputId);
    var f = input && input.files && input.files[0];
    if (!f) { setStatus(fmt(T.noFile, label)); return; }
    setStatus(fmt(T.reading, f.name + " (" + Math.round(f.size / 1024) + " KB)"));
    var rd = new FileReader();
    rd.onload = function () { boot({ fda: rd.result }, label); };
    rd.onerror = function () { setStatus(T.readError); };
    rd.readAsArrayBuffer(f);
  }

  function probe(url) {
    return fetch(url, { method: "HEAD" }).then(function (r) { return r.ok; })
      .catch(function () { return false; });
  }

  var b5 = document.getElementById("boot5");
  var b6 = document.getElementById("boot6");
  var biosBtn = document.getElementById("btn-bios");
  var stopBtn = document.getElementById("btn-stop");
  var demo5 = document.getElementById("demo5");
  var demo6 = document.getElementById("demo6");
  var demoNote = document.getElementById("demo-note");

  if (b5) b5.onclick = function () { bootFromInput("file5", "MS-DOS 5.00"); };
  if (b6) b6.onclick = function () { bootFromInput("file6", "MS-DOS 6.22"); };
  if (biosBtn) biosBtn.onclick = function () { boot({}, T.biosLabel || "SeaBIOS"); };
  if (stopBtn) stopBtn.onclick = function () { destroy(); setStatus(T.stoppedMsg); };
  if (demo5) demo5.onclick = function () { boot({ hda_url: ASSETS.demo5 }, T.demo5Label); };
  if (demo6) demo6.onclick = function () { boot({ hda_url: ASSETS.demo6 }, T.demo6Label); };

  /* Demo images are optional: disable the buttons when the files are absent. */
  Promise.all([probe(ASSETS.demo5), probe(ASSETS.demo6)]).then(function (r) {
    if (demo5) demo5.disabled = !r[0];
    if (demo6) demo6.disabled = !r[1];
    if (!r[0] && !r[1] && demoNote) demoNote.style.display = "block";
  });
})();