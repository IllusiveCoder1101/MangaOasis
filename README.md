# MangaOasis — Full Stack Manga Streaming Platform

**MangaOasis** is a feature-rich, full-stack web application that allows users to browse, stream, and read manga chapters in a seamless and visually engaging interface. Built with a modern Vue.js frontend and a robust Flask backend, it combines real-time responsiveness with a clean, modular architecture.

## Key Features

- **Manga Streaming Interface** — Browse and read a curated library of manga with a clean, responsive layout.
- **Vue.js Frontend** — Single Page Application (SPA) using Vue Router, Axios, and Vite for fast client-side interactions.
- **Flask API Backend** — Handles routing, manga metadata, and user-related logic using RESTful principles.
- **SQLite Database** — Lightweight and portable — ideal for rapid development and easy deployment.
- **Search & Filter System** — Locate manga by title, genre, or author with real-time query handling.
- **Image Viewer** — Stream panel-by-panel images for each manga chapter with smooth scrolling and layout controls.
- **Modular Architecture** — Frontend and backend are decoupled, allowing for independent development or containerized deployment.

---

## Project Structure

| Directory | Description |
|---|---|
| `backend_v1/` | Flask + SQLite + JWT backend |
| `frontend_v1/` | Vue.js 3 SPA |

### Backend Architecture

```
backend_v1/
├── main.py           # Flask app setup (JWT, CORS, SQLAlchemy, error handlers)
├── api.py            # RESTful API endpoints
├── tables.py         # SQLAlchemy models (Users, Admins, Books, Chapters, etc.)
├── error_handler.py  # Custom exceptions + global error handlers
├── run.py            # Entry point
├── requirements.txt  # Python dependencies (19 packages)
└── database/
    └── mangaOasis.db
```

### Backend Highlights
- Structured JSON error responses for all errors (400, 401, 403, 404, 409, 500)
- Input validation on all POST/PUT endpoints (missing fields return 400 with details)
- Admin endpoints return 403 for non-admin users
- Global exception handler with DB session rollback on 500 errors
- JWT error callbacks (expired, invalid, missing tokens all return JSON)
- Passwords are hashed using scrypt via `werkzeug.security` (no plaintext storage)
- Admin credentials stored in a dedicated `admin` table (no hardcoded values)
- User GET endpoint does not expose password hashes
- Admin registration is protected — only existing admins can register new admins

---

## Tech Stack

### Frontend
- **Vue.js 3** — Reactive SPA framework
- **HTML5 / CSS3** — Layout and styling
- **Axios** — HTTP client for API requests
- **Vite** — Fast bundler for Vue development
- **Chart.js** — Admin dashboard graphs
- **Swiper** — Book carousel

### Backend
- **Python 3 / Flask** — Web API framework
- **SQLite** — Lightweight relational database
- **Flask-JWT-Extended** — JWT authentication
- **Flask-RESTful** — REST API structure
- **Werkzeug** — Password hashing (scrypt)

---

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js & npm

---

### Backend Setup

1. Navigate to `backend_v1/` and create a virtual environment:

    ```bash
    cd backend_v1/
    python -m venv .venv
    source .venv/bin/activate        # On macOS/Linux
    .venv\Scripts\activate           # On Windows
    ```

2. Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask backend:

    ```bash
    python run.py
    ```

   Backend server starts at `http://127.0.0.1:5001`.

---

### Frontend Setup

1. Navigate to `frontend_v1/` and install dependencies:

    ```bash
    cd frontend_v1/
    npm install
    ```

2. Start the development server:

    ```bash
    npm run dev
    ```

   Frontend runs at `http://localhost:5173`.

---

## Default Credentials

### Admin
| Email | Password |
|---|---|
| `admin2004@gmail.com` | `admin2004` |

### Users
| Name | Email | Password |
|---|---|---|
| Akiko Tanaka | `akiko@gmail.com` | `abcd1234` |
| Yui | `yui@gmail.com` | `abcd1234` |
| Riku | `riku@gmail.com` | `abcd1234` |

---

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | `/register_user` | Register a new user | None |
| POST | `/login_user` | User login | None |
| POST | `/login_admin` | Admin login | None |
| POST | `/register_admin` | Register a new admin | Admin JWT |

### Books
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/book` | List all books with chapters | JWT |
| POST | `/book` | Add a new book | Admin JWT |
| PUT | `/book/<book_id>` | Update a book | Admin JWT |
| DELETE | `/book/<book_id>` | Delete a book and related data | Admin JWT |

### Chapters
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/chapter` | List all chapters | JWT |
| POST | `/chapter` | Add a chapter | Admin JWT |
| PUT | `/chapter/<chapter_id>` | Update a chapter | Admin JWT |
| DELETE | `/chapter/<chapter_id>` | Delete a chapter | Admin JWT |

### Users
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/user` | List all users with related data | JWT |
| PUT | `/user/<user_id>` | Update user profile | JWT |
| DELETE | `/user/<user_id>` | Delete a user and related data | JWT |

### Feedback
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/feedback` | List all feedback | JWT |
| POST | `/feedback` | Submit feedback | JWT |
| PUT | `/feedback/<feedback_id>` | Update feedback | JWT |
| DELETE | `/feedback/<feedback_id>` | Delete feedback | JWT |

### Watchlist
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/watchlist` | List all watchlist entries | JWT |
| POST | `/watchlist` | Add to watchlist | JWT |
| DELETE | `/watchlist/<user_id>/<book_id>` | Remove from watchlist | JWT |

### Status (Issue/Purchase flow)
| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/get_status` | List all statuses | JWT |
| POST | `/status/request` | Request a book issue | JWT |
| POST | `/status/buy` | Purchase a book | JWT |
| PUT | `/status/accept/<user_id>/<book_id>` | Accept an issue request | Admin JWT |
| PUT | `/status/expiry/<user_id>/<book_id>` | Update expiry | JWT |
| DELETE | `/status/reject/<user_id>/<book_id>` | Reject an issue request | Admin JWT |
| DELETE | `/status/revoke/<user_id>/<book_id>` | Revoke issued book | Admin JWT |
| DELETE | `/status/auto_revoke/<user_id>/<book_id>` | Auto-revoke expired book | JWT |

---

## Author

**Sankalpa Sarkar**
GitHub: [@IllusiveCoder1101](https://github.com/IllusiveCoder1101)

---

## License

This project is licensed under the **MIT License**. See `LICENSE` for more details.
