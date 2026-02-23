#!/usr/bin/env python3
"""
CLI使用示例 - 演示如何通过命令行生成单个封面
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """运行命令并显示输出"""
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"错误: {result.stderr}")
    return result.returncode == 0


def main():
    """演示CLI使用方法"""
    print("🎨 Generate Cover CLI 使用示例")
    print("=" * 50)

    # 检查是否安装了包
    print("\n1. 检查安装状态...")
    if not run_command("which generate-cover"):
        print("请先安装包: pip install -e .")
        return

    # 列出可用风格
    print("\n2. 查看可用风格...")
    run_command("generate-cover --list-styles")

    # 基本使用示例
    print("\n3. 基本使用示例...")
    examples = [
        'generate-cover "AI编程技术分享"',
        'generate-cover "创意设计新趋势" --subtitle "设计师必读" --categories "设计,创意,UI"',
        'generate-cover "重要！系统安全漏洞修复指南" --style shock',
        'generate-cover "生活小技巧" --output "life_tips_cover.png" --output-dir "my_covers"'
    ]

    for i, example in enumerate(examples, 1):
        print(f"\n示例 {i}:")
        print(f"命令: {example}")
        # 注意：这里只是展示命令，不实际执行，因为需要HTML模板文件
        print("(需要 CoverMaster2.html 模板文件才能实际执行)")

    print("\n" + "=" * 50)
    print("💡 使用提示:")
    print("1. 确保有 CoverMaster2.html 模板文件")
    print("2. 可通过 --html-path 指定模板文件路径")
    print("3. 使用 --help 查看完整参数说明")


if __name__ == "__main__":
    main()