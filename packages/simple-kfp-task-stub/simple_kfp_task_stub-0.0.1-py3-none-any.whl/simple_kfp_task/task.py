import os
from typing import Callable

GIT_DIFF_MAX_LENGTH = 10000
PIP_PACKAGE_NAME = "simple-kfp-task"


class Task:

    def __init__(
        self,
        func: Callable = None
    ):
        self.func = func

    @classmethod
    def init(cls, **kwargs):
        return cls(**kwargs)

    def run(self):
        if self.func:
            return self.func()
        else:
            raise ValueError("Function is required for remote execution.")
