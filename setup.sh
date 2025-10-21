#!/bin/bash

# Step 1: Create a virtual environment
python3 -m venv venv

# Step 2: Activate the virtual environment
source venv/bin/activate

# Step 3: Install dependencies from requirements.txt
pip install -r requirements.txt

# Step 4: Confirm installation
echo "Setup complete. Virtual environment created and dependencies installed."