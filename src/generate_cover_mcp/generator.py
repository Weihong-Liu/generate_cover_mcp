"""
HTML-based cover generator using CoverMaster2 template.
"""

import json
import os
import asyncio
from pathlib import Path
from typing import Dict, List, Optional

try:
    from playwright.async_api import async_playwright, Page
except ImportError:
    raise ImportError(
        "Playwright is required. Install with: pip install playwright && playwright install chromium"
    )


class CoverGenerator:
    """HTML-based cover generator using CoverMaster2 template."""

    STYLE_KEYWORDS = {
        'swiss': ['技术', '工具', '开发', 'AI', '编程', '代码', '框架'],
        'acid': ['设计', '创意', '艺术', '潮流', '前卫'],
        'pop': ['新闻', '热点', '娱乐', '有趣', '趋势'],
        'shock': ['警告', '重要', '必看', '紧急', '注意'],
        'diffuse': ['生活', '健康', '情感', '故事', '清新'],
        'sticker': ['可爱', '轻松', '小技巧', '日常', '简单'],
        'journal': ['日记', '记录', '思考', '感悟', '文艺'],
        'cinema': ['深度', '电影', '故事', '专题', '叙事'],
        'tech': ['科技', '数据', '分析', '报告', '研究'],
        'minimal': ['极简', '设计', '美学', '纯粹'],
        'memo': ['笔记', '清单', '总结', '备忘', '实用'],
        'geek': ['黑客', '极客', '编程', '开发', '系统'],
    }

    STYLE_NAMES = {
        'swiss': '🇨🇭 瑞士国际',
        'acid': '💚 故障酸性',
        'pop': '🎨 波普撞色',
        'shock': '⚡️ 冲击波',
        'diffuse': '🌈 弥散光',
        'sticker': '🍭 贴纸风',
        'journal': '📝 手账感',
        'cinema': '🎬 电影感',
        'tech': '🔵 科技蓝',
        'minimal': '⚪️ 极简白',
        'memo': '🟡 备忘录',
        'geek': '🟢 极客黑',
    }

    def __init__(self, html_path: Optional[str] = None, output_dir: str = "covers"):
        """
        Initialize the cover generator.

        Args:
            html_path: Path to CoverMaster2.html template (auto-detected if not specified)
            output_dir: Directory to save generated covers
        """
        if html_path is None:
            html_path = os.environ.get('COVER_HTML_PATH')

        if html_path is None:
            # Try to find HTML template in package directory first
            from importlib.resources import files
            try:
                package_dir = files('generate_cover_mcp')
                html_path = str(package_dir / 'CoverMaster.html')
            except (ImportError, FileNotFoundError):
                # Fallback to current directory
                html_path = 'CoverMaster.html'

        self.html_path = Path(html_path).resolve()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if not self.html_path.exists():
            raise FileNotFoundError(
                f"HTML template not found: {self.html_path}\n"
                f"Please ensure CoverMaster.html is in the package directory or set COVER_HTML_PATH"
            )

    def select_style(self, title: str, categories: List[str] = None) -> str:
        """Automatically select style based on title and categories."""
        style_scores = {style: 0 for style in self.STYLE_KEYWORDS.keys()}

        # Score based on keywords in title and categories
        for style, keywords in self.STYLE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in title:
                    # Give higher weight to longer keyword matches
                    weight = len(keyword) if len(keyword) > 2 else 3
                    style_scores[style] += weight
                if categories:
                    for category in categories:
                        if keyword in category:
                            style_scores[style] += 2

        # Return highest scoring style
        max_score = max(style_scores.values())
        if max_score > 0:
            return max(style_scores.items(), key=lambda x: x[1])[0]

        # Fallback rules
        if any(word in title for word in ['!', '！', '必看', '警告', '注意']):
            return 'shock'
        if any(word in title for word in ['代码', '编程', '开发', 'AI', '技术']):
            return 'swiss'

        return 'swiss'  # Default style

    async def _setup_page(self, page: Page) -> None:
        """Setup the page with the HTML template."""
        await page.goto(f'file://{self.html_path}')
        await page.wait_for_selector('#canvas-stage', timeout=5000)

        # Hide zoom controls
        await page.evaluate('''
            () => {
                const zoomControls = document.querySelector('.absolute.bottom-6');
                if (zoomControls) zoomControls.style.display = 'none';
            }
        ''')
        await asyncio.sleep(0.5)

    async def _enable_auto_fit(self, page: Page) -> None:
        """Enable auto-fit functionality."""
        await page.evaluate('''
            () => {
                if (window.app && typeof window.app.updateState === 'function') {
                    window.app.updateState('autoFit', true);
                }
            }
        ''')

    async def generate_cover(
        self,
        title: str,
        subtitle: str = "精选内容·建议收藏",
        categories: List[str] = None,
        url: str = "",
        style: Optional[str] = None,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Generate a single cover.

        Args:
            title: Cover title
            subtitle: Cover subtitle
            categories: Content categories for style selection
            url: Source URL (used for filename generation)
            style: Force specific style (optional)
            output_filename: Custom output filename (optional)

        Returns:
            Path to generated cover image
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={'width': 1920, 'height': 1080})

            try:
                await self._setup_page(page)

                # Select style
                style_key = style or self.select_style(title, categories)

                # Fill form fields
                title_input = page.locator('input[type="text"]').first
                await title_input.fill(title)
                await asyncio.sleep(0.2)

                await page.fill('textarea', subtitle)
                await asyncio.sleep(0.2)

                # Select style
                style_name = self.STYLE_NAMES.get(style_key, style_key)
                await page.click(f'button:has-text("{style_name}")')
                await asyncio.sleep(0.3)

                # Enable auto-fit
                await self._enable_auto_fit(page)
                await asyncio.sleep(0.3)

                # Reset scale
                await page.evaluate('''
                    () => {
                        const wrapper = document.getElementById('preview-scale-wrapper');
                        if (wrapper) wrapper.style.transform = 'scale(1)';
                    }
                ''')
                await asyncio.sleep(0.2)

                # Take screenshot
                canvas = await page.query_selector('#canvas-stage')
                if not canvas:
                    raise RuntimeError("Canvas element not found")

                # Generate filename
                if output_filename:
                    filename = output_filename
                elif url and 'sn=' in url:
                    file_id = url.split('sn=')[-1][:8]
                    filename = f"cover_{style_key}_{file_id}.png"
                else:
                    file_id = abs(hash(title)) % 100000000
                    filename = f"cover_{style_key}_{file_id}.png"

                filepath = self.output_dir / filename
                await canvas.screenshot(path=str(filepath), type='png')

                return str(filepath)

            finally:
                await browser.close()

    async def batch_generate(
        self,
        articles: List[Dict],
        style_override: Optional[str] = None
    ) -> List[str]:
        """
        Generate covers for multiple articles.

        Args:
            articles: List of article data dictionaries
            style_override: Force specific style for all covers

        Returns:
            List of generated cover file paths
        """
        results = []

        for article in articles:
            try:
                title = article.get('title', 'Untitled')
                categories = article.get('categories', [])
                url = article.get('url', '')
                subtitle = article.get('subtitle', '精选内容·建议收藏')

                filepath = await self.generate_cover(
                    title=title,
                    subtitle=subtitle,
                    categories=categories,
                    url=url,
                    style=style_override
                )
                results.append(filepath)

            except Exception as e:
                print(f"Failed to generate cover for '{article.get('title', 'Unknown')}': {e}")
                continue

        return results

    @classmethod
    def get_available_styles(cls) -> Dict[str, str]:
        """Get all available styles with their display names."""
        return cls.STYLE_NAMES.copy()