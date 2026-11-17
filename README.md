<div align="center">

# 📰 NewsBlog

**A Django news platform with an editorial-first frontend.**

Independent journalism, in-depth features and community updates — powered by Django + Bootstrap 5.

[Features](#-features) · [Stack](#-stack) · [Getting Started](#-getting-started) · [Project Structure](#-project-structure) · [Commands](#-commands) · [Design System](#-design-system)

</div>

---

## ✨ Features

- **Editorial design system** — custom tokens (colors, typography, spacing) layered on top of Bootstrap 5
- **Featured story hero** — full-bleed image with gradient overlay and overlaid headline
- **Responsive story grid** — CSS Grid with 1 / 2 / 3 columns at breakpoints
- **Article reader** — serif body text, drop cap, max 68ch line length, optional image carousel
- **Inline comments** — post, edit (collapse), and delete with role-based permissions
- **Author profiles** — avatar, bio and post history
- **Staff panel** — user management for staff / superusers
- **Auth** — login, logout, register, password-protected actions
- **Image support** — multiple images per post via `ImageField`

---

## 🧰 Stack

| Layer | Tech |
|---|---|
| **Backend** | [Django](https://www.djangoproject.com/) 5.0 |
| **Frontend** | [Bootstrap 5](https://getbootstrap.com/) via [`django-bootstrap5`](https://github.com/zostera/django-bootstrap5) |
| **Typography** | [Fraunces](https://fonts.google.com/specimen/Fraunces) (serif) + [Inter](https://fonts.google.com/specimen/Inter) (sans) |
| **Database** | SQLite (dev) — PostgreSQL-ready |
| **Media** | Pillow + Django `ImageField` |
| **Config** | `python-dotenv` for environment variables |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Git**

### 1. Clone the repository

```bash
git clone git@github.com:your-user/newsblog.git
cd newsblog
```

### 2. Create the virtual environment

The project expects the virtualenv to live in `env/` at the repository root.

```bash
# Linux / macOS
python3 -m venv env
source env/bin/activate

# Windows (cmd)
py -m venv env
env\Scripts\activate.bat

# Windows (PowerShell)
py -m venv env
env\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Then edit `.env` and fill in the values:

```env
SECRET_KEY=your-random-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

> 💡 Generate a secure `SECRET_KEY` with:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. Apply migrations

```bash
cd blog_manager
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** — you're in. 🎉

The admin panel is at **http://127.0.0.1:8000/admin/**.

---

## 📁 Project Structure

```
blog_django/                    ← repository root
│
├── .env                        ← local env vars (git-ignored)
├── .env.example                ← committed template
├── .gitignore
├── README.md
├── requirements.txt
│
├── blog_manager/               ← Django project
│   ├── manage.py
│   ├── db.sqlite3              ← dev database (git-ignored)
│   │
│   ├── config/                 ← project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── news/                   ← main app
│   │   ├── models.py           ← News, Comment, Image
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── static/
│   │   └── css/
│   │       ├── main.css        ← entry point (@imports below)
│   │       ├── _tokens.css
│   │       ├── _base.css
│   │       ├── _layout.css
│   │       ├── _buttons.css
│   │       ├── _atoms.css
│   │       ├── _feed.css
│   │       ├── _article.css
│   │       └── _comments.css
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── news_home.html
│   │   ├── news_detail.html
│   │   ├── news_form.html
│   │   ├── profile.html
│   │   └── auth/
│   │       ├── login.html
│   │       └── register.html
│   │
│   └── media/                  ← uploaded images (git-ignored)
│
└── env/                        ← virtualenv (git-ignored)
```

---

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | ✅ | — | Django secret key |
| `DEBUG` | — | `False` | Enable debug mode |
| `ALLOWED_HOSTS` | — | `localhost,127.0.0.1` | Comma-separated hosts |
| `DATABASE_URL` | — | SQLite | PostgreSQL URL (production) |
| `EMAIL_HOST` | — | — | SMTP host (for password reset) |
| `EMAIL_HOST_USER` | — | — | SMTP user |
| `EMAIL_HOST_PASSWORD` | — | — | SMTP password |

Example `.env.example`:

```env
# Django
SECRET_KEY=change-me-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (production — optional)
# DATABASE_URL=postgres://user:password@localhost:5432/newsblog

# Email (optional)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=
# EMAIL_HOST_PASSWORD=
```

---

## 🎨 Design System

The frontend is built on a small set of design tokens defined in `static/css/_tokens.css`:

| Token | Value | Purpose |
|---|---|---|
| `--ink` | `#14181f` | Primary text (warm near-black) |
| `--paper` | `#faf8f4` | Page background (editorial off-white) |
| `--rule` | `#e3ded4` | Borders and dividers |
| `--accent` | `#c4452c` | Brand accent (terracotta) |
| `--font-serif` | `Fraunces` | Headlines, article body |
| `--font-sans` | `Inter` | UI, navigation, metadata |
| `--radius` | `14px` | Card radius |
| `--shadow-lg` | `0 20px 48px rgba(20,24,31,.12)` | Hover elevation |

All components (`story-card`, `featured-story`, `article-body`, `comment`, …) consume these tokens — change a token, change the whole site.

CSS is split into modular files imported by `main.css`:

```css
@import url("_tokens.css");
@import url("_base.css");
@import url("_layout.css");
@import url("_buttons.css");
@import url("_atoms.css");
@import url("_feed.css");
@import url("_article.css");
@import url("_comments.css");
```

---

## 🧑‍💻 Commands

All Django commands must run from `blog_manager/` with the venv active.

```bash
# Activate venv (from repo root)
source env/bin/activate

# Navigate to Django project
cd blog_manager

# Run dev server
python manage.py runserver

# Make / apply migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Run system checks
python manage.py check

# Collect static files (production)
python manage.py collectstatic
```

Git commands are run from the repository root (`blog_django/`):

```bash
git status
git add .
git commit -m "feat: your message"
git push
```

---

## 🗄️ Database

Development uses **SQLite** out of the box — no driver needed, `db.sqlite3` is created automatically on first `migrate`.

To switch to **PostgreSQL** in production:

1. Install the driver:
   ```bash
   pip install psycopg2-binary
   ```
2. Add it to `requirements.txt`
3. Update `settings.py`:

   ```python
   DATABASES = {
       "default": {
           "ENGINE": "django.db.backends.postgresql",
           "NAME": os.getenv("DB_NAME"),
           "USER": os.getenv("DB_USER"),
           "PASSWORD": os.getenv("DB_PASSWORD"),
           "HOST": os.getenv("DB_HOST", "localhost"),
           "PORT": os.getenv("DB_PORT", "5432"),
       }
   }
   ```

---

## 📦 requirements.txt

```txt
Django>=5.0,<5.1
python-dotenv>=1.0
django-bootstrap5>=24.3
Pillow>=10.0
```

> ⚠️ Use **`django-bootstrap5`** (maintained) — not `django-bootstrap-v5` (abandoned).
> The `{% load bootstrap5 %}` tag in `base.html` comes from `django-bootstrap5`.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push the branch: `git push origin feature/my-feature`
5. Open a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## 📄 License

This project is open-source under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

<div align="center">

Made with ☕ and Django.

**[⬆ back to top](#-newsblog)**

</div>