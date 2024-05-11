from collections.abc import Callable
from pathlib import Path
from typing import ParamSpec, TypeVar

import click

_T = TypeVar("_T")
_P = ParamSpec("_P")
_EntryPoint = Callable[_P, _T]
_ClickOption = Callable[[_EntryPoint[_P, _T]], _EntryPoint[_P, _T]]


def with_verbose() -> _ClickOption[_P, _T]:
    return click.option(
        "-v",
        "verbose",
        count=True,
        help="Configure logging verbosity.",
    )


def with_debugger() -> _ClickOption[_P, _T]:
    return click.option(
        "--pdb",
        "debugger",
        is_flag=True,
        help="Drop into python debugger if an error occurs.",
    )


def with_input_directory(name: str, default: str | Path) -> _ClickOption[_P, _T]:
    return click.option(
        f"--{name.replace('_', '-')}-dir",
        type=click.Path(exists=True, file_okay=False, dir_okay=True),
        default=default,
        show_default=True,
        help=f"Root directory where {name} inputs are stored.",
    )


def with_output_directory(default: str | Path) -> _ClickOption[_P, _T]:
    return click.option(
        "--output-dir",
        "-o",
        type=click.Path(exists=True, file_okay=False, dir_okay=True),
        default=default,
        show_default=True,
        help="Root directory where outputs will be saved.",
    )


def with_num_cores(default: int) -> _ClickOption[_P, _T]:
    return click.option(
        "--num-cores",
        "-c",
        type=click.INT,
        default=default,
        show_default=True,
    )


def with_queue() -> _ClickOption[_P, _T]:
    return click.option(
        "-q",
        "queue",
        type=click.Choice(["all.q", "long.q"]),
        default="all.q",
        help="Queue to submit jobs to.",
    )


def with_progress_bar() -> _ClickOption[_P, _T]:
    return click.option(
        "--progress-bar",
        "--pb",
        is_flag=True,
        help="Show a progress bar.",
    )


def with_dry_run() -> _ClickOption[_P, _T]:
    return click.option(
        "--dry-run",
        "-n",
        is_flag=True,
        help="Don't actually run the workflow.",
    )
