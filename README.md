# Webhook Trigger App

This Flask application serves a single-page site with a clean design inspired by Apple's aesthetic. The landing page presents a large hero section with a button that triggers a POST request to `/trigger-webhook`, which forwards the request to the URL configured via `WEBHOOK_URL`.

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and set `WEBHOOK_URL` to your target.
3. Run the server:
   ```bash
   python main.py
   ```
   The app listens on `http://localhost:5000` by default.

## Deployment

A simple `Dockerfile` is provided. Build the image and run it with your environment variables to expose the webhook URL and port of your choice.
