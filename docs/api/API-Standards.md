# API Standards

---

# Document Information

| Property | Value |
|----------|-------|
| Document | API Standards |
| Version | 1.0 |
| Status | Approved |
| Owner | Engineering |

---

# Purpose

Define consistent standards for designing and implementing REST APIs.

---

# Base URL

/api/v1

Examples

/api/v1/trips

/api/v1/destinations

/api/v1/users

---

# HTTP Methods

GET

Retrieve data

POST

Create resources

PUT

Replace an existing resource

PATCH

Partial update

DELETE

Delete resource

---

# Resource Naming

Use plural nouns.

Good

/trips

/destinations

/bookings

Avoid

/getTrips

/createTrip

/doBooking

---

# JSON

All APIs communicate using JSON.

Request

application/json

Response

application/json

---

# Date Format

ISO 8601

Example

2026-08-15T10:30:00Z

---

# Naming Convention

JSON fields use

camelCase

Example

estimatedBudget

tripStatus

destinationName

---

# Pagination

Default page size

20

Parameters

?page=

&size=

&sort=

---

# Filtering

Example

GET

/trips?status=ACTIVE

/destinations?country=India

---

# Searching

Example

/search?query=Hyderabad

---

# Idempotency

GET

PUT

DELETE

must be idempotent.

POST creates resources.

---

# Version History

| Version | Date | Description | Author |
|----------|------|-------------|--------|
|1.0|2026-07-28|Initial Version|Kasi Viswanath|