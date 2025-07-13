# Webhook Trigger App

This project is a very small Flask application that serves a single-page website. The page contains a button that sends a POST request to `/trigger-webhook` on the server, which then forwards the request to a configured webhook URL.

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file based on `.env.example` and set `WEBHOOK_URL` to your target.
3. Run the server:
   ```bash
   python main.py
   ```
   The app listens on `http://localhost:5000` by default.

## Deployment

A `Dockerfile` is provided for containerized deployments. Build the image and run it with the appropriate environment variables to expose the webhook URL and port.
