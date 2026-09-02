# skill-to-github

把本地技能（skill）或项目开源上传到 GitHub 的完整工作流，一个 WorkBuddy 技能。

## 定位

当你想把自建技能、脚本或任意本地项目目录，脱敏后发布为 GitHub 公开仓库 + Release（含 zip 安装包）时，用这个技能一键跑通全链路：

**脱敏 → 补文档 → 打包 → git → GitHub 建仓/推送/Release**

## 覆盖的完整流程

| 步骤 | 做什么 |
|---|---|
| ① 脱敏 | `copytree` 排除 `.eia_key` / `__pycache__` / `.git` / `*.zip`，替换个人路径为通用占位符 |
| ② 补文档 | 生成 `README.md`、`LICENSE`（MIT）、`.gitignore` |
| ③ 打包 | 用官方 `package_skill.py` 校验并生成 `<name>.zip` |
| ④ git | `init` + `main` 分支 + 提交（noreply 邮箱保护真实邮箱） |
| ⑤ GitHub | 建公开仓库 → 推送 → Release 上传 zip |

## 目录结构

```
skill-to-github/
├── SKILL.md                          # 技能主文件（本工作流说明）
└── references/
    ├── sanitize_snippet.py           # 脱敏脚本模板
    └── release_snippet.py            # Release 创建 + zip 上传脚本模板
```

## 安装

1. 下载本仓库（或 Release 里的 `skill-to-github.zip`）。
2. 解压后把整个 `skill-to-github/` 目录复制到你的技能目录：

   - Windows：`C:\Users\<you>\.workbuddy\skills\`
   - macOS / Linux：`~/.workbuddy/skills/`

3. 之后对 WorkBuddy 说「把 XX 技能开源上传到 GitHub」即可触发。

## 依赖

- 仅 Python 标准库（`urllib` / `shutil` / `json`），零第三方依赖。
- 本地需安装 git。
- 需要 GitHub 账号及一个 PAT token（`repo` 权限）。

## 密钥与安全

- 真实 API key 一律不落盘、不写进源码。
- token 用完即撤销（GitHub Settings → Tokens）。
- 提交作者用 GitHub noreply 邮箱，避免公开真实邮箱。

## 免责声明

本项目仅用于技能/项目分发，不构成任何金融、投资建议。使用者需自行确认所发布内容不包含个人敏感信息与凭证。

## License

[MIT](./LICENSE)
