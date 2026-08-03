# API Documentation Lookup (chub)

When you need to call a third-party library, SDK, or API (e.g., ASR transcription services, ffmpeg integration, cloud storage SDK), use the `chub` CLI to fetch the latest documentation rather than relying on training knowledge. This avoids code errors caused by stale API shapes.

## When to Use

- Need to call APIs from dependencies like `faster-whisper`, `qwen-asr`, `librosa`, etc.
- User requests integration with external services (payments, SMS, object storage, etc.)
- The API shape in training knowledge may be outdated
- Need to confirm parameters, return values, and version differences before writing code

## Workflow

### 1. Find the Documentation ID

```bash
chub search "<library-name>" --json
```

Select the best matching `id` from results (e.g., `openai/chat`, `anthropic/sdk`). If no match, try broader terms.

### 2. Fetch the Documentation

```bash
chub get <id> --lang py    # or --lang js, --lang ts
```

Omit `--lang` when only one language variant exists; it will be auto-selected.

### 3. Write Code Based on Documentation

Read the fetched content and write code according to the API shape described in the documentation. Do not rely on memory — the documentation is the source of truth.

### 4. Annotate Experience

After completing the task, if you discovered undocumented gotchas (workarounds, version quirks, project-specific details), save them for reuse in future sessions:

```bash
chub annotate <id> "Webhook signature verification requires the raw body — do not parse before verifying"
```

Annotations are stored locally, persist across sessions, and are automatically shown in subsequent `chub get` calls. Keep them short and actionable; do not duplicate existing documentation content.

### 5. Provide Documentation Quality Feedback

Always rate the documentation after use to help authors fix outdated or inaccurate docs:

```bash
chub feedback <id> up --label accurate "Examples are clear, model is current"
chub feedback <id> down --label outdated "Lists gpt-4o as latest but gpt-5.4 has been released"
```

Available labels: `outdated`, `inaccurate`, `incomplete`, `wrong-examples`, `wrong-version`, `poorly-structured`, `accurate`, `well-structured`, `helpful`, `good-examples`.

When you find incorrect model names, outdated APIs, missing features, or wrong code patterns in the documentation, always leave a downvote with details.

## Quick Reference

| Goal | Command |
|------|------|
| List all | `chub search` |
| Find documentation | `chub search "stripe"` |
| Exact ID details | `chub search stripe/api` |
| Fetch Python docs | `chub get stripe/api --lang py` |
| Fetch JS docs | `chub get openai/chat --lang js` |
| Save to file | `chub get anthropic/sdk --lang py -o docs.md` |
| Fetch multiple | `chub get openai/chat stripe/api --lang py` |
| Save annotation | `chub annotate stripe/api "requires raw body"` |
| List annotations | `chub annotate --list` |
| Rate | `chub feedback stripe/api up` |

## Notes

- `chub search` without a query lists all available documentation
- ID format is `<author>/<name>` — confirm the ID from search results before fetching
- If multiple languages exist and `--lang` is not passed, chub will prompt which are available
