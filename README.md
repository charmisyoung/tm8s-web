# ⚽ tm8s (Teammates)

**tm8s** is a full-stack web application that allows users to instantly discover the connection between two footballers.

Enter two names (e.g., "Messi" and "Neymar"), and the app scans their entire career history to find exactly which clubs they played for together and during which years.

## ✨ Features

- **Global Search:** Finds players from leagues all over the world using **TheSportsDB** API.
- **Smart Caching:** Implements a local **SQLite** caching layer to minimize API calls and speed up repeat searches.
- **Visual Results:** Displays authentic club crests for every matching connection.
- **Intelligent Filtering:** Automatically detects and filters out "Managerial" roles (e.g., preventing Duncan Ferguson from matching with current Everton players).
- **Fault Tolerance:** Robust error handling for missing API data, broken image links, and "dirty" datasets.

## 🏗️ Tech Stack

### Frontend
- **Framework:** React 18
- **Language:** TypeScript
- **Build Tool:** Vite
- **Styling:** CSS3 (Custom skewed card effects)

### Backend
- **Framework:** FastAPI
- **Language:** Python 3.11+
- **Database:** SQLite + SQLModel (ORM)
- **API:** TheSportsDB (Free Tier)

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have the following installed on your machine:
- [Node.js](https://nodejs.org/) (v18 or higher)
- [Python](https://www.python.org/) (v3.10 or higher)

### 2. Installation

Clone the repository and set up the environments for both server and client.

#### Backend Setup
```bash
cd tm8s-web
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

pip install -r requirements.txt

