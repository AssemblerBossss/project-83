
# Page Analyzer project-83

Page Analyzer - это веб-приложение на Flask, которое позволяет вам проверять и получать основные SEO-теги с веб-сайтов и собирать их в одном месте. Введенный URL-адрес будет добавлен в базу данных. На открывшейся странице вы сможете просмотреть результаты всех выполненных проверок и запустить еще одну. Также вы можете просмотреть все добавленные сайты и даты последних проверок.

**Application developed with using:**
- Python
- Flask
- PostgreSQL
- Bootstrap
- Beautiful Soup
- Requests
- Flake8

## Run locally:
**(It is required that you have previously installed Python, Poetry and PostgreSQL)**

Clone repository:
```
git@github.com:AssemblerBossss/project-83.git
```
Install dependencies:
```
make install
```
Create `.env` file and specify your secret key and database.
```
SECRET_KEY= # Your secret key
DATABASE_URL=postgresql://{user}:{password}@localhost:5432/project-83
# Format DATABASE_URL: {provider}://{user}:{password}@{host}:{port}/{db}
```
Create database:
```
make db-create
```
Load schema:
```
make schema-load
```
Run:
```
make start
```
---
Demonstration:
[Deployed "Page Analyzer" in Railway](https://python-project-83-production-9f72.up.railway.app)
