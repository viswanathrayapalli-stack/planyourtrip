# Migration Strategy

---

Migration Tool

Alembic

---

Rules

Never modify production tables manually.

Every schema change requires:

Migration

Review

Rollback plan

---

Migration Naming

YYYYMMDD_description

Example

20260728_create_trip_table

---

Rollback

Every migration must be reversible where feasible.