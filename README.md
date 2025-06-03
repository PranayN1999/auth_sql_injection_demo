# Auth‑SQLi‑Demo

A minimal Django project that lets you **show, exploit, and then fix a classic SQL‑injection vulnerability**.  
It ships with two authentication flows:

| Path                | Purpose                         | Table used           |
|---------------------|---------------------------------|----------------------|
| `/bad-register/`    | Save **plain‑text** users       | `users_plainuser`    |
| `/bad-login/`       | Vulnerable login  (raw SQL)     | `users_plainuser`    |

---

## 1.  Quick start

```bash
# 1 Clone repo
git clone https://github.com/<you>/django-sqli-demo.git
cd django-sqli-demo

# 2 Create venv & install deps
python -m venv venv
venv\Scripts\activate           # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt # Django 5.x

# 3 Initialise DB (SQLite)
python manage.py migrate

# 4 Seed a demo plain‑text user (id=1)
python manage.py shell -c "from users.models import PlainUser; PlainUser.objects.get_or_create(username='bob', password='Secret123')"

# 5 Run server
python manage.py runserver
