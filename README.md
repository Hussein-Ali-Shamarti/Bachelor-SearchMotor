# Bachelor-SearchMotor

This project is a search engine that uses AI to generate summaries of articles. It consists of a Flask backend, an Ollama AI model, and a React frontend.
This assumes you have a Neon PostgreSQL database with pgvector setup with correct data.
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

**open terminal 1**
   cd backend
pip install flask flask-cors sqlalchemy requests
python app.py

**open terminal 2**
brew install ollama  # For macOS users, or download from https://ollama.ai
ollama pull mistral  # Download the AI model
ollama serve  # Start the AI model

**open terminal 3**
cd frontend
npm install
npm start

Bachelor-SearchMotor/
│── backend/        # Flask API & database
│── frontend/       # React app
│── Items.db        # SQLite database
│── README.md       # This guide