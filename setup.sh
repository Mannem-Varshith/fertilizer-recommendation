#!/bin/bash

# Create .streamlit directory if it doesn't exist
mkdir -p ~/.streamlit/

# Create config.toml file
cat > ~/.streamlit/config.toml << EOF
[server]
headless = true
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
EOF 