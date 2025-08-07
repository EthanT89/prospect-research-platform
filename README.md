# Prospect Research Platform

AI agent orchestration platform for B2B sales automation using CrewAI, FastAPI, and Supabase.

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Supabase account
- OpenAI/Anthropic API keys

### Setup
```bash
# Clone and setup backend
git clone https://github.com/YOUR_USERNAME/prospect-research-platform.git
cd prospect-research-platform
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Setup database
# Run database/schema.sql in Supabase SQL editor

# Start backend
python api/main.py

# Setup frontend (in new terminal)
cd frontend
npm install
npm run dev
```

### Usage
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Architecture

Modular agent-based system:
- **Research Agent**: Company/prospect intelligence
- **Validation Agent**: Lead scoring and verification
- **Context Agent**: Timing and personalization
- **Outreach Agent**: Multi-channel campaigns

## Development

### Testing
```bash
# Backend tests
pytest

# API health check
curl http://localhost:8000/health

# Research test
curl -X POST http://localhost:8000/research/company \
  -H "Content-Type: application/json" \
  -d '{"company_name": "OpenAI", "domain": "openai.com"}'
```

### Contributing
1. Follow the patterns in `CLAUDE.md`
2. Write tests for new features
3. Use type hints throughout
4. Test with Claude Code for AI-assisted development

## Tech Stack
- **Backend**: Python, CrewAI, FastAPI, Supabase
- **Frontend**: Next.js, TypeScript, TailwindCSS
- **AI**: OpenAI/Anthropic, web search tools
- **Deploy**: Railway (backend), Vercel (frontend)

## License
MIT