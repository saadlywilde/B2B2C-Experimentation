# B2B2C Experimentation

This project provides a minimal Django setup demonstrating a simple quote flow inspired by B2B2C insurance platforms. It uses **Django**, **HTMX**, **AlpineJS**, and **Tailwind CSS** to keep the UI responsive with minimal JavaScript.

## Setup

```bash
pip install -r requirements.txt
python b2b2c/manage.py migrate
python b2b2c/manage.py runserver
```

Access the quote creation page at `http://localhost:8000/`.

## Running tests

```bash
python b2b2c/manage.py test quotes
```
