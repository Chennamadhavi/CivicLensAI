# CivicLens AI

CivicLens AI is an AI-powered civic issue reporting platform that helps citizens report public infrastructure and sanitation problems through text descriptions and images.

## Features

* Upload up to 5 images of a civic issue
* AI-powered issue analysis using Gemini
* Automatic classification of complaints
* Severity assessment
* Department recommendation
* Complaint tracking system
* Admin dashboard for complaint management
* Location-based complaint reporting
* Status updates (Open, In Progress, Resolved)

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### AI

* Google Gemini API

### Database

* SQLite

### Libraries

* Streamlit
* Pandas
* Google Generative AI
* Python Dotenv

## Project Structure

CivicLensAI/

├── app.py

├── modules/

│ ├── classify.py

│ ├── image_analyzer.py

│ └── database.py

├── pages/

│ ├── Admin_Dashboard.py

│ └── Saved_Complaints.py

├── requirements.txt

└── README.md

## How It Works

1. User uploads images or enters a complaint description.
2. AI analyzes the issue.
3. Complaint category, severity, department, and summary are generated.
4. Complaint is stored in the database.
5. Admin can review and update complaint status.

## Example Categories

* Roads & Infrastructure
* Waste Management
* Water Supply Issues
* Street Lighting
* Public Safety
* Drainage Problems

## Future Enhancements

* GPS-based location detection
* Interactive maps integration
* Real-time complaint tracking
* Multi-language support
* React + FastAPI version
* Cloud database integration

## Installation

```bash
git clone https://github.com/your-username/CivicLensAI.git
cd CivicLensAI
pip install -r requirements.txt
streamlit run app.py
```

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

## License

This project is developed for educational, research, and hackathon purposes.
