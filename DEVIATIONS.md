# Cruddur — Scaffold Deviations & Engineering Decisions

**Project:** Cruddur — Cloud-native microblogging platform  
**Base:** AWS Bootcamp 2023 scaffold (Andrew Brown)  
**Status:** Independent build — no active cohort as of November 2024  
**Engineer:** Robert  

---

## Context

This project began as an AWS bootcamp scaffold but was deliberately extended beyond the tutorial scope. With no active cohort or schedule constraints, the decision was made to build toward production-quality patterns rather than tutorial completion. Every deviation below represents a conscious architectural or engineering decision made for real-world reasons.

---

## Deviation #1 — Base Docker Image Upgrade

**File:** `backend-flask/Dockerfile`

| | Scaffold | Our Build |
|---|---|---|
| Base image | `python:3.10-slim-buster` | `python:3.10-slim-bullseye` |

**Why:** Debian Buster reached end-of-life. The `deb.debian.org` repositories returned 404 for all Buster packages, making `apt-get` operations impossible. Upgraded to Bullseye (current stable Debian) to restore package management functionality.

**Interview talking point:** Recognized and resolved an EOL base image issue — a common real-world problem in long-running containerized applications.

---

## Deviation #2 — Added psql Client to Backend Image

**File:** `backend-flask/Dockerfile`

| | Scaffold | Our Build |
|---|---|---|
| psql client | Not included | Installed via apt-get |

```dockerfile
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*
```

**Why:** The scaffold assumed schema migrations would be run locally or via scripts. In our ECS Fargate deployment, the RDS instance is in a private subnet with no public access. The only path to run migrations was from inside the VPC — specifically via ECS one-off tasks using the backend container. psql had to be in the image.

**Interview talking point:** Solved a real infrastructure problem — private RDS with no public access — by packaging the migration tooling into the application image and running ephemeral ECS tasks for schema management.

---

## Deviation #3 — Password Recovery Flow Architecture

**File:** `frontend-react-js/src/pages/RecoverPage.js`

| | Scaffold | Our Build (Planned) |
|---|---|---|
| Pattern | Amplify SDK stubs (`Auth.forgotPassword`) | Flask proxy endpoints |
| Endpoints | None — frontend direct | `/api/auth/forgot`, `/api/auth/forgot/confirm` |
| Cognito integration | Frontend direct via Amplify | Backend via boto3 |

**Why:** The existing signin flow uses Amplify/Cognito directly on the frontend, but recovery was implemented as stubs only. Rather than completing the stubs with Amplify, we chose to route recovery through Flask for consistency with production patterns — keeping Cognito credentials server-side and centralizing auth error handling.

**Interview talking point:** Made a deliberate architectural decision to deviate from the scaffold pattern in favor of a proper auth proxy pattern — and can articulate why.

---

## Deviation #4 — Schema Migration Strategy

**File:** `backend-flask/db/schema.sql`

| | Scaffold | Our Build |
|---|---|---|
| Migration method | Local scripts / dev environment | ECS Fargate one-off tasks |
| Execution context | Developer machine | Inside VPC via ephemeral container |

**Why:** RDS is in a private subnet. CloudShell and local machines have no network path to the database. The only VPC-internal execution environment available was ECS itself. We ran schema migrations as ephemeral ECS Fargate tasks using command overrides — a production-standard pattern for containerized migration workflows.

**Key technical challenge:** ECS command overrides require JSON array format. Console input mangles this — CLI is required for reliable execution.

**Interview talking point:** Solved a non-trivial infrastructure problem — running DB migrations against a private RDS with no public access — using ECS one-off tasks. Can explain the full network topology and why each other option (CloudShell, bastion, VPN) was unavailable or impractical.

---

## Deviation #5 — Replies Table Added to Schema

**File:** `backend-flask/db/schema.sql`

| | Scaffold | Our Build |
|---|---|---|
| replies table | Dropped via CASCADE, never recreated | Fully defined with proper columns |

**Why:** The scaffold dropped the replies table in schema.sql but never included a CREATE TABLE for it. The `data_home` query referenced replies in a subquery, causing runtime errors. We defined the full replies schema.

```sql
CREATE TABLE public.replies (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_uuid UUID NOT NULL,
  activity_uuid UUID NOT NULL,
  reply_to_activity_uuid UUID NOT NULL,
  message text NOT NULL,
  likes_count integer DEFAULT 0,
  replies_count integer DEFAULT 0,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```

---

## Deviation #6 — Fixed Denormalized Query Pattern

**File:** `backend-flask/app.py` — `data_home()` route

| | Scaffold | Our Build |
|---|---|---|
| Handle source | `a.handle` (from activities table) | `u.handle` via JOIN to users |
| Query pattern | Denormalized — handle stored on activities | Normalized — handle retrieved via FK join |

**Why:** The scaffold selected `a.handle` from the activities table, but the activities schema has no handle column. Handle belongs to users. We added a proper LEFT JOIN:

```sql
FROM activities a
LEFT JOIN public.users u ON u.uuid = a.user_uuid
```

**Interview talking point:** Identified and corrected a normalized vs denormalized data model mismatch. The scaffold was designed assuming a denormalized schema that didn't match the actual table definitions.

---

## Deviation #7 — db/ Folder Moved Into Backend Build Context

**File/Directory:** `db/` folder location

| | Scaffold | Our Build |
|---|---|---|
| db/ location | Repo root (`/db/schema.sql`) | Inside backend-flask (`/backend-flask/db/schema.sql`) |

**Why:** Docker's build context is scoped to the directory containing the Dockerfile. Files outside that directory cannot be included in the image. The scaffold placed `db/` at the repo root — inaccessible to the backend Dockerfile. We moved it inside `backend-flask/` to make schema and seed files available inside the container for ECS-based migrations.

---

## Deviation #8 — Seed Data with Realistic Content

**File:** `backend-flask/db/seed.sql`

| | Scaffold | Our Build |
|---|---|---|
| Users | Andrew Brown, Andrew Bayko | Andrew Brown, Andrew Bayko, Robert |
| Activities | None | 3 realistic cloud-engineering themed posts |

**Why:** Demo-ready seed data tells a story. Activities reference actual AWS concepts used in the project, making the demo more credible in interview settings.

---

## Architecture Summary

```
Internet
    │
    ▼
ALB (Application Load Balancer)
    ├── /* → frontend-react-js (ECS Fargate)
    └── /api/* → backend-flask (ECS Fargate)
                      │
                      ▼
              RDS PostgreSQL (private subnet)
              - users table
              - activities table  
              - replies table
              
              Schema migrations via:
              ECS one-off Fargate tasks (command override)
```

---

## Task Definition Versioning Log

| Revision | Change |
|---|---|
| :7 | Original scaffold deployment |
| :8 | First fix attempt (image not updated correctly) |
| :9 | JOIN fix for u.handle |
| :10 | Removed reposts_count from replies subquery |
| :11 | Removed trailing comma from replies subquery |

---

## Key Interview Talking Points

1. **Private RDS migration problem** — no public access, solved with ECS one-off tasks
2. **EOL base image** — identified Debian Buster EOL, upgraded to Bullseye
3. **Scaffold vs production patterns** — conscious deviation from Amplify SDK to Flask auth proxy
4. **Schema normalization** — fixed denormalized query assumption in scaffold code
5. **Docker build context** — understood and solved build context scoping issue
6. **ECS command override format** — JSON array required, console mangles it, CLI is reliable
7. **Task definition versioning** — understand why force-new-deployment alone doesn't pull new image when tag is reused
