# 变更日志（CHANGELOG）

> **文档类型：** 版本变更日志
>
> **版本：** v1.0.0
>
> **日期：** YYYY-MM-DD
>
> **维护人：** [项目 Owner / Release Manager]
>
> **规范遵循：** [Keep a Changelog 1.1.0](https://keepachangelog.com/zh-CN/1.1.0/)
>
> **语义化版本：** [Semantic Versioning 2.0.0](https://semver.org/lang/zh-CN/)

本项目所有重要变更均会记录在本文件中。

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## 变更类型说明

| 类型         | 英文        | 说明                                                  |
| :----------- | :---------- | :---------------------------------------------------- |
| **新增**     | Added       | 新增的功能                                            |
| **变更**     | Changed     | 对已有功能的变更                                       |
| **弃用**     | Deprecated  | 即将移除的功能                                         |
| **移除**     | Removed     | 本版本已移除的功能                                     |
| **修复**     | Fixed       | Bug 修复                                              |
| **安全**     | Security    | 安全相关修复（含漏洞、CVE）                           |

## 版本号规则（SemVer）

```
MAJOR.MINOR.PATCH
```

| 版本位    | 何时升                                                                | 示例                |
| :-------- | :-------------------------------------------------------------------- | :------------------ |
| `MAJOR`   | 不兼容的 API 变更                                                     | `1.0.0` → `2.0.0`   |
| `MINOR`   | 向后兼容的功能新增                                                    | `1.0.0` → `1.1.0`   |
| `PATCH`   | 向后兼容的 Bug 修复                                                   | `1.0.0` → `1.0.1`   |

预发布版本：`-alpha` / `-beta` / `-rc.N`，如 `1.0.0-beta.2`。

---

## [Unreleased]

> 本版本尚未发布，记录自上次发布以来的所有变更。发布时将本节提升为正式版本号。

### 新增（Added）

- 新增 {特性描述}，详见 {PR/Issue 链接}
- 新增 {配置项}，默认值 {value}

### 变更（Changed）

- 变更 {行为描述}：从 {旧} 改为 {新}，迁移说明见 {文档链接}
- 性能优化：{指标} 提升 {X}%

### 弃用（Deprecated）

- 弃用 {API/功能}，将在 {版本} 移除，替代方案：{说明}

### 移除（Removed）

- 移除 {API/功能}（自 {版本} 起弃用）

### 修复（Fixed）

- 修复 {Bug 描述}，影响范围 {说明}， Fixes #{issue}

### 安全（Security）

- 修复 {CVE 编号}：{漏洞描述}，CVSS {评分}，升级建议见 {公告链接}

---

## [1.0.0] - YYYY-MM-DD

### 新增（Added）

- 首次正式发布
- 核心功能：{特性 1}
- 核心功能：{特性 2}
- 核心功能：{特性 3}
- 完整文档：README / CONTRIBUTING / FAQ
- CI/CD 流水线（GitHub Actions）
- 覆盖率门禁 ≥ 80%

### 变更（Changed）

- N/A（首次发布）

### 弃用（Deprecated）

- N/A（首次发布）

### 移除（Removed）

- N/A（首次发布）

### 修复（Fixed）

- N/A（首次发布）

### 安全（Security）

- 启用依赖扫描（Dependabot / npm audit / cargo-audit）
- 启用 CodeQL 静态分析

---

## [0.9.0] - YYYY-MM-DD

### 新增（Added）

- Beta 版本发布
- 核心 API 接口稳定

### 变更（Changed）

- {API 名} 签名调整：参数 {old} → {new}

### 修复（Fixed）

- 修复 {bug} 导致的 {现象}

---

## [0.5.0] - YYYY-MM-DD

### 新增（Added）

- Alpha 版本，仅限内部测试

---

## 版本链接

> 维护版本号到 git tag / GitHub Release 的链接。

[Unreleased]: https://github.com/{org}/{repo}/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/{org}/{repo}/releases/tag/v1.0.0
[0.9.0]: https://github.com/{org}/{repo}/releases/tag/v0.9.0
[0.5.0]: https://github.com/{org}/{repo}/releases/tag/v0.5.0

---

## 📌 CHANGELOG 撰写 Checklist

- [ ] 遵循 Keep a Changelog 1.1.0 格式（六大类：Added/Changed/Deprecated/Removed/Fixed/Security）
- [ ] 遵循 Semantic Versioning 2.0.0 版本号规则
- [ ] [Unreleased] 节在最前，发布时提升为正式版本号
- [ ] 每个版本有明确的发布日期（YYYY-MM-DD）
- [ ] 每条变更含 PR / Issue 链接（如适用）
- [ ] Breaking Change 显式标注（如 `**BREAKING**:` 前缀）
- [ ] 安全修复单独归类，标注 CVE 编号与 CVSS 评分
- [ ] 版本链接区维护版本号 → git tag 的 compare 链接
- [ ] 弃用项标注移除版本号与替代方案
- [ ] 不记录无关紧要的内部重构 / 文案修改
