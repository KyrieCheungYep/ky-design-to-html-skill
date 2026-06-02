# KY Design to HTML Skill

一个适用于 Codex / Claude 的 UI 设计稿转 HTML/CSS skill。

它适合用在这类场景：

- 给 AI 一张 UI 截图，让它还原成 HTML/CSS
- 把 landing page 设计稿做成静态网页
- 把 SaaS 页面、后台页面、空状态页面还原成前端页面
- 避免 AI 直接照图写 HTML 后，把页面挤变形、资产画糊、比例跑偏

## 这个 skill 解决什么问题？

很多人会直接对 AI 说：

```text
根据这张图生成 HTML
```

但这样容易翻车。

因为 AI 被迫同时做三件事：

- 理解页面结构
- 复刻视觉样式
- 临时画出复杂视觉资产

这个 skill 会让 AI 先把任务拆开：

- 哪些部分应该用 HTML/CSS 写
- 哪些部分应该当作图片资产
- 页面应该按什么画布比例展示
- 写完后应该截图验证哪里不像

核心流程是：

1. 先拆解页面地图
2. 分离代码结构和视觉资产
3. 设置设计稿画布和浏览器展示比例
4. 写 HTML/CSS
5. 浏览器截图验证
6. 对比修正视觉误差

## 安装方法

### Codex

把 `ky-design-to-html` 文件夹复制到：

```bash
~/.codex/skills/ky-design-to-html
```

### Claude

把 `ky-design-to-html` 文件夹复制到：

```bash
~/.claude/skills/ky-design-to-html
```

## 使用方法

在 Codex 或 Claude 里，可以这样说：

```text
Use $ky-design-to-html to recreate this UI screenshot as a standalone HTML/CSS page.
```

也可以直接用中文：

```text
使用 ky-design-to-html，把这张 UI 截图还原成一个 HTML/CSS 页面。
```

## 文件结构

```text
ky-design-to-html/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── asset-handling.md
│   └── visual-error-taxonomy.md
└── scripts/
    └── screenshot_page.py
```

## 备注

这个 skill 的目标不是让 AI 一次生成完美页面。

它的目标是让 AI 按正确流程工作：

```text
拆解 → 分离资产 → 设置画布 → 写代码 → 截图 → 对比 → 修正
```

真正的还原质量来自后面的截图校准。
