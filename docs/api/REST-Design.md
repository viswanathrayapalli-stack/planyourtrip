# REST Design

---

# Resource Hierarchy

User

↓

Trips

↓

Itinerary

↓

Activities

---

# Example Endpoints

GET

/trips

GET

/trips/{tripId}

POST

/trips

PATCH

/trips/{tripId}

DELETE

/trips/{tripId}

---

# Nested Resources

/trips/{tripId}/itinerary

/trips/{tripId}/budget

/trips/{tripId}/bookings

---

# Response Codes

200 OK

201 Created

204 No Content

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

500 Internal Server Error

---

# Collection Response

{
  "data": [],
  "pagination": {},
  "links": {}
}

---

# Single Resource

{
  "data": {}
}

---

# Version History

|Version|Date|Description|Author|
|--------|----|-----------|------|
|1.0|2026-07-28|Initial Version|Kasi Viswanath|