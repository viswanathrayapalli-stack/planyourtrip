# Module Interactions

---

# Document Information

| Property | Value |
|----------|-------|
| Document | Module Interactions |
| Version | 1.0 |
| Status | Draft |
| Owner | Engineering |
| Last Updated | 2026-07-28 |

---

# Purpose

This document defines how backend modules communicate with each other.

The goal is to maintain low coupling, high cohesion, and clear ownership of business logic.

---

# Design Principles

- Modules communicate through Services.
- Modules never access another module's Repository directly.
- Modules never import another module's database Models.
- Shared utilities belong in the shared package.
- Business events should be used for future asynchronous communication.

---

# Module Dependency Overview

Identity
    │
    ▼
Trip
├── Destination
├── Budget
├── Itinerary
├── Booking
├── Notification
└── AI

---

# Allowed Dependencies

Trip Service
    ↓
Destination Service

Booking Service
    ↓
Notification Service

Trip Service
    ↓
AI Service

---

# Not Allowed

Trip Repository
    ↓
Destination Repository

Booking Model
    ↓
Trip Model

Repository
    ↓
Repository

---

# Shared Components

Shared functionality belongs under:

shared/

- database
- security
- exceptions
- responses
- events
- utils
- constants

---

# Circular Dependency Rule

Modules must not create circular dependencies.

Example (Not Allowed):

Trip → Booking → Trip

Instead:

Trip → Booking

Booking → Event

Trip listens if required.

---

# Future Evolution

Modules should be designed so they can be extracted into independent services with minimal refactoring.

---

# Version History

| Version | Date | Description | Author |
|----------|------|-------------|--------|
| 1.0 | 2026-07-28 | Initial version | Kasi Viswanath |