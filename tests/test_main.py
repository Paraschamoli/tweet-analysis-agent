"""Tests for the Tweet Analysis Agent."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from tweet_analysis_agent.main import handler


@pytest.mark.asyncio
async def test_handler_returns_response():
    """Test that handler accepts messages and returns a response."""
    messages = [{"role": "user", "content": "Analyze tweets about our brand"}]

    # Mock the run_agent function to return a mock response
    mock_response = MagicMock()
    mock_response.run_id = "test-run-id"
    mock_response.status = "COMPLETED"
    mock_response.content = "Analysis completed successfully"

    # Mock _initialized to skip initialization and run_agent to return our mock
    with (
        patch("tweet_analysis_agent.main._initialized", True),
        patch(
            "tweet_analysis_agent.main.run_agent",
            new_callable=AsyncMock,
            return_value=mock_response,
        ),
    ):
        result = await handler(messages)

    # Verify we get a result back
    assert result is not None
    assert result.run_id == "test-run-id"
    assert result.status == "COMPLETED"
    assert result.content == "Analysis completed successfully"


@pytest.mark.asyncio
async def test_handler_with_multiple_messages():
    """Test that handler processes multiple messages correctly."""
    messages = [
        {"role": "system", "content": "You are a social media analyst."},
        {"role": "user", "content": "Analyze sentiment for @ourbrand on X"},
    ]

    mock_response = MagicMock()
    mock_response.run_id = "test-run-id-2"
    mock_response.content = "Sentiment analysis report generated"

    with (
        patch("tweet_analysis_agent.main._initialized", True),
        patch(
            "tweet_analysis_agent.main.run_agent",
            new_callable=AsyncMock,
            return_value=mock_response,
        ) as mock_run,
    ):
        result = await handler(messages)

    # Verify run_agent was called
    mock_run.assert_called_once_with(messages)
    assert result is not None
    assert result.run_id == "test-run-id-2"
    assert result.content == "Sentiment analysis report generated"


@pytest.mark.asyncio
async def test_handler_initialization():
    """Test that handler initializes on first call."""
    messages = [{"role": "user", "content": "Test analysis"}]

    mock_response = MagicMock()
    mock_response.run_id = "init-run-id"
    mock_response.status = "COMPLETED"

    # Start with _initialized as False to test initialization path
    with (
        patch("tweet_analysis_agent.main._initialized", False),
        patch("tweet_analysis_agent.main.initialize_agent", new_callable=AsyncMock) as mock_init,
        patch(
            "tweet_analysis_agent.main.run_agent",
            new_callable=AsyncMock,
            return_value=mock_response,
        ) as mock_run,
        patch("tweet_analysis_agent.main._init_lock", new_callable=MagicMock()) as mock_lock,
    ):
        # Configure the lock to work as an async context manager
        mock_lock_instance = MagicMock()
        mock_lock_instance.__aenter__ = AsyncMock(return_value=None)
        mock_lock_instance.__aexit__ = AsyncMock(return_value=None)
        mock_lock.return_value = mock_lock_instance

        result = await handler(messages)

        # Verify initialization was called
        mock_init.assert_called_once()
        # Verify run_agent was called
        mock_run.assert_called_once_with(messages)
        # Verify we got a result
        assert result is not None
        assert result.run_id == "init-run-id"


@pytest.mark.asyncio
async def test_handler_race_condition_prevention():
    """Test that handler prevents race conditions with initialization lock."""
    messages = [{"role": "user", "content": "Test race condition"}]

    mock_response = MagicMock()
    mock_response.run_id = "race-run-id"

    # Test with multiple concurrent calls
    with (
        patch("tweet_analysis_agent.main._initialized", False),
        patch("tweet_analysis_agent.main.initialize_agent", new_callable=AsyncMock) as mock_init,
        patch(
            "tweet_analysis_agent.main.run_agent",
            new_callable=AsyncMock,
            return_value=mock_response,
        ),
        patch("tweet_analysis_agent.main._init_lock", new_callable=MagicMock()) as mock_lock,
    ):
        # Configure the lock to work as an async context manager
        mock_lock_instance = MagicMock()
        mock_lock_instance.__aenter__ = AsyncMock(return_value=None)
        mock_lock_instance.__aexit__ = AsyncMock(return_value=None)
        mock_lock.return_value = mock_lock_instance

        # Call handler twice to ensure lock is used
        await handler(messages)
        await handler(messages)

        # Verify initialize_agent was called only once (due to lock)
        mock_init.assert_called_once()


@pytest.mark.asyncio
async def test_handler_with_tweet_analysis_query():
    """Test that handler can process a tweet analysis query."""
    messages = [
        {
            "role": "user",
            "content": "Analyze sentiment for tweets about climate change in the last 24 hours",
        }
    ]

    mock_response = MagicMock()
    mock_response.run_id = "analysis-run-id"
    mock_response.content = "Climate change sentiment analysis completed"
    mock_response.metadata = {"tweets_analyzed": 50, "sentiment_score": 0.75}

    with (
        patch("tweet_analysis_agent.main._initialized", True),
        patch(
            "tweet_analysis_agent.main.run_agent",
            new_callable=AsyncMock,
            return_value=mock_response,
        ),
    ):
        result = await handler(messages)

    assert result is not None
    assert result.run_id == "analysis-run-id"
    assert result.content == "Climate change sentiment analysis completed"
    assert result.metadata == {"tweets_analyzed": 50, "sentiment_score": 0.75}


@pytest.mark.asyncio
async def test_handler_with_brand_monitoring_query():
    """Test that handler can process a brand monitoring query."""
    messages = [
        {
            "role": "user",
            "content": "Monitor our brand mentions and compare with competitor XYZ",
        }
    ]

    mock_response = MagicMock()
    mock_response.run_id = "brand-run-id"
    mock_response.content = "Brand monitoring report generated"
    mock_response.comparison_data = {
        "our_brand": {"mentions": 150, "sentiment": 0.8},
        "competitor_xyz": {"mentions": 200, "sentiment": 0.65},
    }

    with (
        patch("tweet_analysis_agent.main._initialized", True),
        patch(
            "tweet_analysis_agent.main.run_agent",
            new_callable=AsyncMock,
            return_value=mock_response,
        ),
    ):
        result = await handler(messages)

    assert result is not None
    assert result.run_id == "brand-run-id"
    assert result.content == "Brand monitoring report generated"
    assert result.comparison_data == {
        "our_brand": {"mentions": 150, "sentiment": 0.8},
        "competitor_xyz": {"mentions": 200, "sentiment": 0.65},
    }
