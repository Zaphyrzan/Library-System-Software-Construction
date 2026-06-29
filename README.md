# Reading Room — Library Management System

A medium-scale Library Management System built with **Django REST Framework** (backend API)
and **React + Vite** (frontend SPA), with **JWT authentication** and a **SQLite** database.

Built for SECJ4383 Software Construction. The system implements the domain model and the five
components designed in Assignment 1.

---

## Architecture

```
Frontend (React + Vite, :5173)  ──HTTP/JSON + JWT──►  Backend (Django REST, :8000)  ──►  SQLite
```

Each Assignment-1 component maps to one Django app:

| Component (Assignment 1) | Django app | Key models |
|---|---|---|
| Catalog Management | `catalog` | Book, Author, Category, BookCopy |
| Member Management & Auth | `members` | Member, Membership, Staff |
| Circulation / Loan | `circulation` | Loan (+ `services.py`) |
| Reservation Management | `reservations` | Reservation (+ `services.py`) |
| Reporting & Fines | `reporting` | Fine, Notification (+ `services.py`) |

Business logic lives in each app's `services.py` so views stay thin and components can call
each other cleanly (e.g. returning a loan issues a fine **and** advances the reservation queue).

---

## Prerequisites

- Python 3.11+
- Node.js 18+

---

## 1. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data       # loads sample books, members, loans, a fine and a hold
python manage.py runserver
```

The API is now at `http://localhost:8000/api/`.
Django admin is at `http://localhost:8000/admin/`.

**Demo logins** (created by `seed_data`):

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | Superuser (admin site) |
| `librarian` | `library123` | Library staff (use this to log into the app) |

---

## 2. Frontend setup

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` and sign in with `librarian / library123`.

> If your backend runs on a different URL, create `frontend/.env` with
> `VITE_API_URL=http://localhost:8000/api`.

---

## Main features (demo walkthrough)

1. **Dashboard** — live counts of titles, copies, members, active/overdue loans, holds and fines.
2. **Catalog** — search books by title, author or ISBN; see available vs total copies.
3. **Members** — view borrowers, their membership rules and active loan counts.
4. **Loans** — issue a loan (validates membership limit + copy availability) and return it.
5. **Reservations** — place a hold; the queue advances automatically on return.
6. **Reports & Fines** — overdue list and outstanding fines; mark fines paid.

**Suggested demo path:** issue a loan on the Loans page → return it → if it was overdue a fine
appears under Reports → any pending hold for that title flips to *Ready for pickup*.

---

## Key API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/token/` | Obtain JWT access + refresh tokens |
| GET | `/api/catalog/books/?search=` | List / search books |
| GET | `/api/members/members/` | List members |
| POST | `/api/circulation/loans/checkout/` | Issue a loan `{member_id, copy_id}` |
| POST | `/api/circulation/loans/{id}/return/` | Return a loan |
| POST | `/api/reservations/reservations/reserve/` | Place a hold `{member_id, book_id}` |
| GET | `/api/reporting/reports/` | Dashboard summary |
| POST | `/api/reporting/fines/{id}/pay/` | Mark a fine paid |

---

## Project structure

```
library_management_system/
├── backend/
│   ├── library_system/        # project settings + root URLs
│   ├── catalog/  members/  circulation/  reservations/  reporting/
│   ├── core/                  # seed_data management command
│   ├── manage.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/client.js       # axios + JWT interceptor
    │   ├── context/AuthContext.jsx
    │   ├── components/         # Navbar, ProtectedRoute
    │   └── pages/              # Dashboard, Catalog, Members, Loans, Reservations, Reports
    └── package.json
```

---

## AI Usage Declaration

We used AI tools (ChatGPT/Claude, GitHub Copilot, and an AI UI tool) to support idea generation,
coding, debugging, documentation and testing. All AI-generated outputs were reviewed, tested,
modified and validated by the group members. We take full responsibility for the final submitted work.
