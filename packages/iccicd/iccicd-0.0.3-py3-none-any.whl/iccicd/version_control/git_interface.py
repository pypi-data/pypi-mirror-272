from iccore import process


class GitInterface:
    def __init__(self) -> None:
        pass

    def add_remote(self, name: str, path: str):
        cmd = f"git remote add {name} {path}"
        process.run(cmd)

    def add(self):
        cmd = "git add ."
        process.run(cmd)

    def commit(self, message: str):
        cmd = f"git commit -m {message}"
        process.run(cmd)

    def push(
        self,
        remote: str = "origin",
        src: str = "HEAD",
        dst: str = "main",
        extra_args: str = "",
    ):
        cmd = f"git push {remote} {src}:{dst} {extra_args}"
        process.run(cmd)

    def push_tags(self, remote: str = "origin"):
        cmd = f"git push --tags {remote}"
        process.run(cmd)

    def tag(self, tag: str):
        cmd = f"git tag {tag}"
        process.run(cmd)

    def set_user_email(self, email: str):
        cmd = f"git config user.email {email}"
        process.run(cmd)

    def set_user_name(self, name: str):
        cmd = f"git config user.name {name}"
        process.run(cmd)
