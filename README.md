# Northstar University Admission System

A beginner-friendly university admission website built with **Python Flask**, HTML, CSS, and SQLite.

## Features
- Home page with university introduction
- Programs/course listing
- Admission application form
- Form validation and successful submission page
- SQLite database stores submitted applications
- Demo admin page to view applications
- Responsive layout for mobile and desktop

## Requirements
- Python 3.9 or newer
- Internet connection for Google Fonts (optional; the site still works without it)

## Run on Windows

1. Extract the ZIP file.
2. Open the extracted `university_admission_system` folder in VS Code.
3. Open Terminal in that folder.
4. Create a virtual environment:

   ```powershell
   python -m venv venv
   ```

5. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\venv\Scripts\Activate.ps1
   ```

6. Install Flask:

   ```powershell
   pip install -r requirements.txt
   ```

7. Start the website:

   ```powershell
   python app.py
   ```

8. Open this address in your browser:

   `http://127.0.0.1:5000`

## Pages
- `/` — Home
- `/programs` — Available programs
- `/apply` — Admission application form
- `/admin` — Demo list of submitted applications

## Database
The first run creates `admissions.db` automatically. Application data is stored locally in this SQLite database.

## Important before real-world use
This is an educational/demo project, not a production admissions portal. The `/admin` page is not password-protected. Before publishing it, add secure administrator login, CSRF protection, stronger validation, HTTPS, privacy notices, backups, and appropriate access controls. Do not enter real sensitive personal information into this demo.
