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

````

Visit **[http://127.0.0.1:8000/bad-login/](http://127.0.0.1:8000/bad-login/)** to begin the demo.

---

## 2.  Demo script

| Step | Action                                          | Expected                            |
| ---- | ----------------------------------------------- | ----------------------------------- |
| A    | Open `/bad-register/`, add `alice / Wonder123`  | “User created!”                     |
| B    | Open `/bad-login/`, enter `alice / Wonder123`   | ✅ success (normal)                  |
| C    | Same page, enter `alice / wrongpass`            | ❌ invalid                           |
| D    | Injection: `alice / ' OR 1=1-- ` *(note space)* | ✅ success **without** real password |

Use `OR id = 2-- ` or `OR username = 'alice'-- ` to target specific rows and illustrate selective hijacking.

---

## 3.  How it works

```
users/
├── models.py        # PlainUser (plain‑text) + CustomUser (hashed)
├── views_vuln.py    # bad_register / bad_login  (string‑spliced SQL)
```

### Vulnerable query (excerpt)

```python
sql = (
    f"SELECT id, username "
    f"FROM users_plainuser "
    f"WHERE username = '{username}' "
    f"AND password = '{password}' "
    f"LIMIT 1;"
)
with connection.cursor() as cur:
    cur.execute(sql)              # ← user input merged into SQL text
    row = cur.fetchone()
```

### Secure replacement

```python
sql = """
    SELECT id, username
    FROM users_plainuser
    WHERE username = %s
      AND password = %s
    LIMIT 1;
"""
with connection.cursor() as cur:
    cur.execute(sql, [username, password])   # 🎯 bound parameters
    row = cur.fetchone()
```

Or switch to Django’s `authenticate()` which always parameterises and hashes passwords.

---

## 4.  Cleaning up after the lesson

1. **Delete** `views_vuln.py`, `/bad-*` routes, and the `PlainUser` model / table.
2. **Re‑enable CSRF** (remove `@csrf_exempt`).
3. **Use hashed passwords** (Django `CustomUser`) in real apps.

---

## 5.  Requirements

* Python 3.9+
* Django 5.x (declared in `requirements.txt`)


