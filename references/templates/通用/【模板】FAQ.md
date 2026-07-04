# {项目名} - 常见问题解答（FAQ）

> **文档状态：** 🟢 已生效 / 🟡 评审中 / 🔴 已归档
>
> **保密级别：** 内部公开 / 公开
>
> **版本：** v1.0.0
>
> **日期：** YYYY-MM-DD
>
> **维护人：** [项目 Owner / 文档负责人]
>
> **阅读对象：** 用户、开发者、运维、第三方接入方
>
> **更新频率：** 每月评审，新问题 48 小时内补充
>
> **关联文档：** [README.md](./README.md) / [CHANGELOG.md](./CHANGELOG.md) / [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 0. 文档导读

### 0.1 文档目的与适用范围

本文件汇集 {项目名} 使用过程中高频出现的问题与解答，按主题分类，便于自助排查。

**适用场景：**

- ✅ 安装、配置、使用过程中的常见障碍
- ✅ 错误信息解读与排查思路
- ✅ 概念澄清与最佳实践
- ❌ 个性化问题（请提 Issue）
- ❌ 安全漏洞上报（请走安全公告流程，勿公开提交）

### 0.2 提问指南

如果本文件未解决问题，请按以下格式提交 Issue：

```
- 环境：[OS / 语言版本 / 项目版本]
- 复现步骤：[1. ... 2. ... 3. ...]
- 预期行为：[...]
- 实际行为：[...]
- 错误日志：[完整堆栈，敏感信息脱敏]
```

### 0.3 变更记录

| 版本 | 日期       | 修订人 | 变更内容                       | 审核人   |
| :--- | :--------- | :----- | :----------------------------- | :------- |
| v0.1 | YYYY-MM-DD | [姓名] | 初稿：安装 + 使用问题           | [姓名]   |
| v0.2 | YYYY-MM-DD | [姓名] | 补充配置 + 错误排查             | [姓名]   |
| v1.0 | YYYY-MM-DD | [姓名] | 正式发布                         | [Owner]  |

---

## 1. 通用问题（General）

### Q1.1 {项目名} 是什么？

{一段话简短说明，引用 README 第一段。}

详见 [README - 功能特性](./README.md#功能特性)。

### Q1.2 {项目名} 适合哪些场景？

- ✅ {场景 1}
- ✅ {场景 2}
- ❌ {不适用场景 1}
- ❌ {不适用场景 2}

### Q1.3 {项目名} 与 {竞品/同类项目} 有什么区别？

| 维度        | {项目名}   | {竞品 A}   | {竞品 B}   |
| :---------- | :--------- | :--------- | :--------- |
| 定位        | {说明}     | {说明}     | {说明}     |
| 语言支持    | {说明}     | {说明}     | {说明}     |
| 性能        | {说明}     | {说明}     | {说明}     |
| 学习成本    | {说明}     | {说明}     | {说明}     |

### Q1.4 {项目名} 的稳定版本是哪个？

当前稳定版本：`v{X.Y.Z}`（[Release Notes](https://github.com/{org}/{repo}/releases)）。

版本策略遵循 [SemVer 2.0.0](https://semver.org/lang/zh-CN/)：

- `MAJOR`：不兼容的 API 变更
- `MINOR`：向后兼容的功能新增
- `PATCH`：向后兼容的 Bug 修复

### Q1.5 如何获取最新版本通知？

- Watch GitHub 仓库的 Releases
- 订阅 {邮件列表 / RSS}
- 关注 {官方博客 / 公众号}

---

## 2. 安装问题（Installation）

### Q2.1 安装时报错 `permission denied` 或 `EACCES`

**现象：**

```bash
npm install {package-name}
# npm ERR! code EACCES
# npm ERR! permission denied
```

**原因：** 全局安装时缺少权限。

**解决方案：**

```bash
# 方案 1：使用 nvm 管理 Node.js（推荐）
nvm install 18
nvm use 18

# 方案 2：修改 npm 默认目录
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 方案 3：使用 sudo（不推荐，可能导致权限混乱）
sudo npm install -g {package-name}
```

### Q2.2 安装时报错 `{dependency} not found` 或 `version mismatch`

**现象：** 依赖版本不满足。

**排查步骤：**

```bash
# 1. 检查当前环境
node --version    # 需 ≥ 18
npm --version
{other-dep} --version

# 2. 清理缓存重装
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# 3. 检查 lockfile 一致性
npm ls {dependency}
```

### Q2.3 在 {OS} 上无法安装 / 运行

**支持平台：**

| 平台       | 架构        | 支持状态        |
| :--------- | :---------- | :-------------- |
| Linux      | x86_64      | ✅ 完全支持     |
| Linux      | arm64       | ✅ 支持         |
| macOS      | x86_64      | ✅ 完全支持     |
| macOS      | arm64 (M1+) | ✅ 支持         |
| Windows    | x86_64      | ⚠️ 实验性支持  |
| Windows    | arm64       | ❌ 暂不支持     |

**Windows 用户建议：** 使用 WSL2 + Linux 子系统。

### Q2.4 安装后命令找不到（`command not found`）

**原因：** 可执行文件路径未加入 `PATH`。

**解决方案：**

```bash
# 检查安装位置
npm bin -g    # npm 全局安装位置
which {command}

# 添加到 PATH
echo 'export PATH="$(npm bin -g):$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Q2.5 企业内网 / 离线环境如何安装？

```bash
# 1. 在外网机器下载 tarball
npm pack {package-name}

# 2. 拷贝到内网机器安装
npm install -g {package-name}-{version}.tgz

# 3. 配置内网镜像（如有）
npm config set registry https://{internal-registry}/
```

---

## 3. 使用问题（Usage）

### Q3.1 如何 {基础操作}？

```bash
{command} --option value
```

**参数说明：**

| 参数        | 说明                  | 默认值    |
| :---------- | :-------------------- | :-------- |
| `--option`  | {说明}                | `default` |
| `--verbose` | 输出详细日志          | `false`   |

详见 [README - 使用示例](./README.md#使用示例)。

### Q3.2 如何 {进阶操作}？

```bash
{advanced-command}
```

**注意事项：**

- {注意 1}
- {注意 2}

### Q3.3 如何查看版本号？

```bash
{command} --version
# 或
{command} -V
```

### Q3.4 如何开启调试模式？

```bash
# 方式 1：环境变量
export DEBUG=*
{command}

# 方式 2：命令行参数
{command} --verbose

# 方式 3：日志级别
export LOG_LEVEL=debug
{command}
```

### Q3.5 如何 {自定义配置}？

编辑配置文件 `{config-path}`：

```yaml
# 关键配置项
field_1: value_1
field_2: value_2
```

完整配置项见 [README - 配置](./README.md#配置)。

### Q3.6 命令执行后无输出 / 卡住

**排查步骤：**

```bash
# 1. 检查进程是否在运行
ps aux | grep {command}

# 2. 查看日志
tail -f {log-path}

# 3. 开启调试模式重新执行
DEBUG=* {command}

# 4. 检查网络连接（如依赖远程服务）
curl -v {endpoint}
```

### Q3.7 如何卸载？

```bash
# npm
npm uninstall -g {package-name}

# 清理配置（可选）
rm -rf ~/.{project-name}
```

---

## 4. 配置问题（Configuration）

### Q4.1 配置文件的优先级是什么？

按以下顺序（从高到低）：

1. **命令行参数**：`--option value`
2. **环境变量**：`{ENV_VAR}`
3. **项目级配置**：`./.{project-name}rc` 或 `./{project-name}.config.js`
4. **用户级配置**：`~/.{project-name}rc`
5. **默认值**

### Q4.2 配置项 `{field}` 支持哪些值？

| 值           | 说明                          |
| :----------- | :---------------------------- |
| `option_a`   | {说明}                        |
| `option_b`   | {说明}                        |
| `option_c`   | {说明}                        |

### Q4.3 配置不生效 / 与预期不符

**排查步骤：**

```bash
# 1. 查看实际生效的配置（含优先级追溯）
{command} config --show

# 2. 检查环境变量
env | grep {PREFIX}

# 3. 检查配置文件路径
{command} config --path

# 4. 验证 YAML / JSON 语法
yamllint {config-file}
```

### Q4.4 如何在 CI 环境中配置？

```yaml
# GitHub Actions 示例
- name: Setup {project}
  run: |
    echo "{field}=${{ secrets.SECRET_FIELD }}" >> .env
    {command} run
```

详见 [CI 集成文档](./docs/ci-integration.md)。

---

## 5. 错误排查（Troubleshooting）

### Q5.1 错误码 `{error-code}` 是什么意思？

| 错误码  | 含义                  | 排查方向                          |
| :------ | :-------------------- | :-------------------------------- |
| `E001`  | 参数校验失败          | 检查输入参数类型与必填项          |
| `E002`  | 网络超时              | 检查网络连接 / 增大 `timeout`     |
| `E003`  | 权限不足              | 检查 Token / Scope                |
| `E004`  | 资源不存在            | 检查 ID 是否正确 / 是否已删除     |
| `E005`  | 限流触发              | 降低频率 / 申请更高配额           |
| `E999`  | 服务内部错误          | 查看 `request_id` 联系运维        |

### Q5.2 出现 `Connection refused` / `ETIMEDOUT`

**可能原因：**

- 目标服务未启动
- 防火墙拦截
- DNS 解析失败
- 代理配置错误

**排查命令：**

```bash
# 1. 测试连通性
ping {host}
telnet {host} {port}
curl -v {endpoint}

# 2. 检查本地端口
lsof -i :{port}

# 3. 检查代理
env | grep -i proxy
```

### Q5.3 出现 `Out of memory` / `OOMKilled`

**解决方案：**

```bash
# 1. 增大 Node.js 内存上限
export NODE_OPTIONS="--max-old-space-size=4096"
{command}

# 2. 检查内存泄漏
{command} --inspect
# 打开 chrome://inspect 取内存快照

# 3. K8s 环境调大资源限制
resources:
  limits:
    memory: "4Gi"
```

### Q5.4 出现 `Segmentation fault` (core dumped)

**收集信息：**

```bash
# 1. 启用 core dump
ulimit -c unlimited

# 2. 重现问题
{command}

# 3. 用 gdb 分析
gdb {command} core.{pid}
bt
```

提交 Issue 时附上：操作系统版本、{项目} 版本、core dump 文件。

### Q5.5 升级后行为异常 / 兼容性问题

**排查步骤：**

1. 阅读 [CHANGELOG](./CHANGELOG.md) 中的 `**BREAKING**:` 标注
2. 检查依赖版本是否匹配
3. 清理缓存重装：

```bash
rm -rf node_modules package-lock.json
npm install
```

4. 如无法解决，回退到上一个稳定版本：

```bash
npm install -g {package-name}@{previous-version}
```

---

## 6. 性能问题（Performance）

### Q6.1 {项目名} 的性能基线是多少？

| 指标        | 基线值         | 测试环境              |
| :---------- | :------------- | :-------------------- |
| QPS         | ≥ 1,000        | 4C8G / 单实例         |
| P99 延迟    | ≤ 200ms        | 4C8G / 单实例         |
| 内存占用    | ≤ 512MB        | 空闲态                |
| 启动时间    | ≤ 3s           | 冷启动                |

### Q6.2 如何优化性能？

- **配置层面**：开启缓存、调整线程池大小、启用压缩
- **使用层面**：批量代替循环单次、避免大对象序列化、合理使用索引
- **架构层面**：读写分离、水平扩展、CDN 加速

详见 [性能优化指南](./docs/performance.md)。

### Q6.3 内存占用过高怎么办？

```bash
# 1. 监控内存
{command} stats --memory

# 2. 检查是否有内存泄漏
{command} --inspect
# Chrome DevTools → Memory → Take heap snapshot

# 3. 调整 GC 策略
export NODE_OPTIONS="--max-old-space-size=2048 --gc-interval=100"
```

---

## 7. 集成与扩展（Integration）

### Q7.1 如何与 {第三方系统} 集成？

详见 [集成文档](./docs/integrations/{system}.md)。

### Q7.2 是否提供 SDK？

| 语言     | 仓库                                | 状态        |
| :------- | :---------------------------------- | :---------- |
| Java     | `github.com/{org}/sdk-java`         | ✅ 稳定     |
| Python   | `github.com/{org}/sdk-python`       | ✅ 稳定     |
| Node.js  | `github.com/{org}/sdk-node`         | ✅ 稳定     |
| Go       | `github.com/{org}/sdk-go`           | 🟡 Beta     |
| Rust     | —                                   | 🔜 规划中   |

### Q7.3 如何编写自定义插件？

```typescript
// 示例：自定义插件骨架
export default class MyPlugin {
  name = 'my-plugin';

  apply(context) {
    context.hooks.beforeRun.tapPromise(this.name, async (config) => {
      // 自定义逻辑
    });
  }
}
```

详见 [插件开发指南](./docs/plugins.md)。

### Q7.4 是否支持 {协议/标准}？

| 协议/标准        | 支持状态        |
| :--------------- | :-------------- |
| OpenAPI 3.1      | ✅              |
| GraphQL          | ✅              |
| gRPC             | ✅              |
| WebSocket        | 🟡 实验性       |
| MQTT             | ❌              |

---

## 8. 维护说明（Maintenance）

### Q8.1 如何贡献新的 FAQ？

1. Fork 仓库
2. 编辑 `FAQ.md`，按主题归类追加 Q&A
3. 提交 PR，标题 `docs(faq): add Q{编号} {主题}`
4. 等待 Review

### Q8.2 FAQ 更新频率？

- **新问题**：48 小时内补充
- **过时问题**：每季度评审，标注或移除
- **重大变更**：随版本发布同步更新

### Q8.3 反馈 FAQ 错误 / 过时信息

请 [提交 Issue](https://github.com/{org}/{repo}/issues/new?labels=faq&template=faq-issue.md)，标注 `faq` label。

---

## 📌 FAQ 撰写 Checklist

- [ ] §0 文档导读：目的 / 提问指南 / 变更记录
- [ ] §1 通用问题：≥ 5 个基础认知问题
- [ ] §2 安装问题：覆盖权限 / 依赖 / 平台 / 命令找不到 / 离线场景
- [ ] §3 使用问题：覆盖基础操作 / 进阶操作 / 调试 / 卸载
- [ ] §4 配置问题：覆盖优先级 / 取值 / 不生效 / CI 场景
- [ ] §5 错误排查：错误码字典 + Top 5 高频错误
- [ ] §6 性能问题：基线数据 + 优化建议
- [ ] §7 集成扩展：SDK / 插件 / 协议支持
- [ ] §8 维护说明：贡献流程 / 更新频率 / 反馈渠道
- [ ] 每个 Q 含：现象 / 原因 / 解决方案 / 命令示例
- [ ] 命令示例可复制粘贴运行
- [ ] 链接到 README / CHANGELOG / CONTRIBUTING 完整
