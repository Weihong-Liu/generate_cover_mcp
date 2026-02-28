"""Generate Cover MCP Server - HTML-based cover generation service."""

__version__ = "0.0.1"

import sys
import subprocess
import os
from pathlib import Path
from threading import Lock

_browser_check_done = False
_browser_check_lock = Lock()


def _get_proxy_env():
    """Get proxy environment variables for subprocess."""
    env = os.environ.copy()
    # Ensure proxy variables are set
    if 'https_proxy' not in env and 'HTTPS_PROXY' in env:
        env['https_proxy'] = env['HTTPS_PROXY']
    if 'http_proxy' not in env and 'HTTP_PROXY' in env:
        env['http_proxy'] = env['HTTP_PROXY']
    if 'all_proxy' not in env and 'ALL_PROXY' in env:
        env['all_proxy'] = env['ALL_PROXY']
    return env


def ensure_browser_installed(force=False) -> bool:
    """
    Ensure Playwright Chromium browser is installed.
    Returns True if browser is available, False otherwise.
    """
    global _browser_check_done

    with _browser_check_lock:
        if _browser_check_done and not force:
            return True

        try:
            from playwright.sync_api import sync_playwright
            # Try to launch browser to verify installation
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                browser.close()
            _browser_check_done = True
            return True
        except Exception:
            # Browser not installed, try to install it
            print("📦 首次运行，正在自动安装 Chromium 浏览器...")
            print("   这可能需要 1-2 分钟，请稍候...")

            try:
                env = _get_proxy_env()
                # Show proxy status
                if env.get('https_proxy'):
                    print(f"   使用代理: {env['https_proxy']}")

                result = subprocess.run(
                    [sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"],
                    env=env,
                    capture_output=False,  # Show progress to user
                    text=True,
                    check=False
                )
                if result.returncode == 0:
                    print("\n✅ 浏览器安装完成！")
                    _browser_check_done = True
                    return True
                else:
                    print(f"\n❌ 浏览器安装失败 (退出码: {result.returncode})")
                    print(f"\n请手动运行: {sys.executable} -m playwright install chromium --with-deps")
                    return False
            except Exception as install_error:
                print(f"❌ 浏览器安装出错: {install_error}")
                print(f"\n请手动运行: {sys.executable} -m playwright install chromium --with-deps")
                return False


# Try to ensure browser on import (but don't block if it fails)
try:
    ensure_browser_installed()
except Exception:
    pass


# Core module - always available
from .generator import CoverGenerator

__all__ = ["CoverGenerator", "__version__", "ensure_browser_installed"]


# Optional MCP server - only import if dependencies are available
try:
    from .server import main as server_main
    __all__.append("server_main")
except ImportError:
    pass

# CLI - always available
try:
    from .cli import main as cli_main
    __all__.append("cli_main")
except ImportError:
    pass
