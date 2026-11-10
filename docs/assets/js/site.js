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
