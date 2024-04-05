# Tennis Match Dashboard

A web application for displaying live tennis match data and statistics.

## Overview

This web application fetches live tennis match data from the SofaScore API. It provides endpoints to retrieve match data in JSON format as well as a web page for visualizing the matches in a tabular format. The application also fetches and displays statistics for each match, including service, points, games, and return statistics.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mdSHash/SofaScoreScraper.git
# Install dependencies:
pip install -r requirements.txt

# Run the application:
python app.py

# Access the application in your web browser at http://localhost:5000.

# Usage
Use the /api/tennis/matches endpoint to retrieve match data in JSON format.
Visit the /tennis/matches route in your browser to view the matches in a tabular format with statistics.
Technologies Used
Flask: Web framework for Python
SQLite: Database management system
Requests: HTTP library for making API requests

# Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.
