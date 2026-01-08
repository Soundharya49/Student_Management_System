# Student Management System

A simple system to manage student data using Flask, MongoDB, and React.

## Prerequisites

- Python 3.8+
- Node.js & npm (for frontend)
- MongoDB

## Setup

### Backend

1. Navigate to the backend directory:
   ```sh
   cd backend
   ```
2. Create and activate virtual environment:
   ```sh
   python -m venv venv
   # Windows:
   .\venv\Scripts\Activate
   # Linux/Mac:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the backend:
   ```sh
   python app.py
   ```
   
### Frontend

1. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```s
   npm install
   ```
3. Start the development server:
   ```sh
   npm run dev
   ```
   

## Usage

1. Open the frontend in your browser.
2. Login using the credentials defined in `backend/.env`.
3. Use the dashboard to Add, Edit, or Delete students.
