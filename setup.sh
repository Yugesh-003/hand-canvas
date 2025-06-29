#!/bin/bash
# Temple Runner Setup Script

echo "🏛️  TEMPLE RUNNER SETUP 🏛️"
echo "================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "temple_runner_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv temple_runner_env
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment and install packages
echo "📥 Installing dependencies..."
source temple_runner_env/bin/activate
pip install -r requirements.txt

echo ""
echo "🎉 SETUP COMPLETE!"
echo "================================"
echo ""
echo "To run the game:"
echo "  1. source temple_runner_env/bin/activate"
echo "  2. python main.py"
echo ""
echo "To run the demo (no display required):"
echo "  1. source temple_runner_env/bin/activate"
echo "  2. python demo.py"
echo ""
echo "To test the installation:"
echo "  1. source temple_runner_env/bin/activate"
echo "  2. python test_game.py"
echo ""
echo "Happy gaming! 🎮"
