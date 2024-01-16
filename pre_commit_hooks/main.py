import argparse
import sys
from functools import wraps
from typing import Callable, Sequence

from pre_commit_hooks.util import run_gradle_task, run_gradle_wrapper_task


def parse_args(tasks: Sequence[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w",
        "--wrapper",
        action="store_true",
        help="Runs commands using gradlew. Requires gradle wrapper configuration within the project.",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="Prints the output of all executed gradle commands.",
    )
    parser.add_argument(
        "tasks",
        nargs="*",
        help="extra tasks",
        default=list(tasks),
    )
    return parser.parse_args()


def gradle_task_main(*tasks: str) -> int:
    args = parse_args(tasks)

    gradle = run_gradle_wrapper_task if args.wrapper else run_gradle_task

    return gradle(args.output, *args.tasks)


def gradle_spotless_main() -> int:
    return gradle_task_main("spotlessCheck", "spotlessApply")


def gradle_check_main() -> int:
    return gradle_task_main("check")


def gradle_build_main() -> int:
    return gradle_task_main("build")


def gradle_detekt_main() -> int:
    return gradle_task_main("detekt")


def use_gradle_wrapper(func: Callable[[], int]) -> Callable[[], int]:
    @wraps(func)
    def wrapper():
        sys.argv.append("--wrapper")
        return func()

    return wrapper


gradlew_task_main = use_gradle_wrapper(gradle_task_main)
gradlew_spotless_main = use_gradle_wrapper(gradle_spotless_main)
gradlew_check_main = use_gradle_wrapper(gradle_check_main)
gradlew_build_main = use_gradle_wrapper(gradle_build_main)
gradlew_detekt_main = use_gradle_wrapper(gradle_detekt_main)
