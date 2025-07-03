# Calorie Estimator

A modern web application that helps users track their calorie intake by analyzing food images using AI. The application provides detailed nutritional information and personalized health recommendations.

## Features

- User authentication and profile management
- Food image upload and analysis
- Calorie estimation using AI
- Nutritional value assessment
- Health recommendations
- Dietary restriction support
- Progress tracking

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd calorie-estimator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Create an account or log in to access the dashboard

4. Upload food images to get calorie estimates and nutritional information

## Project Structure

```
calorie-estimator/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── static/            # Static files
│   └── uploads/       # Uploaded images
└── templates/         # HTML templates
    ├── base.html      # Base template
    ├── index.html     # Home page
    ├── login.html     # Login page
    ├── register.html  # Registration page
    └── dashboard.html # User dashboard
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. # Calorie-Eatimator
