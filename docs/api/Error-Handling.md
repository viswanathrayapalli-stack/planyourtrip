# Error Handling

---

# Standard Error Response

{
  "success": false,
  "error": {
      "code": "TRIP_NOT_FOUND",
      "message": "Trip not found."
  },
  "timestamp": "...",
  "path": "/api/v1/trips/123"
}

---

# Validation Error

{
  "success": false,
  "errors": [
      {
          "field": "startDate",
          "message": "Start date is required."
      }
  ]
}

---

# Error Categories

Validation

Authentication

Authorization

Business Rule

Infrastructure

Unexpected

---

# Logging

Unexpected errors

↓

Structured Logs

↓

Monitoring

---

# Never Return

Database errors

Stack traces

Passwords

Secrets

---

# Version History

|Version|Date|Description|Author|
|--------|----|-----------|------|
|1.0|2026-07-28|Initial Version|Kasi Viswanath|