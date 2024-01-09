import argparse

from pre_commit_hooks.util import run_gradle_task, run_gradle_wrapper_task


def parse_args(*tasks: str):
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
    )
    return parser.parse_args()


def gradle_task_main(*tasks: str) -> int:
    args = parse_args(*tasks)

    if args.wrapper:
        return run_gradle_wrapper_task(args.output, *args.tasks)
    else:
        return run_gradle_task(args.output, *args.tasks)


def gradle_spotless_main() -> int:
    return gradle_task_main("spotlessCheck", "spotlessApply")


def gradle_check_main() -> int:
    return gradle_task_main("check")


def gradle_build_main() -> int:
    return gradle_task_main("build")
