# {项目名}（{英文名}）

> **文档类型：** 项目入口文档（README）
>
> **文档状态：** 🟢 活跃 / 🟡 评审中 / 🔴 已归档
>
> **保密级别：** 机密 / 内部公开 / 公开
>
> **版本：** vX.X.X
>
> **日期：** YYYY-MM-DD
>
> **维护人：** [项目 Owner / 团队]
>
> **关联文档：** [CHANGELOG.md](./CHANGELOG.md) / [CONTRIBUTING.md](./CONTRIBUTING.md) / [LICENSE](./LICENSE)

[![GitHub Release](https://img.shields.io/github/v/release/{org}/{repo}?style=flat-square)](https://github.com/{org}/{repo}/releases)
[![GitHub License](https://img.shields.io/github/license/{org}/{repo}?style=flat-square)](LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/{org}/{repo}/ci.yml?branch=main&style=flat-square)](https://github.com/{org}/{repo}/actions)
[![Coverage](https://img.shields.io/codecov/c/github/{org}/{repo}?style=flat-square)](https://codecov.io/gh/{org}/{repo})

{一句话项目定位，如：「面向 AI agent 的工业级项目初始化 skill，把一个空目录变成带完整质量护栏的生产级项目。」}

## 功能特性

- **特性 1**：[一句话说明，如：覆盖 9 种语言一键初始化]
- **特性 2**：[一句话说明，如：CI 质量门禁 + tag 触发 Release 工作流]
- **特性 3**：[一句话说明，如：本地 pre-commit/lefthook 双重工业级检查]
- **特性 4**：[一句话说明，如：覆盖率门禁行业底线 80%]

> 完整能力矩阵见 [§ 能力概览](#能力概览)。

## 安装

### 前置依赖

| 依赖       | 最低版本 | 说明                         |
| :--------- | :------- | :--------------------------- |
| {Node.js}  | 18+      | 运行环境                     |
| {git}      | 2.30+    | 版本控制                     |
| {其他}     | {版本}   | {说明}                       |

### 方式一：通过包管理器安装（推荐）

```bash
# npm
npm install {package-name}

# pnpm
pnpm add {package-name}

# uv (Python)
uv add {package-name}

# cargo (Rust)
cargo add {crate-name}
```

### 方式二：从源码构建

```bash
git clone https://github.com/{org}/{repo}.git
cd {repo}
{build-command}
```

### 方式三：直接下载二进制

```bash
# 从 GitHub Releases 下载对应平台二进制
curl -L https://github.com/{org}/{repo}/releases/latest/download/{binary}-{os}-{arch}.tar.gz | tar xz
```

## 快速开始

```bash
# 1. 进入目标目录
cd /path/to/project

# 2. 初始化
{init-command}

# 3. 验证
{verify-command}
```

**预期输出：**

```
{预期输出示例}
```

## 使用示例

```bash
# 示例 1：基础用法
{command-1}

# 示例 2：带参数
{command-2} --option value

# 示例 3：进阶用法
{command-3}
```

更多示例见 [`docs/examples/`](./docs/examples/)。

## 配置

### 配置文件

主配置文件位于 `{config-path}`，关键字段：

| 字段             | 类型    | 默认值    | 说明                          |
| :--------------- | :------ | :-------- | :---------------------------- |
| `{field_1}`      | string  | `default` | {说明}                        |
| `{field_2}`      | integer | `80`      | {说明}                        |
| `{field_3}`      | boolean | `false`   | {说明}                        |
| `{field_env}`    | string  | —         | 优先从环境变量 `{ENV_VAR}` 读取 |

### 环境变量

| 变量名           | 必填 | 默认值 | 说明                          |
| :--------------- | :--: | :----- | :---------------------------- |
| `{ENV_API_KEY}`  |  ✅  | —      | API 密钥                       |
| `{ENV_LOG_LEVEL}`|  —   | `info` | 日志级别                       |
| `{ENV_TIMEOUT}`  |  —   | `30`   | 请求超时（秒）                 |

> **安全提醒**：密钥、Token 等敏感信息禁止硬编码到配置文件，必须通过环境变量或 KMS 注入。

## 能力概览

### `references/` —— 参考文档

| 文件 | 内容 | 何时读 |
| ---- | ---- | ------ |
| [`references/{file}.md`](references/{file}.md) | {说明} | {时机} |

### `scripts/` —— 工具脚本

| 脚本 | 用途 |
| ---- | ---- |
| `scripts/{script-1}.sh` | {说明} |
| `scripts/{script-2}.sh` | {说明} |

### `templates/` —— 模板

```
templates/
├── {category-1}/   # {说明}
└── {category-2}/   # {说明}
```

## 完整流程链路

```mermaid
flowchart LR
    A["意图确认"] --> B["初始化"]
    B --> C["配置"]
    C --> D["本地验证"]
    D --> E["CI 门禁"]
```

1. **阶段 0 · 意图确认**：{说明}
2. **阶段 1 · 初始化**：{说明}
3. **阶段 2 · 配置**：{说明}
4. **阶段 3 · CI 门禁**：{说明}
5. **🛑 阶段 4 · 验证（STOP）**：{说明}

## 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解：

- Fork / Branch / PR 规范
- 代码风格与测试要求
- Commit message 规范
- 行为准则

### 贡献者

感谢所有贡献者：

[![Contributors](https://img.shields.io/github/contributors/{org}/{repo}?style=flat-square)](https://github.com/{org}/{repo}/graphs/contributors)

## 路线图

- [x] {已完成特性 1}
- [x] {已完成特性 2}
- [ ] {计划特性 1}
- [ ] {计划特性 2}

详见 [Roadmap](./docs/ROADMAP.md)。

## 常见问题

常见问题请见 [FAQ.md](./FAQ.md)。如未找到答案，请 [提交 Issue](https://github.com/{org}/{repo}/issues/new)。

## 变更日志

详见 [CHANGELOG.md](./CHANGELOG.md)。

## 许可证

[MIT](./LICENSE) © {年份} {作者/组织}

## 致谢

- {依赖项目 1} —— {说明}
- {依赖项目 2} —— {说明}
- {灵感来源}

## 联系方式

- **Issue**：[提交 Issue](https://github.com/{org}/{repo}/issues)
- **讨论**：[GitHub Discussions](https://github.com/{org}/{repo}/discussions)
- **邮件**：{email}
- **Slack/Discord**：{邀请链接}

---

## 📌 README 撰写 Checklist

- [ ] 标题 + 一句话定位
- [ ] 徽章（Release / License / Build / Coverage）
- [ ] 功能特性（≥ 4 条）
- [ ] 安装（≥ 2 种方式，含前置依赖）
- [ ] 快速开始（含预期输出）
- [ ] 使用示例（≥ 3 个，覆盖基础到进阶）
- [ ] 配置（配置文件 + 环境变量表）
- [ ] 能力概览（目录结构说明）
- [ ] 完整流程链路（含验证 STOP 点）
- [ ] 贡献链接 + 贡献者徽章
- [ ] 路线图
- [ ] FAQ / CHANGELOG / LICENSE 链接完整
- [ ] 许可证 + 致谢 + 联系方式
