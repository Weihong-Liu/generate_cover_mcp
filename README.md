# Generate Cover MCP

A Model Context Protocol (MCP) server for generating HTML-based covers using CoverMaster2.

## Features

- Generate beautiful covers from article data
- Multiple style options (Swiss, Acid, Pop, Shock, etc.)
- Automatic style selection based on content
- Batch processing support
- HTML-based rendering with Playwright

## Installation

```bash
pip install generate-cover-mcp
```

Or install from source:

```bash
git clone https://github.com/yourusername/generate-cover-mcp
cd generate-cover-mcp
pip install -e .
```

## Prerequisites

You need to install Playwright browsers:

```bash
playwright install chromium
```

## Usage

### Command Line Interface (推荐)

直接通过命令行生成单个封面：

```bash
# 基本用法
generate-cover "AI编程技术分享"

# 指定副标题和分类
generate-cover "AI编程技术分享" --subtitle "技术干货" --categories "技术,AI,编程"

# 指定风格
generate-cover "重要通知" --style shock

# 指定输出文件名和目录
generate-cover "我的文章" --output "my_cover.png" --output-dir "my_covers"

# 列出所有可用风格
generate-cover --list-styles
```

### As MCP Server

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "generate-cover": {
      "command": "generate-cover-mcp",
      "args": []
    }
  }
}
```

### Available Tools

- `generate_cover`: Generate a single cover from article data
- `batch_generate_covers`: Generate multiple covers from a list of articles
- `list_styles`: List available cover styles

## Configuration

The server includes a CoverMaster.html template file. You can also specify a custom template path via environment variable:

```bash
export COVER_HTML_PATH=/path/to/your/CoverMaster.html
```

## Article Data Format

```json
{
  "title": "Your Article Title",
  "categories": ["tech", "programming"],
  "url": "https://example.com/article?sn=12345678"
}
```

## Available Styles

- `swiss`: 🇨🇭 瑞士国际 - For tech, tools, development content
- `acid`: 💚 故障酸性 - For design, creative, art content
- `pop`: 🎨 波普撞色 - For news, entertainment, trending content
- `shock`: ⚡️ 冲击波 - For warnings, important, urgent content
- `diffuse`: 🌈 弥散光 - For lifestyle, health, emotional content
- `sticker`: 🍭 贴纸风 - For cute, casual, simple content
- `journal`: 📝 手账感 - For diary, thoughts, literary content
- `cinema`: 🎬 电影感 - For deep, movie, story content
- `tech`: 🔵 科技蓝 - For technology, data, analysis content
- `minimal`: ⚪️ 极简白 - For minimalist, design, aesthetic content
- `memo`: 🟡 备忘录 - For notes, lists, practical content
- `geek`: 🟢 极客黑 - For hacker, geek, programming content

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
isort src/

# Type checking
mypy src/
```

## License

MIT License - see LICENSE file for details.