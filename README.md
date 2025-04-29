# Bachelor-SearchMotor

This project is a search engine that uses AI to generate summaries of articles. It consists of a Flask backend and a React frontend.
## Getting Started

### Prerequisites

- Python 3.x
- Node.js
- Homebrew (for macOS users)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Bachelor-SearchMotor.git
   cd Bachelor-SearchMotor
  
2. **Setting up .env**
   Open a terminal
   cd backend
   Create a .env file or open the current one
   Insert/Edit this text: OPENAI_API_KEY= ""   // add your API key here

3. **open a terminal**
   cd backend
   pip install -r requirements.txt
   python app.py  **type this when the install is completed, to start the backend system**

4. **open a second terminal**
cd frontend
npm install
npm start    **to start the frontend**

#### Structure
Bachelor-SearchMotor/
│── backend/        # Flask API & database
│── frontend/       # React app
│── database.db        # SQLite database
│── README.md       # This guide