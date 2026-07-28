# Entity Relationship Model

---

# Core Entities

User

Trip

Destination

Itinerary

Activity

Budget

Booking

Accommodation

Transportation

Notification

TravelDocument

---

# Relationships

User

1

↓

Many

Trips

Trip

1

↓

Many

Destinations

Trip

1

↓

Many

Bookings

Trip

1

↓

Many

Activities

Trip

1

↓

1

Budget

Trip

1

↓

Many

Travel Documents

Destination

1

↓

Many

Activities

---

# Aggregate Root

Trip

Trip owns:

- Itinerary
- Budget
- Booking
- Activities
- Documents