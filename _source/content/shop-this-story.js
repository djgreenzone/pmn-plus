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

  // Always-visible slider bar: sizes/moves the thumb to track scroll, drags to scroll,
  // and hides itself when the cards don't overflow. Card widths are fixed (flex-basis),
  // so geometry is stable regardless of image load.
  var wireSlider = function (root) {
    var items = root.querySelector(".sts-items");
    var bar = root.querySelector(".sts-bar");
    if (!items || !bar) return;
    var thumb = bar.querySelector(".sts-bar-thumb");
    var sync = function () {
      var sw = items.scrollWidth, cw = items.clientWidth, max = sw - cw;
      if (max <= 2) { bar.hidden = true; return; }
      bar.hidden = false;
      var bw = bar.clientWidth;
      var tw = Math.max(bw * (cw / sw), 28);
      thumb.style.width = tw + "px";
      thumb.style.transform = "translateX(" + (items.scrollLeft / max) * (bw - tw) + "px)";
    };
    var drag = false;
    var seek = function (clientX) {
      var r = bar.getBoundingClientRect(), tw = thumb.offsetWidth, bw = bar.clientWidth;
      var pos = Math.max(0, Math.min(clientX - r.left - tw / 2, bw - tw));
      var max = items.scrollWidth - items.clientWidth;
      items.scrollLeft = (bw - tw) > 0 ? (pos / (bw - tw)) * max : 0;
    };
    items.addEventListener("scroll", sync, { passive: true });
    window.addEventListener("resize", sync);
    bar.addEventListener("pointerdown", function (e) {
      drag = true; try { bar.setPointerCapture(e.pointerId); } catch (x) {}
      seek(e.clientX); e.preventDefault();
    });
    bar.addEventListener("pointermove", function (e) { if (drag) seek(e.clientX); });
    var stop = function () { drag = false; };
    bar.addEventListener("pointerup", stop);
    bar.addEventListener("pointercancel", stop);
    sync();
    setTimeout(sync, 80);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(sync);
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
        if (inline) {
          el.insertAdjacentHTML("beforeend",
            '<div class="sts-items">' + found.map(card).join("") + "</div>");
        } else {
          // CTA target: all one team -> that collection, mixed -> the whole shop
          var teams = found.map(function (p) { return p.t || ""; });
          var same = teams.every(function (t) { return t === teams[0]; });
          var cta = { href: "/shop", label: "Shop all merch" };
          if (same && /samoa/i.test(teams[0])) cta = { href: "/shop/toa-samoa", label: "Shop all Toa Samoa" };
          else if (same && /tonga/i.test(teams[0])) cta = { href: "/shop/mate-maa-tonga", label: "Shop all Mate Ma'a Tonga" };
          var ctaHref = cta.href + "?ref=story-" + encodeURIComponent(slugOfPost);
          if (!el.querySelector(".sts-head")) {
            el.insertAdjacentHTML("afterbegin", '<p class="sts-head">Shop this story</p>');
          }
          // terminal "see all" card lives at the end of the slider
          var seeAll = '<a class="sts-card sts-seeall" href="' + ctaHref + '" data-pid="sts-seeall" aria-label="' +
            esc(cta.label) + '"><span class="sts-seeall-ar" aria-hidden="true">&rarr;</span>' +
            '<span class="sts-seeall-t">' + esc(cta.label) + '</span></a>';
          el.insertAdjacentHTML("beforeend",
            '<div class="sts-items">' + found.map(card).join("") + seeAll + "</div>");
          // visible slider bar between the cards and the CTA
          el.insertAdjacentHTML("beforeend",
            '<div class="sts-bar" hidden><span class="sts-bar-thumb"></span></div>');
          // and a primary CTA button underneath
          el.insertAdjacentHTML("beforeend",
            '<a class="sts-shopall" href="' + ctaHref + '" data-pid="sts-shopall">' + esc(cta.label) +
            ' <span aria-hidden="true">&rarr;</span></a>');
          wireSlider(el);
        }

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
        var a = e.target.closest ? e.target.closest(".sts-card, .sts-shopall") : null;
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
