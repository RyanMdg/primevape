#!/bin/bash

# Start PrimeVape Frontend

echo "🚀 Starting PrimeVape Frontend..."
echo ""

cd primevape-frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ Dependencies not installed!"
    echo "Run the following commands first:"
    echo "  cd primevape-frontend"
    echo "  npm install"
    exit 1
fi

echo "✅ Starting development server on http://localhost:5173"
echo ""
npm run dev
