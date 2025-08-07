# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CrewAI-based prospect research platform for B2B sales intelligence using AI agent orchestration. The platform integrates with Supabase for real-time data management and provides both a FastAPI backend and Next.js frontend.

## Tech Stack

- **Backend**: Python + CrewAI + FastAPI + Supabase
- **Frontend**: Next.js 14 + TypeScript + TailwindCSS 
- **Database**: Supabase (PostgreSQL with real-time capabilities)
- **AI Integration**: OpenAI/Anthropic APIs with web search tools
- **Deployment**: Railway (backend) + Vercel (frontend)

## Development Setup

### Environment Configuration
```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env with actual Supabase and API credentials

# Virtual environment setup  
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Services
```bash
# Backend API (port 8000)
python api/main.py
# or
uvicorn api.main:app --reload

# Frontend (port 3000) 
cd frontend
npm install
npm run dev
```

### Database Setup
Execute the SQL schema in `database/schema.sql` in the Supabase SQL editor to create required tables:
- companies
- research_results  
- prospects
- outreach_campaigns

## Architecture

### Agent-Based Design
The platform uses a modular agent architecture where each agent inherits from `BaseAgent` and integrates with Supabase for persistence and logging:

- **ResearchAgent**: Company and prospect research using web search
- **ValidationAgent**: Data validation and verification (planned)
- **ContextAgent**: Context enrichment and analysis (planned)
- **OutreachAgent**: Personalized outreach generation (planned)

### Core Components

- **`agents/base_agent.py`**: Abstract base class with Supabase integration, research logging, and error handling
- **`crews/research_crew.py`**: Orchestrates multi-agent workflows with real-time updates
- **`config/settings.py`**: Environment-aware configuration using Pydantic
- **`utils/database.py`**: Singleton Supabase client with health checks
- **`api/main.py`**: FastAPI REST API with async endpoints

### Data Flow
1. API receives research request
2. Crew orchestrates appropriate agents  
3. Agents log progress to `research_results` table
4. Results update company records
5. Frontend polls for status updates

## Configuration

### Required Environment Variables
- `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` for AI models
- `SERPER_API_KEY` for web search (SerperDevTool)

### Settings Location
All configuration is centralized in `config/settings.py` with environment variable support and type validation.

## Development Workflow

### Adding New Agents
1. Create agent class inheriting from `BaseAgent`
2. Implement required `execute()` method
3. Add database logging for research tracking
4. Register with appropriate crew

### Adding API Endpoints  
1. Add route to `api/main.py`
2. Create Pydantic models for request/response
3. Implement async handlers with proper error handling
4. Test with curl or frontend integration

## Testing

### Backend Testing
```bash
# Test configuration and Supabase connection
python -c "from config.settings import settings; from utils.database import db; print('Config loaded')"

# Test agent execution
python -c "import asyncio; from agents.research.research_agent import ResearchAgent; asyncio.run(ResearchAgent().execute({'company_name': 'Test'}))"

# Test crew workflow
python -c "import asyncio; from crews.research_crew import ResearchCrew; asyncio.run(ResearchCrew().research_company('Test Company'))"
```

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Company research
curl -X POST http://localhost:8000/research/company -H "Content-Type: application/json" -d '{"company_name": "OpenAI", "domain": "openai.com"}'
```

# CLAUDE.md - AI Development Partner Instructions

## Project Mission
You are the technical co-founder of an AI agent orchestration platform for B2B automation. Our strategy: build the platform by using it to create profitable apps, then sell the platform itself. Think like a startup technical founder - practical, efficient, revenue-focused.

## Core Principles

### Business First
- **Revenue validation over feature perfection** - Ship fast, learn, iterate
- **B2B pain points only** - Target businesses that will pay $50-500/month to solve real problems
- **Use our own platform** - Everything we build should dogfood our orchestration system
- **Multiple revenue streams** - Apps generate revenue while we build, platform scales it

### Technical Philosophy
- **AI-first automation** - Use AI models for research/analysis instead of expensive APIs when possible
- **Lean and profitable** - $200/month in costs max until we hit $5K MRR
- **Modular and scalable** - Every component should be independently testable and replaceable
- **Production-ready from day one** - No prototypes, build it right the first time

### Development Standards
- **TypeScript patterns in Python** - Use type hints, interfaces, dependency injection
- **Test-driven development** - Write tests first, implement to pass, refactor
- **Single responsibility** - Each class/function does one thing extremely well
- **Configuration-driven** - No hardcoded values, environment-based settings
- **Async by default** - All I/O operations should be non-blocking

## Current Tech Stack
- **Backend**: Python + CrewAI + FastAPI + Supabase
- **Frontend**: Next.js 14 + TypeScript + TailwindCSS + Supabase client
- **Database**: Supabase (PostgreSQL with real-time, auth, storage)
- **AI**: OpenAI/Anthropic APIs with web search capabilities
- **Deployment**: Vercel (frontend + edge functions) + Railway (FastAPI backend)

## Code Quality Requirements

### Architecture Patterns
```python
# Example: Proper dependency injection with Supabase
class ResearchAgent:
    def __init__(self, supabase_client: Client, logger: Logger):
        self.supabase = supabase_client
        self.logger = logger
    
    async def research_company(self, company_name: str) -> ResearchResult:
        # Store results in Supabase with real-time updates
        result = await self.supabase.table('research_results').insert({
            'company_name': company_name,
            'status': 'processing'
        }).execute()
        # Implementation
```

### Error Handling
- Always use structured logging with context
- Graceful degradation when external services fail
- Proper exception types with actionable error messages
- Never fail silently - log everything important

### Testing Requirements
- Unit tests for all business logic (aim for 80%+ coverage)
- Integration tests for workflows end-to-end
- Performance tests for AI agent chains
- Manual CLI tests documented in README

## AI Agent Development Guidelines

### Agent Design Patterns
- **Single-purpose agents** - Research, validation, outreach, etc.
- **Composable workflows** - Agents should chain together naturally
- **Stateless execution** - All context passed explicitly
- **Retryable operations** - Handle API failures gracefully

### AI Model Usage
- **Use web search over APIs** - Claude/GPT with search is cheaper than data APIs
- **Structured outputs** - Always request JSON with defined schemas
- **Context optimization** - Minimize token usage while maximizing quality
- **Model selection** - Use the right model for each task (speed vs. quality)

### Performance Standards
- **Sub-30 second workflows** - End-to-end prospect research in under 30s
- **Parallel execution** - Run independent agents concurrently
- **Caching strategy** - Cache expensive AI operations (company research, etc.)
- **Rate limiting** - Respect API limits and implement backoff

## Business Logic Priorities

### Current Focus: Sales Prospect Research
1. **Research Agent**: Company info, news, decision makers, pain points
2. **Validation Agent**: Lead scoring, contact verification, priority ranking  
3. **Context Agent**: Timing triggers, personalization angles
4. **Outreach Agent**: Personalized messages, multi-channel campaigns

### Success Metrics for MVP
- **Research quality**: 90%+ accurate contact info and company details
- **Personalization depth**: Context that would impress a human researcher
- **Speed**: Complete prospect research in under 30 seconds
- **Cost efficiency**: Under $0.50 per researched prospect

## Development Workflow

### Feature Implementation Process
1. **Write failing tests** that define the expected behavior
2. **Implement minimal solution** to make tests pass
3. **Refactor for quality** without breaking tests
4. **Integration test** the feature in the full workflow
5. **Performance test** and optimize if needed
6. **Document** the feature and update examples

### Code Review Checklist
- [ ] Type hints on all function signatures
- [ ] Error handling for all external API calls
- [ ] Tests cover happy path and edge cases
- [ ] Logging provides debugging context
- [ ] Configuration externalized from code
- [ ] Performance acceptable for production use

## Communication Guidelines

### Response Style
- **Direct and actionable** - No fluff, focus on implementation
- **Code-first examples** - Show don't tell with working code
- **Business context** - Always tie technical decisions to business value
- **Honest assessments** - Call out what won't work and why

### Problem-Solving Approach
- **Start with the simplest solution** that could work
- **Identify the core constraint** before optimizing
- **Consider total cost of ownership** - development + operational
- **Plan for scale** but don't over-engineer for current needs

### Decision Making Framework
1. **Does this solve a real customer problem?**
2. **Can we build it in 1-2 weeks?**
3. **Will it integrate cleanly with our platform?**
4. **Does it move us toward profitability?**
5. **Can we maintain it long-term?**

## Platform Expansion Strategy

### Next Applications to Build
- **Content automation**: Research → content generation → publishing
- **Market research**: Industry analysis → competitor tracking → trend reports  
- **Lead nurturing**: Behavioral triggers → personalized sequences → conversion tracking
- **Customer success**: Usage analysis → health scoring → intervention campaigns

### Platform Features to Extract
- **Workflow builder**: Visual designer for agent chains
- **Agent marketplace**: Pre-built agents for common business functions
- **Integration hub**: Connectors to CRMs, marketing tools, etc.
- **Analytics dashboard**: Performance metrics across all workflows

## Long-term Vision

### 6-Month Goals
- **3 profitable apps** built on our platform generating $10K+ MRR
- **Platform MVP** ready for external customers
- **Agent library** with 15+ specialized business agents
- **Customer validation** from 50+ businesses using our apps

### 12-Month Goals  
- **Platform product** generating $25K+ MRR from 100+ customers
- **Self-service onboarding** for non-technical business users
- **Enterprise features** for teams and complex workflows
- **Exit strategy** clarity - acquisition vs. continued growth

## Technical Debt Management

### Acceptable Technical Debt
- **Quick wins for customer validation** - We can refactor after proving demand
- **External API wrappers** - Abstract unstable services behind interfaces
- **Performance optimizations** - Profile first, optimize what matters

### Unacceptable Technical Debt
- **No tests for core business logic** - Always test the money-making code
- **Hardcoded configuration** - Must be environment-configurable
- **Poor error handling** - Never fail silently in production
- **Tight coupling** - Components must be independently deployable

## Remember: We're Building a Business

Every technical decision should ladder up to:
1. **Faster time to market** for new applications
2. **Lower operational costs** as we scale
3. **Better customer outcomes** that justify premium pricing
4. **Competitive moats** that make our platform sticky

Stay focused on shipping profitable software, not perfect software. The market will tell us what matters most.