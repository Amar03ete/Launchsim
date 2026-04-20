"""
MiroFish Backend - Flask Application Entrypoint for Vercel
"""

import os
import sys

# Add project root directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

# Create Flask application instance for Vercel
app = create_app()

if __name__ == '__main__':
    app.run()
