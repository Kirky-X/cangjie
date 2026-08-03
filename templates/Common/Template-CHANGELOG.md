# Changelog (CHANGELOG)

> **Document Type:** Version Changelog
>
> **Document Status:** 🟢 Active / 🟡 Under Review / 🔴 Archived
>
> **Confidentiality Level:** Confidential / Internal / Public
>
> **Version:** vX.X.X
>
> **Date:** YYYY-MM-DD
>
> **Maintainer:** [Project Owner / Release Manager]
>
> **Standards Followed:** [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
>
> **Semantic Versioning:** [Semantic Versioning 2.0.0](https://semver.org/)

All important changes to this project will be recorded in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versioning follows [Semantic Versioning](https://semver.org/).

## Change Type Description

| Type         | Description                                                  |
| :----------- | :---------------------------------------------------- |
| **Added**     | New features                                            |
| **Changed**     | Changes to existing features                                       |
| **Deprecated**  | Features that will be removed                                         |
| **Removed**     | Features removed in this version                                     |
| **Fixed**       | Bug fixes                                              |
| **Security**    | Security-related fixes (including vulnerabilities, CVEs)                           |

## Version Number Rules (SemVer)

```
MAJOR.MINOR.PATCH
```

| Version Segment    | When to Bump                                                                | Example                |
| :-------- | :-------------------------------------------------------------------- | :------------------ |
| `MAJOR`   | Incompatible API changes                                                     | `1.0.0` → `2.0.0`   |
| `MINOR`   | Backward-compatible feature additions                                                    | `1.0.0` → `1.1.0`   |
| `PATCH`   | Backward-compatible bug fixes                                                   | `1.0.0` → `1.0.1`   |

Pre-release versions: `-alpha` / `-beta` / `-rc.N`, e.g., `1.0.0-beta.2`.

---

## [Unreleased]

> This version has not been released yet. Records all changes since the last release. Promote this section to a formal version number upon release.

### Added

- Added {Feature Description}, see {PR/Issue link}
- Added {Configuration Item}, default value {value}

### Changed

- Changed {Behavior Description}: from {old} to {new}, migration notes in {document link}
- Performance optimization: {Metric} improved by {X}%

### Deprecated

- Deprecated {API/Feature}, will be removed in {Version}, alternative: {description}

### Removed

- Removed {API/Feature} (deprecated since {Version})

### Fixed

- Fixed {Bug Description}, impact scope {description}, Fixes #{issue}

### Security

- Fixed {CVE Number}: {Vulnerability Description}, CVSS {Score}, upgrade notes in {announcement link}

---

## [1.0.0] - YYYY-MM-DD

### Added

- First official release
- Core features: {Feature 1}
- Core features: {Feature 2}
- Core features: {Feature 3}
- Complete documentation: README / CONTRIBUTING / FAQ
- CI/CD pipeline (GitHub Actions)
- Coverage gate ≥ 80%

### Changed

- N/A (First release)

### Deprecated

- N/A (First release)

### Removed

- N/A (First release)

### Fixed

- N/A (First release)

### Security

- Enabled dependency scanning (Dependabot / npm audit / cargo-audit)
- Enabled CodeQL static analysis

---

## [0.9.0] - YYYY-MM-DD

### Added

- Beta version release
- Core API interfaces stabilized

### Changed

- {API Name} signature adjustment: parameter {old} → {new}

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

- [ ] Follows Keep a Changelog 1.1.0 format (six categories: Added/Changed/Deprecated/Removed/Fixed/Security)
- [ ] Follows Semantic Versioning 2.0.0 version number rules
- [ ] [Unreleased] section is first, promoted to formal version number upon release
- [ ] Each version has a clear release date (YYYY-MM-DD)
- [ ] Each change includes PR / Issue link (if applicable)
- [ ] Breaking Changes explicitly annotated (e.g., `**BREAKING**:` prefix)
- [ ] Security fixes categorized separately, annotated with CVE number and CVSS score
- [ ] Version links section maintains version number → git tag compare links
- [ ] Deprecated items annotated with removal version and alternative
- [ ] Don't record trivial internal refactoring / copy changes
