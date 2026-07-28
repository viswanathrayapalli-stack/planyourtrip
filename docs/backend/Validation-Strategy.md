# Validation Strategy

---

# Document Information

| Property | Value |
|----------|-------|
| Document | Validation Strategy |
| Version | 1.0 |
| Status | Draft |
| Owner | Engineering |

---

# Purpose

Define validation responsibilities across the application.

Validation is performed in multiple layers to ensure data integrity.

---

# Validation Layers

Client Validation

↓

API Validation

↓

Business Validation

↓

Database Validation

---

# Layer Responsibilities

## Client Validation

Performed by Next.js.

Examples:

- Required fields
- Date picker constraints
- Input formatting

Purpose:

Improve user experience.

---

## API Validation

Performed using Pydantic.

Examples:

- Required fields
- String length
- Email format
- Enum validation

---

## Business Validation

Performed in Services.

Examples:

- End date must be after start date.
- Budget cannot be negative.
- Booking cannot be confirmed twice.
- Destination must be active.

---

## Database Validation

Performed by PostgreSQL.

Examples:

- Foreign Keys
- Unique Constraints
- Check Constraints
- Not Null

---

# Validation Principles

- Validate as early as possible.
- Keep business rules in the Service layer.
- Do not duplicate business validation in the Repository layer.
- Database constraints are the final line of defense.

---

# Error Messages

Validation messages should:

- Be clear
- Be user-friendly
- Avoid technical details
- Be consistent

Example:

Good:

"Trip end date must be after the start date."

Avoid:

"Constraint violation."

---

# Version History

| Version | Date | Description | Author |
|----------|------|-------------|--------|
|1.0|2026-07-28|Initial version|Kasi Viswanath|