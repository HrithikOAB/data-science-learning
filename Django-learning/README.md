# Django OTP Login System — Student Handbook, Quiz & Practice Set

### Based on today's class: `Person` model + OTP-based login flow

This handbook recaps exactly what we built today, then gives you a **bug hunt**, a **quiz**, and **practice problems** to extend the same app. Complete these before the next session.

---

## Part A — Recap: What We Built Today

### The Flow (in plain English)
```
1. User visits /account/login
       → login_page() renders login.html (a form asking for email/mobile)

2. User submits the form
       → otp_send() runs
           - reads "email_or_mobile" from POST
           - generates a random OTP
           - if a Person with that number exists → update their OTP
           - if not → create a new Person with that number + OTP
           - renders otp-verify.html, passing the number back so the next
             step knows who is verifying

3. User enters the OTP they received
       → otp_verify() runs
           - reads "otp" and "user_number" from POST
           - checks if a Person exists with THAT number AND THAT otp
           - if yes → redirect to the profile page
           - if no  → return "Wrong OTP"

4. (Optional) User asks to resend
       → resend_otp() runs — same logic as otp_send(), generates a fresh OTP

5. User lands on /account/profile
       → profile_page() renders profile.html
```

### The `Person` Model
```python
class Person(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True)
    number = models.IntegerField()
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.number)
```

| Field | Type | Why |
|---|---|---|
| `name` | `CharField` | Short text, optional (`null=True, blank=True`) |
| `number` | `IntegerField` | Mobile number / identifier used to look the user up |
| `address` | `TextField` | Longer free text, optional |
| `image` | `ImageField` | Profile picture, optional |
| `otp` | `IntegerField` | The current OTP for that person, optional |

### Key Django Concepts Used Today
| Concept | Where it showed up |
|---|---|
| `request.POST.get('field_name')` | Reading form data submitted via POST |
| `Model.objects.filter(...).exists()` | Checking if a matching row exists, without fetching it |
| `Model.objects.get(...)` | Fetching exactly one matching row |
| `Model.objects.create(...)` | Creating and saving a new row in one line |
| `instance.save()` | Persisting changes to an existing row |
| `render(request, template, context)` | Returning an HTML page, optionally with data |
| `redirect('url_name')` | Sending the browser to a different URL |
| `path('url/', view, name='...')` | Mapping a URL to a view function |
| `include('app.urls')` | Plugging one app's URLs into the project |

---

## Part B — Bug Hunt 🐞

The code we wrote today **works**, but it has real bugs and design issues — the kind you'll actually run into on the job. Your task: **find and fix each one.** Don't just read the list — open the code, try to break it, and confirm the bug before fixing it.

1. **The OTP isn't always 4 digits.**
   `random.randint(0000, 9999)` can return something like `7` or `45`. Is that actually a 4-digit OTP? Try printing `random.randint(0000, 9999)` a few times and see what you get. How would you guarantee it's always 4 digits (as a string, e.g. `"0045"`)?

2. **`resend_otp` doesn't send back the same context as `otp_send`.**
   Compare the `render(...)` call at the end of `otp_send` with the one at the end of `resend_otp`. What's missing? What would break in the template because of this?

3. **The `edit-profile` URL is defined three times.**
   ```python
   path('edit-profile', profile_page, name='edit_profile'),
   path('edit-profile', profile_page, name='change_password'),
   path('edit-profile', profile_page, name='logout'),
   ```
   All three point to the exact same view. If you clicked a "Logout" button linked to `{% url 'logout' %}`, would it actually log the user out? What *should* each of these three routes actually do?

4. **There's no real "login state."**
   After `otp_verify` succeeds, we `redirect('profile')` — but we never store *who* is logged in anywhere (no session, no cookie). If you now open `/account/profile` directly in a new browser tab **without ever entering an OTP**, what happens? Is that a problem? (Hint: yes — this is a security bug.)

5. **`number` is an `IntegerField`.**
   What happens if a user's mobile number starts with a `0`, e.g. `0987654321`? What happens if they type a `+` for a country code, e.g. `+919876543210`? Would `IntegerField` accept that? What field type would be safer?

6. **Redundant `.save()` after `.create()`.**
   ```python
   Person.objects.create(number=number, otp=otp).save()
   ```
   `.objects.create()` already saves the row to the database. Is the extra `.save()` doing anything useful? What does `.create()` actually return?

7. **No uniqueness constraint on `number`.**
   Even though the view checks `.exists()` before creating, is there anything at the *database level* stopping two rows from ever having the same `number`? What Django field option would enforce this?

> ✍️ **Submit:** For each bug, write 1–2 sentences explaining the problem, plus your fixed code snippet.

---

## Part C — Quiz

Answer in your own words. No need for full paragraphs — a few clear sentences per answer is enough.

### Section 1: Concepts
1. What is the difference between `Person.objects.get()` and `Person.objects.filter().first()`? What happens if `.get()` finds zero matches? What if it finds more than one?
2. What does `request.POST.get('otp')` return if the `otp` field was **not** submitted in the form? Why is `.get()` safer here than `request.POST['otp']`?
3. Explain, in your own words, why `redirect('profile')` uses the **name** `'profile'` and not a hardcoded URL like `redirect('/account/profile')`. What's the advantage?
4. What is the purpose of `include('Main.urls')` in the project's `urls.py`? What would break if you removed it?
5. Why does the `Person` model's `__str__` method matter? Where would you actually *see* its effect?

### Section 2: Predict the Output
6. If `Person.objects.filter(number=9876543210).exists()` returns `False`, which branch of `otp_send()` runs — the `if` or the `else`?
7. Suppose a user's OTP in the database is `4521` (an integer), but the form sends `"4521"` (a string) via `request.POST.get('otp')`. Will `Person.objects.filter(number=number, otp=user_otp).exists()` correctly match it? Why or why not?
8. If two different people both submit the login form with the **same** mobile number one after another, what will happen to the `Person` row in the database by the time the second one finishes?

### Section 3: Short Design Questions
9. Right now, an OTP never expires — it stays valid forever until the next one is generated. What field would you add to the model to support **OTP expiry** (e.g., valid for 5 minutes)?
10. If you wanted to make sure `otp_send` and `otp_verify` only accept `POST` requests (not `GET`), what Django feature/decorator would you reach for?

---

## Part D — Practice Problems (Extend the App)

Work on these in order — each one builds on the last, and on today's code.

### Problem 1 — Fix the Bugs 🟢
Apply your fixes from **Part B** to your actual project. Confirm each fix by testing the broken behavior first, then testing that your fix resolves it.

### Problem 2 — Proper Login Session 🟡
Right now, reaching `/account/profile` doesn't require having verified an OTP.
- After a successful `otp_verify`, store the person's id in `request.session` (e.g., `request.session['person_id'] = person.id`).
- At the top of `profile_page`, check if `request.session.get('person_id')` exists. If not, redirect to `login`.
- Add a real `logout` view that clears the session (`request.session.flush()`) and redirects to `login`.

### Problem 3 — 4-Digit OTP, Always 🟢
Fix the OTP generator so it **always** produces a 4-digit code, even if it starts with a 0 (e.g., `"0057"`). Think about whether `otp` should even be an `IntegerField` once you consider this.

### Problem 4 — OTP Expiry 🔴
- Add a new field to the `Person` model: `otp_created_at = models.DateTimeField(null=True, blank=True)`.
- Every time an OTP is generated, set this field to `timezone.now()`.
- In `otp_verify`, check that the OTP was generated **less than 5 minutes ago**. If it's expired, show a message like `"OTP expired. Please request a new one."` instead of verifying.
- Run `makemigrations` and `migrate` after changing the model — don't forget this step!

### Problem 5 — Resend Cooldown 🔴
Prevent users from spamming the "Resend OTP" button.
- Using the same `otp_created_at` field from Problem 4, block `resend_otp` from generating a new OTP if the last one was created **less than 30 seconds ago**.
- Show a message telling the user how many seconds they need to wait.

### Problem 6 — Build a Parallel Flow: Email-Based Signup with OTP 🔴
Design and build a **separate** feature (new model + new views + new urls) for user registration via email OTP:
- A `Register` form collecting `name` and `email`.
- Generate and "send" (print to console is fine for now) an OTP.
- A verification step, same pattern as today, but for `email` instead of `number`.
- Once verified, create a proper account and log the user in.

This is intentionally open-ended — plan your model fields and views before writing code.

### Problem 7 — Register the Model in Admin 🟢
Register `Person` in `admin.py` with `list_display` showing `name`, `number`, and `otp`, so you (the "admin") can see and manage OTP records without touching the database directly. (This connects back to what you learned about the admin panel earlier.)

---

## Submission Checklist

- [ ] Part B: All 7 bugs identified and fixed, with before/after code
- [ ] Part C: Quiz answered (Sections 1–3)
- [ ] Problem 1: Bug fixes applied to the real project
- [ ] Problem 2: Session-based login working (profile page protected, logout works)
- [ ] Problem 3: OTP always 4 digits
- [ ] Problem 4: OTP expiry implemented (stretch)
- [ ] Problem 5: Resend cooldown implemented (stretch)
- [ ] Problem 6: Parallel email-OTP signup flow (stretch)
- [ ] Problem 7: `Person` visible and manageable in the admin panel

**Come to the next session with your project running** — we'll pick a few bug fixes and Problem 2 (sessions) to review together as a class.

---

## Answer Key — Bug Hunt (For Instructor Reference)

<details>
<summary>Click to expand — recommend NOT sharing this with students until after Part B is submitted</summary>

1. **4-digit OTP:** Use `random.randint(1000, 9999)`, or generate as a string: `str(random.randint(0, 9999)).zfill(4)`.
2. **Missing context in `resend_otp`:** It should mirror `otp_send`'s render call: `render(request, 'otp-verify.html', {'user_number': number, 'message': 'OTP resent'})`.
3. **Duplicate `edit-profile` paths:** Only the first (`edit_profile`) is ever reachable by URL; `change_password` and `logout` need their **own** paths (e.g., `change-password/`, `logout/`) and their **own** view functions with real logic.
4. **No login state:** Add session handling (see Problem 2) — without it, anyone can visit `/account/profile` directly.
5. **`number` as `IntegerField`:** Leading zeros are silently dropped, and `+` breaks it entirely. Should be `CharField(max_length=15)`.
6. **Redundant `.save()`:** `.objects.create()` already saves and returns the created instance; calling `.save()` on it again is a harmless but pointless extra database write.
7. **No uniqueness constraint:** Add `unique=True` to the `number` field (and re-run migrations) to enforce it at the database level, not just in application logic.

</details>