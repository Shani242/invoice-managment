# 📊 Invoicely: AI-Powered Invoice Management System

Invoicely is a full-stack automated expense tracking platform. It allows users to upload images of invoices or receipts and uses **Artificial Intelligence** to automatically extract financial data, categorize expenses, and provide a searchable management dashboard.

---

## 🏛️ Architecture Overview

The project is built using a **Decoupled Layered Architecture**, separating the concerns of data extraction, business logic, and user interface.



### 🔹 Backend (FastAPI + PostgreSQL)
Built for high performance and scalability using a **Repository Pattern**:
* **API Layer (`/app/api`):** Handles RESTful communication and enforces data validation via Pydantic schemas.
* **Service Layer (`/app/services`):** The "Brain" of the app. Contains the `OCRService` which manages the complex logic of communicating with Google Vision AI and parsing raw text.
* **Repository Layer (`/app/repositories`):** Decouples the database logic from the API. It handles complex SQL joins and server-side sorting/filtering.
* **Models (`/app/models`):** Defines the relational database schema using SQLAlchemy.

### 🔹 Frontend (React + Tailwind CSS)
A modern, responsive Single Page Application (SPA):
* **Context API:** Provides global authentication state and secure JWT handling.
* **Service Layer:** Centralized Axios instance for communicating with the FastAPI backend.
* **Tailwind CSS:** Utilizes a utility-first approach for a sleek, modern "SaaS" aesthetic with built-in dark-mode support capability.

---

## 🧠 Core Logic & Features

### 1. AI Data Extraction (OCR)
The application uses **Google Cloud Vision** to transform pixels into data. 
* **Multi-Language Support:** The regex engine is optimized for both Hebrew and English invoice formats.
* **Smart Identification:** Automatically detects Business IDs (H.P.), transaction dates, and isolates the "Total Amount" by identifying the highest numerical value in the proximity of financial keywords.

### 2. Scalable Server-Side Management
To ensure the app remains fast even with thousands of invoices:
* **Server-Side Sorting:** Sorting logic is performed by the PostgreSQL engine rather than the browser.
* **Relational Mapping:** Expenses are logically linked to Invoices, allowing for detailed audit trails of every financial record.



### 3. Secure Authentication
* **JWT (JSON Web Tokens):** Secure, stateless authentication flow.
* **Bcrypt:** Industry-standard password hashing to ensure user data security.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React 18, Tailwind CSS, Lucide Icons |
| **Backend** | FastAPI (Python 3.10+), Uvicorn |
| **Database** | PostgreSQL, SQLAlchemy ORM |
| **AI/ML** | Google Cloud Vision API |
| **Auth** | OAuth2 with Password Flow & JWT |

---

## 📁 Project Structure

```text
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers (Invoices, Auth)
│   │   ├── core/         # Security & JWT logic
│   │   ├── models/       # Database entities
│   │   ├── repositories/ # SQL Query logic (Separation of concerns)
│   │   ├── schemas/      # Pydantic models (Data shapes)
│   │   └── services/     # OCR & External AI logic
│   └── main.py           # Entry point
└── frontend/
    ├── src/
    │   ├── components/   # UI Modules (Table, Upload)
    │   ├── context/      # Auth State
    │   ├── pages/        # Dashboard, Login
    │   └── services/     # Axios API configuration