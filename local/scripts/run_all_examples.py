#!/usr/bin/env python3
"""
Newton 示例统一运行脚本
支持列出示例、运行示例、性能测试、交互选择等功能
"""
import argparse
import importlib
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

import warp as wp

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from newton.examples import get_examples, run, init, create_parser

# 结果保存目录
RESULTS_DIR = Path(__file__).parent.parent / "results"
SCREENSHOTS_DIR = RESULTS_DIR / "screenshots"
PERFORMANCE_DIR = RESULTS_DIR / "performance"
TEST_REPORTS_DIR = RESULTS_DIR / "test_reports"

# 创建必要的目录
for d in [RESULTS_DIR, SCREENSHOTS_DIR, PERFORMANCE_DIR, TEST_REPORTS_DIR]:
    d.mkdir(exist_ok=True, parents=True)


def get_categories(examples):
    """按分类组织示例"""
    categories = defaultdict(list)
    for name, module_path in examples.items():
        parts = module_path.split(".")
        category = parts[2] if len(parts) > 2 else "other"
        categories[category].append((name, module_path))
    return dict(sorted(categories.items()))


def list_examples(category_filter=None):
    """列出示例"""
    examples = get_examples()
    categories = get_categories(examples)

    if category_filter:
        if category_filter not in categories:
            print(f"错误: 分类 '{category_filter}' 不存在")
            print(f"可用分类: {', '.join(categories.keys())}")
            return
        categories = {category_filter: categories[category_filter]}

    total = 0
    print("=== Newton 示例列表 ===")
    for cat, items in categories.items():
        print(f"\n[{cat}] ({len(items)} 个示例):")
        for name, _ in items:
            print(f"  - {name}")
            total += 1
    print(f"\n总计: {total} 个示例")


def run_example(example_name, test_mode=False, device=None, num_frames=100):
    """运行单个示例"""
    examples = get_examples()
    if example_name not in examples:
        print(f"错误: 示例 '{example_name}' 不存在")
        return False

    print(f"\n=== 运行示例: {example_name} ===")

    try:
        # 保存原始sys.argv
        original_argv = sys.argv.copy()
        # 清空sys.argv避免和newton内部参数解析冲突
        sys.argv = [sys.argv[0]]
        if device:
            sys.argv.extend(["--device", device])
        if test_mode:
            sys.argv.append("--test")
        sys.argv.extend(["--viewer", "null" if test_mode else "gl"])
        sys.argv.extend(["--num-frames", str(num_frames)])
        sys.argv.append("--quiet")

        # 设置设备
        if device:
            wp.set_device(device)

        # 导入示例模块
        module_path = examples[example_name]
        mod = importlib.import_module(module_path)

        # 创建参数
        parser = getattr(mod.Example, "create_parser", create_parser)()
        args = parser.parse_args(sys.argv[1:])

        # 初始化查看器
        viewer, args = init(parser)

        # 创建示例实例
        example = mod.Example(viewer, args)

        # 测量性能
        start_time = time.time()
        run(example, args)
        elapsed = time.time() - start_time

        fps = num_frames / elapsed if elapsed > 0 else 0
        memory_used = 0

        print(f"✅ 示例运行完成: {example_name}")
        print(f"   耗时: {elapsed:.2f}s, 帧率: {fps:.2f} FPS")

        # 保存性能数据
        if not test_mode:
            perf_data = {
                "example": example_name,
                "elapsed": elapsed,
                "fps": fps,
                "device": device or wp.get_device().name,
                "timestamp": time.time()
            }
            perf_file = PERFORMANCE_DIR / f"{example_name}.json"
            with open(perf_file, "w") as f:
                json.dump(perf_data, f, indent=2)

        return True

    except Exception as e:
        print(f"❌ 示例运行失败: {example_name}")
        print(f"   错误: {str(e)}")

        # 保存错误日志
        error_file = TEST_REPORTS_DIR / f"{example_name}_error.log"
        with open(error_file, "w") as f:
            f.write(str(e))

        return False
    finally:
        # 恢复原始sys.argv
        sys.argv = original_argv


def run_by_category(category, test_mode=False, device=None):
    """按分类运行示例"""
    examples = get_examples()
    categories = get_categories(examples)

    if category not in categories:
        print(f"错误: 分类 '{category}' 不存在")
        print(f"可用分类: {', '.join(categories.keys())}")
        return

    items = categories[category]
    print(f"\n=== 运行分类 [{category}] 的 {len(items)} 个示例 ===")

    results = []
    for name, _ in items:
        success = run_example(name, test_mode=test_mode, device=device)
        results.append((name, success))

    # 统计结果
    success_count = sum(1 for _, s in results if s)
    total = len(results)
    print(f"\n=== 分类 [{category}] 运行完成 ===")
    print(f"成功: {success_count}/{total}, 失败: {total - success_count}/{total}")

    # 保存报告
    report = {
        "category": category,
        "total": total,
        "success": success_count,
        "failed": total - success_count,
        "results": results,
        "timestamp": time.time()
    }
    report_file = TEST_REPORTS_DIR / f"category_{category}_report.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)


def run_all(test_mode=False, device=None):
    """运行所有示例"""
    examples = get_examples()
    categories = get_categories(examples)

    total = len(examples)
    print(f"\n=== 运行所有 {total} 个示例 ===")

    results = []
    for cat, items in categories.items():
        print(f"\n--- 分类: {cat} ---")
        for name, _ in items:
            success = run_example(name, test_mode=test_mode, device=device)
            results.append((name, success, cat))

    # 统计结果
    success_count = sum(1 for _, s, _ in results if s)
    print(f"\n=== 全部示例运行完成 ===")
    print(f"成功: {success_count}/{total}, 失败: {total - success_count}/{total}")

    # 生成详细报告
    report = {
        "total": total,
        "success": success_count,
        "failed": total - success_count,
        "results": results,
        "device": device or wp.get_device().name,
        "timestamp": time.time()
    }
    report_file = TEST_REPORTS_DIR / "full_test_report.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    # 生成可读性报告
    text_report = [
        "Newton 示例测试报告",
        "=" * 40,
        f"测试时间: {time.ctime()}",
        f"设备: {device or wp.get_device().name}",
        f"总示例数: {total}",
        f"成功: {success_count} ({success_count/total*100:.1f}%)",
        f"失败: {total - success_count} ({(total - success_count)/total*100:.1f}%)",
        "\n失败列表:"
    ]

    for name, success, cat in results:
        if not success:
            text_report.append(f"  - [{cat}] {name}")

    text_report_path = TEST_REPORTS_DIR / "full_test_report.txt"
    with open(text_report_path, "w") as f:
        f.write("\n".join(text_report))

    print(f"\n测试报告已保存到: {text_report_path}")


def benchmark_all(device=None):
    """性能基准测试所有示例"""
    examples = get_examples()
    total = len(examples)

    print(f"\n=== 性能基准测试 {total} 个示例 ===")

    results = []
    for name in examples.keys():
        # 预热
        print(f"\n预热: {name}")
        run_example(name, test_mode=True, num_frames=10, device=device)

        # 正式测试
        print(f"\n测试: {name}")
        run_example(name, test_mode=False, num_frames=200, device=device)

        # 读取性能数据
        perf_file = PERFORMANCE_DIR / f"{name}.json"
        if perf_file.exists():
            with open(perf_file, "r") as f:
                data = json.load(f)
                results.append(data)

    # 生成性能报告
    results.sort(key=lambda x: x["fps"], reverse=True)

    report = [
        "Newton 性能基准测试报告",
        "=" * 60,
        f"测试时间: {time.ctime()}",
        f"设备: {device or wp.get_device().name}",
        "\n性能排名 (FPS 从高到低):",
        "-" * 60,
        f"{'示例名称':<30} {'FPS':<10} {'显存 (MB)':<12} {'耗时 (s)':<10}"
    ]

    for res in results:
        report.append(f"{res['example']:<30} {res['fps']:<10.2f} {res['memory_mb']:<12.2f} {res['elapsed']:<10.2f}")

    report_path = PERFORMANCE_DIR / "benchmark_report.txt"
    with open(report_path, "w") as f:
        f.write("\n".join(report))

    print(f"\n性能报告已保存到: {report_path}")


def interactive_mode():
    """交互式选择运行示例"""
    examples = get_examples()
    categories = get_categories(examples)

    print("=== 交互式示例选择器 ===")
    print("\n可用分类:")
    for i, cat in enumerate(categories.keys(), 1):
        print(f"{i}. {cat} ({len(categories[cat])} 个示例)")
    print(f"{len(categories)+1}. 所有示例")

    try:
        choice = int(input("\n请选择分类编号: ")) - 1
        cats = list(categories.keys())

        if choice == len(cats):
            # 运行所有
            run_all()
        elif 0 <= choice < len(cats):
            selected_cat = cats[choice]
            items = categories[selected_cat]

            print(f"\n分类 [{selected_cat}] 的示例:")
            for i, (name, _) in enumerate(items, 1):
                print(f"{i}. {name}")
            print(f"{len(items)+1}. 运行分类所有示例")

            ex_choice = int(input("\n请选择示例编号: ")) - 1
            if ex_choice == len(items):
                run_by_category(selected_cat)
            elif 0 <= ex_choice < len(items):
                run_example(items[ex_choice][0])
            else:
                print("无效选择")
        else:
            print("无效选择")

    except KeyboardInterrupt:
        print("\n退出交互模式")
    except ValueError:
        print("输入无效，请输入数字")


def main():
    parser = argparse.ArgumentParser(description="Newton 示例统一运行脚本")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出示例")
    list_parser.add_argument("--category", help="按分类筛选")

    # run 命令
    run_parser = subparsers.add_parser("run", help="运行示例")
    run_parser.add_argument("example", nargs="?", help="示例名称")
    run_parser.add_argument("--category", help="按分类运行")
    run_parser.add_argument("--all", action="store_true", help="运行所有示例")
    run_parser.add_argument("--test", action="store_true", help="测试模式")
    run_parser.add_argument("--device", help="运行设备 (e.g. cuda:0, cpu)")

    # benchmark 命令
    bench_parser = subparsers.add_parser("benchmark", help="性能基准测试")
    bench_parser.add_argument("--device", help="运行设备")

    # interactive 命令
    subparsers.add_parser("interactive", help="交互模式")

    args = parser.parse_args()

    if args.command == "list":
        list_examples(args.category)

    elif args.command == "run":
        if args.all:
            run_all(test_mode=args.test, device=args.device)
        elif args.category:
            run_by_category(args.category, test_mode=args.test, device=args.device)
        elif args.example:
            run_example(args.example, test_mode=args.test, device=args.device)
        else:
            run_parser.print_help()

    elif args.command == "benchmark":
        benchmark_all(device=args.device)

    elif args.command == "interactive":
        interactive_mode()


if __name__ == "__main__":
    main()
