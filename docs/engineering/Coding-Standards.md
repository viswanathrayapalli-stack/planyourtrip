# Coding Standards

## Purpose

Define the coding practices used throughout PlanYourTrip.

---

## General Principles

- Write code for humans first.
- Keep functions focused on one responsibility.
- Prefer composition over inheritance.
- Avoid premature optimization.
- Avoid duplicate logic.
- Keep implementations simple.

---

## Naming Conventions

### Variables

Use descriptive names.

Good

destinationId

Bad

id1

---

### Functions

Use verb-based names.

calculateBudget()

generateItinerary()

searchDestinations()

---

### Classes

Use nouns.

DestinationService

BudgetCalculator

WeatherProvider

---

### Constants

UPPER_SNAKE_CASE

MAX_ITINERARY_DAYS

---

## File Naming

Python

snake_case.py

TypeScript

kebab-case.ts

React Components

PascalCase.tsx

---

## Folder Naming

Lowercase

Singular where practical

---

## Comments

Explain WHY.

Don't explain WHAT.

---

## Logging

Structured logging only.

Never use print() in production.

---

## Error Handling

Raise meaningful exceptions.

Never silently ignore errors.

---

## Documentation

Public APIs require documentation.

Complex algorithms require explanation.

---

## Refactoring

Leave the code cleaner than you found it.