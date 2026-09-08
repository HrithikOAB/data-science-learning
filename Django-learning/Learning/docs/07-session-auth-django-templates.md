# Session Auth (Django + HTML templates)

This is the **classic website login**. You have real HTML pages, `<form>` submits, and Django remembers you with a cookie. Built in the `Main` app.

## The flow (what happens when you log in)

1. You submit the login form (email + password).
2. Django checks the password with `authenticate()`.
3. If correct, `login()` creates a **session** on the server and sends a **session id cookie** to your browser.
4. On every next request, `SessionMiddleware` + `AuthenticationMiddleware` read that cookie and set `request.user` for you.
5. `logout()` destroys the session — the cookie no longer means anything.

That's why it's **stateful**: the *server* remembers you.

## The user model

We use a custom user, so login works on it:

```python
# Main/models.py
class Person(AbstractUser):
    name = models.CharField(max_length=10, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)
```

```python
# Learning/settings.py
AUTH_USER_MODEL = "Main.Person"
```

## The views

### Sign up — create a user

```python
# Main/views.py
def signup_page(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        user = Person.objects.create(name=name, email=email, number=mobile, username=email)
        user.set_password(password)   # NEVER save a raw password — hash it
        user.save()
        return redirect('login')
    else:
        return render(request, 'signup.html')
```

**Key point:** `set_password()` hashes the password. Never store the raw text.

### Log in — start the session

```python
# Main/views.py
def login_page(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)          # <-- creates the session + cookie
            return redirect('profile')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')
```

**Two functions in one:** `GET` shows the form, `POST` processes it. `authenticate()` checks the credentials; `login()` starts the session.

> Note: the username **is** the email here — we saved `username=email` at signup, so `authenticate(username=email, ...)` works.

### Profile — a protected page

```python
# Main/views.py
def profile_page(request):
    if request.user.is_authenticated:      # <-- the "guard"
        user = request.user
        return render(request, 'profile.html', {'user': user})
    else:
        return redirect('login')
```

`request.user.is_authenticated` is how you protect a page. Not logged in? Bounce them to login.

### Log out — end the session

```python
# Main/views.py
def logout_view(request):
    logout(request)      # <-- destroys the session
    return redirect('login')
```

## The URLs

```python
# Main/urls.py
urlpatterns = [
    path('login/',        login_page,   name='login'),
    path('signup/',       signup_page,  name='signup'),
    path('profile/',      profile_page, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('logout',        logout_view,  name='logout'),
]
```

These are included under the `api/` prefix:

```python
# Learning/urls.py
path('api/', include('Main.urls')),
```

So the real page URLs are `/api/login/`, `/api/signup/`, `/api/profile/`, `/api/logout`.

The **`name=`** part matters — templates use it with `{% url 'login' %}` so links keep working even if you change the path.

## The template (the form)

```html
<!-- Templates/login.html -->
<form action="{% url 'login' %}" method="POST">
    {% csrf_token %}                        <!-- REQUIRED for POST forms -->

    <input type="text"     name="email"    placeholder="Enter Email"    required>
    <input type="password" name="password" placeholder="Enter Password" required>

    <button type="submit">Login</button>
</form>
```

**Two must-knows:**
- `{% csrf_token %}` — Django blocks any POST form without it (protection against cross-site request forgery). Leave it out and you get a **403 error**.
- The `name="email"` / `name="password"` values are exactly what `request.POST.get('email')` reads in the view. They must match.

## What makes it all work (settings)

```python
# Learning/settings.py
MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',   # reads/writes the session
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware', # sets request.user
    ...
]

TEMPLATES = [{
    ...
    "DIRS": [BASE_DIR / "Templates"],   # so Django finds login.html, signup.html, profile.html
    ...
}]
```

## Try it out

Start the server and use your **browser** (cookies happen automatically):

```bash
cd Learning
python manage.py runserver
```

1. Sign up → `http://127.0.0.1:8000/api/signup/`
2. Log in → `http://127.0.0.1:8000/api/login/`
3. See your profile → `http://127.0.0.1:8000/api/profile/`
4. Log out → `http://127.0.0.1:8000/api/logout`

Try visiting `/api/profile/` *before* logging in — you'll be redirected to login. That's the guard working.

## Session vs Token — the one-line difference

Session auth keeps state on the **server** and rides on a **cookie** — perfect for browser websites. For APIs (mobile apps, JS frontends) you usually want the stateless version → [Token auth](08-token-auth-drf-fbv.md).
