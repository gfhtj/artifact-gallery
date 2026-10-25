# artifact-gallery · 交付物版本画廊

一个 WorkBuddy 技能：像 NoCode / PPT 侧边缩略图一样，管理 AI 对话产出的交付物**版本时间线**。

## 它解决什么问题

AI 对话里反复改写同一份交付物（简历、报告、网页）时，旧版本会被直接覆盖、无处可寻。
本技能把每次改动登记为快照，形成可回溯的版本画廊：

- **左栏**：全部产物列表（同一文件跨对话自动累积版本）
- **中栏**：放大预览选中版本（HTML 实时渲染）
- **右栏**：PPT 式版本缩略图，**最新版本固定在最底部**
- **点旧版本** → 仅放大预览，不改动任何文件
- **点"回撤到此版本"** → 显式恢复（旧版本永不丢失，回撤本身也记为新版本）

## 安装（WorkBuddy）

方式一：导入 zip
1. 把 `artifact-gallery/` 打包成 zip（或直接用 Release 里的 `artifact-gallery.zip`）
2. WorkBuddy → 技能管理 → 导入技能 → 上传该 zip
3. 要求：zip 内含 `SKILL.md`，且 SKILL.md frontmatter 有 `name` 与 `description`（本仓库已满足）

方式二：手动放置
1. 把 `artifact-gallery/` 整个文件夹拷到 `~/.workbuddy/skills/artifact-gallery/`
2. 重启 WorkBuddy 会话

## 使用

对 agent 说：

- 「把 \<文件\> 登记一个版本」→ `scripts/register_version.py <file> "<说明>"`
- 「打开版本画廊」→ 两种查看方式：
  - **离线单文件（推荐）**：`py scripts/build_gallery.py <输出路径.html>`，生成自包含 HTML（所有版本已内联），任意浏览器可开，无需服务器
  - **在线画廊（支持一键回撤写文件）**：`py scripts/gallery_server.py [端口]`（默认 8731），打开 `http://localhost:8731`

## 依赖

- 仅 Python 3 标准库，**无需 pip 安装任何包**
- 版本数据默认存 `<工作区>/.workbuddy/artifacts/`（`manifest.json` + 快照目录），可用环境变量 `ART_ROOT` 重定向

## 目录结构

```
artifact-gallery/
├── SKILL.md                     # 技能说明（含 name/description frontmatter）
├── scripts/
│   ├── register_version.py      # 版本登记：快照 + manifest 写入 + 版本递增
│   ├── build_gallery.py         # 生成离线单文件画廊（内联全部版本）
│   ├── gallery_server.py        # 本地画廊服务（支持回撤写文件）
│   ├── seed_existing.py         # 批量导入已有交付物为 v1
│   └── make_demo_multiversion.py# 单产物多版本演示
└── assets/
    ├── gallery.html             # 在线画廊页面模板
    └── gallery_standalone.html  # 离线画廊模板（含 __DATA__ 占位）
```

## License

MIT
