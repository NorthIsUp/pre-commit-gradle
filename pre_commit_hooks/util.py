import os
import subprocess
from typing import Any

from whichcraft import which


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class CalledProcessError(RuntimeError):
    pass


def cmd_output(output: bool, *cmd: str, **kwargs: Any) -> str:
    retcode = kwargs.pop("retcode", 0)
    kwargs.setdefault("stdout", subprocess.PIPE)
    kwargs.setdefault("stderr", subprocess.PIPE)
    kwargs.setdefault("shell", True)
    proc = subprocess.Popen(" ".join(cmd), encoding="utf8", **kwargs)
    stdout, stderr = proc.communicate()
    print(stdout) if output else 0
    if retcode is not None and proc.returncode != retcode:
        print(stderr)
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout


def require_gradle(msg: str = "Gradle could not be detected."):
    if which("gradle") is None:
        print(f"{bcolors.FAIL}{msg}{bcolors.ENDC}")
        raise RuntimeError(msg)


def require_gradlew(
    msg: str = "Could not locate gradle wrapper. Initialize with `gradle wrapper`, or remove the -w (--wrapper) flag to use native gradle.",
):
    if which("gradlew", path=".") is None:
        print(f"{bcolors.FAIL}{msg}{bcolors.ENDC}")
        raise RuntimeError(msg)


def run_gradle_task(output: bool, *tasks: str) -> int:
    require_gradle()

    try:
        print(
            "{}Running 'gradle {}' with native gradle.{}".format(
                bcolors.OKBLUE, " ".join(tasks), bcolors.ENDC
            )
        )
        cmd_output(output, "gradle", *tasks)
        return 0
    except CalledProcessError:
        print(
            f"{bcolors.FAIL}The above error occurred running gradle task.{bcolors.ENDC}"
        )
        return 1


def run_gradle_wrapper_task(output: bool, *tasks: str) -> int:
    require_gradlew()

    try:
        print(
            "{}Running 'gradle {}' with wrapper enabled.{}".format(
                bcolors.OKBLUE, " ".join(tasks), bcolors.ENDC
            )
        )
        cmd_output(output, ".{}gradlew".format(os.path.sep), *tasks)
        return 0
    except CalledProcessError:
        print(
            f"{bcolors.FAIL}The above error occurred running gradle wrapper task.{bcolors.ENDC}"
        )
        return 1
