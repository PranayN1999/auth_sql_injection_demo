# users/views_vuln.py
from django.db import connection
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PlainUser   

@csrf_exempt               # demo only
def bad_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        #### SQL Injection Vulnerable query

        sql = (
            f"SELECT id, username "
            f"FROM users_plainuser "           # ← table from the new model
            f"WHERE username = '{username}' "
            f"AND password = '{password}' "
            f"LIMIT 1;"
        )

        with connection.cursor() as cur:
            cur.execute(sql)
            row = cur.fetchone()



        #### Parameterized Queries
        ## To prevent SQL Injection

        # sql = """
        #     SELECT id, username
        #     FROM users_plainuser
        #     WHERE username = %s           -- placeholders!
        #       AND password = %s
        #     LIMIT 1;
        # """
        # with connection.cursor() as cur:
        #     cur.execute(sql, [username, password])   # 🎯 bound parameters
        #     row = cur.fetchone()

        if row:
            return HttpResponse(f"✅ Logged in as {row[1]} (id={row[0]})")
        return HttpResponse("❌ Invalid username / password")

    return HttpResponse("""
        <h2>🚩 Vulnerable login (plain‑text table)</h2>
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <button>Log in</button>
        </form>
        <p>Try password <code>' OR 1=1-- </code> to bypass.</p>
    """)


@csrf_exempt                       # demo only – restore CSRF later
def bad_register(request):
    """
    Plain‑text registration for demo purposes.

    • Saves username / password directly to PlainUser (no hashing).
    • On duplicate username, shows an error.
    """
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            return HttpResponse("<h3>❌  Both fields are required</h3>")

        try:
            PlainUser.objects.create(username=username, password=password)
            return HttpResponse(
                "<h3>✅  User created!</h3>"
                '<p><a href="/bad-login/">Go to vulnerable login</a></p>'
            )
        except IntegrityError:
            return HttpResponse("<h3>❌  Username already exists</h3>")

    # GET → show simple form
    return HttpResponse(
        """
        <h2>🚩 Vulnerable Registration (plain‑text passwords)</h2>
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <button>Register</button>
        </form>
        """
    )