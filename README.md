# 推背图浏览器

《推背图》六十象全文浏览器 —— 原文与白话解读并排展示，配朝代时间线导航。

## 使用方式

1. 双击 `tuibeitu.html` 直接打开，或用浏览器访问
2. 点击顶部朝代时间线可快速跳转到任一朝代
3. 键盘 ← → 翻页，点击按钮翻页
4. 通过 URL hash 可直达指定象（如 `tuibeitu.html#39`）

## 技术说明

- 纯 HTML/CSS/JS 单文件，零外部依赖
- 数据内联，无需服务器即可运行
- 响应式设计，适配手机端

## 数据来源

据金圣叹批注版《推背图》整理，白话解读由 AI 辅助生成，仅供参考。

## 部署

扔到任何静态文件托管即可：
- GitHub Pages
- Vercel / Netlify
- 任意 HTTP 服务器

## 项目结构

```
├── tuibeitu.html          -- 主文件（数据 + 样式 + 逻辑）
├── scripts/               -- 数据提取与处理脚本
│   ├── extract_data.py
│   ├── add_meta.py
│   ├── to_js.py
│   └── merge.py
├── data_raw.json          -- 六十象结构化数据（中间产物）
├── docs/
│   └── superpowers/
│       ├── specs/         -- 设计文档
│       └── plans/         -- 实施计划
└── README.md
```
