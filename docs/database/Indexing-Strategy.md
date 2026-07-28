# Indexing Strategy

---

Index Frequently Queried Columns

Examples

email

trip_status

country

city

start_date

---

Composite Indexes

Examples

(user_id, status)

(country, city)

---

Avoid

Indexing every column.

Indexes improve reads but slow writes.

---

Review indexes regularly as usage evolves.