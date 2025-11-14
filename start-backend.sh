#!/bin/bash

# Start PrimeVape Backend

echo "🚀 Starting PrimeVape Backend..."
echo ""

cd primevape-backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run the following commands first:"
    echo "  cd primevape-backend"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo "  python seed.py"
    exit 1
fi

# Activate virtual environment and start server
source venv/bin/activate
echo "✅ Virtual environment activated"
echo "✅ Starting Flask server on http://localhost:5001"
echo ""
python app.py
