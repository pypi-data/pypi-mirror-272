from .git_interface import GitInterface


class GitlabUser:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email


class GitlabProject:
    def __init__(self, instance_url: str, repo_url: str) -> None:
        self.instance_url = instance_url
        self.repo_url = repo_url

    def _get_project_url(self):
        return f"{self.project.instance_url}/{self.repo_url}"

    url = property(_get_project_url)


class GitlabInterface:
    def __init__(
        self, project: GitlabProject, user: GitlabUser, access_token: str
    ) -> None:
        self.token = access_token
        self.project = project
        self.user = user
        self.git = GitInterface()
        self.remote_name = "origin"
        self.oath_origin_initialized = False

    def initialize_oath_origin(self):
        self.remote_name = "gitlab_oath_origin"
        self.git.set_user_email(self.user.email)
        self.git.set_user_name(self.user.name)

        url_prefix = f"https://oauth2:{self.token}"
        self.git.add_remote(self.remote_name, f"{url_prefix}@{self.project.url}.git")

    def push_change_ci(self, message: str):

        if not self.oath_origin_initialized:
            self.initialize_oath_origin()

        self.git.add()
        self.git.commit(message)
        self.git.push(self.remote_name, "HEAD", "main", "-o ci.skip")
