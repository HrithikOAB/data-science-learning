# What is Authentication? (and its types)

Before any login code makes sense, you need one simple idea:

> **Authentication** = proving **who you are**.
> **Authorization** = deciding **what you're allowed to do**.

Example: showing your ID card at a bank is *authentication*. Whether that ID lets you open the vault is *authorization*. Login first, permissions second.

This doc explains the common **types** of authentication, then points you to the two we actually built in this project.

## The types (in plain words)

| Type | One-line idea | Stateful? | Where the "proof" lives |
|---|---|---|---|
| **Session / Cookie** | Server remembers you after login | Stateful (server stores a session) | A cookie in the browser |
| **Token** | You get a token string, send it every time | Stateless | An `Authorization` header |
| **JWT** | A *self-contained* token (signed, holds data) | Stateless | An `Authorization` header |
| **Basic auth** | Send username+password on every request | Stateless | An `Authorization` header (base64) |
| **OAuth / social login** | "Login with Google/GitHub" | Depends | An external provider |
| **API key** | One secret string identifies an app | Stateless | A header or query param |

**Stateful vs stateless — the key difference:**
- **Stateful (sessions):** the *server* keeps a record of who's logged in. The browser just holds a cookie with a session id. Great for websites you open in a browser.
- **Stateless (tokens):** the server keeps *nothing*. The client holds a token and proves itself on every request. Great for APIs, mobile apps, and other programs.

## When do you use which?

- **Building a website with HTML pages?** → Session auth. The browser handles cookies automatically, and you get forms + redirects for free.
- **Building an API for a mobile app / another program / a JS frontend?** → Token auth (or JWT). No cookies needed — the client just sends a token.

## How this maps to *this* project

We built **both**, so you can compare them side-by-side:

| Feature | App | Auth type | Read next |
|---|---|---|---|
| HTML login/signup/profile pages | `Main` | **Session** auth | [07-session-auth-django-templates.md](07-session-auth-django-templates.md) |
| JSON API login/register/profile | `tokenAuth` | **Token** auth (DRF) | [08-token-auth-drf-fbv.md](08-token-auth-drf-fbv.md) |

Both apps log in the **same custom user** — `Main.Person` (set in `settings.py` as `AUTH_USER_MODEL = "Main.Person"`). Same users, two different ways to prove who they are.

**Next up:** [Session auth with Django + HTML templates](07-session-auth-django-templates.md)
