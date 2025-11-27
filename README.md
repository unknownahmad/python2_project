



========================================================================================================
                       ⭐ Champions League Gambling Simulator (GUI Edition) ⭐
========================================================================================================



Authors:

-Amal El Haj
-Ahmad Sbai


========================================================================================================
🎮 Description

Champions League Gambling Simulator is an interactive Python GUI application where users can register, log in, choose a team, place bets, and simulate a Champions League–style knockout tournament.

It uses a full Tkinter-based interface with betting mechanics, AI-powered football facts, user statistics, and a persistent database.

This project demonstrates modular decomposition, OOP, API integration, error handling, data validation, and GUI design — fulfilling the full set of project criteria.


=========================================================================================================

🎯 Purpose of the Program

The program aims to create an immersive football betting simulation while showcasing:

-Graphical UI design

-Authentication + registration system

-Age verification

-Database usage

-AI integration

-Threaded match simulation

-Logging & statistics

-Python core concepts (functions, OOP, decorators, lambda, generators, etc.)

=========================================================================================================

🧪 Main Features

    ✔ User System

        -Register / Login

        -Password validation via regex

        -Age verification (21+)

        -Persistent user data saved in SQLite

    ✔ Premium User Upgrade

        -Using class inheritance, users with total winnings ≥ 10,000 become:

        -PremiumUser
        
        -A premium badge is displayed in the GUI.

    ✔ Tournament Simulation

        -Round of 16

        -Quarter Finals

        -Semi Finals

        -Final

        -Realistic score + penalty shootouts

        -Cash-out option

        -Threaded execution (no GUI freeze)

    ✔ AI Integration (DeepSeek API)

        -A fun football fact appears on the login screen.

    ✔ External File Usage

        -SQLite database

        -Logger file

        -External .env for storing API secret

        -External team file (teams.txt)

    ✔ GUI Features

        -Modern styling

        -Coloured UI

        -Horizontal button layout

        -Premium user banner

        -Scrollable match output box

=========================================================================================================

📦 Project Structure

    python2_project/
    ├── data/
    │   ├── teams.txt
    │   ├── test_users.db
    │   ├── user.txt
    │   └── users.db
    │
    ├── logs/
    │   ├── game_log.txt
    │   └── results.txt
    │
    ├── tests/
    │   ├── __pycache__/
    │   ├── __init__.py
    │   ├── test_auth_db.py
    │   ├── test_simulate_match_terminal.py
    │   ├── test_valid_password.py
    │
    ├── auth.py
    ├── betting.py
    ├── conftest.py
    ├── db.py
    ├── deepseek_client.py
    ├── desktop.ini
    ├── gui_login.py
    ├── gui_main.py
    ├── logger.py
    ├── main.py
    ├── menu.py
    ├── private.env
    ├── README.md
    ├── requirements.txt
    ├── tournament.py
    ├── user.py
    └── utils.py


=========================================================================================================


🛠️ Installation & Setup

    1. Clone the repository
    git clone <your-repo-url>
    cd project-folder

    2. Create a virtual environment
    python -m venv venv
    source venv/bin/activate         # Mac/Linux
    venv\Scripts\activate            # Windows

    3. Install dependencies
    pip install -r requirements.txt

    4. Create private.env

    Inside the root folder add:

    DEEPSEEK_API_KEY=your_api_key_here

    5. Run the app
    python main.py

=========================================================================================================

🎥 How to Use

    Open the program

    Register (must be 21+)

    Log in

    Select your team

    Enter bet amount

    Start the tournament

    After each round choose:

    Continue

    Cash Out

    Winnings multiply each round — reach 10,000+ total, and you become a Premium User.

=========================================================================================================

🧩 Completed Criteria Checklist

    ✔ Menu / Interaction

        GUI handles all navigation

        No restarting required

        Exit only via logout

    ✔ Decomposition

        All logic split across multiple modules

        No long files

        main.py only launches GUI

    ✔ Git Deployment

        requirements.txt

        .gitignore

        README.md

        Multiple commits

    ✔ External File Usage

        SQLite database (🌶️ bonus)

        Text files

        Logs

        .env for secrets

    ✔ API Usage

        DeepSeek AI integration

        Displays fun football facts

    ✔ Connected AI (🌶️ bonus)

    ✔ Testing

        Pytest tests for auth & password validation

    ✔ Data Structures

        Lists → teams

        Dicts → multipliers

        Tuples → DB rows

        Sets → unique teams

        Generators → team_generator

        Lambda → alphabetical sorting

        Decorator → logging decorator

    ✔ OOP

        User class

        PremiumUser class (inheritance)

    ✔ Validation

        Regex password validation

        Error handling everywhere

    ✔ Logging

        All major actions logged

    ✔ Submission on Time (🌶️ bonus)

=========================================================================================================

❤️ Acknowledgements

    DeepSeek API

    Tkinter documentation

    Python SQLite

    Official Logging docs