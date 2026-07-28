# Request Lifecycle

---

# Document Information

| Property | Value |
|----------|-------|
| Document | Request Lifecycle |
| Version | 1.0 |
| Status | Draft |
| Owner | Engineering |

---

# Purpose

Describe how an HTTP request travels through the backend.

---

# Request Flow

Browser

↓

Next.js Frontend

↓

REST API

↓

FastAPI Router

↓

Authentication

↓

Validation

↓

Application Service

↓

Repository

↓

Database

↓

Repository

↓

Service

↓

Response Model

↓

JSON Response

↓

Frontend

---

# Detailed Steps

## 1. Request Received

FastAPI receives the request.

---

## 2. Authentication

JWT validation

Current user resolution

Authorization

---

## 3. Validation

Pydantic validates request payload.

---

## 4. Business Logic

Application Service executes business rules.

---

## 5. Data Access

Repository retrieves or updates data.

---

## 6. Response Construction

Service returns DTO.

API serializes response.

---

## Error Flow

Request

↓

Validation Error

↓

Business Exception

↓

Global Exception Handler

↓

Standard Error Response

---

# Logging

Every request should include:

- Request ID
- User ID (if authenticated)
- Processing time
- HTTP status

---

# Version History

| Version | Date | Description | Author |
|----------|------|-------------|--------|
|1.0|2026-07-28|Initial version|Kasi Viswanath|