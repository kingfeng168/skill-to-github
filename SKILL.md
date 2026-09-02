---
name: skill-to-github
agent_created: true
description: "把本地技能（skill）或项目开源上传到 GitHub 的完整工作流。当用户要求把某个技能/项目开源、上传到 GitHub、发布到 GitHub、开源上传、推到公开仓库、打包分发时使用。覆盖脱敏（剔除密钥/缓存/个人路径）→ 补写 README/LICENSE/.gitignore → 官方打包 zip → git 初始化提交 → GitHub 建公开仓库 + 推送 + Release 上传 zip 全链路。适用于需要反复开源多个技能或项目的场景。"
---

# skill-to-github — 开源上传到 GitHub

把 `~/.workbuddy/skills/<name>/` 下的自建技能（或任意本地项目目录），脱敏后发布为 GitHub 公开仓库 + Release（含 zip 安装包）。

## 关键事实

- WorkBuddy 官方技能市场（BuiltinMarket）当前接口仅支持「搜索 + 安装」，**无 publish 入口**。真正可控的开源 = GitHub 公开仓库 + zip 分发。
- 技能标准目录：`SKILL.md`（必需）+ `scripts/` + `references/` + `assets/`。
- 密钥安全规范：真实 API key 一律不落盘、不写进源码，只经 `--api-key` / 环境变量 / 本地 `.eia_key` 读取。
- 打包脚本（仅技能需要）：`<workbuddy-install>/resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/skill-creator/scripts/package_skill.py`。

## 前置条件

1. 本地已装 git（`git --version`）。
2. 用户提供 GitHub 账号与 PAT token：引导其打开 `https://github.com/settings/tokens/new`，Note 填 `workbuddy`，Expiration 选 `7 days`，Scopes 勾选 `repo`，生成后复制 `ghp_` 开头令牌。
3. 输出目录统一放 `./release/`（用户约定，不写 C 盘）。

## 工作流

### 1. 脱敏：生成干净副本

用 Python `shutil.copytree` 复制到发布目录，`ignore` 排除 `.eia_key`、`__pycache__`、`.git`、`*.zip`；随后遍历文本文件替换个人路径（如 `C:\Users\<you>\Desktop\output\` → `./output/`），并把个人化措辞通用化。二进制模式读写以保留原换行符。模板见 `references/sanitize_snippet.py`。

脱敏后必须验证：
- `grep -rn "<你的用户名>\|<你的个人目录>\|.eia_key" <发布目录>` 应无残留（「如何配置自己的 key」类说明文字除外）。
- 确认 `.eia_key`、`__pycache__`、`.git`、`*.zip` 均已排除。

### 2. 补写文档

- `README.md`：一句话定位 + 模块/功能清单 + 目录结构 + 安装方法（复制到 `~/.workbuddy/skills/`）+ 依赖说明 + 密钥配置 + 免责声明 + License 链接。
- `LICENSE`：MIT 最通用，版权行写作者名。
- `.gitignore`：`__pycache__/`、`*.pyc`、`.eia_key`、`*.zip`、`.DS_Store`。

### 3. 打包 zip（仅技能需要）

```bash
python package_skill.py "<发布目录>/<name>" "<输出目录>"
```

脚本先自动校验（frontmatter、命名、结构、description 质量），通过后生成 `<name>.zip`。

### 4. git 初始化 + 提交

```bash
cd "<发布目录>/<name>" && git init && git branch -M main
git config user.name "作者名"
git config user.email "<id>+<login>@users.noreply.github.com"   # 用 noreply 邮箱保护真实邮箱
git add -A && git commit -m "Initial commit: <name>"
```

### 5. GitHub 建仓库 + 推送 + Release

用 token 调 GitHub REST API：

- 取用户名：`GET https://api.github.com/user`（`Authorization: token <TOKEN>`）
- 建仓库：`POST https://api.github.com/user/repos`，body `{"name":"<name>","description":"...","public":true}`
- 推送：`git push https://x-access-token:<TOKEN>@github.com/<owner>/<name>.git main`
- 建 Release + 传 zip：`POST /repos/<owner>/<repo>/releases` 得 `id`，再 `POST https://uploads.github.com/repos/<owner>/<repo>/releases/<id>/assets?name=<name>.zip`（`Content-Type: application/zip`，body 为 zip 二进制）。

用 Python `urllib` 脚本一次完成 Release 创建 + 资产上传（可靠处理二进制与中文路径）。模板见 `references/release_snippet.py`。

## 安全要点

- token 用完即提醒用户到 GitHub 页面 Delete；脚本里硬编码的 token 用后立即替换为占位符。
- 推送用带 token 的临时 URL，`origin` 保持干净 URL，`git config` 不残留 token/password。
- 提交作者用 GitHub noreply 邮箱，避免公开真实邮箱。

## 收尾

- 给用户：公开仓库链接 + Release 链接 + zip 下载链接。
- 其余自建技能/项目可复用本流程逐个开源。
