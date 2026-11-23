(function () {
  "use strict";

  var base = window.ZH_BASE || "";

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) { node.className = cls; }
    if (text !== undefined) { node.textContent = text; }
    return node;
  }

  var links = document.querySelectorAll(".zh-nav-link");

  // 当前页高亮
  var here = window.location.pathname;
  Array.prototype.forEach.call(links, function (a) {
    var href = a.getAttribute("href");
    if (href && (href === here || href + "index.html" === here)) {
      a.classList.add("is-active");
    }
  });

  // 按目录分组
  var nav = document.querySelector(".zh-nav");
  if (nav) {
    var groups = {};
    Array.prototype.forEach.call(links, function (a) {
      var g = a.getAttribute("data-group") || "/";
      if (!groups[g]) { groups[g] = []; }
      groups[g].push(a);
    });
    var labels = { "/": "通用指南", "/go/": "Go 系列", "/docguide/": "文档指南" };
    Object.keys(groups).sort().forEach(function (g) {
      var box = el("div", "zh-group");
      box.appendChild(el("h3", "zh-group-title", labels[g] || g));
      groups[g].forEach(function (a) { box.appendChild(a); });
      nav.appendChild(box);
    });
  }

  // 移动端抽屉
  var toggle = document.getElementById("zh-toggle");
  var sidebar = document.getElementById("zh-sidebar");
  if (toggle && sidebar) {
    toggle.addEventListener("click", function () {
      sidebar.classList.toggle("is-open");
    });
  }

  // 站内搜索（Fuse.js 按字符模糊匹配，中文无需分词）
  var input = document.getElementById("zh-search-input");
  var results = document.getElementById("zh-search-results");
  if (!input || !results || typeof window.Fuse === "undefined") { return; }

  var fuse = null;
  fetch(base + "/assets/search-index.json")
    .then(function (r) { return r.json(); })
    .then(function (data) {
      fuse = new window.Fuse(data, {
        keys: [
          { name: "title", weight: 0.6 },
          { name: "excerpt", weight: 0.4 }
        ],
        threshold: 0.35,
        ignoreLocation: true,
        minMatchCharLength: 2
      });
    })
    .catch(function () { /* 索引不可用时静默降级为无搜索 */ });

  function render(items) {
    while (results.firstChild) { results.removeChild(results.firstChild); }
    items.slice(0, 12).forEach(function (item) {
      var li = el("li");
      var a = el("a", null, item.title);
      a.href = item.url;
      li.appendChild(a);
      results.appendChild(li);
    });
  }

  input.addEventListener("input", function () {
    var q = input.value.trim();
    if (!fuse || q.length < 2) { render([]); return; }
    render(fuse.search(q).map(function (r) { return r.item; }));
  });
})();

/* ===== 右侧本页目录（TOC）：扫描正文标题，生成可点击目录并做滚动高亮 ===== */
(function () {
  "use strict";

  var main = document.querySelector(".zh-main");
  var toc = document.getElementById("zh-toc");
  if (!main || !toc) { return; }

  var headings = main.querySelectorAll("h1, h2, h3, h4");
  if (!headings.length) { toc.style.display = "none"; return; }

  var title = document.createElement("p");
  title.className = "zh-toc-title";
  title.textContent = "本页目录";
  toc.appendChild(title);

  var nav = document.createElement("nav");
  nav.className = "zh-toc-nav";
  nav.setAttribute("aria-label", "本页目录");
  toc.appendChild(nav);

  var list = document.createElement("ul");
  list.className = "zh-toc-list";
  nav.appendChild(list);

  var links = [];
  Array.prototype.forEach.call(headings, function (h, idx) {
    // kramdown 已为标题生成 id；缺失时兜底生成一个，保证锚点可用
    if (!h.id) {
      var slug = (h.textContent || "").trim()
        .toLowerCase()
        .replace(/\s+/g, "-")
        .replace(/[^\w\u4e00-\u9fa5-]/g, "")
        .slice(0, 40);
      h.id = slug || ("sec-" + idx);
    }

    var li = document.createElement("li");
    var a = document.createElement("a");
    a.className = "zh-toc-link zh-toc-lvl-" + h.tagName.charAt(1);
    a.href = "#" + h.id;
    a.setAttribute("data-target", h.id);
    var text = (h.textContent || "").trim();
    a.textContent = text;
    a.title = text; // 长标题 hover 显示全文
    li.appendChild(a);
    list.appendChild(li);
    links.push({ link: a, heading: h });
  });

  // 平滑滚动到目标，并同步地址栏锚点（无顶栏遮挡，无需偏移）
  list.addEventListener("click", function (e) {
    var node = e.target;
    var a = node && node.closest ? node.closest("a") : null;
    if (!a) { return; }
    var target = document.getElementById(a.getAttribute("data-target"));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      if (history.replaceState) { history.replaceState(null, "", "#" + target.id); }
    }
  });

  // 滚动高亮（scroll-spy）：标题进入视口顶部 30% 区域时标记为当前
  if ("IntersectionObserver" in window) {
    var byId = {};
    links.forEach(function (o) { byId[o.heading.id] = o.link; });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var link = byId[entry.target.id];
        if (!link || !entry.isIntersecting) { return; }
        links.forEach(function (o) { o.link.classList.remove("is-active"); });
        link.classList.add("is-active");
      });
    }, { rootMargin: "0px 0px -70% 0px", threshold: 0 });

    links.forEach(function (o) { observer.observe(o.heading); });
  }
})();

/* ===== 代码块增强：行号 + 复制按钮 + “已复制”提示 ===== */
(function () {
  "use strict";

  var main = document.querySelector(".zh-main");
  if (!main) { return; }

  var toastEl = null;
  function showToast(msg) {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "zh-toast";
      toastEl.setAttribute("role", "status");
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    void toastEl.offsetWidth; // 强制重排以重启过渡
    toastEl.classList.add("is-visible");
    clearTimeout(toastEl._t);
    toastEl._t = setTimeout(function () { toastEl.classList.remove("is-visible"); }, 1500);
  }

  function copyText(text, btn) {
    function ok() {
      showToast("已复制");
      var prev = btn.textContent;
      btn.textContent = "已复制";
      btn.classList.add("is-copied");
      setTimeout(function () {
        btn.textContent = prev;
        btn.classList.remove("is-copied");
      }, 1500);
    }
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.top = "-9999px";
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try { document.execCommand("copy"); } catch (e) { /* 忽略 */ }
      document.body.removeChild(ta);
      ok();
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(ok).catch(fallback);
    } else {
      fallback();
    }
  }

  var pres = main.querySelectorAll("pre");
  Array.prototype.forEach.call(pres, function (pre) {
    if (pre.closest && pre.closest(".zh-codeblock")) { return; } // 防御重复处理

    var codeEl = pre.querySelector("code") || pre;
    var text = (codeEl.textContent || "").replace(/\n$/, "");
    var lines = text.split("\n");
    if (lines.length === 1 && !text.trim()) { return; } // 跳过空块

    var gutter = document.createElement("pre");
    gutter.className = "zh-ln";
    gutter.setAttribute("aria-hidden", "true");
    var gcode = document.createElement("code");
    gcode.textContent = lines.map(function (_, i) { return i + 1; }).join("\n");
    gutter.appendChild(gcode);

    var wrap = document.createElement("div");
    wrap.className = "zh-codeblock";

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "zh-copy-btn";
    btn.textContent = "复制";
    btn.setAttribute("aria-label", "复制代码");

    var inner = document.createElement("div");
    inner.className = "zh-code-inner";
    inner.appendChild(gutter);

    var parent = pre.parentNode;
    parent.insertBefore(wrap, pre); // 在原 <pre> 位置插入外层容器
    inner.appendChild(pre);         // 原 <pre> 移入 inner（与行号并列）
    wrap.appendChild(btn);
    wrap.appendChild(inner);

    btn.addEventListener("click", function (e) {
      e.preventDefault();
      copyText(text, btn);
    });
  });
})();

/* ===== 主题切换（深色 / 浅色） ===== */
(function () {
  "use strict";

  var btn = document.getElementById("zh-theme-toggle");
  if (!btn) { return; }
  var label = btn.querySelector(".zh-theme-label");

  function sync() {
    var t = document.documentElement.getAttribute("data-theme") || "light";
    if (label) { label.textContent = t === "dark" ? "浅色" : "深色"; }
    btn.setAttribute("aria-label", t === "dark" ? "切换到浅色主题" : "切换到深色主题");
  }
  sync();

  btn.addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("data-theme") || "light";
    var next = cur === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem("zh-theme", next); } catch (e) {}
    sync();
  });
})();
