# Backend Architecture

---

# Purpose

Describe the internal architecture of the FastAPI backend.

---

# Architecture Style

Modular Monolith

Layered Architecture

Domain Driven Design (Lightweight)

Repository Pattern

Dependency Injection

---

# Backend Layers

HTTP

↓

API

↓

Application Service

↓

Repository

↓

Database

---

# Responsibilities

API

- Receive requests
- Validate input
- Return responses

Service

- Business rules
- Transactions
- Orchestration

Repository

- Database access only

Shared

- Common reusable functionality

Infrastructure

- External integrations

---

# Principles

- Thin APIs
- Fat Services
- Thin Repositories
- No business logic in models
- No SQL inside Services