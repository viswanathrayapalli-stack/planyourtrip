# ADR-002: Repository Structure

---

# Status

Accepted

---

# Date

2026-07-28

---

# Context

The repository should remain organized and scalable as the project grows, supporting clear separation between application code, documentation, infrastructure, and testing.

---

# Decision

Adopt a modular repository structure with dedicated top-level directories for frontend, backend, documentation, testing, infrastructure, scripts, and assets.

```
planyourtrip/

backend/
frontend/
docs/
tests/
infrastructure/
scripts/
assets/
.github/
```

---

# Alternatives Considered

Monolithic source directory

```
src/
```

Backend-only repository

Separate repositories

---

# Rationale

A single repository simplifies development while maintaining clear separation of responsibilities.

Documentation is version-controlled alongside code.

Testing is centralized and visible.

Future CI/CD pipelines become easier to manage.

---

# Consequences

Positive

- Clear organization
- Easier onboarding
- Scalable documentation
- Consistent development workflow

Trade-offs

- More directories during early development
- Requires discipline to maintain organization

---

# Related Documents

Engineering Blueprint

Architecture Principles

README

---

# Version History

| Version | Date | Description |
|----------|------|-------------|
| 1.0 | 2026-07-28 | Initial decision |