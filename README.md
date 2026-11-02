# BahiKhata.AI

![Tests](https://github.com/Ragavendhar25/bahikhata-ai/actions/workflows/main.yml/badge.svg)

Voice-based digital ledger for small neighbourhood shops.
The shopkeeper speaks in Tamil, Hindi or English, and the app writes the entry in the ledger.

## Problem
Small shops keep credit (udhaar) in paper notebooks. Pages get lost, totals are wrong,
and typing during rush hour is slow.

## How it works
Voice → Whisper (speech to text) → LLM (finds item, quantity, price) → fuzzy match (fixes spelling) → database

## Features
- Customers and ledger with automatic balance
- Voice and text entry in Tamil, Hindi, English
- Item name auto-correction
- WhatsApp bill link
- Automated tests with GitHub Actions

## Tech stack
Python, FastAPI, SQLAlchemy, SQLite, Groq (Whisper + LLM), RapidFuzz, pytest, GitHub Actions

## Screenshots
![Recorder](screenshots/recorder.png)
![API docs](screenshots/docs.png)

## Run locally
1. `python -m venv venv` then activate it
2. `pip install -r requirements.txt`
3. Create `.env` with `GROQ_API_KEY=your_key`
4. `python -m uvicorn main:app --reload`
5. Open http://127.0.0.1:8000/recorder

## Roadmap
Docker, credit risk score, pre-order queue, cloud deployment
