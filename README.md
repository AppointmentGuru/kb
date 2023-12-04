# kb

## Getting started

Install `pipenv`

```
pip install pipenv
```

Install requirements: `pipenv install`

A knowledgebase. A simple Django website with the ability to build out to a static website which can be deployed to netlify

## Commands

* **Build static website:** `pipenv run python manage.py build_website`
* **Build search index:** `pipenv run python manage.py build_index`
* **Deploy to netlify:** (after building): `ntl deploy --prod`

## Get started

Create a `.env` file in the same directory as `settings.py` (`kb`).

```bash
DATABASE_NAME=..
DATABASE_USER=..
DATABASE_PASSWORD=..
DATABASE_HOST=..
DATABASE_PORT=..
MELIA_URL=..
MELIA_API_KEY=..
```
