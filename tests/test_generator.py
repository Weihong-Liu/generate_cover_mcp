"""
Tests for the cover generator.
"""

import pytest
import asyncio
import json
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

from generate_cover_mcp.generator import CoverGenerator


class TestCoverGenerator:
    """Test cases for CoverGenerator."""

    @patch('pathlib.Path.exists', return_value=True)
    def test_style_selection(self, mock_exists):
        """Test automatic style selection."""
        generator = CoverGenerator(html_path="dummy.html")

        # Test tech keywords
        assert generator.select_style("AI编程技术分享") == "swiss"
        assert generator.select_style("代码开发工具") == "swiss"

        # Test design keywords
        assert generator.select_style("创意设计分享") == "acid"

        # Test warning keywords
        assert generator.select_style("重要！必看内容") == "shock"

        # Test with categories
        assert generator.select_style("文章标题", ["技术", "编程"]) == "swiss"

    def test_get_available_styles(self):
        """Test getting available styles."""
        styles = CoverGenerator.get_available_styles()

        assert isinstance(styles, dict)
        assert "swiss" in styles
        assert "acid" in styles
        assert styles["swiss"] == "🇨🇭 瑞士国际"

    def test_init_with_missing_html(self):
        """Test initialization with missing HTML file."""
        with pytest.raises(FileNotFoundError):
            CoverGenerator(html_path="nonexistent.html")

    @patch.dict('os.environ', {'COVER_HTML_PATH': '/custom/path.html'})
    @patch('pathlib.Path.exists', return_value=True)
    def test_init_with_env_var(self, mock_exists):
        """Test initialization with environment variable."""
        generator = CoverGenerator()
        assert str(generator.html_path) == "/custom/path.html"


@pytest.mark.asyncio
class TestAsyncCoverGenerator:
    """Async test cases for CoverGenerator."""

    @patch('generate_cover_mcp.generator.async_playwright')
    @patch('pathlib.Path.exists', return_value=True)
    async def test_generate_cover(self, mock_exists, mock_playwright):
        """Test cover generation."""
        # Mock playwright components
        mock_browser = AsyncMock()
        mock_page = Mock()  # Page should be a regular Mock, not AsyncMock
        mock_canvas = AsyncMock()

        # Set up the async context manager and method chain
        mock_playwright_instance = AsyncMock()
        mock_playwright.return_value = mock_playwright_instance
        mock_playwright_instance.__aenter__.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_page.return_value = mock_page

        # query_selector is async and should return the canvas when awaited
        mock_page.query_selector = AsyncMock(return_value=mock_canvas)

        # Mock page methods - some are async, some are sync
        mock_page.goto = AsyncMock()
        mock_page.wait_for_selector = AsyncMock()
        mock_page.evaluate = AsyncMock()

        # Mock the locator chain properly - locator() is sync, returns sync Locator
        mock_locator = Mock()  # Locator itself is sync
        mock_first_locator = Mock()  # .first is also sync
        mock_first_locator.fill = AsyncMock()  # But .fill() is async
        mock_locator.first = mock_first_locator
        mock_page.locator.return_value = mock_locator

        mock_page.fill = AsyncMock()
        mock_page.click = AsyncMock()
        mock_canvas.screenshot = AsyncMock()
        mock_browser.close = AsyncMock()

        generator = CoverGenerator(html_path="dummy.html", output_dir="test_output")

        result = await generator.generate_cover(
            title="Test Title",
            subtitle="Test Subtitle"
        )

        assert result is not None
        assert "test_output" in result