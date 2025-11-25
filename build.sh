#!/usr/bin/env bash
# Build script for Render

echo "🔨 Installing Python dependencies..."
pip install -r requirements-cloudrun.txt

echo "📊 Creating database..."
python -c "import sqlite3; from pathlib import Path; db = Path('devopsmcp.db'); schema = Path('schema_sqlite.sql'); conn = sqlite3.connect(db); conn.executescript(open(schema, encoding='utf-8').read()); conn.close(); print('✅ Database created')"

echo "✅ Build complete!"
