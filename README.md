# Automated Multi-Platform Posting System

A Python-based application built using FastAPI that publishes a single message across multiple third-party platforms through their REST APIs.

## Features

- FastAPI REST API integration
- Automated multi-platform posting
- Message validation (maximum 200 characters)
- Exactly one CTA URL validation
- URL validation
- Independent platform execution
- Individual success and failure handling
- Structured posting results
- Environment-based API credentials

## Technologies Used

- Python 3.x
- FastAPI
- Uvicorn
- Pydantic
- HTTPX
- REST APIs
- Python-dotenv

## Integrated Platforms

1. LinkedIn
2. Discord
3. Telegram
4. Slack
5. Dev.to

*Platform availability and successful publishing depend on valid credentials, API permissions and platform requirements.*

## Project Structure

```text
AutomatedMultiPlatformPostingSystem/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── config.py
│   ├── platforms/
│   │   ├── base.py
│   │   ├── linkedin.py
│   │   ├── discord.py
│   │   ├── telegram.py
│   │   ├── slack.py
│   │   └── devto.py
│   └── services/
│       └── posting_service.py
│
├── tests/
│   └── test_posting.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/MeghnaPujari22/AutomatedMultiPlatformPostingSystem.git
```

Navigate to the project:

```bash
cd AutomatedMultiPlatformPostingSystem
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the root directory.

Configure the required API credentials using `.env.example` as a reference.

Never commit your `.env` file or expose private API credentials.

## Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000
```

Open API documentation:

http://localhost:4000/docs

## API Endpoint

**POST** `/posting`

URL:

```text
http://localhost:4000/posting
```

### Sample Request

```json
{
  "message": "Explore our latest business platform https://example.com"
}
```

### Sample Response

The following is an illustrative response showing the expected response structure. Actual results depend on API execution.

```json
{
  "success": true,
  "results": [
    {
      "platform": "Discord",
      "status": "success",
      "posted_url": "https://discord.com/channels/example",
      "public_access": false,
      "date": "2026-11-19",
      "time": "10:30:00",
      "error": null
    },
    {
      "platform": "LinkedIn",
      "status": "failed",
      "posted_url": null,
      "public_access": false,
      "date": null,
      "time": null,
      "error": "Authentication failed"
    }
  ]
}
```

## Input Validation

- Message cannot exceed 200 characters.
- Exactly one CTA URL must be included.
- URL format must be validated.
- Invalid requests return appropriate validation errors.

## Error Handling

Each platform is handled independently. A failure on one platform should not prevent attempts to publish to other platforms.

## Testing

Run the tests:

```bash
pytest -v
```

## Screenshots

See the `screenshots/` directory for API documentation, request/response and execution evidence.

## Security

- API credentials are stored in environment variables.
- `.env` is excluded from Git.
- Never publish access tokens, passwords or private credentials.

## Author

**Meghna Revansiddha Pujari**

GitHub: https://github.com/MeghnaPujari22

LinkedIn: https://www.linkedin.com/in/meghna-pujari-7b2b25202

## License

This project was developed as part of a Python Practical Test.
