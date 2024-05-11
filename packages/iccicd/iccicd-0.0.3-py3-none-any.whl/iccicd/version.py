class Version:
    def __init__(self, input: str | None = None) -> None:
        self.major = 0
        self.minor = 0
        self.patch = 0

        if input:
            self.read(input)

    def read(self, input: str):
        major, minor, patch = input.split(".")
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
