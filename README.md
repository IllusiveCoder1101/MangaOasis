# 🌸 MangaOasis — Full Stack Manga Streaming Platform

**MangaOasis** is a feature-rich, full-stack web application that allows users to browse, stream, and read manga chapters in a seamless and visually engaging interface. Built with a modern Vue.js frontend and a robust Flask backend, it combines real-time responsiveness with asynchronous task handling for an optimized experience. Designed with scalability and modularity in mind, MangaOasis is ideal for manga fans and developers alike who want a clean, extensible streaming platform.


## 🌟 Key Features

- 📖 **Manga Streaming Interface**  
  Browse and read a curated library of manga with a clean, responsive layout.

- ⚡ **Vue.js Frontend**  
  Single Page Application (SPA) using Vue Router, Axios, and Vite for fast client-side interactions.

- 🔧 **Flask API Backend**  
  Handles routing, manga metadata, and user-related logic using RESTful principles.

- 💾 **SQLite Database**  
  Lightweight and portable—ideal for rapid development and easy deployment.

- 🔁 **Asynchronous Task Queue**  
  Redis + Celery power background jobs like image preprocessing, chapter indexing, or scheduled updates.

- 🔍 **Search & Filter System**  
  Locate manga by title, genre, or author with real-time query handling.

- 🖼️ **Image Viewer**  
  Stream panel-by-panel images for each manga chapter with smooth scrolling and layout controls.

- 🔄 **Modular Architecture**  
  Frontend and backend are decoupled, allowing for independent development or containerized deployment.

- 🧪 **Developer Friendly**  
  Clean project structure with clear separation of concerns and environment variable support.

---
---

## 📦 Tech Stack

### Frontend
- **Vue.js** – Reactive SPA framework
- **HTML5 / CSS3** – Layout and styling
- **Axios** – HTTP client for API requests
- **Vite** – Fast bundler for Vue development

### Backend
- **Python 3 / Flask** – Web API framework
- **SQLite** – Lightweight relational database
- **Redis** – Message broker for async jobs
- **Celery** – Distributed task queue

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js & npm
- Redis server (running locally or remotely)

---

### 🔧 Backend Setup

1. Create and activate a virtual environment:

    ```bash
    python -m venv env
    env\Scripts\activate        # On Windows
    ```

2. Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure environment variables:  
   Create a `.env` file in the root directory with the following keys:

    ```
    FLASK_APP=run.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    DATABASE_URL=sqlite:///db.sqlite3
    REDIS_URL=redis://localhost:6379/0
    ```

4. Run the Flask backend:

    ```bash
    python run.py
    ```

   Backend server starts at `http://127.0.0.1:5000`.

---

### 🌐 Frontend Setup

1. Move into the `frontend/` folder:

    ```bash
    cd frontend/
    ```

2. Install dependencies and start the development server:

    ```bash
    npm install
    npm run dev
    ```

   Frontend runs at `http://localhost:5173`.

---

---

## 🧑‍💻 Author

**Sankalpa Sarkar**  
GitHub: [@IllusiveCoder1101](https://github.com/IllusiveCoder1101)  
📬 Email: snklpsrkr@gmail.com

---

## 📜 License

This project is licensed under the **MIT License**. See `LICENSE` for more details.

---

> _Built for manga lovers, by a manga lover. Dive into your digital manga haven — MangaOasis!_
