![image](https://github.com/user-attachments/assets/0ab89a99-6514-4b51-afd6-09236b95aa12)

![image](https://github.com/user-attachments/assets/7b8c7cac-e1c0-4083-8626-ea6f6336cbd0)




# Weather Dashboard

## Description
Weather Dashboard is a web application that visualizes weather data for multiple cities. It displays daily weather summaries, including average, maximum, and minimum temperatures, as well as alerts for high temperatures. The application uses Chart.js for data visualization and Flask for the backend API.

## Technologies Used
- HTML, CSS, JavaScript
- Chart.js for data visualization
- Flask for the backend API
- Fetch API (OpenWeatherAPI) for making network requests

## Features
- Displays daily weather summary for cities
- Visualizes average, maximum, and minimum temperatures in a bar chart
- Alerts for temperatures exceeding a specified threshold

## Installation

Follow the steps below to set up the Weather Monitoring Project on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.6 or later**: [Download Python](https://www.python.org/downloads/)
- **pip**: Package manager for Python (usually included with Python installations)
- **Git (optional)**: For cloning the repository

### Step 1: Clone or Download the Project

To get the project files, you can either clone the repository or download it as a ZIP file.
git clone <repo-url>

### Step 2: Change working directory to backend and install requirements.txt
in weather_backend.py, make sure to change to add your OpenWeatherAPI Key








Weather Dashboard
Description
Weather Dashboard is a web application that visualizes weather data for multiple cities. It displays daily weather summaries, including average, maximum, and minimum temperatures, as well as alerts for high temperatures. The application uses Chart.js for data visualization and Flask for the backend API.

Technologies Used
HTML, CSS, JavaScript
Chart.js: For data visualization
Flask: For the backend API
Fetch API: (OpenWeatherAPI) for making network requests
Features
Displays daily weather summary for cities.
Visualizes average, maximum, and minimum temperatures in a bar chart.
Alerts for temperatures exceeding a specified threshold.
Installation
Follow the steps below to set up the Weather Dashboard on your local machine.

Prerequisites
Ensure you have the following installed:

Python 3.6 or later: Download Python
pip: Package manager for Python (usually included with Python installations)
Git (optional): For cloning the repository
Step 1: Clone or Download the Project
To get the project files, you can either clone the repository or download it as a ZIP file.

bash
Copy code
git clone <repo-url>
cd WEATHERNEW
Step 2: Set Up the Backend
Navigate to the backend directory:

bash
Copy code
cd backend
Install required Python packages:

bash
Copy code
pip install -r requirements.txt
Configuration:

Open weather_backend.py.
Replace YOUR_API_KEY_HERE with your OpenWeather API key to enable weather data fetching:
python
Copy code
API_KEY = "YOUR_API_KEY_HERE"
Step 3: Run the Backend Server
Run the Flask server from the backend directory:

bash
Copy code
python weather_backend.py
This will start the backend server, which will handle API requests from the frontend.

Step 4: Open the Frontend
Navigate to the frontend folder.
Open index.html in your preferred web browser to access the Weather Dashboard interface.


## License

MIT License

Copyright (c) [2024] [Gargee Meshram]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.








