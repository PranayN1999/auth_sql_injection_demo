from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()                    # ⬅ NO auto‑login
            return redirect("login")       # take them to the sign‑in page
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def home(request):
    ctx = {
        "has_org": bool(request.user.organization),
        "org_name": request.user.organization.name
                    if request.user.organization else "",
    }
    return render(request, "home.html", ctx)
