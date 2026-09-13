# 🍅 FocusStudy — A Lightweight Student Focus & Study Management System

> **One-line pitch:** A lightweight study companion that combines task management, a Pomodoro focus timer, and learning-data visualization — so students can plan what to study, actually focus while doing it, and finally *see* where their time went.

<p align="left">
  <img alt="Vue" src="https://img.shields.io/badge/Vue-3.5-4FC08D?logo=vuedotjs&logoColor=white">
  <img alt="Vite" src="https://img.shields.io/badge/Vite-6-646CFF?logo=vite&logoColor=white">
  <img alt="Element Plus" src="https://img.shields.io/badge/Element%20Plus-2.9-409EFF">
  <img alt="ECharts" src="https://img.shields.io/badge/ECharts-5.5-AA344D">
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow">
</p>

---

## 📖 Table of Contents

- [The Problem](#-the-problem)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Reference](#-api-reference)
- [Running the Tests](#-running-the-tests)
- [Project Structure](#-project-structure)
- [Design Decisions](#-design-decisions)
- [Known Limitations](#-known-limitations)
- [Roadmap](#-roadmap)
- [AI Usage Disclosure](#-ai-usage-disclosure)
- [About the Hackathon](#-about-the-hackathon)
- [License](#-license)

---

## 🎯 The Problem

Students don't usually fail because they're lazy. They fail because:

1. **They don't know what to do next.** Tasks live in their head, in chat messages, and on scraps of paper.
2. **They can't hold focus.** "Study for two hours" is an intention, not a plan — and phones win.
3. **They have no feedback loop.** After a week of studying, they genuinely cannot say *which subject* got the time and which got ignored.

Most study apps solve one of these. FocusStudy puts all three in a single small tool: **plan a task → focus on it with a timer → watch the data accumulate.** The loop is the point.

**Target users:** middle school, high school, and university students who want something lighter than Notion and more honest than a to-do list.

---

## ✨ Features

### 1. Task Management
- Create tasks with **name, subject, priority, and deadline**
- Edit, delete, and toggle completion inline
- Completed tasks get a strikethrough style, so progress is visible at a glance
- Live count of unfinished tasks
- **Empty state** instead of a blank table when there's nothing yet

### 2. Pomodoro Focus Timer
- Circular progress countdown with start / pause / reset
- **Configurable focus & break durations** (defaults 25 / 5 min, adjustable in the UI and remembered across sessions)
- **Bind the timer to a task** — when the Pomodoro finishes, the record is automatically tagged with that task's name and subject
- Desktop notification on completion; auto-switches between focus and break mode
- **Leave-page warning** while the timer is running, so an accidental refresh doesn't silently kill your session
- Today's summary (total minutes + Pomodoro count) that stays correct even if the tab stays open past midnight

### 3. Learning Data Visualization
- Summary cards: total minutes focused, Pomodoros completed, subjects covered
- **Bar chart** of the last 7 days of focus time
- **Donut chart** of time distribution across subjects
- Charts resize responsively with the window

### 4. Offline-First Data Layer
This is the feature I'm most deliberate about:

- All data is written to **`localStorage` first** — the app is fully usable with **no backend running at all**
- When the FastAPI backend *is* reachable, changes sync to it in the background
- Network failures degrade silently instead of blocking the UI
- Creating, **editing, completing, and deleting** tasks all sync to the server — not just creating

---

## 🛠 Tech Stack

### Frontend
| Technology | Version | Why this choice |
|---|---|---|
| **Vue 3** | 3.5 | Composition API + `<script setup>` keeps each page's logic readable in one file. Reactive state maps naturally onto a timer and a task list. |
| **Vite** | 6 | Instant dev server and HMR. Zero-config, and it handles the `/api` dev proxy for me. |
| **Vue Router** | 4 | Three clean routes, with lazy loading for the timer and stats pages so the first paint stays fast. |
| **Element Plus** | 2.9 | Production-ready form, table, dialog, and progress components. I customized the theme through CSS variables instead of fighting the defaults. |
| **ECharts** | 5.5 | Bar and pie charts with a mature option API; wrapped in one reusable component. |

### Backend
| Technology | Version | Why this choice |
|---|---|---|
| **Python** | 3.10+ | Readable, and the best language for me to learn data handling in. |
| **FastAPI** | 0.115 | Type-hint-driven validation via Pydantic, plus automatic interactive docs at `/docs` — which made front/back integration dramatically easier to debug. |
| **Uvicorn** | 0.32 | Standard ASGI server, one command to run. |

### Storage
| Technology | Why |
|---|---|
| **`localStorage`** | Primary store. Works offline, survives refresh, zero setup. |
| **JSON files** | Server-side store. Deliberately database-free so a judge can clone and run without installing MySQL/Postgres. |

### Testing
| Technology | Why |
|---|---|
| **pytest** | Unit tests for the pure statistics logic. |
| **FastAPI TestClient** | Integration tests that hit real HTTP endpoints against a temp data directory. |

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────┐
│              Browser (Vue 3 SPA)             │
│                                              │
│  TasksView   TimerView   StatsView           │
│      │           │           │               │
│      └───────────┴───────────┘               │
│                  │                           │
│           api.js (fetch wrapper)             │
│                  │                           │
│        localStorage  ←── offline fallback    │
└──────────────────┼───────────────────────────┘
                   │  /api/*  (Vite dev proxy)
                   ▼
┌──────────────────────────────────────────────┐
│            FastAPI (main.py)                 │
│   routing + Pydantic validation + HTTP codes │
│                  │                           │
│                  ▼                           │
│           stats.py (pure logic)              │
│      aggregation · grouping · lookup         │
│                  │                           │
│                  ▼                           │
│        data/tasks.json · records.json        │
└──────────────────────────────────────────────┘
```

**The key architectural idea** is the split between `main.py` and `stats.py`: HTTP concerns live in the routing layer, while all aggregation logic is pure functions with no file or network access. That makes the business logic fully unit-testable, and it's the main thing I'd point a reviewer toward.

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version | Check with |
|---|---|---|
| Node.js | ≥ 18 | `node -v` |
| Python | ≥ 3.10 | `python --version` |
| Git | any | `git --version` |

### 1. Clone

```bash
git clone https://github.com/Duckweed-yhb/Beginner-s-Paradise-FirstCommit.git
cd Beginner-s-Paradise-FirstCommit
```

### 2. Start the Backend

```bash
cd focusstudy-server

# Create and activate a virtual environment
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API on port 8000
uvicorn main:app --reload --port 8000
```

Verify it's alive: <http://127.0.0.1:8000/> → `{"message":"FocusStudy API 运行中", ...}`
Interactive API docs: <http://127.0.0.1:8000/docs>

### 3. Start the Frontend

In a **second terminal**:

```bash
cd focusstudy-web
npm install
npm run dev
```

Open <http://localhost:5173> — the Vite dev server proxies every `/api/*` request to the backend on port 8000 automatically.

> **The backend is optional.** If you skip step 2 entirely, the frontend still works: it falls back to `localStorage`, and a failed request never blocks the UI. This is intentional, not an accident.

### 4. Production Build

```bash
cd focusstudy-web
npm run build      # outputs to dist/
npm run preview    # serve dist/ locally to verify
```

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `port 5173 already in use` | Another Vite instance is running | Kill it, or `npm run dev -- --port 5174` |
| `Module not found: fastapi` | Virtualenv not activated | Re-run the activate command for your OS |
| Frontend loads but data doesn't persist to server | Backend not running, or on a different port | Start uvicorn on **8000**, or update the proxy target in `focusstudy-web/vite.config.js` |
| Charts don't render | Zero records so far | Complete one Pomodoro; the stats page shows an empty state until then |
| CORS error in console | Frontend served from an unexpected origin | Add that origin to `allow_origins` in `focusstudy-server/main.py` |

---

## 🔌 API Reference

Base URL: `http://127.0.0.1:8000`

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/tasks` | List all tasks |
| `POST` | `/api/tasks` | Create a task → `201` |
| `PUT` | `/api/tasks/{task_id}` | Partially update a task (edit / complete / uncomplete) |
| `DELETE` | `/api/tasks/{task_id}` | Delete a task |

<details>
<summary><b>Request / response examples</b></summary>

**POST `/api/tasks`**

```json
{
  "name": "Finish Chapter 5 exercises",
  "subject": "Math",
  "priority": "high",
  "deadline": "2026-09-20"
}
```

Response `201`:

```json
{
  "name": "Finish Chapter 5 exercises",
  "subject": "Math",
  "priority": "high",
  "deadline": "2026-09-20",
  "id": 1789000000000,
  "done": false
}
```

**PUT `/api/tasks/{id}`** — send only what changes; other fields are preserved.

```json
{ "done": true }
```

Constraints enforced by Pydantic: `name` length 1–100, `priority` ∈ `high | medium | low`. Violations return `422`; unknown ids return `404`.

</details>

### Focus Records

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/records` | List all focus records |
| `POST` | `/api/records` | Create a record → `201` |
| `DELETE` | `/api/records/{record_id}` | Delete a record |

```json
{
  "taskName": "Finish Chapter 5 exercises",
  "subject": "Math",
  "minutes": 25,
  "date": "2026-09-10"
}
```

`minutes` must be 1–1440. If `date` is omitted or empty, the server fills in **its own local date** (not UTC — see [Design Decisions](#-design-decisions)).

### Statistics

`GET /api/stats`

```json
{
  "total_minutes": 100,
  "total_count": 3,
  "by_subject": { "Math": 50, "English": 50 },
  "by_date": { "2026-09-09": 25, "2026-09-10": 75 }
}
```

### System

`GET /` — health check, returns the running version and today's local date.

---

## 🧪 Running the Tests

```bash
cd focusstudy-server

# Install test dependencies (includes the runtime ones)
pip install -r requirements-dev.txt

# Run everything
python -m pytest -v
```

The suite covers two layers:

- **`tests/test_stats.py`** — pure logic: aggregation, grouping, and dirty-data tolerance (missing fields, `None`, numeric strings, `bool` sneaking in as an `int` subclass, empty lists).
- **`tests/test_api.py`** — real HTTP through `TestClient`: status codes, `422` validation, `404` handling, partial-update semantics, local-date filling, and the resilience case where `data/*.json` is corrupted on disk.

Tests point the data directory at a pytest temp folder, so **running them never touches your real `data/`**.

---

## 📁 Project Structure

```
Beginner-s-Paradise-FirstCommit/
├── README.md                      # ← you are here
├── LICENSE                        # MIT
├── HACKATHON.md                   # Hackathon rules, judging criteria, prizes
├── 项目日记.md                     # Project diary: milestones & daily plan
├── 学习日志.md                     # Learning log: what I learned each lesson
├── 零基础前置学习路线...md          # Prerequisite learning roadmap
├── 项目实战开发路线...md            # Development roadmap
│
├── FocusStudy课程/                 # 19-lesson self-study course (00–18)
│   ├── 00-课程总览与学习地图.md
│   ├── 01-...md ~ 18-...md
│   └── 课程地图.html
│
├── focusstudy-web/                # Frontend (Vue 3 + Vite)
│   ├── index.html
│   ├── vite.config.js             # dev server + /api proxy + build chunking
│   ├── package.json
│   └── src/
│       ├── main.js                # app bootstrap, Element Plus registration
│       ├── App.vue                # layout shell + top navigation
│       ├── api.js                 # single place for all backend calls
│       ├── storage.js             # localStorage layer + shared keys
│       ├── time.js                # local-date helpers (timezone-safe)
│       ├── styles.css             # global theme (tomato-orange primary)
│       ├── router/index.js        # 3 routes, lazy-loaded
│       ├── components/
│       │   └── BaseChart.vue      # reusable ECharts wrapper
│       └── views/
│           ├── TasksView.vue      # task management
│           ├── TimerView.vue      # Pomodoro timer
│           └── StatsView.vue      # data visualization
│
└── focusstudy-server/             # Backend (FastAPI)
    ├── main.py                    # HTTP layer: routes, validation, status codes
    ├── stats.py                   # pure aggregation logic (unit-tested)
    ├── requirements.txt           # runtime deps
    ├── requirements-dev.txt       # + pytest, httpx
    ├── pytest.ini
    ├── tests/
    │   ├── test_stats.py
    │   └── test_api.py
    └── data/                      # JSON storage (gitignored)
```

---

## 🧠 Design Decisions

These are the choices I'd want a reviewer to ask me about, and the reasoning behind each.

**1. Why no database?**
The judging criteria reward a runnable project over an impressive tech stack, and "Technical Execution" explicitly says the stack doesn't need to be advanced, only *justified*. A JSON file means a judge can clone, `pip install`, and run in under two minutes with zero infrastructure. For a single-user study tool, a database would add setup friction and buy nothing.

**2. Why is the frontend still fully usable without the backend?**
Because a study tool that breaks when the network does is worse than useless — it's a distraction during exactly the moment you're trying to concentrate. `localStorage` is the source of truth for the UI; the server is a sync target. Every network call is wrapped so that failure is invisible rather than fatal.

**3. Why split `main.py` and `stats.py`?**
Mixed routing and business logic can only be tested by spinning up the whole server and asserting on HTTP responses. Pulling aggregation into pure functions means the actual logic gets fast, direct unit tests — including the ugly inputs (dirty records, `bool` masquerading as `int`) that are painful to produce through the API.

**4. Local dates, not UTC — and this was a real bug.**
JavaScript's `toISOString().slice(0, 10)` returns the **UTC** date. In UTC+8, a Pomodoro finished at 00:30 local time was being filed under the previous day. I switched to deriving the date from the local timezone on both sides. Small bug, but it silently corrupts exactly the data the whole app exists to collect.

**5. Why compute "today" reactively instead of once at page load?**
`const today = new Date()` evaluated once in `setup()` freezes for as long as the tab stays open. Leave the timer page open past midnight and the "today's summary" card silently reports the wrong day. Deriving it from a reactive tick keeps it correct.

**6. Why does `PUT` accept partial updates?**
Because ticking a checkbox should not require the client to echo back every other field. If the UI sends only `{"done": true}`, a naive full-replace would wipe the task's name, subject, and deadline. `exclude_none=True` on the update model makes "only what changed" the contract.

**7. Why is the timer still `setInterval`-based?**
It's the simplest thing that works, and correctness here is about the *display*, not precision timekeeping. A production version would store the target end timestamp and compute the remainder on each tick, so tab throttling couldn't cause drift — noted in the limitations as a known tradeoff rather than pretended away.

---

## ⚠️ Known Limitations

I'd rather list these honestly than have a reviewer find them.

- **Single user, no auth.** Anyone who can reach the server sees the same data. Out of scope for a personal tool, but it means this isn't deployable as a public multi-user service.
- **`setInterval` drift.** Background-tab throttling can make the countdown lag behind wall-clock time.
- **No concurrent-write protection.** Two simultaneous writers to the same JSON file could lose a write. Acceptable for one user; would need locking or a real database for many.
- **localStorage/server reconciliation is naive.** If the same data diverges, local wins. There's no merge strategy, no timestamps, no conflict resolution.
- **Frontend tests are missing.** Backend logic has real coverage; the Vue components are verified manually via a checklist (see Lesson 16). Adding Vitest is on the roadmap.
- **`/api/stats` trusts the stored `minutes` field.** It tolerates *malformed* data but doesn't re-derive minutes from session start/end times, since those aren't stored.

---

## 🗺 Roadmap

- [ ] Store session start/end timestamps so durations are verifiable, not just asserted
- [ ] Timestamp-based timer to eliminate background-throttling drift
- [ ] Vitest + Vue Test Utils for component-level tests
- [ ] Export/import data as JSON so students can back up or move devices
- [ ] Weekly and monthly trend views beyond the current 7-day window
- [ ] PWA support for genuine offline installation

---

## 🤖 AI Usage Disclosure

The hackathon rules require disclosing where AI assistance was used. Being precise about this matters more than looking impressive.

**AI was used for:**
- Explaining unfamiliar concepts (Vite's proxy config, ECharts option schema, Pydantic validators, FastAPI dependency injection)
- Debugging: interpreting error messages and console traces when I got stuck
- Reviewing code I had already written — pointing out the UTC/local date bug, the stale `today` value, and the deprecated `el-radio-button` API
- Drafting and tightening this README's English wording
- Generating the initial structure of the pytest suite, which I then read, ran, and corrected until it passed

**AI was NOT used for:**
- Deciding what the project should be, or what its three core features are
- Designing the data model (task and focus-record schemas)
- Writing the task management, timer, or statistics logic in the first place
- Choosing the tech stack
- Producing any code that I have not read and understood well enough to explain

**What I verified myself:** every endpoint was exercised in the browser and through `/docs`; the test suite was run locally (`python -m pytest -v`) and passes; the production build succeeds (`npm run build`).

The core business logic — task CRUD, the Pomodoro state machine, and the aggregation rules — was written by hand first, following the "read → type → modify → explain" method in the course materials. Full details, including specific bugs and how I found them, are in [`学习日志.md`](学习日志.md).

---

## 🏆 About the Hackathon

This project was built for **Beginner's Paradise — FirstCommit**, a beginner-friendly online hackathon for students aged 13–21.

- **Judging weights:** Learning & Growth **30%** · Creativity & Impact **25%** · Technical Execution **25%** · Presentation **20%**
- **Submission requirements:** runnable project, public GitHub repo, project description, 3–5 minute demo video, and a README with run instructions

Full rules, prize breakdown, and submission checklist: [`HACKATHON.md`](HACKATHON.md)

Because "Learning & Growth" carries the heaviest weight, the development process is documented in detail rather than hidden:
- [`学习日志.md`](学习日志.md) — lesson-by-lesson record of concepts learned, obstacles hit, and how each was resolved
- [`项目日记.md`](项目日记.md) — project milestones and evolving design thinking

---

## 📄 License

[MIT](LICENSE) © 2026 Duckweed-yhb

Free to use, modify, and learn from.
