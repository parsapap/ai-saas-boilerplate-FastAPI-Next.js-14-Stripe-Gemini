#!/bin/bash

echo "🚀 Starting Next.js Frontend..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo "✅ Starting development server..."
npm run dev
