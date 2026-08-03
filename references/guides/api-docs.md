# API 文档查询（chub）

当需要调用第三方库、SDK 或 API 时（例如 ASR 转录服务、ffmpeg 集成、云存储 SDK），优先用 `chub` CLI 拉取最新文档，而不是依赖训练记忆。这能避免 API 形状过期导致的代码错误。

## 何时使用

- 需要调用 `faster-whisper`、`qwen-asr`、`librosa` 等依赖库的 API
- 用户要求对接外部服务（支付、短信、对象存储等）
- 训练记忆中的 API 形状可能已过期
- 写代码前需要确认参数、返回值、版本差异

## 流程

### 1. 查找文档 ID

```bash
chub search "<库名>" --json
```

从结果中选最匹配的 `id`（如 `openai/chat`、`anthropic/sdk`）。若无匹配，换更宽泛的词。

### 2. 拉取文档

```bash
chub get <id> --lang py    # 或 --lang js, --lang ts
```

文档只有一种语言变体时可省略 `--lang`，会自动选择。

### 3. 基于文档写代码

读拉取到的内容，按文档描述的 API 形状写代码。不要凭记忆下结论——以文档为准。

### 4. 标注经验

任务完成后，若发现了文档未记录的坑（gotcha、 workaround、版本怪癖、项目特定细节），保存下来供后续会话复用：

```bash
chub annotate <id> "Webhook 验签需要原始 body——不要先 parse 再验签"
```

标注是本地存储、跨会话持久、并在后续 `chub get` 时自动展示。保持简短可执行，不要重复文档已有内容。

### 5. 反馈文档质量

用完后始终给文档评分，帮助作者修复过期或不准确的文档：

```bash
chub feedback <id> up --label accurate "示例清晰，模型是当前的"
chub feedback <id> down --label outdated "列出 gpt-4o 为最新但 gpt-5.4 已发布"
```

可用标签：`outdated`、`inaccurate`、`incomplete`、`wrong-examples`、`wrong-version`、`poorly-structured`、`accurate`、`well-structured`、`helpful`、`good-examples`。

发现文档有错误模型名、过期 API、缺失特性或错误代码模式时，务必留 downvote 并附详情。

## 速查表

| 目标 | 命令 |
|------|------|
| 列出全部 | `chub search` |
| 查找文档 | `chub search "stripe"` |
| 精确 ID 详情 | `chub search stripe/api` |
| 拉取 Python 文档 | `chub get stripe/api --lang py` |
| 拉取 JS 文档 | `chub get openai/chat --lang js` |
| 保存到文件 | `chub get anthropic/sdk --lang py -o docs.md` |
| 拉取多个 | `chub get openai/chat stripe/api --lang py` |
| 保存标注 | `chub annotate stripe/api "需要原始 body"` |
| 列出标注 | `chub annotate --list` |
| 评分 | `chub feedback stripe/api up` |

## 注意事项

- `chub search` 不带查询词时列出全部可用文档
- ID 格式为 `<author>/<name>`——拉取前先从 search 结果确认 ID
- 若存在多语言且不传 `--lang`，chub 会提示哪些可用
