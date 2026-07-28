# Module Architecture

---

# Document Information

| Property | Value |
|----------|-------|
| Document | Module Architecture |
| Version | 1.0 |
| Status | Draft |
| Owner | Engineering |
| Last Updated | 2026-07-28 |

---

# Purpose

This document defines the internal module organization of the PlanYourTrip backend.

Each module represents a business capability and owns its own APIs, business logic, persistence, validation, and tests.

---

# Module Design Principles

Every module should:

- Represent one business capability
- Be independently testable
- Hide implementation details
- Expose only necessary interfaces
- Avoid direct coupling with other modules

---

# Backend Structure

backend/
└── app/
    ├── core/
    ├── shared/
    ├── modules/
    └── main.py

---

# Module List

Identity

Destination

Trip

Itinerary

Budget

Booking

Transportation

Accommodation

Notification

AI

Administration

---

# Standard Module Structure

Each module follows the same layout.

module/

api.py

service.py

repository.py

models.py

schemas.py

validators.py

exceptions.py

dependencies.py

tests/

README.md

---

# Responsibilities

API

Receives HTTP requests.

Validates input.

Returns responses.

No business logic.

---

Service

Contains business rules.

Coordinates workflows.

Calls repositories.

Handles transactions.

---

Repository

Reads and writes data.

No business rules.

---

Models

Database entities.

---

Schemas

Request and response models.

---

Validators

Business validation rules.

---

Exceptions

Module-specific exceptions.

---

Dependencies

Dependency injection.

---

Tests

Unit and integration tests.

---

README

Explains the module.

---

# Shared Package

Shared code belongs here.

shared/

database/

security/

events/

exceptions/

responses/

pagination/

utils/

constants/

---

# Module Communication

Preferred

Trip Service

↓

Destination Service

Avoid

Trip Repository

↓

Destination Repository

Modules communicate through services, not repositories.

---

# Dependency Rules

Allowed

API

↓

Service

↓

Repository

↓

Database

Not Allowed

API

↓

Database

Service

↓

Database

Repository

↓

Another Repository

---

# Future Growth

Modules should be designed so they can become independent services without significant redesign.

---

# Version History

| Version | Date | Description | Author |
|----------|------|-------------|--------|
| 1.0 | 2026-07-28 | Initial version | Kasi Viswanath |