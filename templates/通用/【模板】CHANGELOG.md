# Changelog

> **Document Type:** Version Change Log
>
> **Version:** v1.0.0
>
> **Date:** YYYY-MM-DD
>
> **Maintainer:** [Project Owner / Release Manager]
>
> **Standard Followed:** [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
>
> **Semantic Versioning:** [Semantic Versioning 2.0.0](https://semver.org/)

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versioning follows [Semantic Versioning](https://semver.org/).

## Change Type Description

| Type | Description |
| :----------- | :---------------------------------------------------- |
| **Added** | New features |
| **Changed** | Changes to existing functionality |
| **Deprecated** | Features that will be removed soon |
| **Removed** | Features removed in this version |
| **Fixed** | Bug fixes |
| **Security** | Security-related fixes (including vulnerabilities, CVEs) |

## Version Number Rules (SemVer)

```
MAJOR.MINOR.PATCH
```

| Version Segment | When to Bump | Example |
| :-------- | :-------------------------------------------------------------------- | :------------------ |
| `MAJOR` | Incompatible API changes | `1.0.0` → `2.0.0` |
| `MINOR` | Backward-compatible new functionality | `1.0.0` → `1.1.0` |
| `PATCH` | Backward-compatible bug fixes | `1.0.0` → `1.0.1` |

Pre-release versions: `-alpha` / `-beta` / `-rc.N`, e.g., `1.0.0-beta.2`.

---

## [Unreleased]

> This version has not been released yet; records all changes since the last release. On release, promote this section to the formal version number.

### Added

- Added {feature description}, see {PR/Issue link}
- Added {config item}, default value {value}

### Changed

- Changed {behavior description}: from {old} to {new}, migration guide at {doc link}
- Performance optimization: {metric} improved by {X}%

### Deprecated

- Deprecated {API/feature}, will be removed in {version}, alternative: {description}

### Removed

- Removed {API/feature} (deprecated since {version})

### Fixed

- Fixed {bug description}, impact scope {description}, Fixes #{issue}

### Security

- Fixed {CVE ID}: {vulnerability description}, CVSS {score}, upgrade guide at {announcement link}

---

## [1.0.0] - YYYY-MM-DD

### Added

- Initial formal release
- Core features: {Feature 1}
- Core features: {Feature 2}
- Core features: {Feature 3}
- Complete documentation: README / CONTRIBUTING / FAQ
- CI/CD pipeline (GitHub Actions)
- Coverage gate ≥ 80%

### Changed

- N/A (first release)

### Deprecated

- N/A (first release)

### Removed

- N/A (first release)

### Fixed

- N/A (first release)

### Security

- Enabled dependency scanning (Dependabot / npm audit / cargo-audit)
- Enabled CodeQL static analysis

---

## [0.9.0] - YYYY-MM-DD

### Added

- Beta release
- Core API interfaces stable

### Changed

- {API name} signature adjustment: parameter {old} → {new}

### Fixed

- Fixed {bug} causing {symptom}

---

## [0.5.0] - YYYY-MM-DD

### Added

- Alpha version, internal testing only

---

## Version Links

> Maintain links from version numbers to git tags / GitHub Releases.

[Unreleased]: https://github.com/{org}/{repo}/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/{org}/{repo}/releases/tag/v1.0.0
[0.9.0]: https://github.com/{org}/{repo}/releases/tag/v0.9.0
[0.5.0]: https://github.com/{org}/{repo}/releases/tag/v0.5.0

---

## 📌 CHANGELOG Writing Checklist

- [ ] Follow Keep a Changelog 1.1.0 format (six categories: Added/Changed/Deprecated/Removed/Fixed/Security)
- [ ] Follow Semantic Versioning 2.0.0 version number rules
- [ ] [Unreleased] section at the top, promoted to formal version on release
- [ ] Each version has a clear release date (YYYY-MM-DD)
- [ ] Each change includes PR / Issue link (if applicable)
- [ ] Breaking Changes explicitly annotated (e.g., `**BREAKING**:` prefix)
- [ ] Security fixes categorized separately, with CVE ID and CVSS score
- [ ] Version links section maintains version → git tag compare links
- [ ] Deprecated items annotated with removal version and alternative
- [ ] Do not record trivial internal refactoring / copy changes
