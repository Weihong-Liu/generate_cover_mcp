#!/usr/bin/env python3
"""
测试CLI功能的脚本
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from generate_cover_mcp.cli import parse_categories, main
import argparse


def test_parse_categories():
    """测试分类解析功能"""
    print("测试分类解析功能...")

    # 测试用例
    test_cases = [
        ("技术,AI,编程", ["技术", "AI", "编程"]),
        ("技术, AI, 编程", ["技术", "AI", "编程"]),  # 带空格
        ("", []),  # 空字符串
        ("单个分类", ["单个分类"]),
        ("技术,AI,编程,", ["技术", "AI", "编程"]),  # 末尾逗号
    ]

    for input_str, expected in test_cases:
        result = parse_categories(input_str)
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{input_str}' -> {result}")


def test_cli_help():
    """测试CLI帮助信息"""
    print("\n测试CLI帮助信息...")

    # 模拟命令行参数
    original_argv = sys.argv
    try:
        sys.argv = ['generate-cover', '--help']
        try:
            main()
        except SystemExit:
            print("  ✓ 帮助信息正常显示")
    except Exception as e:
        print(f"  ✗ 帮助信息测试失败: {e}")
    finally:
        sys.argv = original_argv


def test_list_styles():
    """测试列出风格功能"""
    print("\n测试列出风格功能...")

    original_argv = sys.argv
    try:
        sys.argv = ['generate-cover', '--list-styles']
        try:
            main()
            print("  ✓ 风格列表正常显示")
        except SystemExit:
            print("  ✓ 风格列表正常显示")
    except Exception as e:
        print(f"  ✗ 风格列表测试失败: {e}")
    finally:
        sys.argv = original_argv


def main_test():
    """主测试函数"""
    print("🧪 CLI功能测试")
    print("=" * 40)

    test_parse_categories()
    test_cli_help()
    test_list_styles()

    print("\n" + "=" * 40)
    print("💡 注意: 实际封面生成需要 CoverMaster2.html 模板文件")
    print("可以通过以下命令测试完整功能:")
    print('generate-cover "测试标题" --html-path /path/to/CoverMaster2.html')


if __name__ == "__main__":
    main_test()