<div align="center">

# 🎲 Neo-Sheet

**A RESTful API for building and managing custom RPG character sheets for any tabletop system.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.x-A30000?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-planned-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-planned-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-planned-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)](./LICENSE)

[Quick Start](#-quick-start) · [Features](#-features) · [Tech Stack](#%EF%B8%8F-tech-stack) · [Roadmap](#%EF%B8%8F-roadmap) · [Docs](#-documentation)

<!-- Replace with a real preview: Swagger UI screenshot or a GIF of the API in action -->
<!-- ![Neo-Sheet Preview](docs/preview.gif) -->

</div>

---

##  Concept

> **Neo-Sheet is a schema-driven API that lets developers define RPG character sheets for any system — D&D, Ordem Paranormal, homebrew rules — without writing a single line of backend code per system.**

Instead of hardcoding attributes, statuses, and inventory structures, the API exposes a flexible **profile system**. A "profile" describes how a character sheet should look (fields, overrides, custom schemas). Clients then use these profiles to generate character sheets at runtime. The core API stays stack-agnostic, validated, and easy to extend.

---

##  Features

| Feature | Description |
|---------|-------------|
|  **Dynamic Schemas** | Define each game system's sheet structure via `added_fields`, `field_overrides`, and `custom_schema`. |
|  **User & Auth Management** | Full registration, login, token refresh, password reset, and profile endpoints powered by `djoser` + `simplejwt`. |
|  **JWT Authentication** | Stateless authentication with `Bearer` tokens and configurable lifetimes. |
|  **Profile CRUD** | Create, list, retrieve, update, and delete system profiles with owner-based permissions. |
|  **Granular Permissions** | Public, optional-auth, and protected endpoints — reflected accurately in the OpenAPI schema. |
|  **Dice Engine** | Roll `XdY` notation with advanced operators (`kh`, `kl`, `!`) and modifiers. |
|  **Official vs. Private Profiles** | Staff-created official profiles are visible to everyone; user profiles stay private. |
|  **Interactive Docs** | Auto-generated OpenAPI 3.0 schema with Swagger UI and Redoc. |
|  **Tested** | Unit + integration tests with `pytest`, `factory-boy`, and a coverage target of 85%+. |

---

##  Quick Start

```bash
# 1. Clone and enter the project
git clone https://github.com/<your-user>/neo-sheet.git && cd neo-sheet

# 2. Create a virtualenv and install dependencies
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# 3. Apply migrations and run the dev server
python manage.py migrate && python manage.py runserver