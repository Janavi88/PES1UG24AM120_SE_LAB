# Lab 2 – Agile Backlog Creation & Sprint Simulation in Jira

## Project
**Smart Lab Equipment & Slot Reservation Portal**

## Objective

The objective of this lab is to convert the functional requirements identified in Lab 1 into an Agile backlog using **Epics and User Stories**, prioritize and estimate the stories using **Story Points**, simulate a Scrum Sprint in Jira, and analyze sprint progress using the **Burndown Chart**.

## Tools Used

- Jira Software
- Scrum Framework
- GitHub

---

# 1. Project Overview

The project is a **Smart Lab Equipment & Slot Reservation Portal** that allows students to view equipment availability, reserve equipment slots, cancel reservations, and enables Lab Technicians to manage equipment status and track equipment usage.

The system also supports late-return detection and disciplinary restrictions for repeated late returns.

---

# 2. Epics

The functional requirements from Lab 1 were converted into the following Epics:

| Epic | Description |
|---|---|
| **Equipment Availability & Reservation** | Allows students to view equipment availability and reserve equipment slots. |
| **Reservation Management** | Allows students to manage and cancel their existing reservations. |
| **Equipment Status Management** | Allows Lab Technicians to manage the status of laboratory equipment. |
| **Equipment Usage Tracking** | Tracks equipment usage through expected and actual return timestamps. |
| **Late Return & Disciplinary Management** | Handles late-return detection and disciplinary restrictions. |

---

# 3. User Stories

## Epic 1 – Equipment Availability & Reservation

### View Equipment Availability
**As a student, I want to view real-time equipment availability, so that I can find an available lab equipment slot.**

- Priority: High
- Story Points: 3

### Reserve Equipment Slot
**As a student, I want to reserve an available equipment slot for up to 2 hours within the next 7 days, so that I can use the equipment when needed.**

- Priority: High
- Story Points: 8

### Generate Reservation Confirmation
**As a student, I want to receive a reservation token after booking equipment, so that I have confirmation of my reservation.**

- Priority: High
- Story Points: 3

---

## Epic 2 – Reservation Management

### Cancel Reservation
**As a student, I want to cancel my reservation before the reserved slot begins, so that the equipment becomes available to other students.**

- Priority: High
- Story Points: 3

---

## Epic 3 – Equipment Status Management

### Update Equipment Status
**As a Lab Technician, I want to update the status of equipment, so that students can see whether the equipment is available for reservation.**

- Priority: High
- Story Points: 5

### Prevent Reservation of Unavailable Equipment
**As a Lab Technician, I want uncalibrated, under-maintenance, and unavailable equipment to be blocked from reservations, so that students only reserve usable equipment.**

- Priority: High
- Story Points: 5

---

## Epic 4 – Equipment Usage Tracking

### Record Expected Return Time
**As a Lab Technician, I want to record the scheduled return time for equipment, so that the system knows when the equipment is expected back.**

- Priority: Medium
- Story Points: 3

### Record Actual Equipment Return Time
**As a Lab Technician, I want to record the actual return time of equipment, so that the system can track whether the equipment was returned on time.**

- Priority: Medium
- Story Points: 3

---

## Epic 5 – Late Return & Disciplinary Management

### Flag Late Returns
**As a Lab Technician, I want the system to automatically flag late equipment returns, so that late-return rules can be enforced.**

- Priority: Medium
- Story Points: 5

### Apply Disciplinary Restriction
**As a Lab Technician, I want to apply disciplinary restrictions to students with repeated late returns, so that disciplinary rules can be enforced.**

- Priority: Medium
- Story Points: 5

---

# 4. Story Point Estimation

Story points were assigned using the **Fibonacci sequence** based on:

- Complexity
- Amount of work
- Risk and uncertainty

Story points represent **relative effort** rather than a direct number of hours.

| Story | Story Points |
|---|---:|
| View Equipment Availability | 3 |
| Reserve Equipment Slot | 8 |
| Generate Reservation Confirmation | 3 |
| Cancel Reservation | 3 |
| Update Equipment Status | 5 |
| Prevent Reservation of Unavailable Equipment | 5 |
| Record Expected Return Time | 3 |
| Record Actual Equipment Return Time | 3 |
| Flag Late Returns | 5 |
| Apply Disciplinary Restriction | 5 |

**Total Backlog Story Points: 43**

---

# 5. Sprint Simulation

A Scrum Sprint was created in Jira to simulate development of the core functionality.

### Sprint Goal

> Implement core equipment reservation and management functionality.

The selected stories were moved through the following workflow:

```text
To Do → In Progress → Done
