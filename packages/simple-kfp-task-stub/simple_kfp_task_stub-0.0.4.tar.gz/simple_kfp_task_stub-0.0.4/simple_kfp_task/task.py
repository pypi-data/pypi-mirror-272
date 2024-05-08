class Task:

    def __init__(
        self,
        **kwargs,
    ):
        self.func = kwargs.get("func")

    @classmethod
    def init(cls, **kwargs):
        return cls(**kwargs)

    def run(self):
        if self.func:
            return self.func()
        else:
            raise ValueError("Function is required for remote execution.")
