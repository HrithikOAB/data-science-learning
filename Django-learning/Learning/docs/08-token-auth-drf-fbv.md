# Token Auth with Function-Based Views (`@api_view`)

This is how you log in to an **API** — no HTML, no cookies. The client logs in once, gets a **token string**, and sends that token on every request. Built in the `tokenAuth` app using plain functions decorated with `@api_view`.

## The flow (what happens)

1. **Register** → create a user.
2. **Login** → server hands back a **token** (`{"token": "abc123..."}`).
3. Client stores the token and sends it on every request:
   `Authorization: Token abc123...`
4. Server reads the header, finds the user — no session, no cookie.
5. **Logout** → delete the token so it stops working.

It's **stateless**: the server stores nothing about "who's logged in" — the token *is* the proof.

## Setup (do this first)

Token auth needs DRF's token app and a database table for the tokens.

```python
# Learning/settings.py
INSTALLED_APPS = [
    ...
    "rest_framework",
    "rest_framework.authtoken",   # <-- creates the Token table
    "tokenAuth",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",   # <-- reads the "Authorization: Token ..." header
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",   # <-- APIs require login by default
    ],
}
```

Then create the token table:

```bash
python manage.py migrate
```

## The serializer

Turns a `Person` object into JSON for the profile response:

```python
# tokenAuth/serializers.py
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'username', 'email', 'name', 'number', 'address', 'image']
```

(New to serializers? Read [01-serializers-explained.md](01-serializers-explained.md).)

## The views

`@api_view(['POST'])` means "this function is an API endpoint that only accepts POST." It gives you `request.data` (parsed JSON) and a nice `Response` object.

### Register — make a user

```python
# tokenAuth/views.py
@api_view(['POST'])
def register_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if Person.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)

    user = Person.objects.create_user(username=email, email=email, password=password)
    return Response({'response': 'User registered successfully'})
```

`create_user()` hashes the password for you.

### Login — hand out a token

```python
# tokenAuth/views.py
@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if Person.objects.filter(email=email).exists():
        if Person.objects.get(email=email).check_password(password):
            user = Person.objects.get(email=email)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
    else:
        return Response({'error': 'Invalid credentials'}, status=401)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)   # <-- the important line
        return Response({'token': token.key})

    return Response({'error': 'Invalid credentials'}, status=401)
```

**Key line:** `Token.objects.get_or_create(user=user)` — returns the user's existing token, or makes a new one. The client keeps `token.key`.

### Profile — a protected endpoint

```python
# tokenAuth/views.py
@api_view(['GET'])
@permission_classes([IsAuthenticated])   # <-- must send a valid token
def profile_view(request):
    serializer = PersonSerializer(request.user)
    return Response(serializer.data)
```

`@permission_classes([IsAuthenticated])` is the guard. No valid token → `401 Unauthorized`. When a valid token *is* sent, DRF fills in `request.user` for you.

### Logout — kill the token

```python
# tokenAuth/views.py
@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})
```

Deleting the token is logout — that token string is now useless.

## The URLs

```python
# tokenAuth/urls.py
urlpatterns = [
    path('login/',    login_view),
    path('logout/',   logout_view),
    path('register/', register_view),
    path('profile/',  profile_view),
]
```

Mounted under `api-token-auth/`:

```python
# Learning/urls.py
path('api-token-auth/', include('tokenAuth.urls')),
```

So the real endpoints are:

| Endpoint | Method | Needs token? |
|---|---|---|
| `/api-token-auth/register/` | POST | no |
| `/api-token-auth/login/` | POST | no |
| `/api-token-auth/profile/` | GET | **yes** |
| `/api-token-auth/logout/` | POST | **yes** |

## Try it out

Start the server:

```bash
cd Learning
python manage.py runserver
```

```bash
# 1. Register
curl -X POST http://127.0.0.1:8000/api-token-auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"sam@test.com","password":"supersecret123"}'

# 2. Login — copy the "token" from the response
curl -X POST http://127.0.0.1:8000/api-token-auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"sam@test.com","password":"supersecret123"}'
# -> {"token":"9f2c1e8a...."}

# 3. Get your profile — send the token in the header
curl http://127.0.0.1:8000/api-token-auth/profile/ \
  -H "Authorization: Token 9f2c1e8a...."

# 4. Logout — the token stops working after this
curl -X POST http://127.0.0.1:8000/api-token-auth/logout/ \
  -H "Authorization: Token 9f2c1e8a...."
```

Try step 3 **without** the `Authorization` header — you'll get `401`. That's `IsAuthenticated` doing its job.

## Token vs Session — quick recap

| | Session ([doc 07](07-session-auth-django-templates.md)) | Token (this doc) |
|---|---|---|
| Proof of login | Cookie (automatic in browser) | `Authorization: Token ...` header (you send it) |
| Server stores state? | Yes (session) | No (stateless) |
| Best for | HTML websites | APIs, mobile apps, JS frontends |

Not sure what any of this means? Start at [06-what-is-authentication.md](06-what-is-authentication.md).
