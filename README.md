# NEXTSTEP

A comprehensive AI-powered assessment and learning platform built with FastAPI. Designed to evaluate and track student progress through multiple assessment phases with AI-generated feedback using Google's Generative AI.

## Features

- **Multi-Phase Assessment**: Structured assessment process with multiple phases
- **User Authentication**: Secure login and signup system with bcrypt hashing
- **AI-Powered Feedback**: Integration with Google Generative AI (Gemini) for intelligent feedback
- **Dashboard**: Real-time progress tracking and analytics
- **Admin Panel**: Administrative dashboard for managing assessments and users
- **Assessment Management**: Create, manage, and grade assessments
- **Result Tracking**: Detailed result analysis and reporting
- **FastAPI Backend**: Modern, fast API framework with automatic documentation
##  System Architecture  

![Next Step Assessment Flow](https://github.com/Yuvneet22/NEXTSTEP/blob/main/assets/system_architecture.png)

## Project Structure

```
NEXTSTEP/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                  # Flask app initialization
│   ├── models.py                # Database models
│   ├── database.py              # Database configuration
│   ├── static/                  # Static files
│   │   └── images/
│   │       └── assessment/
│   └── templates/               # HTML templates
│       ├── base.html
│       ├── login.html
│       ├── signup.html
│       ├── dashboard.html
│       ├── admin_dashboard.html
│       ├── assessment.html
│       ├── assessment_phase3.html
│       ├── assessment_final.html
│       └── result.html
├── data/                        # Data files
│   ├── __init__.py
│   ├── questions_data.py        # Question data
│   ├── questions_phase3.py
│   └── questions_final.py
├── scripts/                     # Utility scripts
│   ├── list_users.py
│   ├── manage_test_data.py
│   ├── migrate_db_v2.py
│   ├── migrate_db_v5.py
│   ├── rename_images.py
│   └── verify_classification.py
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README.md                    # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/NEXTSTEP.git
cd NEXTSTEP
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
python run.py
```

The application will be available at `http://127.0.0.1:8000`

API documentation available at `http://127.0.0.1:8000/docs`

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
APP_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///assessment.db
GEMINI_API_KEY=your-gemini-api-key-from-google
APP_PORT=8000
APP_HOST=127.0.0.1
```

**Important**: Get your `GEMINI_API_KEY` from [Google AI Studio](https://makersuite.google.com/app/apikey)

See `.env` file for more details.

## Usage

### User Registration and Login
- Navigate to `/signup` to create a new account
- Use `/login` to access existing accounts
- Access the dashboard after successful authentication

### Taking Assessments
- Select an assessment from the dashboard
- Complete all question phases
- View results and feedback upon completion

### Admin Functions
- Access `/admin` to manage assessments
- View user statistics and progress
- Manage test data and user accounts

## Database

The application uses SQLite by default. Database migrations are available in the `scripts/` directory:
- `migrate_db_v2.py` - Database schema updates
- `migrate_db_v5.py` - Latest schema version

## Utilities

Run utility scripts from the project root:

```bash
# List all users
python scripts/list_users.py

# Manage test data
python scripts/manage_test_data.py

# Verify classification
python scripts/verify_classification.py

# Rename assessment images
python scripts/rename_images.py
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
