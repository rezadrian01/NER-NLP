#!/bin/bash

# Setup script for Wayang NER and Knowledge Graph Builder
# Author: Ahmad Reza Adrian

echo "=========================================="
echo "Wayang NER Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found: Python $python_version"

# Check if Python 3.10+
required_version="3.10"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "⚠️  Warning: Python 3.10+ recommended"
fi

echo ""

# Create virtual environment (optional)
read -p "Create virtual environment? (y/n): " create_venv
if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo "To activate: source venv/bin/activate"
    echo ""
fi

# Install dependencies
read -p "Install dependencies from requirements.txt? (y/n): " install_deps
if [ "$install_deps" = "y" ] || [ "$install_deps" = "Y" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
    echo ""
fi

# Download spaCy model
read -p "Download spaCy multilingual model? (y/n): " download_spacy
if [ "$download_spacy" = "y" ] || [ "$download_spacy" = "Y" ]; then
    echo "Downloading spaCy model..."
    python3 -m spacy download xx_ent_wiki_sm
    echo "✅ spaCy model downloaded"
    echo ""
fi

# Create output directory
echo "Creating output directory..."
mkdir -p output
mkdir -p templates
mkdir -p data
echo "✅ Directories created"
echo ""

# Run tests
read -p "Run test suite? (y/n): " run_tests
if [ "$run_tests" = "y" ] || [ "$run_tests" = "Y" ]; then
    echo "Running tests..."
    python3 test_examples.py
    echo ""
fi

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Run full pipeline: python3 pipeline.py"
echo "2. Launch web app: python3 app.py"
echo "3. Run tests: python3 test_examples.py"
echo ""
echo "For help, see README.md"
echo ""
