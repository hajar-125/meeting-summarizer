# Meeting Summarizer

An automated application that processes meeting videos/audio records, transcribes them, extracts key information, and generates summaries in multiple formats.

## Features

- **Audio Extraction**: Convert video files to audio using ffmpeg
- **Transcription**: Convert audio to text using Whisper STT
- **Summarization**: Generate summaries using Claude API
- **Information Extraction**: Extract decisions, tasks, and responsible parties
- **Export Options**:
  - PDF generation using WeasyPrint
  - Notion database integration
  - Email delivery via SMTP or SendGrid

## Prerequisites

- Python 3.11+
- ffmpeg
- Docker (optional)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Usage

### Running Locally

```bash
python -m uvicorn src.main:app --reload
```

### Running with Docker

```bash
docker-compose up
```

## Project Structure

```
├── src/
│   ├── main.py                 # FastAPI entry point
│   ├── audio/                   # Audio processing
│   ├── processing/              # Text processing and summarization
│   ├── extraction/              # Information extraction
│   └── export/                  # Export functionality
├── tests/                       # Test suite
├── docs/                        # Documentation
└── docker-compose.yml           # Docker configuration
```

## Configuration

See `.env.example` for all available configuration options.

## Development

Run tests:
```bash
pytest tests/
```

## License

MIT
