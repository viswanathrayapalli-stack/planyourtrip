# System Architecture

---

# Document Information

| Property | Value |
|----------|-------|
| Document | System Architecture |
| Version | 1.0 |
| Status | Draft |
| Owner | Engineering |
| Last Updated | 2026-07-28 |

---

# Purpose

This document describes the overall architecture of PlanYourTrip, including major components, interactions, deployment boundaries, and external integrations.

It serves as the primary technical reference for system design.

---

# Architectural Style

PlanYourTrip follows a Modular Monolith architecture.

Characteristics:

- Single deployable backend
- Independent business modules
- Shared database
- Clear module boundaries
- REST API communication
- AI integrated as a supporting capability

---

# High-Level System Overview

```

                User

                  │

                  ▼

         Next.js Frontend

                  │

          REST / HTTPS API

                  │

                  ▼

           FastAPI Backend

                  │

     ┌────────────────────────────┐

     │       Business Modules      │

     │                            │

     │ User                       │

     │ Destination                │

     │ Trip                       │

     │ Itinerary                  │

     │ Budget                     │

     │ Booking                    │

     │ Notification               │

     │ AI                         │

     └────────────────────────────┘

                  │

                  ▼

            PostgreSQL

                  │

                  ▼

               Redis
          (future caching)

```

---

# External Services

PlanYourTrip integrates with several external platforms.

```
Google Maps Platform

↓

Location Search

↓

Distance Matrix

↓

Places API
```

```
OAuth Providers

↓

Google Login

↓

Future Social Login
```

```
LLM Providers

↓

OpenAI

↓

Future Multi-LLM Support
```

---

# Frontend Architecture

Technology

- Next.js
- TypeScript

Responsibilities

- UI rendering
- User interactions
- Form validation
- API communication
- Authentication
- Responsive design

The frontend should contain minimal business logic.

---

# Backend Architecture

Technology

- FastAPI
- Python

Responsibilities

- Business logic
- Validation
- Authentication
- Authorization
- AI orchestration
- Database access
- Integration with external services

---

# Module Overview

```
User Module

Destination Module

Trip Module

Itinerary Module

Budget Module

Booking Module

Notification Module

AI Module
```

Each module owns:

- API
- Services
- Schemas
- Repositories
- Business rules

---

# Shared Components

Shared functionality is centralized.

```
shared/

database/

security/

exceptions/

responses/

pagination/

utils/

constants/

events/
```

---

# Database Layer

Database

PostgreSQL

Access Pattern

API

↓

Service

↓

Repository

↓

Database

No business logic should exist in repositories.

---

# AI Layer

AI supports the business modules.

Responsibilities:

- Trip recommendations
- Itinerary generation
- Route optimization
- Conversational assistant

AI does not own business rules.

---

# Security Architecture

Authentication

OAuth

JWT

Authorization

Role-based access control (RBAC)

Principles

- Least privilege
- Secure secrets
- Input validation
- HTTPS only

---

# Observability

The system provides:

- Structured logging
- Health checks
- Metrics
- Error tracking
- Request tracing

---

# Deployment Architecture

Initial Deployment

```
Next.js

↓

Vercel

```

```
FastAPI

↓

Railway / Render / Azure

```

```
PostgreSQL

↓

Managed Database
```

Future deployment can evolve without changing the application architecture.

---

# Scalability Strategy

Current

Modular Monolith

Future

Module extraction into Microservices

Examples

```
AI Module

↓

Independent Service
```

```
Notification Module

↓

Independent Service
```

---

# Non-Functional Requirements

Performance

- Fast API responses
- Efficient database queries

Availability

- High uptime

Maintainability

- Modular codebase

Security

- Secure by design

Scalability

- Horizontal evolution through modularization

---

# Architecture Review Checklist

Every architectural change should answer:

- Does it align with the Engineering Blueprint?
- Does it follow Architecture Principles?
- Does it preserve module boundaries?
- Is it testable?
- Does it improve maintainability?
- Should an ADR be created?

---

# Related Documents

- Engineering Blueprint
- Product Architecture
- Domain Model
- Architecture Principles
- ADR-001
- ADR-002
- ADR-003

---

# Version History

| Version | Date | Description | Author |
|----------|------------|---------------------------|----------------|
| 1.0 | 2026-07-28 | Initial version | Kasi Viswanath |