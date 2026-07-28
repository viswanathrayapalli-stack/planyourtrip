# Database Architecture

---

# Document Information

| Property | Value |
|----------|-------|
| Document | Database Architecture |
| Version | 1.0 |
| Status | Draft |
| Owner | Engineering |
| Last Updated | 2026-07-28 |

---

# Purpose

This document defines the database architecture, design principles, and persistence strategy for PlanYourTrip.

---

# Database Technology

Primary Database

PostgreSQL

ORM

SQLAlchemy

Migration Tool

Alembic

---

# Database Principles

- Normalize transactional data
- Prefer explicit relationships
- Avoid duplicated data
- Use foreign keys for integrity
- Store timestamps in UTC
- Support future scalability

---

# Persistence Flow

Client

↓

API

↓

Service

↓

Repository

↓

SQLAlchemy

↓

PostgreSQL

---

# Transaction Strategy

Transactions are managed in the Service layer.

Repositories should not control transactions.

---

# Soft Delete

Entities requiring historical data should use:

deleted_at

instead of physical deletion.

---

# Auditing

Every major entity should include:

created_at

updated_at

created_by

updated_by

---

# Version History

| Version | Date | Description | Author |
|----------|------|-------------|--------|
|1.0|2026-07-28|Initial Version|Kasi Viswanath|