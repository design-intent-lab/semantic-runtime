#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════════╗"
echo "║  Semantic Runtime — Reference Executable    ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Verify dependencies
command -v blender >/dev/null 2>&1 || { echo "❌ Blender not found. Install Blender 4.x and add to PATH."; exit 1; }
python3 -c "import json, yaml" 2>/dev/null || echo "⚠️  pyyaml not installed — using built-in YAML parser"
python3 -c "import json" 2>/dev/null || { echo "❌ Python 3 not available."; exit 1; }

mkdir -p output

echo "▶ Intent: $(head -1 example.intent.yaml | cut -d: -f2-)"
echo "▶ Running..."
echo ""

python3 runtime.py example.intent.yaml output/

echo ""
echo "✅ Done. Open output/ for results."
