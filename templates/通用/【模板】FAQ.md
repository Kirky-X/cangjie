# {Project Name} - Frequently Asked Questions (FAQ)

> **Document Status:** 🟢 Active / 🟡 Under Review / 🔴 Archived
>
> **Confidentiality Level:** Internal / Public
>
> **Version:** v1.0.0
>
> **Date:** YYYY-MM-DD
>
> **Maintainer:** [Project Owner / Documentation Lead]
>
> **Audience:** Users, developers, ops, third-party integrators
>
> **Update Frequency:** Monthly review; new questions added within 48 hours
>
> **Related Documents:** [README.md](./README.md) / [CHANGELOG.md](./CHANGELOG.md) / [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 0. Document Guide

### 0.1 Document Purpose & Scope

This file collects frequently encountered questions and answers during {Project Name} usage, organized by topic for self-service troubleshooting.

**Applicable Scenarios:**

- ✅ Common obstacles during installation, configuration, and usage
- ✅ Error message interpretation and troubleshooting approaches
- ✅ Concept clarification and best practices
- ❌ Personalized issues (please submit an Issue)
- ❌ Security vulnerability reporting (use security advisory process, don't submit publicly)

### 0.2 Asking Guide

If this file doesn't solve your problem, submit an Issue in the following format:

```
- Environment: [OS / Language version / Project version]
- Reproduction steps: [1. ... 2. ... 3. ...]
- Expected behavior: [...]
- Actual behavior: [...]
- Error log: [full stack trace, sensitive info masked]
```

### 0.3 Change Log

| Version | Date | Author | Changes | Reviewer |
| :--- | :--------- | :----- | :----------------------------- | :------- |
| v0.1 | YYYY-MM-DD | [Name] | Initial draft: Installation + Usage questions | [Name] |
| v0.2 | YYYY-MM-DD | [Name] | Added Configuration + Troubleshooting | [Name] |
| v1.0 | YYYY-MM-DD | [Name] | Formal release | [Owner] |

---

## 1. General

### Q1.1 What is {Project Name}?

{One-paragraph brief description, referencing the first paragraph of the README.}

See [README - Features](./README.md#features).

### Q1.2 What scenarios is {Project Name} suitable for?

- ✅ {Scenario 1}
- ✅ {Scenario 2}
- ❌ {Not applicable scenario 1}
- ❌ {Not applicable scenario 2}

### Q1.3 What's the difference between {Project Name} and {competitor/similar project}?

| Dimension | {Project Name} | {Competitor A} | {Competitor B} |
| :---------- | :--------- | :--------- | :--------- |
| Positioning | {Description} | {Description} | {Description} |
| Language Support | {Description} | {Description} | {Description} |
| Performance | {Description} | {Description} | {Description} |
| Learning Curve | {Description} | {Description} | {Description} |

### Q1.4 What is the stable version of {Project Name}?

Current stable version: `v{X.Y.Z}` ([Release Notes](https://github.com/{org}/{repo}/releases)).

Versioning follows [SemVer 2.0.0](https://semver.org/):

- `MAJOR`: Incompatible API changes
- `MINOR`: Backward-compatible new functionality
- `PATCH`: Backward-compatible bug fixes

### Q1.5 How to get latest version notifications?

- Watch GitHub repository Releases
- Subscribe to {mailing list / RSS}
- Follow {official blog / WeChat account}

---

## 2. Installation

### Q2.1 Installation error `permission denied` or `EACCES`

**Symptom:**

```bash
npm install {package-name}
# npm ERR! code EACCES
# npm ERR! permission denied
```

**Cause:** Insufficient permissions during global installation.

**Solution:**

```bash
# Option 1: Use nvm to manage Node.js (recommended)
nvm install 18
nvm use 18

# Option 2: Change npm default directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Option 3: Use sudo (not recommended, may cause permission issues)
sudo npm install -g {package-name}
```

### Q2.2 Installation error `{dependency} not found` or `version mismatch`

**Symptom:** Dependency version not satisfied.

**Troubleshooting steps:**

```bash
# 1. Check current environment
node --version    # Need ≥ 18
npm --version
{other-dep} --version

# 2. Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# 3. Check lockfile consistency
npm ls {dependency}
```

### Q2.3 Cannot install/run on {OS}

**Supported Platforms:**

| Platform | Architecture | Support Status |
| :--------- | :---------- | :-------------- |
| Linux | x86_64 | ✅ Fully supported |
| Linux | arm64 | ✅ Supported |
| macOS | x86_64 | ✅ Fully supported |
| macOS | arm64 (M1+) | ✅ Supported |
| Windows | x86_64 | ⚠️ Experimental |
| Windows | arm64 | ❌ Not supported |

**Windows recommendation:** Use WSL2 + Linux subsystem.

### Q2.4 Command not found after installation

**Cause:** Executable path not added to `PATH`.

**Solution:**

```bash
# Check installation location
npm bin -g    # npm global install location
which {command}

# Add to PATH
echo 'export PATH="$(npm bin -g):$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Q2.5 How to install in enterprise intranet / offline environment?

```bash
# 1. Download tarball on external network machine
npm pack {package-name}

# 2. Copy to intranet machine and install
npm install -g {package-name}-{version}.tgz

# 3. Configure intranum mirror (if available)
npm config set registry https://{internal-registry}/
```

---

## 3. Usage

### Q3.1 How to {basic operation}?

```bash
{command} --option value
```

**Parameter Description:**

| Parameter | Description | Default |
| :---------- | :-------------------- | :-------- |
| `--option` | {Description} | `default` |
| `--verbose` | Output detailed logs | `false` |

See [README - Usage Examples](./README.md#usage-examples).

### Q3.2 How to {advanced operation}?

```bash
{advanced-command}
```

**Notes:**

- {Note 1}
- {Note 2}

### Q3.3 How to check version?

```bash
{command} --version
# or
{command} -V
```

### Q3.4 How to enable debug mode?

```bash
# Option 1: Environment variable
export DEBUG=*
{command}

# Option 2: Command line parameter
{command} --verbose

# Option 3: Log level
export LOG_LEVEL=debug
{command}
```

### Q3.5 How to {customize configuration}?

Edit config file `{config-path}`:

```yaml
# Key config items
field_1: value_1
field_2: value_2
```

See [README - Configuration](./README.md#configuration) for full config options.

### Q3.6 Command produces no output / hangs

**Troubleshooting steps:**

```bash
# 1. Check if process is running
ps aux | grep {command}

# 2. Check logs
tail -f {log-path}

# 3. Re-run with debug mode
DEBUG=* {command}

# 4. Check network connectivity (if dependent on remote services)
curl -v {endpoint}
```

### Q3.7 How to uninstall?

```bash
# npm
npm uninstall -g {package-name}

# Clean config (optional)
rm -rf ~/.{project-name}
```

---

## 4. Configuration

### Q4.1 What is the priority of configuration files?

In the following order (highest to lowest):

1. **Command line parameters**: `--option value`
2. **Environment variables**: `{ENV_VAR}`
3. **Project-level config**: `./.{project-name}rc` or `./{project-name}.config.js`
4. **User-level config**: `~/.{project-name}rc`
5. **Default values**

### Q4.2 What values does config item `{field}` support?

| Value | Description |
| :----------- | :---------------------------- |
| `option_a` | {Description} |
| `option_b` | {Description} |
| `option_c` | {Description} |

### Q4.3 Configuration not taking effect / unexpected behavior

**Troubleshooting steps:**

```bash
# 1. Check effective configuration (with priority tracing)
{command} config --show

# 2. Check environment variables
env | grep {PREFIX}

# 3. Check config file path
{command} config --path

# 4. Validate YAML / JSON syntax
yamllint {config-file}
```

### Q4.4 How to configure in CI environment?

```yaml
# GitHub Actions example
- name: Setup {project}
  run: |
    echo "{field}=${{ secrets.SECRET_FIELD }}" >> .env
    {command} run
```

See [CI Integration Documentation](./docs/ci-integration.md).

---

## 5. Troubleshooting

### Q5.1 What does error code `{error-code}` mean?

| Error Code | Meaning | Troubleshooting Direction |
| :------ | :-------------------- | :-------------------------------- |
| `E001` | Parameter validation failed | Check input parameter types and required fields |
| `E002` | Network timeout | Check network connectivity / increase `timeout` |
| `E003` | Insufficient permissions | Check Token / Scope |
| `E004` | Resource not found | Check if ID is correct / has been deleted |
| `E005` | Rate limit triggered | Reduce frequency / request higher quota |
| `E999` | Internal server error | Check `request_id`, contact ops |

### Q5.2 `Connection refused` / `ETIMEDOUT`

**Possible causes:**

- Target service not started
- Firewall blocking
- DNS resolution failure
- Proxy configuration error

**Troubleshooting commands:**

```bash
# 1. Test connectivity
ping {host}
telnet {host} {port}
curl -v {endpoint}

# 2. Check local ports
lsof -i :{port}

# 3. Check proxy
env | grep -i proxy
```

### Q5.3 `Out of memory` / `OOMKilled`

**Solution:**

```bash
# 1. Increase Node.js memory limit
export NODE_OPTIONS="--max-old-space-size=4096"
{command}

# 2. Check for memory leaks
{command} --inspect
# Open chrome://inspect to take memory snapshot

# 3. K8s: Increase resource limits
resources:
  limits:
    memory: "4Gi"
```

### Q5.4 `Segmentation fault` (core dumped)

**Collect information:**

```bash
# 1. Enable core dump
ulimit -c unlimited

# 2. Reproduce issue
{command}

# 3. Analyze with gdb
gdb {command} core.{pid}
bt
```

When submitting an Issue, include: OS version, {Project} version, core dump file.

### Q5.5 Abnormal behavior after upgrade / compatibility issues

**Troubleshooting steps:**

1. Read `**BREAKING**:` annotations in [CHANGELOG](./CHANGELOG.md)
2. Check if dependency versions match
3. Clear cache and reinstall:

```bash
rm -rf node_modules package-lock.json
npm install
```

4. If still unresolved, rollback to previous stable version:

```bash
npm install -g {package-name}@{previous-version}
```

---

## 6. Performance

### Q6.1 What are the performance baselines for {Project Name}?

| Metric | Baseline | Test Environment |
| :---------- | :------------- | :-------------------- |
| QPS | ≥ 1,000 | 4C8G / Single instance |
| P99 Latency | ≤ 200ms | 4C8G / Single instance |
| Memory Usage | ≤ 512MB | Idle state |
| Startup Time | ≤ 3s | Cold start |

### Q6.2 How to optimize performance?

- **Configuration level**: Enable cache, adjust thread pool size, enable compression
- **Usage level**: Batch instead of loop single calls, avoid large object serialization, use indexes properly
- **Architecture level**: Read-write separation, horizontal scaling, CDN acceleration

See [Performance Optimization Guide](./docs/performance.md).

### Q6.3 Memory usage too high?

```bash
# 1. Monitor memory
{command} stats --memory

# 2. Check for memory leaks
{command} --inspect
# Chrome DevTools → Memory → Take heap snapshot

# 3. Adjust GC strategy
export NODE_OPTIONS="--max-old-space-size=2048 --gc-interval=100"
```

---

## 7. Integration & Extension

### Q7.1 How to integrate with {third-party system}?

See [Integration Documentation](./docs/integrations/{system}.md).

### Q7.2 Is an SDK provided?

| Language | Repository | Status |
| :------- | :---------------------------------- | :---------- |
| Java | `github.com/{org}/sdk-java` | ✅ Stable |
| Python | `github.com/{org}/sdk-python` | ✅ Stable |
| Node.js | `github.com/{org}/sdk-node` | ✅ Stable |
| Go | `github.com/{org}/sdk-go` | 🟡 Beta |
| Rust | — | 🔜 Planned |

### Q7.3 How to write custom plugins?

```typescript
// Example: Custom plugin skeleton
export default class MyPlugin {
  name = 'my-plugin';

  apply(context) {
    context.hooks.beforeRun.tapPromise(this.name, async (config) => {
      // Custom logic
    });
  }
}
```

See [Plugin Development Guide](./docs/plugins.md).

### Q7.4 Does it support {protocol/standard}?

| Protocol/Standard | Support Status |
| :--------------- | :-------------- |
| OpenAPI 3.1 | ✅ |
| GraphQL | ✅ |
| gRPC | ✅ |
| WebSocket | 🟡 Experimental |
| MQTT | ❌ |

---

## 8. Maintenance

### Q8.1 How to contribute a new FAQ?

1. Fork the repository
2. Edit `FAQ.md`, add Q&A organized by topic
3. Submit PR with title `docs(faq): add Q{number} {topic}`
4. Wait for review

### Q8.2 FAQ update frequency?

- **New questions**: Added within 48 hours
- **Outdated questions**: Reviewed quarterly, annotated or removed
- **Major changes**: Updated with version releases

### Q8.3 Report FAQ errors / outdated information

Please [submit an Issue](https://github.com/{org}/{repo}/issues/new?labels=faq&template=faq-issue.md) with the `faq` label.

---

## 📌 FAQ Writing Checklist

- [ ] §0 Document Guide: Purpose / Asking guide / Change log
- [ ] §1 General: ≥ 5 basic knowledge questions
- [ ] §2 Installation: Covers permissions / dependencies / platforms / command not found / offline
- [ ] §3 Usage: Covers basic operations / advanced operations / debugging / uninstall
- [ ] §4 Configuration: Covers priority / values / not taking effect / CI scenarios
- [ ] §5 Troubleshooting: Error code dictionary + Top 5 high-frequency errors
- [ ] §6 Performance: Baseline data + optimization suggestions
- [ ] §7 Integration & Extension: SDK / plugins / protocol support
- [ ] §8 Maintenance: Contribution flow / update frequency / feedback channel
- [ ] Each Q includes: Symptom / Cause / Solution / Command example
- [ ] Command examples are copy-paste runnable
- [ ] Links to README / CHANGELOG / CONTRIBUTING are complete
