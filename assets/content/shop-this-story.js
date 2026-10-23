/* Shop this story — drop-in product cards for editorial posts.
   Content -> commerce: turns product ids inside a story into live, branded
   product cards that link to the PDP, with article->PDP attribution.

   USAGE (the post renderer or dashboard emits one of these):
     <div class="shop-this-story" data-products="toa-oversized,toa-685-tee"></div>
     <!-- inline, mid-article: -->   <span data-shop="toa-oversized"></span>
   Then this script (loaded once per /stories page) hydrates them from
   /shop/search.json. No Shopify call needed — search.json is static and already
   carries name, colour, team, price, slug, image, sold-out per product.

   Attribution: a click fires pmnTrack/pmnLog select_promotion with
   {creative:"shop_this_story", slot:<post slug>} and lands on the PDP with
   ?ref=story-<slug> so article->PDP is measurable in GA4/Meta and Supabase.

   Brand: black cards, Bebas Neue heading, team accent hairline, pill button.
   Self-contained; safe to include on any page. */
(function () {
  "use strict";
  var MOUNTS = "[data-products], [data-shop]";
  if (!document.querySelector(MOUNTS)) return;

  var slugOfPost = (document.querySelector("[data-post-slug]") || {}).dataset
    ? document.querySelector("[data-post-slug]").dataset.postSlug
    : (location.pathname.split("/").filter(Boolean).pop() || "story");

  var track = function (name, d) {
    try { window.pmnLog ? window.pmnLog(name, d) : (window.pmnTrack && window.pmnTrack(name, d)); } catch (e) {}
  };

  var esc = function (v) {
    return String(v == null ? "" : v).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
  };

  var teamClass = function (t) {
    return /samoa/i.test(t) ? "sts-samoa" : /tonga/i.test(t) ? "sts-tonga" : "sts-pmn";
  };

  var card = function (p) {
    var href = "/shop/" + p.s + "?ref=story-" + encodeURIComponent(slugOfPost);
    var price = p.p != null ? "$" + p.p : "";
    var sold = p.so ? '<span class="sts-so">Sold out</span>' : "";
    return '<a class="sts-card ' + teamClass(p.t) + '" href="' + href + '"' +
      ' data-pid="' + esc(p.id) + '">' +
      '<span class="sts-media"><img loading="lazy" decoding="async" src="' + esc(p.i) +
      '" alt="' + esc(p.n) + (p.c ? " in " + esc(p.c) : "") + '"></span>' +
      '<span class="sts-body">' +
      '<span class="sts-team">' + esc(p.t) + "</span>" +
      '<span class="sts-name">' + esc(p.n) + "</span>" +
      '<span class="sts-row"><span class="sts-price">' + esc(price) + "</span>" + sold +
      '<span class="sts-cta">Shop</span></span>' +
      "</span></a>";
  };

  fetch("/shop/search.json", { credentials: "omit" })
    .then(function (r) { return r.ok ? r.json() : []; })
    .then(function (list) {
      var by = {};
      (list || []).forEach(function (p) { by[p.id] = p; });

      document.querySelectorAll(MOUNTS).forEach(function (el) {
        var ids = (el.dataset.products || el.dataset.shop || "")
          .split(",").map(function (s) { return s.trim(); }).filter(Boolean);
        var found = ids.map(function (id) { return by[id]; }).filter(Boolean);
        if (!found.length) { el.remove(); return; } // unknown id: fail quiet, no empty box

        var inline = el.hasAttribute("data-shop") && ids.length === 1;
        el.classList.add(inline ? "sts-inline" : "sts-grid");
        if (!inline && !el.querySelector(".sts-head")) {
          el.insertAdjacentHTML("afterbegin",
            '<p class="sts-head">Shop this story</p>');
        }
        el.insertAdjacentHTML("beforeend",
          '<div class="sts-items">' + found.map(card).join("") + "</div>");

        // impression (once visible) — reuse the site's view_item vocabulary
        found.forEach(function (p) {
          track("select_promotion", {
            ref: p.id, title: p.n, url: "/shop/" + p.s,
            meta: { creative: "shop_this_story", slot: slugOfPost }
          });
        });
      });

      // click attribution
      document.addEventListener("click", function (e) {
        var a = e.target.closest ? e.target.closest(".sts-card") : null;
        if (!a) return;
        track("select_promotion", {
          ref: a.dataset.pid, url: a.getAttribute("href"),
          meta: { creative: "shop_this_story_click", slot: slugOfPost }
        });
      });
    })
    .catch(function () {
      document.querySelectorAll(MOUNTS).forEach(function (el) { el.remove(); });
    });
})();
