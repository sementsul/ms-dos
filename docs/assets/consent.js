/* ms-dos.su consent manager.
 *
 * Design rules (GDPR / ePrivacy / 152-ФЗ / CCPA):
 *  - nothing is loaded from analytics hosts before an explicit click;
 *  - "reject" is as easy to reach as "accept" and is not pre-selected;
 *  - the choice is stored locally with a version and a timestamp;
 *  - Global Privacy Control and Do Not Track are treated as opt-out signals;
 *  - the user can reopen the settings dialog from any page footer.
 */
(function () {
  "use strict";

  var KEY = "mbfu_consent";
  var VERSION = "1";
  var GA_ID = "G-Y8PG2P181B";
  var METRIKA_ID = 106570050;

  var stored = null;
  try {
    stored = JSON.parse(localStorage.getItem(KEY) || "null");
  } catch (e) {
    stored = null;
  }

  function readChoice() {
    if (!stored || stored.v !== VERSION || typeof stored.analytics !== "boolean") {
      return null;
    }
    return stored;
  }

  function save(analytics) {
    stored = { v: VERSION, analytics: !!analytics, ts: new Date().toISOString() };
    try {
      localStorage.setItem(KEY, JSON.stringify(stored));
    } catch (e) {
      /* private mode: the choice still applies for this page view */
    }
  }

  function optOutSignal() {
    if (navigator.globalPrivacyControl === true) return true;
    var dnt = navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack;
    return dnt === "1" || dnt === "yes";
  }

  var loaded = false;

  function loadTrackers() {
    if (loaded) return;
    loaded = true;

    /* Google Analytics 4 */
    var ga = document.createElement("script");
    ga.async = true;
    ga.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(ga);

    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA_ID, { anonymize_ip: true });

    /* Yandex Metrica: session recording (webvisor) stays off by design */
    (function (m, e, t, r, i, k, a) {
      m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); };
      m[i].l = 1 * new Date();
      for (var j = 0; j < document.scripts.length; j++) {
        if (document.scripts[j].src === r) { return; }
      }
      k = e.createElement(t);
      a = e.getElementsByTagName(t)[0];
      k.async = 1;
      k.src = r;
      a.parentNode.insertBefore(k, a);
    })(window, document, "script", "https://mc.yandex.ru/metrika/tag.js?id=" + METRIKA_ID, "ym");

    window.ym(METRIKA_ID, "init", {
      ssr: true,
      webvisor: false,
      clickmap: true,
      ecommerce: "dataLayer",
      referrer: document.referrer,
      url: location.href,
      accurateTrackBounce: true,
      trackLinks: true
    });
  }

  function apply(choice) {
    if (choice && choice.analytics) {
      loadTrackers();
    }
  }

  var banner = document.getElementById("consent");
  var dialog = document.getElementById("consent-dialog");
  var checkbox = document.getElementById("consent-analytics");

  function showBanner() {
    if (banner) banner.hidden = false;
  }

  function hideBanner() {
    if (banner) banner.hidden = true;
  }

  function openSettings() {
    if (!dialog) return;
    var choice = readChoice();
    if (checkbox) {
      checkbox.checked = choice ? choice.analytics : false;
      checkbox.disabled = false;
    }
    if (typeof dialog.showModal === "function") {
      dialog.showModal();
    } else {
      dialog.setAttribute("open", "open");
    }
  }

  function closeSettings() {
    if (!dialog) return;
    if (typeof dialog.close === "function") dialog.close();
    else dialog.removeAttribute("open");
  }

  function clearAnalyticsCookies() {
    var names = document.cookie ? document.cookie.split(";") : [];
    var hosts = [location.hostname, "." + location.hostname.split(".").slice(-2).join(".")];
    names.forEach(function (pair) {
      var name = pair.split("=")[0].trim();
      if (!/^(_ga|_gid|_gat|_ym|ymex|_ym_uid|_ym_d|_ym_isad|_ym_visorc)/.test(name)) {
        return;
      }
      hosts.forEach(function (h) {
        document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=" + h;
      });
      document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
    });
  }

  function decide(analytics) {
    save(analytics);
    hideBanner();
    if (!analytics) clearAnalyticsCookies();
    apply({ analytics: analytics });
  }

  function wire() {
    var accept = document.getElementById("consent-accept");
    var reject = document.getElementById("consent-reject");
    var saveBtn = document.getElementById("consent-save");

    if (accept) accept.addEventListener("click", function () { decide(true); });
    if (reject) reject.addEventListener("click", function () { decide(false); });

    document.querySelectorAll("[data-consent-settings]").forEach(function (el) {
      el.addEventListener("click", function (ev) {
        ev.preventDefault();
        openSettings();
      });
    });

    if (dialog) {
      dialog.addEventListener("click", function (ev) {
        if (ev.target === dialog) closeSettings();
      });
    }

    if (saveBtn) {
      saveBtn.addEventListener("click", function (ev) {
        ev.preventDefault();
        var value = checkbox ? checkbox.checked : false;
        decide(value);
        closeSettings();
      });
    }
  }

  function init() {
    wire();
    var choice = readChoice();
    if (choice) {
      apply(choice);
      hideBanner();
      return;
    }
    if (optOutSignal()) {
      save(false);
      hideBanner();
      return;
    }
    showBanner();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.MBFUConsent = {
    open: openSettings,
    reset: function () {
      try { localStorage.removeItem(KEY); } catch (e) {}
      location.reload();
    }
  };
})();