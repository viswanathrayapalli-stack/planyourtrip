# Domain Model

---

# Document Information

| Property | Value |
|----------|-------|
| Document | Domain Model |
| Version | 1.0 |
| Status | Draft |
| Owner | Product & Engineering |
| Last Updated | 2026-07-28 |

---

# Purpose

The Domain Model defines the core business entities of PlanYourTrip and the relationships between them.

It provides a common language shared by Product, Engineering, QA, and AI.

---

# Design Principles

The model should be:

- Business-centric
- Technology independent
- Easy to understand
- Extensible
- Modular

The domain model describes the business, not the database.

---

# Core Domains

- User
- Trip
- Destination
- Itinerary
- Budget
- Booking
- Transportation
- Accommodation
- Activity
- AI Assistant
- Notification
- Travel Document

---

# High-Level Domain Relationship

User
│
├── Trips
│     │
│     ├── Destinations
│     ├── Itinerary
│     ├── Budget
│     ├── Bookings
│     ├── Activities
│     ├── Transportation
│     └── Documents
│
└── Preferences

AI Assistant supports every domain.