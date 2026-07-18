# API Documentation Retrieval (chub)

When you need to call third-party libraries, SDKs, or APIs (e.g., ASR transcription services, ffmpeg integration, cloud storage SDKs), prefer using the `chub` CLI to fetch the latest documentation instead of relying on training memory. This avoids code errors caused by stale API shapes.

## When to Use

- Need to call APIs from dependency libraries such as `faster-whisper`, `qwen-asr`, `librosa`
- User requests integration with external services (payments, SMS, object storage, etc.)
- API shapes in training memory may be outdated
- Need to confirm parameters, return values, and version differences before writing code

## Workflow

### 1. Search for Documentation ID

```bash
chub search "<library name>" --json
```

From the results, select the best-matching `id` (e.g., `openai/chat`, `anthropic/sdk`). If no match is found, try a broader search term.

### 2. Fetch Documentation

```bash
chub get <id> --lang py    # or --lang js, --lang ts
```

When only one language variant exists, you can omit `--lang` and it will auto-select.

### 3. Write Code Based on Documentation

Read the fetched content and write code according to the API shapes described in the documentation. Do not rely on memory — the documentation is authoritative.

### 4. Annotate Learnings

After completing the task, if you discovered gotchas, workarounds, version quirks, or project-specific details not documented, save them for reuse in future sessions:

```bash
chub annotate <id> "Webhook signature verification requires the raw body — do not parse before verifying"
```

Annotations are stored locally, persist across sessions, and are automatically displayed in subsequent `chub get` calls. Keep them short and actionable; do not duplicate existing documentation content.

### 5. Provide Documentation Quality Feedback

Always rate the documentation after use to help authors fix outdated or inaccurate docs:

```bash
chub feedback <id> up --label accurate "Examples are clear, model is current"
chub feedback <id> down --label outdated "Lists gpt-4o as latest but gpt-5.4 has been released"
```

Available labels: `outdated`, `inaccurate`, `incomplete`, `wrong-examples`, `wrong-version`, `poorly-structured`, `accurate`, `well-structured`, `helpful`, `good-examples`.

When you find incorrect model names, outdated APIs, missing features, or wrong code patterns in documentation, be sure to leave a downvote with details.

## Quick Reference

| Goal | Command |
|------|------|
| List all | `chub search` |
| Search docs | `chub search "stripe"` |
| Exact ID details | `chub search stripe/api` |
| Fetch Python docs | `chub get stripe/api --lang py` |
| Fetch JS docs | `chub get openai/chat --lang js` |
| Save to file | `chub get anthropic/sdk --lang py -o docs.md` |
| Fetch multiple | `chub get openai/chat stripe/api --lang py` |
| Save annotation | `chub annotate stripe/api "requires raw body"` |
| List annotations | `chub annotate --list` |
| Rate | `chub feedback stripe/api up` |

## Notes

- `chub search` without a query lists all available documents
- ID format is `<author>/<name>` — confirm the ID from search results before fetching
- If multiple languages exist and `--lang` is not specified, chub will indicate which are available
