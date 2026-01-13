# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""tweet-analysis-agent - A Bindu Agent."""

import argparse
import asyncio
import json
import os
import sys
import traceback
from pathlib import Path
from textwrap import dedent
from typing import Any

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.openrouter import OpenRouter
from agno.tools.x import XTools
from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global agent instance
agent: Agent | None = None
_initialized = False
_init_lock = asyncio.Lock()


def load_config() -> dict:
    """Load agent configuration from project root."""
    # Try multiple possible locations for agent_config.json
    possible_paths = [
        Path(__file__).parent.parent / "agent_config.json",  # Project root
        Path(__file__).parent / "agent_config.json",  # Same directory as main.py
        Path.cwd() / "agent_config.json",  # Current working directory
    ]

    for config_path in possible_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except (PermissionError, json.JSONDecodeError) as e:
                print(f"⚠️  Error reading {config_path}: {type(e).__name__}")
                continue
            except Exception as e:
                print(f"⚠️  Unexpected error reading {config_path}: {type(e).__name__}")
                continue

    # If no config found or readable, create a minimal default
    print("⚠️  No agent_config.json found, using default configuration")
    return {
        "name": "tweet-analysis-agent",
        "description": "AI agent for tweet analysis and brand monitoring",
        "version": "1.0.0",
        "deployment": {
            "url": "http://127.0.0.1:3774",
            "expose": True,
            "protocol_version": "1.0.0",
            "proxy_urls": ["127.0.0.1"],
            "cors_origins": ["*"],
        },
        "environment_variables": [
            {"key": "OPENAI_API_KEY", "description": "OpenAI API key for LLM calls", "required": False},
            {"key": "OPENROUTER_API_KEY", "description": "OpenRouter API key for LLM calls", "required": False},
            {"key": "X_CONSUMER_KEY", "description": "X/Twitter API consumer key", "required": True},
            {"key": "X_CONSUMER_SECRET", "description": "X/Twitter API consumer secret", "required": True},
            {"key": "X_ACCESS_TOKEN", "description": "X/Twitter API access token", "required": True},
            {"key": "X_ACCESS_TOKEN_SECRET", "description": "X/Twitter API access token secret", "required": True},
            {"key": "X_BEARER_TOKEN", "description": "X/Twitter API bearer token", "required": True},
        ],
    }


async def initialize_agent() -> None:
    """Initialize the tweet analysis agent with proper model and tools."""
    global agent

    # Get API keys from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    model_name = os.getenv("MODEL_NAME", "openai/gpt-4o")

    # Get X/Twitter API credentials
    x_consumer_key = os.getenv("X_CONSUMER_KEY")
    x_consumer_secret = os.getenv("X_CONSUMER_SECRET")
    x_access_token = os.getenv("X_ACCESS_TOKEN")
    x_access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
    x_bearer_token = os.getenv("X_BEARER_TOKEN")

    # Model selection logic (supports both OpenAI and OpenRouter)
    if openai_api_key:
        model = OpenAIChat(id="gpt-4o", api_key=openai_api_key)
        print("✅ Using OpenAI GPT-4o")
    elif openrouter_api_key:
        model = OpenRouter(
            id=model_name,
            api_key=openrouter_api_key,
            cache_response=True,
            supports_native_structured_outputs=True,
        )
        print(f"✅ Using OpenRouter model: {model_name}")
    else:
        error_msg = (
            "No API key provided. Set OPENAI_API_KEY or OPENROUTER_API_KEY environment variable.\n"
            "For OpenRouter: https://openrouter.ai/keys\n"
            "For OpenAI: https://platform.openai.com/api-keys"
        )
        raise ValueError(error_msg)

    # Check X/Twitter credentials
    if not all([x_consumer_key, x_consumer_secret, x_access_token, x_access_token_secret, x_bearer_token]):
        error_msg = (
            "X/Twitter API credentials missing. Set all required environment variables:\n"
            "X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET, X_BEARER_TOKEN\n"
            "Get credentials from: https://developer.twitter.com/en/portal/dashboard"
        )
        raise ValueError(error_msg)

    # Initialize X/Twitter tools
    x_tools = XTools(
        consumer_key=x_consumer_key,
        consumer_secret=x_consumer_secret,
        access_token=x_access_token,
        access_token_secret=x_access_token_secret,
        bearer_token=x_bearer_token,
        include_post_metrics=True,
        wait_on_rate_limit=True,
    )

    # Create the tweet analysis agent
    agent = Agent(
        name="Social Media Analyst",
        model=model,
        tools=[x_tools],
        description=dedent("""\
            You are a senior Brand Intelligence Analyst specializing in social media
            listening on X (Twitter). Your mission is to transform raw tweet content
            and engagement metrics into executive-ready intelligence reports.

            Expertise includes:
            - Real-time tweet analysis and sentiment classification
            - Engagement metrics analysis (likes, retweets, replies, reach)
            - Brand health monitoring and competitive intelligence
            - Strategic recommendations and response strategies
            - Viral content analysis and influencer impact assessment\
        """),
        instructions=dedent("""\
            Core Analysis Steps:
            1. Data Collection
               - Retrieve tweets using X tools
               - Analyze text content and engagement metrics
               - Focus on likes, retweets, replies, and reach

            2. Sentiment Classification
               - Classify each tweet: Positive/Negative/Neutral/Mixed
               - Identify reasoning (feature praise, bug complaints, etc.)
               - Weight by engagement volume and author influence

            3. Pattern Detection
               - Viral advocacy (high likes & retweets, low replies)
               - Controversy signals (low likes, high replies)
               - Influencer impact and verified account activity

            4. Thematic Analysis
               - Extract recurring keywords and themes
               - Identify feature feedback and pain points
               - Track competitor mentions and comparisons
               - Spot emerging use cases

            Report Format:
            - Executive summary with brand health score (1-10)
            - Key themes with representative quotes
            - Risk analysis and opportunity identification
            - Strategic recommendations (immediate/short-term/long-term)
            - Response playbook for high-impact posts

            Guidelines:
            - Be objective and evidence-backed
            - Focus on actionable insights
            - Highlight urgent issues requiring attention
            - Provide solution-oriented recommendations\
        """),
        expected_output=dedent("""\
            # Social Media Intelligence Report 📊

            ## Brand Health Score: {score}/10

            ## Executive Summary
            {Concise overview of brand sentiment, key findings, and overall health}

            ## Sentiment Analysis
            - Positive Sentiment: {percentage}% ({count} tweets)
            - Negative Sentiment: {percentage}% ({count} tweets)
            - Neutral Sentiment: {percentage}% ({count} tweets)
            - Mixed Sentiment: {percentage}% ({count} tweets)

            ## Key Themes & Topics
            {Top themes with representative quotes and engagement metrics}

            ## Engagement Analysis
            - Total Engagement: {total}
            - Average Engagement per Tweet: {average}
            - Top Performing Tweet: {engagement} (content preview)

            ## Influencer Impact
            {Verified accounts and influencers with significant reach}

            ## Risk Assessment
            {Critical issues, complaints, and potential crises}

            ## Strategic Recommendations
            ### Immediate Actions (Next 24-48 hours)
            {Priority responses and monitoring needs}

            ### Short-term Initiatives (Next 1-2 weeks)
            {Engagement opportunities and content strategy}

            ### Long-term Strategy (Next 1-3 months)
            {Brand positioning and competitive response}

            ## Response Playbook
            {Template responses for common scenarios and high-impact posts}

            ---
            Analysis conducted by AI Social Media Intelligence Agent
            Report Generated: {current_date}
            Data Period: {analysis_period}\
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
    print("✅ Tweet Analysis Agent initialized")


async def run_agent(messages: list[dict[str, str]]) -> Any:
    """Run the agent with the given messages."""
    global agent
    if not agent:
        error_msg = "Agent not initialized"
        raise RuntimeError(error_msg)

    # Run the agent and get response
    response = await agent.arun(messages)
    return response


async def handler(messages: list[dict[str, str]]) -> Any:
    """Handle incoming agent messages with lazy initialization."""
    global _initialized

    # Lazy initialization on first call
    async with _init_lock:
        if not _initialized:
            print("🔧 Initializing Tweet Analysis Agent...")
            await initialize_agent()
            _initialized = True

    # Run the async agent
    result = await run_agent(messages)
    return result


async def cleanup() -> None:
    """Clean up any resources."""
    print("🧹 Cleaning up Tweet Analysis Agent resources...")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(description="Bindu Tweet Analysis Agent")

    parser.add_argument(
        "--openai-api-key",
        type=str,
        default=os.getenv("OPENAI_API_KEY"),
        help="OpenAI API key (env: OPENAI_API_KEY)",
    )
    parser.add_argument(
        "--openrouter-api-key",
        type=str,
        default=os.getenv("OPENROUTER_API_KEY"),
        help="OpenRouter API key (env: OPENROUTER_API_KEY)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_NAME", "openai/gpt-4o"),
        help="Model ID for OpenRouter (env: MODEL_NAME)",
    )
    parser.add_argument(
        "--x-consumer-key",
        type=str,
        default=os.getenv("X_CONSUMER_KEY"),
        help="X/Twitter API consumer key (env: X_CONSUMER_KEY)",
    )
    parser.add_argument(
        "--x-consumer-secret",
        type=str,
        default=os.getenv("X_CONSUMER_SECRET"),
        help="X/Twitter API consumer secret (env: X_CONSUMER_SECRET)",
    )
    parser.add_argument(
        "--x-access-token",
        type=str,
        default=os.getenv("X_ACCESS_TOKEN"),
        help="X/Twitter API access token (env: X_ACCESS_TOKEN)",
    )
    parser.add_argument(
        "--x-access-token-secret",
        type=str,
        default=os.getenv("X_ACCESS_TOKEN_SECRET"),
        help="X/Twitter API access token secret (env: X_ACCESS_TOKEN_SECRET)",
    )
    parser.add_argument(
        "--x-bearer-token",
        type=str,
        default=os.getenv("X_BEARER_TOKEN"),
        help="X/Twitter API bearer token (env: X_BEARER_TOKEN)",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to agent_config.json (optional)",
    )

    return parser


def set_environment_variables(args) -> None:
    """Set environment variables from command-line arguments."""
    env_vars = {
        "OPENAI_API_KEY": args.openai_api_key,
        "OPENROUTER_API_KEY": args.openrouter_api_key,
        "MODEL_NAME": args.model,
        "X_CONSUMER_KEY": args.x_consumer_key,
        "X_CONSUMER_SECRET": args.x_consumer_secret,
        "X_ACCESS_TOKEN": args.x_access_token,
        "X_ACCESS_TOKEN_SECRET": args.x_access_token_secret,
        "X_BEARER_TOKEN": args.x_bearer_token,
    }

    for key, value in env_vars.items():
        if value:
            os.environ[key] = value


def run_agent_server(config: dict) -> None:
    """Run the agent server with the given configuration."""
    try:
        # Bindufy and start the agent server
        print("🚀 Starting Bindu Tweet Analysis Agent server...")
        print(f"🌐 Server will run on: {config.get('deployment', {}).get('url', 'http://127.0.0.1:3774')}")
        bindufy(config, handler)
    except KeyboardInterrupt:
        print("\n🛑 Tweet Analysis Agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup on exit
        asyncio.run(cleanup())


def main():
    """Run the main entry point for the Tweet Analysis Agent."""
    parser = create_argument_parser()
    args = parser.parse_args()

    # Set environment variables from CLI args
    set_environment_variables(args)

    print("🤖 Tweet Analysis Agent - Social Media Intelligence AI")
    print("📊 Capabilities: Tweet sentiment analysis, brand monitoring, competitive intelligence")

    # Load configuration
    config = load_config()

    # Run the agent server
    run_agent_server(config)


if __name__ == "__main__":
    main()
