# 推背图浏览器明显改版 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把现有单文件《推背图》浏览器改造成有目录、搜索、探索入口、注音注解和内容说明的沉浸式阅读工作台。

**Architecture:** 继续保留 `tuibeitu.html` 单文件架构，复用内联 `TUI_BEI_DATA`，重写页面 shell、CSS 和渲染逻辑。新增 `GLOSSARY` 词表、目录过滤状态、阅读偏好存储和注音注解渲染函数，不引入外部依赖。

**Tech Stack:** HTML5 + CSS3 + Vanilla JavaScript + browser `localStorage`

---

## File Structure

- Modify: `E:\推背图浏览器\tuibeitu.html`
  - 保留 `TUI_BEI_DATA` 数据数组。
  - 重写 `<style>` 为三栏阅读工作台样式。
  - 重写 `<body>` 内的应用骨架。
  - 替换现有 tab 式 JS 为目录、搜索、注解、阅读记忆和导航渲染。
- Keep unchanged: `E:\推背图浏览器\data_raw.json`
- Keep unchanged: `E:\推背图浏览器\data.js`
- Keep unchanged: `E:\推背图浏览器\scripts\*.py`

---

### Task 1: Establish Baseline And Locate Replacement Boundaries

**Files:**
- Read: `E:\推背图浏览器\tuibeitu.html`

- [ ] **Step 1: Confirm repository is clean enough to edit**

Run:

```powershell
git status --short
```

Expected: no unstaged user changes in `tuibeitu.html`. If unrelated files are dirty, leave them alone.

- [ ] **Step 2: Locate the major HTML sections**

Run:

```powershell
rg -n "<style>|</style>|<body>|</body>|const TUI_BEI_DATA|const DYNASTIES|function renderTimeline|DOMContentLoaded" tuibeitu.html
```

Expected: lines for CSS block, body block, data start, config start and current JS start. Use these as edit boundaries.

- [ ] **Step 3: Verify current data shape before changing render logic**

Run:

```powershell
rg -n '"id": 1|"ganZhi"|"title"|"chen"|"song"|"jinPi"|"baiHua"|"period"' tuibeitu.html
```

Expected: all listed fields exist in embedded data. Do not modify the data array in this task.

---

### Task 2: Replace Page Shell With Reading Workspace

**Files:**
- Modify: `E:\推背图浏览器\tuibeitu.html`

- [ ] **Step 1: Replace the body application skeleton**

Replace the current `<body>` application markup before the data `<script>` with this shell:

```html
<body>
<div id="app" class="app-shell">
  <header class="topbar">
    <div class="brand">
      <p class="eyebrow">六十象原文 · 金批 · 白话 · 注音</p>
      <h1>推背图浏览器</h1>
    </div>
    <div class="top-actions">
      <button class="ghost-btn" id="continueBtn" type="button">继续阅读</button>
      <button class="ghost-btn" id="randomBtn" type="button">随机一象</button>
    </div>
  </header>

  <section class="quick-routes" aria-label="探索入口">
    <button class="route-chip" type="button" data-jump="2">从唐朝开始</button>
    <button class="route-chip" type="button" data-period="近现代">近现代三象</button>
    <button class="route-chip" type="button" data-period="未来">只看未来象</button>
    <button class="route-chip" type="button" id="glossaryRoute">带注音的字词</button>
  </section>

  <main class="workspace">
    <aside class="sidebar" aria-label="目录与搜索">
      <div class="panel compact-panel">
        <label class="search-label" for="searchInput">搜索象序、干支、题名、正文</label>
        <input id="searchInput" class="search-input" type="search" placeholder="如：甲子、唐、谶、近现代">
      </div>

      <div class="panel">
        <div class="panel-heading">
          <h2>朝代</h2>
          <button class="text-btn" id="clearFilterBtn" type="button">全部</button>
        </div>
        <div id="periodFilters" class="period-filters"></div>
      </div>

      <div class="panel directory-panel">
        <div class="panel-heading">
          <h2>六十象</h2>
          <span id="resultCount" class="muted"></span>
        </div>
        <div id="directoryList" class="directory-list"></div>
      </div>
    </aside>

    <article class="reader" aria-live="polite">
      <div class="reader-head">
        <p id="currentMeta" class="current-meta"></p>
        <h2 id="currentTitle"></h2>
        <div id="currentTags" class="tag-row"></div>
      </div>

      <section class="text-section">
        <div class="section-title">
          <span>谶曰</span>
        </div>
        <div id="chenContent" class="classical-text"></div>
      </section>

      <section class="text-section">
        <div class="section-title">
          <span>颂曰</span>
        </div>
        <div id="songContent" class="classical-text"></div>
      </section>

      <details class="text-section note-section" open>
        <summary>金圣叹批</summary>
        <div id="jinpiContent" class="annotation-text"></div>
      </details>
    </article>

    <aside class="insights" aria-label="解读与注释">
      <div class="panel insight-card">
        <div class="panel-heading">
          <h2>看懂这一象</h2>
        </div>
        <p id="quickSummary" class="quick-summary"></p>
      </div>

      <div class="panel">
        <div class="panel-heading">
          <h2>白话解读</h2>
        </div>
        <div id="baihuaContent" class="baihua-text"></div>
      </div>

      <div class="panel">
        <div class="panel-heading">
          <h2>字词注解</h2>
        </div>
        <div id="glossaryList" class="glossary-list"></div>
      </div>

      <div class="panel source-note">
        <h2>内容说明</h2>
        <p>原文与金批据整理文本展示；白话解读为解释性文本，仅供阅读参考，不作事实断言。</p>
      </div>
    </aside>
  </main>

  <footer class="reader-nav">
    <button id="prevBtn" class="nav-btn" type="button">上一象</button>
    <span id="indicator" class="indicator"></span>
    <button id="nextBtn" class="nav-btn" type="button">下一象</button>
  </footer>
</div>
```

- [ ] **Step 2: Keep the embedded data script after the shell**

Confirm the markup is followed by:

```html
<script>
const TUI_BEI_DATA = [
```

Expected: `TUI_BEI_DATA` remains embedded in `tuibeitu.html`; there is no `<script src="data.js"></script>`.

- [ ] **Step 3: Run static markup check**

Run:

```powershell
rg -n "app-shell|workspace|directoryList|chenContent|glossaryList|const TUI_BEI_DATA" tuibeitu.html
```

Expected: all shell anchors and the data constant are present.

---

### Task 3: Redesign CSS For Three-Column Reading Experience

**Files:**
- Modify: `E:\推背图浏览器\tuibeitu.html`

- [ ] **Step 1: Replace the `<style>` block**

Replace the entire existing CSS with this structure. Keep values close to these tokens unless visual verification shows a problem:

```css
:root {
  --ink: #1f211d;
  --ink-soft: #4d5149;
  --paper: #f7f1e4;
  --paper-deep: #eee3cf;
  --line: rgba(55, 48, 38, 0.16);
  --bg: #161713;
  --bg-panel: #20231d;
  --cinnabar: #b7422f;
  --bronze: #8c7650;
  --green: #4f6758;
  --muted: #8e8779;
  --shadow: 0 18px 50px rgba(0, 0, 0, 0.28);
  --serif: "Noto Serif SC", "Songti SC", "SimSun", serif;
  --sans: "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
}

* {
  box-sizing: border-box;
}

html {
  color-scheme: dark;
}

body {
  margin: 0;
  min-height: 100vh;
  background:
    linear-gradient(180deg, rgba(183, 66, 47, 0.08), transparent 280px),
    var(--bg);
  color: var(--paper);
  font-family: var(--sans);
}

button,
input {
  font: inherit;
}

button {
  cursor: pointer;
}

.app-shell {
  width: min(1440px, calc(100vw - 32px));
  margin: 0 auto;
  padding: 28px 0 24px;
}

.topbar {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 24px;
  padding: 8px 0 18px;
}

.eyebrow {
  margin: 0 0 8px;
  color: var(--bronze);
  font-size: 13px;
  letter-spacing: 0.08em;
}

.brand h1 {
  margin: 0;
  color: var(--paper);
  font-family: var(--serif);
  font-size: 34px;
  font-weight: 700;
}

.top-actions,
.quick-routes,
.reader-nav,
.tag-row,
.period-filters {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.ghost-btn,
.route-chip,
.nav-btn,
.text-btn,
.period-btn {
  border: 1px solid rgba(247, 241, 228, 0.18);
  border-radius: 8px;
  background: rgba(247, 241, 228, 0.06);
  color: var(--paper);
  min-height: 38px;
  padding: 8px 13px;
}

.ghost-btn:hover,
.route-chip:hover,
.nav-btn:hover,
.period-btn:hover,
.period-btn.active {
  border-color: rgba(183, 66, 47, 0.8);
  background: rgba(183, 66, 47, 0.18);
}

.text-btn {
  min-height: 30px;
  padding: 4px 8px;
  color: var(--bronze);
  background: transparent;
}

.quick-routes {
  margin-bottom: 18px;
}

.workspace {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr) 340px;
  gap: 16px;
  align-items: start;
}

.sidebar,
.insights {
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: sticky;
  top: 16px;
  max-height: calc(100vh - 32px);
  overflow: auto;
}

.panel,
.reader {
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: var(--shadow);
}

.panel {
  background: rgba(247, 241, 228, 0.08);
  padding: 14px;
}

.reader {
  background: var(--paper);
  color: var(--ink);
  padding: 32px;
  min-height: 70vh;
}

.compact-panel {
  padding: 12px;
}

.panel-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.panel h2,
.section-title,
.note-section summary {
  margin: 0;
  color: inherit;
  font-size: 15px;
  font-weight: 700;
}

.search-label {
  display: block;
  margin-bottom: 8px;
  color: var(--muted);
  font-size: 12px;
}

.search-input {
  width: 100%;
  border: 1px solid rgba(247, 241, 228, 0.16);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.18);
  color: var(--paper);
  padding: 11px 12px;
  outline: none;
}

.search-input:focus {
  border-color: var(--cinnabar);
}

.directory-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.directory-item {
  width: 100%;
  display: grid;
  grid-template-columns: 38px 1fr;
  gap: 10px;
  text-align: left;
  border: 1px solid rgba(247, 241, 228, 0.12);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.12);
  color: var(--paper);
  padding: 10px;
}

.directory-item.active {
  border-color: var(--cinnabar);
  background: rgba(183, 66, 47, 0.18);
}

.directory-index {
  color: var(--bronze);
  font-family: var(--serif);
}

.directory-title {
  display: block;
  color: var(--paper);
  font-size: 14px;
}

.directory-meta,
.muted {
  color: var(--muted);
  font-size: 12px;
}

.reader-head {
  padding-bottom: 20px;
  border-bottom: 1px solid var(--line);
}

.current-meta {
  margin: 0 0 10px;
  color: var(--bronze);
  font-size: 14px;
}

#currentTitle {
  margin: 0 0 14px;
  color: var(--ink);
  font-family: var(--serif);
  font-size: 32px;
  line-height: 1.25;
}

.tag {
  border-radius: 999px;
  background: rgba(79, 103, 88, 0.12);
  color: var(--green);
  padding: 4px 9px;
  font-size: 12px;
}

.text-section {
  margin-top: 26px;
}

.section-title {
  color: var(--cinnabar);
  margin-bottom: 12px;
}

.classical-text,
.annotation-text,
.baihua-text {
  white-space: pre-line;
  line-height: 2;
}

.classical-text {
  font-family: var(--serif);
  font-size: 19px;
}

.annotation-text,
.baihua-text {
  color: var(--ink-soft);
  font-size: 15px;
}

.note-section {
  border: 0;
  box-shadow: none;
}

.note-section summary {
  color: var(--cinnabar);
  cursor: pointer;
}

.annotated {
  border-bottom: 1px dotted var(--cinnabar);
  color: var(--cinnabar);
}

.annotated ruby {
  ruby-position: over;
}

.annotated rt {
  color: var(--bronze);
  font-size: 0.58em;
}

.quick-summary {
  margin: 0;
  color: var(--paper);
  line-height: 1.8;
}

.glossary-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.glossary-item {
  border-top: 1px solid rgba(247, 241, 228, 0.12);
  padding-top: 10px;
}

.glossary-term {
  color: var(--paper);
  font-weight: 700;
}

.glossary-pinyin {
  color: var(--bronze);
  margin-left: 6px;
}

.glossary-note,
.source-note p {
  color: var(--muted);
  line-height: 1.7;
  margin: 6px 0 0;
  font-size: 13px;
}

.reader-nav {
  justify-content: center;
  margin-top: 18px;
}

.indicator {
  min-width: 120px;
  color: var(--bronze);
  text-align: center;
}

.empty-state {
  color: var(--muted);
  line-height: 1.7;
  padding: 12px 0;
}

@media (max-width: 1180px) {
  .workspace {
    grid-template-columns: 260px minmax(0, 1fr);
  }

  .insights {
    grid-column: 1 / -1;
    position: static;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    max-height: none;
  }
}

@media (max-width: 820px) {
  .app-shell {
    width: min(100vw - 20px, 720px);
    padding-top: 16px;
  }

  .topbar {
    align-items: start;
    flex-direction: column;
  }

  .brand h1 {
    font-size: 28px;
  }

  .workspace {
    grid-template-columns: 1fr;
  }

  .sidebar,
  .insights {
    position: static;
    max-height: none;
  }

  .reader {
    padding: 22px;
  }

  #currentTitle {
    font-size: 25px;
  }

  .classical-text {
    font-size: 17px;
  }

  .insights {
    display: flex;
  }
}
```

- [ ] **Step 2: Verify core selectors exist**

Run:

```powershell
rg -n "workspace|directory-item|annotated|@media \\(max-width: 820px\\)" tuibeitu.html
```

Expected: all selectors exist once or more.

---

### Task 4: Replace Runtime State And Render Functions

**Files:**
- Modify: `E:\推背图浏览器\tuibeitu.html`

- [ ] **Step 1: Add constants and state after `TUI_BEI_DATA`**

Replace the existing code after the data array with:

```js
const DYNASTIES = [
  { name: "总纲", range: [1, 1] },
  { name: "唐", range: [2, 10] },
  { name: "五代", range: [11, 14] },
  { name: "宋", range: [15, 24] },
  { name: "元", range: [25, 26] },
  { name: "明", range: [27, 32] },
  { name: "清", range: [33, 36] },
  { name: "近现代", range: [37, 39] },
  { name: "未来", range: [40, 60] },
];

const STORAGE_KEY = "tuibeitu-reader-state";

let currentIndex = 0;
let currentFilter = "全部";
let searchQuery = "";
```

- [ ] **Step 2: Add safe HTML and preference helpers**

Insert:

```js
function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function readPrefs() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
  } catch {
    return {};
  }
}

function savePrefs() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      lastId: currentIndex + 1,
      filter: currentFilter,
    }));
  } catch {
    // localStorage can be unavailable for local files in some browsers.
  }
}

function getCurrentImage() {
  return TUI_BEI_DATA[currentIndex];
}

function getDynastyForId(id) {
  return DYNASTIES.find(d => id >= d.range[0] && id <= d.range[1]) || DYNASTIES[0];
}
```

- [ ] **Step 3: Add directory filtering helpers**

Insert:

```js
function imageMatchesQuery(image, query) {
  if (!query) return true;
  const needle = query.trim().toLowerCase();
  const haystack = [
    image.id,
    image.ganZhi,
    image.title,
    image.period,
    image.chen,
    image.song,
    image.jinPi,
    image.baiHua,
  ].join(" ").toLowerCase();
  return haystack.includes(needle);
}

function getVisibleImages() {
  return TUI_BEI_DATA.filter(image => {
    const periodOk = currentFilter === "全部" || image.period === currentFilter;
    return periodOk && imageMatchesQuery(image, searchQuery);
  });
}
```

- [ ] **Step 4: Add directory and filter rendering**

Insert:

```js
function renderPeriodFilters() {
  const container = document.getElementById("periodFilters");
  const periods = ["全部", ...DYNASTIES.map(d => d.name)];
  container.innerHTML = periods.map(period => `
    <button class="period-btn${period === currentFilter ? " active" : ""}" type="button" data-period="${escapeHtml(period)}">
      ${escapeHtml(period)}
    </button>
  `).join("");

  container.querySelectorAll(".period-btn").forEach(button => {
    button.addEventListener("click", () => {
      currentFilter = button.dataset.period;
      renderAll();
      savePrefs();
    });
  });
}

function renderDirectory() {
  const images = getVisibleImages();
  document.getElementById("resultCount").textContent = `${images.length} 项`;
  const list = document.getElementById("directoryList");

  if (!images.length) {
    list.innerHTML = `<p class="empty-state">没有找到匹配内容。换个关键词试试。</p>`;
    return;
  }

  list.innerHTML = images.map(image => `
    <button class="directory-item${image.id === currentIndex + 1 ? " active" : ""}" type="button" data-id="${image.id}">
      <span class="directory-index">${image.id}</span>
      <span>
        <span class="directory-title">${escapeHtml(image.title || image.ganZhi)}</span>
        <span class="directory-meta">${escapeHtml(image.ganZhi)} · ${escapeHtml(image.period || getDynastyForId(image.id).name)}</span>
      </span>
    </button>
  `).join("");

  list.querySelectorAll(".directory-item").forEach(button => {
    button.addEventListener("click", () => navigateTo(Number(button.dataset.id) - 1));
  });
}
```

- [ ] **Step 5: Add article and insight rendering without glossary yet**

Insert:

```js
function getQuickSummary(image) {
  const text = image.baiHua || "";
  const cleaned = text.replace(/【[^】]+】/g, "").trim();
  const firstParagraph = cleaned.split(/\n+/).find(Boolean) || "这一象暂无白话摘要。";
  return firstParagraph.length > 120 ? `${firstParagraph.slice(0, 120)}...` : firstParagraph;
}

function renderArticle() {
  const image = getCurrentImage();
  const dynasty = getDynastyForId(image.id);
  document.getElementById("currentMeta").textContent = `第 ${image.id} / 60 象 · ${image.ganZhi}`;
  document.getElementById("currentTitle").textContent = image.title || dynasty.name;
  document.getElementById("currentTags").innerHTML = [
    dynasty.name,
    image.startYear && image.endYear ? `${image.startYear}-${image.endYear}` : "解释性阅读",
  ].map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join("");
  document.getElementById("chenContent").textContent = image.chen || "暂无内容";
  document.getElementById("songContent").textContent = image.song || "暂无内容";
  document.getElementById("jinpiContent").textContent = image.jinPi || "暂无内容";
  document.getElementById("quickSummary").textContent = getQuickSummary(image);
  document.getElementById("baihuaContent").textContent = image.baiHua || "暂无白话解读";
  document.getElementById("indicator").textContent = `第 ${image.id} / 60 象`;
  document.getElementById("prevBtn").disabled = currentIndex === 0;
  document.getElementById("nextBtn").disabled = currentIndex === TUI_BEI_DATA.length - 1;
}

function renderAll() {
  renderPeriodFilters();
  renderDirectory();
  renderArticle();
}
```

- [ ] **Step 6: Add navigation and event binding**

Insert:

```js
function navigateTo(index) {
  if (index < 0 || index >= TUI_BEI_DATA.length) return;
  currentIndex = index;
  window.location.hash = `#${currentIndex + 1}`;
  renderAll();
  savePrefs();
  document.querySelector(".reader").scrollIntoView({ behavior: "smooth", block: "start" });
}

function navigateFromHashOrPrefs() {
  const hashId = Number(window.location.hash.slice(1));
  const prefs = readPrefs();
  const preferredId = Number(prefs.lastId);
  if (hashId >= 1 && hashId <= TUI_BEI_DATA.length) {
    currentIndex = hashId - 1;
  } else if (preferredId >= 1 && preferredId <= TUI_BEI_DATA.length) {
    currentIndex = preferredId - 1;
  }
  if (prefs.filter) currentFilter = prefs.filter;
}

function bindEvents() {
  document.getElementById("searchInput").addEventListener("input", event => {
    searchQuery = event.target.value;
    renderDirectory();
  });
  document.getElementById("clearFilterBtn").addEventListener("click", () => {
    currentFilter = "全部";
    renderAll();
    savePrefs();
  });
  document.getElementById("prevBtn").addEventListener("click", () => navigateTo(currentIndex - 1));
  document.getElementById("nextBtn").addEventListener("click", () => navigateTo(currentIndex + 1));
  document.getElementById("randomBtn").addEventListener("click", randomImage);
  document.getElementById("continueBtn").addEventListener("click", () => {
    const lastId = Number(readPrefs().lastId);
    if (lastId >= 1 && lastId <= TUI_BEI_DATA.length) navigateTo(lastId - 1);
  });
  document.querySelectorAll(".route-chip[data-jump]").forEach(button => {
    button.addEventListener("click", () => navigateTo(Number(button.dataset.jump) - 1));
  });
  document.querySelectorAll(".route-chip[data-period]").forEach(button => {
    button.addEventListener("click", () => {
      currentFilter = button.dataset.period;
      renderAll();
      savePrefs();
    });
  });
  document.addEventListener("keydown", event => {
    if (event.key === "ArrowLeft") navigateTo(currentIndex - 1);
    if (event.key === "ArrowRight") navigateTo(currentIndex + 1);
  });
  window.addEventListener("hashchange", () => {
    const id = Number(window.location.hash.slice(1));
    if (id >= 1 && id <= TUI_BEI_DATA.length && id !== currentIndex + 1) {
      currentIndex = id - 1;
      renderAll();
      savePrefs();
    }
  });
}

function randomImage() {
  if (TUI_BEI_DATA.length <= 1) return;
  let nextIndex = currentIndex;
  while (nextIndex === currentIndex) {
    nextIndex = Math.floor(Math.random() * TUI_BEI_DATA.length);
  }
  navigateTo(nextIndex);
}

document.addEventListener("DOMContentLoaded", () => {
  navigateFromHashOrPrefs();
  bindEvents();
  renderAll();
});
```

- [ ] **Step 7: Static check for old tab runtime removal**

Run:

```powershell
rg -n "currentTab|tabContent|renderTimeline|timeline-node|\\.tab" tuibeitu.html
```

Expected: no matches, because the new reading page no longer uses tab/timeline rendering.

---

### Task 5: Add Glossary, Pinyin Markup, And Current-Image Notes

**Files:**
- Modify: `E:\推背图浏览器\tuibeitu.html`

- [ ] **Step 1: Add `GLOSSARY` after `DYNASTIES`**

Insert:

```js
const GLOSSARY = [
  { term: "白头翁", pinyin: "bai2 tou2 weng1", displayPinyin: "bái tóu wēng", meaning: "白发老人。", note: "常被用作隐喻人物或时代气象的象征。" },
  { term: "乾坤", pinyin: "qian2 kun1", displayPinyin: "qián kūn", meaning: "天地。", note: "在古典语境中也常指天下、局势或阴阳两端。" },
  { term: "干戈", pinyin: "gan1 ge1", displayPinyin: "gān gē", meaning: "兵器。", note: "常借指战争、兵乱。" },
  { term: "金批", pinyin: "jin1 pi1", displayPinyin: "jīn pī", meaning: "金圣叹批注。", note: "本浏览器中指金圣叹对各象的解释文本。" },
  { term: "甲子", pinyin: "jia3 zi3", displayPinyin: "jiǎ zǐ", meaning: "六十甲子的第一位。", note: "也可泛指时间循环的起点。" },
  { term: "癸亥", pinyin: "gui3 hai4", displayPinyin: "guǐ hài", meaning: "六十甲子的最后一位。", note: "与甲子相对，常带有一轮循环结束之意。" },
  { term: "阴阳", pinyin: "yin1 yang2", displayPinyin: "yīn yáng", meaning: "中国古代哲学中的一组基本范畴。", note: "常用来解释消长、转化、循环。" },
  { term: "天数", pinyin: "tian1 shu4", displayPinyin: "tiān shù", meaning: "天命、气数。", note: "古文中常指历史兴衰似乎自有规律。" },
  { term: "谶", pinyin: "chen4", displayPinyin: "chèn", meaning: "预言、隐语。", note: "《推背图》中指带象征意味的短句。" },
  { term: "讖", pinyin: "chen4", displayPinyin: "chèn", meaning: "“谶”的繁体或异体写法。", note: "含义同“谶”。" },
  { term: "颂", pinyin: "song4", displayPinyin: "sòng", meaning: "韵文式说明。", note: "本书中常与“谶曰”互相补充。" },
  { term: "牝", pinyin: "pin4", displayPinyin: "pìn", meaning: "雌性。", note: "古文中常与阴性、柔顺、门户等象征有关。" },
  { term: "阙", pinyin: "que4", displayPinyin: "què", meaning: "宫门、宫阙，也可指缺失。", note: "需结合原句判断具体含义。" },
  { term: "讴", pinyin: "ou1", displayPinyin: "ōu", meaning: "歌唱。", note: "古文中常用于民间歌咏、称颂。" },
  { term: "赤羽", pinyin: "chi4 yu3", displayPinyin: "chì yǔ", meaning: "红色羽毛。", note: "在谶语中可作为颜色与物象的组合暗示。" },
];
```

- [ ] **Step 2: Add glossary matching helpers**

Insert before `renderArticle()`:

```js
function getImageText(image) {
  return [image.ganZhi, image.title, image.chen, image.song, image.jinPi, image.baiHua].join("\n");
}

function getGlossaryForImage(image) {
  const text = getImageText(image);
  return GLOSSARY.filter(item => text.includes(item.term));
}

function renderAnnotatedText(text) {
  const value = String(text || "暂无内容");
  const sorted = [...GLOSSARY].sort((a, b) => b.term.length - a.term.length);
  let html = escapeHtml(value);

  sorted.forEach(item => {
    const escapedTerm = escapeHtml(item.term);
    const markup = `<span class="annotated" title="${escapeHtml(item.meaning)}"><ruby>${escapedTerm}<rt>${escapeHtml(item.displayPinyin)}</rt></ruby></span>`;
    html = html.split(escapedTerm).join(markup);
  });

  return html;
}
```

- [ ] **Step 3: Update `imageMatchesQuery()` to include glossary terms**

Replace its `haystack` construction with:

```js
const glossaryTerms = GLOSSARY
  .filter(item => getImageText(image).includes(item.term))
  .map(item => `${item.term} ${item.displayPinyin} ${item.meaning}`)
  .join(" ");
const haystack = [
  image.id,
  image.ganZhi,
  image.title,
  image.period,
  image.chen,
  image.song,
  image.jinPi,
  image.baiHua,
  glossaryTerms,
].join(" ").toLowerCase();
```

- [ ] **Step 4: Update `renderArticle()` to use annotated HTML**

Replace the three text assignments:

```js
document.getElementById("chenContent").textContent = image.chen || "暂无内容";
document.getElementById("songContent").textContent = image.song || "暂无内容";
document.getElementById("jinpiContent").textContent = image.jinPi || "暂无内容";
```

With:

```js
document.getElementById("chenContent").innerHTML = renderAnnotatedText(image.chen);
document.getElementById("songContent").innerHTML = renderAnnotatedText(image.song);
document.getElementById("jinpiContent").innerHTML = renderAnnotatedText(image.jinPi);
```

- [ ] **Step 5: Add glossary list rendering**

Insert:

```js
function renderGlossary() {
  const image = getCurrentImage();
  const items = getGlossaryForImage(image);
  const container = document.getElementById("glossaryList");

  if (!items.length) {
    container.innerHTML = `<p class="empty-state">这一象暂无重点字词注解。</p>`;
    return;
  }

  container.innerHTML = items.map(item => `
    <div class="glossary-item" id="glossary-${encodeURIComponent(item.term)}">
      <div>
        <span class="glossary-term">${escapeHtml(item.term)}</span>
        <span class="glossary-pinyin">${escapeHtml(item.displayPinyin)}</span>
      </div>
      <p class="glossary-note">${escapeHtml(item.meaning)}${item.note ? ` ${escapeHtml(item.note)}` : ""}</p>
    </div>
  `).join("");
}
```

- [ ] **Step 6: Call glossary rendering from `renderAll()`**

Replace:

```js
function renderAll() {
  renderPeriodFilters();
  renderDirectory();
  renderArticle();
}
```

With:

```js
function renderAll() {
  renderPeriodFilters();
  renderDirectory();
  renderArticle();
  renderGlossary();
}
```

- [ ] **Step 7: Bind the glossary route**

In `bindEvents()`, add:

```js
document.getElementById("glossaryRoute").addEventListener("click", () => {
  document.getElementById("glossaryList").scrollIntoView({ behavior: "smooth", block: "start" });
});
```

- [ ] **Step 8: Verify annotation anchors exist**

Run:

```powershell
rg -n "const GLOSSARY|renderAnnotatedText|getGlossaryForImage|renderGlossary|glossaryRoute" tuibeitu.html
```

Expected: all functions and constants exist.

---

### Task 6: Verification, Polish, And Commit

**Files:**
- Modify: `E:\推背图浏览器\tuibeitu.html`

- [ ] **Step 1: Run static smoke checks**

Run:

```powershell
rg -n "推背图浏览器|searchInput|periodFilters|directoryList|renderAll|GLOSSARY|localStorage|randomImage" tuibeitu.html
```

Expected: all anchors exist.

- [ ] **Step 2: Check that the old UI anchors are gone**

Run:

```powershell
rg -n "id=\"timeline\"|id=\"tabContent\"|class=\"tabs\"|currentTab|renderTimeline" tuibeitu.html
```

Expected: no matches.

- [ ] **Step 3: Open `tuibeitu.html` in a browser**

Run by double-clicking the file or opening:

```text
E:\推背图浏览器\tuibeitu.html
```

Expected: a three-column reading workspace appears on desktop.

- [ ] **Step 4: Verify direct hash routing**

Open:

```text
E:\推背图浏览器\tuibeitu.html#39
```

Expected: page shows 第 39 / 60 象, directory item 39 is active, previous/next buttons are enabled.

- [ ] **Step 5: Verify search**

In the search box, type:

```text
唐
```

Expected: directory narrows to Tang-related entries.

Then type:

```text
谶
```

Expected: directory still shows entries because original text and glossary include the term.

- [ ] **Step 6: Verify filters and routes**

Click:

```text
近现代三象
```

Expected: directory shows 近现代 entries only.

Click:

```text
全部
```

Expected: directory returns to all 60 entries.

Click:

```text
随机一象
```

Expected: current image changes and URL hash updates.

- [ ] **Step 7: Verify annotation behavior**

Find a visible annotated term such as:

```text
谶
```

Expected: term displays pinyin above the character and hover title shows the short meaning. The right-side 字词注解 panel lists matching terms for the current image.

- [ ] **Step 8: Verify keyboard navigation**

Press:

```text
ArrowRight
ArrowLeft
```

Expected: page moves to next and previous image, and URL hash updates.

- [ ] **Step 9: Verify mobile layout**

Resize browser width below 820px.

Expected: workspace becomes one column; sidebar, reader and insights stack without horizontal scrolling.

- [ ] **Step 10: Check git diff**

Run:

```powershell
git diff -- tuibeitu.html
```

Expected: diff only changes the application shell, styles and runtime logic in `tuibeitu.html`; embedded data values are not unintentionally rewritten.

- [ ] **Step 11: Commit implementation**

Run:

```powershell
git add tuibeitu.html
git commit -m "feat: redesign tuibeitu reading workspace"
```

Expected: commit succeeds.
