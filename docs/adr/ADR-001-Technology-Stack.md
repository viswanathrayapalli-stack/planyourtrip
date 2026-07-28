# ADR-001: Technology Stack

---

# Status

Accepted

---

# Date

2026-07-28

---

# Context

PlanYourTrip requires a modern, maintainable technology stack that supports rapid development, scalability, AI integration, and an excellent developer experience.

---

# Decision

The project will use the following technologies:

| Layer | Technology |
|--------|------------|
| Frontend | Next.js |
| Frontend Language | TypeScript |
| Backend | FastAPI |
| Backend Language | Python |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Cache | Redis (planned) |
| AI Framework | LangGraph + LangChain |
| Authentication | OAuth + JWT |
| Maps | Google Maps Platform |
| Version Control | Git + GitHub |

---

# Alternatives Considered

Frontend

- React + Vite
- Angular
- Vue

Backend

- Spring Boot
- NestJS
- Django

Database

- MySQL
- MongoDB

AI

- Custom orchestration
- Semantic Kernel

---

# Rationale

Next.js provides an excellent React-based framework with server-side rendering and strong ecosystem support.

FastAPI offers high performance, automatic OpenAPI generation, and excellent developer productivity.

PostgreSQL provides a mature, reliable relational database suitable for structured travel data.

LangGraph enables structured AI workflows while allowing deterministic business logic to remain separate.

---

# Consequences

Positive

- Strong developer experience
- Excellent scalability
- Mature ecosystems
- Clear separation between deterministic logic and AI

Trade-offs

- Team must maintain proficiency in both TypeScript and Python.
- Two primary runtimes increase operational complexity.

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