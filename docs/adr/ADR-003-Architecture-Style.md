# ADR-003: Architecture Style

---

# Status

Accepted

---

# Date

2026-07-28

---

# Context

PlanYourTrip is expected to grow into a feature-rich travel platform with AI capabilities. The architecture should support modular development while remaining simple enough for a small team to build and maintain.

---

# Decision

Adopt a **Modular Monolith** architecture.

The application will be deployed as a single service while being internally organized into independent business modules with clear boundaries.

---

# Architecture Overview

```
                FastAPI

        ┌───────────────────────┐
        │   Destination Module  │
        ├───────────────────────┤
        │      Trip Module      │
        ├───────────────────────┤
        │    Itinerary Module   │
        ├───────────────────────┤
        │     Budget Module     │
        ├───────────────────────┤
        │    Booking Module     │
        ├───────────────────────┤
        │       AI Module       │
        ├───────────────────────┤
        │ Notification Module   │
        └───────────────────────┘

               PostgreSQL
```

---

# Alternatives Considered

- Traditional layered monolith
- Microservices
- Serverless architecture

---

# Rationale

A Modular Monolith provides:

- Simpler deployment
- Lower operational overhead
- Clear module boundaries
- Easier debugging
- Faster development
- Straightforward future migration to microservices if required

---

# Consequences

## Positive

- Single deployment unit
- Easier local development
- Lower infrastructure cost
- Strong modularity

## Trade-offs

- All modules share one runtime
- Requires discipline to maintain module boundaries

---

# Related Documents

- Engineering Blueprint
- Architecture Principles
- Domain Model

---

# Version History

| Version | Date | Description | Author |
|----------|------------|-----------------|----------------|
| 1.0 | 2026-07-28 | Initial version | Kasi Viswanath |