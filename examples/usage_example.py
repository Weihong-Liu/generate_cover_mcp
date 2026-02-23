#!/usr/bin/env python3
"""
Example usage of the generate-cover-mcp package.
"""

import asyncio
import json
from pathlib import Path

from generate_cover_mcp.generator import CoverGenerator


async def main():
    """Example usage of the cover generator."""

    # Initialize the generator
    # Make sure you have CoverMaster.html in your current directory
    # or set the COVER_HTML_PATH environment variable
    try:
        generator = CoverGenerator(
            html_path="CoverMaster.html",  # Update this path
            output_dir="example_covers"
        )
    except FileNotFoundError:
        print("Error: CoverMaster.html not found!")
        print("Please ensure the HTML template file is available.")
        return

    # Example 1: Generate a single cover
    print("Generating single cover...")
    try:
        cover_path = await generator.generate_cover(
            title="AI编程技术分享：如何使用Claude进行代码开发",
            subtitle="精选内容·建议收藏",
            categories=["技术", "AI", "编程"],
            url="https://example.com/article?sn=12345678"
        )
        print(f"✓ Single cover generated: {cover_path}")
    except Exception as e:
        print(f"✗ Failed to generate single cover: {e}")

    # Example 2: Generate multiple covers
    print("\nGenerating batch covers...")

    # Load sample articles
    sample_articles = [
        {
            "title": "创意设计新趋势：2026年UI设计指南",
            "subtitle": "设计师必读",
            "categories": ["设计", "创意", "UI"],
            "url": "https://example.com/article?sn=87654321"
        },
        {
            "title": "重要！系统安全漏洞修复指南",
            "subtitle": "紧急通知·立即查看",
            "categories": ["安全", "系统"],
            "url": "https://example.com/article?sn=11223344"
        },
        {
            "title": "生活小技巧：提高工作效率的10个方法",
            "subtitle": "实用干货分享",
            "categories": ["生活", "效率"],
            "url": "https://example.com/article?sn=44332211"
        }
    ]

    try:
        cover_paths = await generator.batch_generate(sample_articles)
        print(f"✓ Batch covers generated: {len(cover_paths)} files")
        for path in cover_paths:
            print(f"  - {path}")
    except Exception as e:
        print(f"✗ Failed to generate batch covers: {e}")

    # Example 3: List available styles
    print("\nAvailable styles:")
    styles = CoverGenerator.get_available_styles()
    for style_key, style_name in styles.items():
        keywords = CoverGenerator.STYLE_KEYWORDS.get(style_key, [])
        print(f"  {style_key}: {style_name}")
        print(f"    Keywords: {', '.join(keywords[:3])}...")

    print(f"\nAll covers saved to: {generator.output_dir}")


if __name__ == "__main__":
    asyncio.run(main())