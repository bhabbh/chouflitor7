# Chouflitor7

Chouflitor7 is a web application for organizing and joining padel matches. It allows users to create matches, view available matches, and join existing matches.

## Features

- User authentication (signup, login, logout)
- Create new padel matches
- View available and full matches
- Join existing matches
- Detailed match view with Google Maps integration

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/chouflitor7.git
   cd chouflitor7
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root directory and add the following:
   ```
   SECRET_KEY=your_secret_key_here
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   ```
   Replace `your_secret_key_here` with a secure random string and `your_google_maps_api_key_here` with your Google Maps API key.

2. In `match_details.html`, replace `YOUR_API_KEY` in the Google Maps script tag with `{{ google_maps_api_key }}`.

## Database Setup

The database will be automatically created when you run the application for the first time. However, if you need to reset the database, you can use the following steps:

1. Ensure you're in the project directory with your virtual environment activated.
2. Run the Python interpreter:
   ```
   python
   ```
3. In the Python shell, run:
   ```python
   from app import db
   db.drop_all()
   db.create_all()
   exit()
   ```

## Running the Application

1. Ensure you're in the project directory with your virtual environment activated.

2. Run the application:
   ```
   python run.py
   ```

3. Open a web browser and navigate to `http://127.0.0.1:5000/`

## Usage

- Sign up for a new account or log in to an existing account.
- Create a new match by clicking on "Create Match" and filling out the form.
- View available matches on the home page.
- Click on a match to view its details and join if spots are available.

## Contributing

Contributions to Chouflitor7 are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.