# Schema Design

---

# Primary Keys

UUID

Example

trip_id UUID

---

# Foreign Keys

trip_id

user_id

destination_id

---

# Required Columns

Every table should include:

id

created_at

updated_at

---

# Optional Audit Columns

created_by

updated_by

deleted_at

---

# Constraints

NOT NULL where appropriate.

Use CHECK constraints for valid status values where practical.

Use UNIQUE constraints for natural identifiers (for example, email).

---

# Enumerations

Examples

TripStatus

TripType

BookingStatus

NotificationType