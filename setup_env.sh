#!/bin/bash

echo "========================================="
echo "TAUC Dashboard - Environment Setup"
echo "========================================="
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    echo "✓ .env file already exists"
    echo ""
    echo "Current contents (credentials hidden):"
    grep "^TAUC_" .env | sed 's/=.*/=***/' || echo "  (no TAUC_ variables found)"
    echo ""
    read -p "Do you want to recreate it? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env file"
        exit 0
    fi
fi

echo "Creating .env file..."
echo ""

# Copy template
cp .env.example .env

echo "✓ .env file created from template"
echo ""
echo "Please edit .env and add your credentials:"
echo "  - For OAuth: Set TAUC_CLIENT_ID and TAUC_CLIENT_SECRET"
echo "  - For AK/SK: Set TAUC_ACCESS_KEY and TAUC_SECRET_KEY"
echo ""
echo "Edit with:"
echo "  nano .env    (or vim, emacs, etc.)"
echo ""

# Offer to open editor
read -p "Open .env in nano now? (y/N) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    nano .env
    echo ""
    echo "✓ .env file saved"
fi

echo ""
echo "========================================="
echo "Next steps:"
echo "========================================="
echo "1. Verify .env has your credentials"
echo "2. Install dependencies: pip install -r requirements.txt"
echo "3. Launch dashboard: ./run.sh"
echo ""
echo "The dashboard will auto-populate credentials from .env!"
echo "========================================="
