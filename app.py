"""
LaunchSim Backend — Vercel Serverless Entrypoint

Vercel requires Python serverless functions to live inside the /api directory
at the repository root. This file imports the Flask app from the backend package
and exposes it as `app` so Vercel can invoke it.
"""

import os
import sys

# Add the backend directory to sys.path so the `app` package is importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend'))

from app import create_app  # noqa: E402

# Vercel looks for a variable named `app` in this file
app = create_app()

if __name__ == '__main__':
    app.run()
