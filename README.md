<p align="center">
  <img src="https://raw.githubusercontent.com/getbindu/create-bindu-agent/refs/heads/main/assets/light.svg" alt="bindu Logo" width="200">
</p>

<h1 align="center">Tweet Analysis Agent</h1>
<h3 align="center">AI Social Media Intelligence Assistant</h3>

<p align="center">
  <strong>Professional social media intelligence and brand monitoring powered by AI</strong><br/>
  Real-time tweet analysis, sentiment classification, brand health monitoring, and competitive intelligence
</p>

<p align="center">
  <a href="https://github.com/ParasChamoli/tweet-analysis-agent/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/ParasChamoli/tweet-analysis-agent/main.yml?branch=main" alt="Build Status">
  </a>
  <a href="https://pypi.org/project/tweet-analysis-agent/">
    <img src="https://img.shields.io/pypi/v/tweet-analysis-agent" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python Version">
  <a href="https://github.com/ParasChamoli/tweet-analysis-agent/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/ParasChamoli/tweet-analysis-agent" alt="License">
  </a>
</p>

---

## 🎯 What is Tweet Analysis Agent?

An AI-powered social media intelligence assistant that analyzes tweets to extract insights such as sentiment, key topics, engagement patterns, and trends. It helps users understand public opinion, monitor brand perception, track trending discussions, and make data-driven decisions from Twitter/X content.

### Key Features
*   **🔍 Real-time Tweet Analysis** - Analyze sentiment, engagement, and trends from X/Twitter
*   **📊 Brand Health Monitoring** - Track brand perception and competitive intelligence
*   **📈 Engagement Metrics Analysis** - Likes, retweets, replies, and reach analytics
*   **🎯 Sentiment Classification** - Positive/Negative/Neutral/Mixed sentiment detection
*   **📋 Professional Reporting** - Executive-ready social media intelligence reports
*   **⚡ Lazy Initialization** - Fast boot times, initializes on first request
*   **🔐 Secure API Handling** - No API keys required at startup

---

## 🛠️ Tools & Capabilities

### Built-in Tools
*   **XTools** - X/Twitter API integration for tweet search and analysis
*   **Real-time Analysis** - Live sentiment tracking and trend detection

### Analysis Methodology
1.  **Data Collection** - Retrieve tweets using X/Twitter API
2.  **Sentiment Analysis** - Classify each tweet and aggregate sentiment
3.  **Engagement Analysis** - Analyze likes, retweets, replies, and reach
4.  **Brand Intelligence** - Monitor brand mentions and competitive positioning
5.  **Reporting** - Generate comprehensive social media intelligence reports

---

> **🌐 Join the Internet of Agents**
> Register your agent at [bindus.directory](https://bindus.directory) to make it discoverable worldwide and enable agent-to-agent collaboration. It takes 2 minutes and unlocks the full potential of your agent.

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/ParasChamoli/tweet-analysis-agent.git
cd tweet-analysis-agent

# Set up virtual environment with uv
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys:
# Choose ONE LLM provider:
# OPENAI_API_KEY=sk-...      # For OpenAI GPT-4o
# OPENROUTER_API_KEY=sk-...  # For OpenRouter (cheaper alternative)

# REQUIRED: Add X/Twitter API credentials
# Get credentials from: https://developer.twitter.com/en/portal/dashboard
X_CONSUMER_KEY=your_consumer_key
X_CONSUMER_SECRET=your_consumer_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
X_BEARER_TOKEN=your_bearer_token
```

### 3. Run Locally

```bash
# Start the tweet analysis agent
python tweet_analysis_agent/main.py

# Or using uv
uv run python tweet_analysis_agent/main.py
```

### 4. Test with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at: http://localhost:3774
```

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file:

```env
# Choose ONE provider (both can be set, OpenAI takes priority)
OPENAI_API_KEY=sk-...      # OpenAI API key
OPENROUTER_API_KEY=sk-...  # OpenRouter API key (alternative)

# REQUIRED: X/Twitter API credentials
X_CONSUMER_KEY=your_consumer_key
X_CONSUMER_SECRET=your_consumer_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
X_BEARER_TOKEN=your_bearer_token

# Optional
DEBUG=true                # Enable debug logging
MODEL_NAME=openai/gpt-4o  # Model selection (OpenRouter only)
```

### Port Configuration
Default port: `3774` (can be changed in `agent_config.json`)

---

## 💡 Usage Examples

### Via HTTP API

```bash
curl -X POST http://localhost:3774/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Analyze sentiment for tweets about climate change in the last 24 hours"
      }
    ]
  }'
```

### Sample Analysis Queries

```text
"Analyze sentiment around our brand on X for the past 10 tweets"
"Monitor competitor mentions and compare sentiment vs our brand"
"Generate a brand health report from recent social media activity"
"Identify trending topics and user sentiment about our product"
"Create a social media intelligence report for executive review"
```

### Expected Output Format

```markdown
# Social Media Intelligence Report 📊

## Brand Health Score: 7.5/10

## Executive Summary
{Concise overview of brand sentiment, key findings, and overall health}

## Sentiment Analysis
- Positive Sentiment: 60% (30 tweets)
- Negative Sentiment: 15% (8 tweets)
- Neutral Sentiment: 20% (10 tweets)
- Mixed Sentiment: 5% (2 tweets)

## Engagement Analysis
- Total Engagement: 12,500
- Average Engagement per Tweet: 250
- Top Performing Tweet: {engagement} (content preview)

## Key Themes & Topics
{Top themes with representative quotes and engagement metrics}

## Influencer Impact
{Verified accounts and influencers with significant reach}

## Strategic Recommendations
### Immediate Actions (Next 24-48 hours)
{Priority responses and monitoring needs}

### Short-term Initiatives (Next 1-2 weeks)
{Engagement opportunities and content strategy}

### Long-term Strategy (Next 1-3 months)
{Brand positioning and competitive response}
```

---

## 🐳 Docker Deployment

### Quick Docker Setup

```bash
# Build the image
docker build -t tweet-analysis-agent .

# Run container
docker run -d \
  -p 3774:3774 \
  -e OPENAI_API_KEY=your_key_here \
  -e X_CONSUMER_KEY=your_consumer_key \
  -e X_CONSUMER_SECRET=your_consumer_secret \
  -e X_ACCESS_TOKEN=your_access_token \
  -e X_ACCESS_TOKEN_SECRET=your_access_token_secret \
  -e X_BEARER_TOKEN=your_bearer_token \
  --name tweet-analysis-agent \
  tweet-analysis-agent

# Check logs
docker logs -f tweet-analysis-agent
```

### Docker Compose (Recommended)

`docker-compose.yml`:

```yaml
version: '3.8'
services:
  tweet-analysis-agent:
    build: .
    ports:
      - "3774:3774"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - X_CONSUMER_KEY=${X_CONSUMER_KEY}
      - X_CONSUMER_SECRET=${X_CONSUMER_SECRET}
      - X_ACCESS_TOKEN=${X_ACCESS_TOKEN}
      - X_ACCESS_TOKEN_SECRET=${X_ACCESS_TOKEN_SECRET}
      - X_BEARER_TOKEN=${X_BEARER_TOKEN}
    restart: unless-stopped
```

Run with Compose:

```bash
# Start with compose
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 📁 Project Structure

```text
tweet-analysis-agent/
├── tweet_analysis_agent/
│   ├── skills/
│   │   └── tweet-analysis/
│   │       └── skill.yaml          # Skill configuration
│   ├── __init__.py                 # Package initialization
│   ├── __version__.py              # Version information
│   └── main.py                     # Main agent implementation
├── agent_config.json               # Bindu agent configuration
├── pyproject.toml                  # Python dependencies
├── Dockerfile.agent                # Multi-stage Docker build
├── docker-compose.yml              # Docker Compose setup
├── README.md                       # This documentation
├── .env.example                    # Environment template
└── tests/                          # Test files
    └── test_main.py
```

---

## 🔌 API Reference

### Health Check

```bash
GET http://localhost:3774/health
```

Response:
```json
{"status": "healthy", "agent": "Tweet Analysis Agent"}
```

### Chat Endpoint

```bash
POST http://localhost:3774/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Your tweet analysis query here"}
  ]
}
```

---

## 🧪 Testing

### Local Testing

```bash
# Install test dependencies
uv sync --group dev

# Run tests
pytest tests/

# Test with specific API key
OPENAI_API_KEY=test_key python -m pytest
```

### Integration Test

```bash
# Start agent
python tweet_analysis_agent/main.py &

# Test API endpoint
curl -X POST http://localhost:3774/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Analyze tweets about AI"}]}'
```

---

## 🚨 Troubleshooting

### Common Issues & Solutions

**"ModuleNotFoundError"**
```bash
uv sync --force
```

**"Port 3774 already in use"**
Change port in `agent_config.json` or kill the process:
```bash
lsof -ti:3774 | xargs kill -9
```

**"No API key provided"**
Check if `.env` exists and variable names match. Or set directly:
```bash
export OPENAI_API_KEY=your_key
```

**"X/Twitter API credentials missing"**
Ensure all 5 X/Twitter credentials are set in `.env`:
```bash
X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET, X_BEARER_TOKEN
```

**"API rate limit exceeded"**
The agent implements exponential backoff. Wait and try again.

**Docker build fails**
```bash
docker system prune -a
docker-compose build --no-cache
```

---

## 📊 Dependencies

### Core Packages
*   **bindu** - Agent deployment framework
*   **agno** - AI agent framework
*   **openai** - OpenAI client
*   **tweepy** - X/Twitter API client
*   **requests** - HTTP requests
*   **rich** - Console output
*   **python-dotenv** - Environment management

### Development Packages
*   **pytest** - Testing framework
*   **ruff** - Code formatting/linting
*   **pre-commit** - Git hooks

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1.  Fork the repository
2.  Create a feature branch: `git checkout -b feature/improvement`
3.  Make your changes following the code style
4.  Add tests for new functionality
5.  Commit with descriptive messages
6.  Push to your fork
7.  Open a Pull Request

**Code Style:**
*   Follow PEP 8 conventions
*   Use type hints where possible
*   Add docstrings for public functions
*   Keep functions focused and small

---

## 📄 License
MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Credits & Acknowledgments
*   **Developer:** Paras Chamoli
*   **Framework:** Bindu - Agent deployment platform
*   **Agent Framework:** Agno - AI agent toolkit
*   **Twitter API:** X/Twitter Developer Platform

## 🔗 Useful Links
*   🌐 **Bindu Directory:** [bindus.directory](https://bindus.directory)
*   📚 **Bindu Docs:** [docs.getbindu.com](https://docs.getbindu.com)
*   🐙 **GitHub:** [github.com/ParasChamoli/tweet-analysis-agent](https://github.com/ParasChamoli/tweet-analysis-agent)
*   💬 **Discord:** Bindu Community

<br>

<p align="center">
  <strong>Built with ❤️ by Paras Chamoli</strong><br/>
  <em>Transforming social media data into actionable intelligence with AI</em>
</p>

<p align="center">
  <a href="https://github.com/ParasChamoli/tweet-analysis-agent/stargazers">⭐ Star on GitHub</a> •
  <a href="https://bindus.directory">🌐 Register on Bindu</a> •
  <a href="https://github.com/ParasChamoli/tweet-analysis-agent/issues">🐛 Report Issues</a>
</p>

> **Note:** This agent follows the Bindu pattern with lazy initialization and secure API key handling. It boots without API keys and only fails at runtime if keys are needed but not provided.
