"""
MCP Server for HTML-based cover generation.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

from .generator import CoverGenerator


class CoverMCPServer:
    """MCP Server for cover generation."""

    def __init__(self):
        self.server = Server("generate-cover-mcp")
        self.generator: Optional[CoverGenerator] = None
        self._setup_handlers()

    def _setup_handlers(self):
        """Setup MCP server handlers."""

        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            """List available tools."""
            return ListToolsResult(
                tools=[
                    Tool(
                        name="generate_cover",
                        description="Generate a single cover from article data",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "Cover title"
                                },
                                "subtitle": {
                                    "type": "string",
                                    "description": "Cover subtitle",
                                    "default": "精选内容·建议收藏"
                                },
                                "categories": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Content categories for style selection"
                                },
                                "url": {
                                    "type": "string",
                                    "description": "Source URL (used for filename generation)"
                                },
                                "style": {
                                    "type": "string",
                                    "description": "Force specific style (optional)",
                                    "enum": [
                                        "swiss", "acid", "pop", "shock", "diffuse",
                                        "sticker", "journal", "cinema", "tech",
                                        "minimal", "memo", "geek"
                                    ]
                                },
                                "output_filename": {
                                    "type": "string",
                                    "description": "Custom output filename (optional)"
                                },
                                "html_path": {
                                    "type": "string",
                                    "description": "Path to CoverMaster2.html template (optional)"
                                },
                                "output_dir": {
                                    "type": "string",
                                    "description": "Output directory for covers (optional)"
                                }
                            },
                            "required": ["title"]
                        }
                    ),
                    Tool(
                        name="batch_generate_covers",
                        description="Generate multiple covers from a list of articles",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "articles": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "title": {"type": "string"},
                                            "subtitle": {"type": "string"},
                                            "categories": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            },
                                            "url": {"type": "string"}
                                        },
                                        "required": ["title"]
                                    },
                                    "description": "List of article data"
                                },
                                "style_override": {
                                    "type": "string",
                                    "description": "Force specific style for all covers",
                                    "enum": [
                                        "swiss", "acid", "pop", "shock", "diffuse",
                                        "sticker", "journal", "cinema", "tech",
                                        "minimal", "memo", "geek"
                                    ]
                                },
                                "html_path": {
                                    "type": "string",
                                    "description": "Path to CoverMaster2.html template (optional)"
                                },
                                "output_dir": {
                                    "type": "string",
                                    "description": "Output directory for covers (optional)"
                                }
                            },
                            "required": ["articles"]
                        }
                    ),
                    Tool(
                        name="list_styles",
                        description="List all available cover styles with descriptions",
                        inputSchema={
                            "type": "object",
                            "properties": {}
                        }
                    )
                ]
            )

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls."""
            try:
                if name == "generate_cover":
                    return await self._generate_cover(arguments)
                elif name == "batch_generate_covers":
                    return await self._batch_generate_covers(arguments)
                elif name == "list_styles":
                    return await self._list_styles(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
            except Exception as e:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )

    async def _generate_cover(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Generate a single cover."""
        # Initialize generator with custom paths if provided
        html_path = arguments.get("html_path")
        output_dir = arguments.get("output_dir", "covers")

        generator = CoverGenerator(html_path=html_path, output_dir=output_dir)

        # Extract parameters
        title = arguments["title"]
        subtitle = arguments.get("subtitle", "精选内容·建议收藏")
        categories = arguments.get("categories", [])
        url = arguments.get("url", "")
        style = arguments.get("style")
        output_filename = arguments.get("output_filename")

        # Generate cover
        filepath = await generator.generate_cover(
            title=title,
            subtitle=subtitle,
            categories=categories,
            url=url,
            style=style,
            output_filename=output_filename
        )

        # Determine style used
        used_style = style or generator.select_style(title, categories)
        style_name = generator.STYLE_NAMES.get(used_style, used_style)

        result = {
            "success": True,
            "filepath": filepath,
            "title": title,
            "style": used_style,
            "style_name": style_name,
            "message": f"Cover generated successfully: {filepath}"
        }

        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(result, indent=2))]
        )

    async def _batch_generate_covers(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Generate multiple covers."""
        # Initialize generator with custom paths if provided
        html_path = arguments.get("html_path")
        output_dir = arguments.get("output_dir", "covers")

        generator = CoverGenerator(html_path=html_path, output_dir=output_dir)

        # Extract parameters
        articles = arguments["articles"]
        style_override = arguments.get("style_override")

        # Generate covers
        filepaths = await generator.batch_generate(articles, style_override)

        result = {
            "success": True,
            "generated_count": len(filepaths),
            "total_articles": len(articles),
            "filepaths": filepaths,
            "style_override": style_override,
            "message": f"Generated {len(filepaths)} covers out of {len(articles)} articles"
        }

        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(result, indent=2))]
        )

    async def _list_styles(self, arguments: Dict[str, Any]) -> CallToolResult:
        """List all available styles."""
        styles = CoverGenerator.get_available_styles()
        keywords = CoverGenerator.STYLE_KEYWORDS

        result = {
            "styles": {
                style_key: {
                    "name": style_name,
                    "keywords": keywords.get(style_key, [])
                }
                for style_key, style_name in styles.items()
            }
        }

        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(result, indent=2))]
        )

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="generate-cover-mcp",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    ),
                ),
            )


def main():
    """Main entry point."""
    server = CoverMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()