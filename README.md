# Bachelor-SearchMotor

This project is a search engine that uses AI to generate summaries of articles.
It consists of a Flask backend and a React frontend.
## Getting Started

### Prerequisites

    Python 3.x
    Node.js (includes npm)
    Homebrew (for macOS users)

## Installation
1. **Clone the repository**

git clone https://github.com/yourusername/Bachelor-SearchMotor.git
cd Bachelor-SearchMotor

2. **Setting up the backend environment**

Open a terminal and navigate into the backend folder:
cd backend

### Create and activate a virtual environment:
# Create a virtual environment
python -m venv venv

# Activate the environment
# For Windows
venv\Scripts\activate
# For macOS/Linux
source venv/bin/activate

You should now see a (venv) at the start of your terminal prompt.

3. **Installing backend dependencies**

While inside the backend folder and with the virtual environment activated, install the Python packages:

pip install -r requirements.txt

4. **Setting up environment variables**

    Create or open the existing .env file inside the backend folder.

    Add the following line:

OPENAI_API_KEY="your-openai-api-key-here"
Replace "your-openai-api-key-here" with your actual OpenAI API key.

5. **Starting the backend server**

After installing the dependencies and setting up the .env file, start the Flask server:

python app.py

6. **Setting up the frontend**

Open a second terminal window:
cd frontend
npm install
npm start

This will start the frontend development server, typically available at http://localhost:3000/.

## Structure

Bachelor-SearchMotor/
│── backend/         # Flask API & database
│── frontend/        # React app
│── database.db      # SQLite database
│── README.md        # This guide