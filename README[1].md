# Django Internship Assignment

## Features:
- DRF APIs (public/private)
- JWT Authentication
- Celery + Redis background tasks
- Telegram Bot storing usernames

## Setup
1. Clone repo & `cd` into project
2. Create `.env` file from `.env.example`
3. Install packages: `pip install -r requirements.txt`
4. Migrate DB: `python manage.py migrate`
5. Run dev server: `python manage.py runserver`
6. Run Celery: `celery -A internship_project worker -l info`
7. Start Telegram Bot: `python manage.py telegram_bot`
