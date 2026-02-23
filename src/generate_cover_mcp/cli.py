"""
Command line interface for generating covers.
"""

import argparse
import asyncio
import sys
from pathlib import Path
from typing import List, Optional

from .generator import CoverGenerator


def parse_categories(categories_str: str) -> List[str]:
    """Parse comma-separated categories string."""
    if not categories_str:
        return []
    return [cat.strip() for cat in categories_str.split(',') if cat.strip()]


async def generate_single_cover_cli(
    title: str,
    subtitle: Optional[str] = None,
    categories: Optional[str] = None,
    url: Optional[str] = None,
    style: Optional[str] = None,
    output_filename: Optional[str] = None,
    html_path: Optional[str] = None,
    output_dir: str = "covers"
) -> None:
    """Generate a single cover from command line arguments."""

    try:
        # Initialize generator
        generator = CoverGenerator(html_path=html_path, output_dir=output_dir)

        # Parse categories
        category_list = parse_categories(categories) if categories else []

        # Set default subtitle if not provided
        if subtitle is None:
            subtitle = "精选内容·建议收藏"

        print(f"🎨 生成封面中...")
        print(f"   标题: {title}")
        print(f"   副标题: {subtitle}")
        if category_list:
            print(f"   分类: {', '.join(category_list)}")
        if style:
            print(f"   指定风格: {style}")

        # Generate cover
        filepath = await generator.generate_cover(
            title=title,
            subtitle=subtitle,
            categories=category_list,
            url=url or "",
            style=style,
            output_filename=output_filename
        )

        # Show results
        used_style = style or generator.select_style(title, category_list)
        style_name = generator.STYLE_NAMES.get(used_style, used_style)

        print(f"\n✅ 封面生成成功！")
        print(f"   文件路径: {filepath}")
        print(f"   使用风格: {style_name}")
        print(f"   输出目录: {generator.output_dir}")

    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
        print("请确保 CoverMaster2.html 模板文件存在")
        print("或通过 --html-path 参数指定正确路径")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        sys.exit(1)


def list_styles_cli() -> None:
    """List all available styles."""
    styles = CoverGenerator.get_available_styles()
    keywords = CoverGenerator.STYLE_KEYWORDS

    print("📋 可用封面风格:")
    print("=" * 50)

    for style_key, style_name in styles.items():
        style_keywords = keywords.get(style_key, [])
        print(f"\n🎯 {style_key}")
        print(f"   名称: {style_name}")
        print(f"   关键词: {', '.join(style_keywords[:5])}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="生成HTML封面 - 单条文章命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 基本用法
  generate-cover "AI编程技术分享"

  # 指定副标题和分类
  generate-cover "AI编程技术分享" --subtitle "技术干货" --categories "技术,AI,编程"

  # 指定风格
  generate-cover "重要通知" --style shock

  # 指定输出文件名
  generate-cover "我的文章" --output "my_cover.png"

  # 列出所有可用风格
  generate-cover --list-styles
        """
    )

    # Main arguments
    parser.add_argument(
        'title',
        nargs='?',
        help='文章标题 (必需，除非使用 --list-styles)'
    )

    parser.add_argument(
        '--subtitle', '-s',
        default=None,
        help='副标题 (默认: "精选内容·建议收藏")'
    )

    parser.add_argument(
        '--categories', '-c',
        default=None,
        help='分类，用逗号分隔 (例如: "技术,AI,编程")'
    )

    parser.add_argument(
        '--url', '-u',
        default=None,
        help='文章URL (用于生成文件名)'
    )

    parser.add_argument(
        '--style',
        choices=[
            'swiss', 'acid', 'pop', 'shock', 'diffuse',
            'sticker', 'journal', 'cinema', 'tech',
            'minimal', 'memo', 'geek'
        ],
        help='指定封面风格 (不指定则自动选择)'
    )

    parser.add_argument(
        '--output', '-o',
        default=None,
        help='输出文件名 (例如: "my_cover.png")'
    )

    parser.add_argument(
        '--html-path',
        default=None,
        help='CoverMaster2.html 模板文件路径'
    )

    parser.add_argument(
        '--output-dir',
        default='covers',
        help='输出目录 (默认: covers)'
    )

    # Utility arguments
    parser.add_argument(
        '--list-styles',
        action='store_true',
        help='列出所有可用的封面风格'
    )

    args = parser.parse_args()

    # Handle list styles
    if args.list_styles:
        list_styles_cli()
        return

    # Validate required arguments
    if not args.title:
        parser.error("需要提供文章标题，或使用 --list-styles 查看可用风格")

    # Run cover generation
    asyncio.run(generate_single_cover_cli(
        title=args.title,
        subtitle=args.subtitle,
        categories=args.categories,
        url=args.url,
        style=args.style,
        output_filename=args.output,
        html_path=args.html_path,
        output_dir=args.output_dir
    ))


if __name__ == "__main__":
    main()