**Basketball League Simulator (Django)**

A full-stack web application that allows users to create, manage, and simulate custom basketball leagues with realistic scheduling and live standings. Built using Django, this project features dynamic game simulation, role-based access control, and real-time team statistics updates.

Author: Hinsley Casenet

## Features

*League Creation & Management*
  Users can create and manage multiple basketball leagues with custom teams and players.

*Dynamic Game Scheduling*
  Simulates seasons using randomized intervals while respecting rest days and availability for teams.

*Live Standings & Stats*
  Tracks game results, team records, and updates league standings in real-time.

*User Authentication & Role Management*  
  Built with Django Authentication and custom permission logic for admin/user role access.

*Simulator Logic*
  Includes randomized game outcomes, win/loss tracking, and dynamic point scoring simulation.

---

## Tech Stack

- **Backend:** Django ORM, SQLite
- **Frontend:** HTML, CSS (Django Templates)
- **Auth:** Django Authentication System
- **Data Handling:** Relational Models (Teams, Games, Players)
- **Design Principles:** Model-View-Controller architecture, role-based access control

---

## How to Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/basketball-league-simulator.git
cd basketball-league-simulator

# Create virtual environment
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (for admin access)
python manage.py createsuperuser

# Start server
python manage.py runserver
