import sys
from pathlib import Path
from typing import List, Dict, Union

import pydantic
import yaml
import colorama
from colorama import Fore
import click
import git

VERSION = "0.2.2"
README_URL = "https://github.com/laorange/stoken"
BASE_DIR = Path.cwd().resolve()
colorama.just_fix_windows_console()


class Config(pydantic.BaseModel):
    suffix: List[str]
    token: Dict[str, str]


class Stoken:
    def __init__(self, mode: str, encoding: str, variable_prefix: str, variable_suffix: str, debug: bool, no_git: bool):
        self.mode = mode
        self.encoding = encoding
        self.variable_prefix = variable_prefix
        self.variable_suffix = variable_suffix
        self.debug = debug
        self.no_git = no_git

        if mode == "debug":
            self.debug = True
            self.mode = "auto"

        self.config = self.get_config()
        self.git_repo = None if no_git else self.get_git_repo()

    @staticmethod
    def quit_with_info(info: str = None):
        info = info + '\n\n' if info else ''
        input(f"{info}Press ENTER to exist: ")
        sys.exit(1)

    @staticmethod
    def get_git_repo() -> Union[git.repo.base.Repo, None]:
        git_dev = BASE_DIR.resolve()
        while 1:
            if (git_dev / ".git").exists():
                try:
                    repo = git.repo.base.Repo(git_dev)
                    print(f"Found git root: {repo.git_dir}")
                    return repo
                except:
                    return None

            if git_dev.parent == git_dev:
                return None

            git_dev = git_dev.parent

    @staticmethod
    def get_config() -> Config:
        YAML_PATH = BASE_DIR / "stoken.yaml"
        YAML_PATH = YAML_PATH if YAML_PATH.exists() else BASE_DIR / "stoken.yml"
        if not YAML_PATH.exists():
            Stoken.quit_with_info(
                f"{Fore.RED}ERROR: Can't find configuration file! Create `stoken.yaml` in `{BASE_DIR}`. "
                f"Please refer to {README_URL}.{colorama.Style.RESET_ALL}"
            )
        else:
            print(f"{Fore.GREEN}stoken: read {YAML_PATH}{Fore.RESET}")

        with YAML_PATH.open("rt", encoding="utf-8") as yaml_file:
            try:
                config = Config(**yaml.load(yaml_file, Loader=yaml.SafeLoader))
                return config
            except Exception as e:
                Stoken.quit_with_info(
                    f"{Fore.RED}{e}\n\nFail to read configuration file. Please refer to {README_URL} and modify the `{YAML_PATH}`.{colorama.Style.RESET_ALL}"
                )

    def execute_for_file(self, file: Path):
        text_of_this_file = ""
        change_num = 0

        for line_num, line in enumerate(file.open(encoding=self.encoding)):
            content_of_this_line = line

            for key, token in self.config.token.items():
                variable = f"{self.variable_prefix}{key}{self.variable_suffix}"

                if self.mode == "auto":
                    if token in line:
                        self.mode = "hide"
                    elif variable in line:
                        self.mode = "restore"

                if self.mode == "hide":
                    if token in line:
                        content_of_this_line = content_of_this_line.replace(token, variable)
                        change_num += 1

                elif self.mode == "restore":
                    if variable in line:
                        content_of_this_line = content_of_this_line.replace(variable, token)
                        change_num += 1

            if content_of_this_line != line:
                print(f"{file.relative_to(BASE_DIR)} line-{line_num + 1}: {Fore.RED}{line.strip()} {Fore.RESET}-> {Fore.GREEN}{content_of_this_line.strip()}{Fore.RESET}")

            text_of_this_file += content_of_this_line

        if change_num:
            if not self.debug:
                with file.open("wt", encoding=self.encoding) as f:
                    f.write(text_of_this_file)
        else:
            if self.debug:  # print no-token files‘ names only in debug mode
                print(f"{file.relative_to(BASE_DIR)}: No tokens were found.")

    def execute(self, path: Path = None):
        if path is None:
            path = BASE_DIR

        if self.git_repo is not None:
            if Path(self.git_repo.git_dir) == path or self.git_repo.ignored(path):
                if path.is_dir() or path.suffix in self.config.suffix:
                    print(f"{path.relative_to(BASE_DIR)} has been ignored.")
                return

        if path.is_dir():
            for file in path.iterdir():
                self.execute(file)
        else:
            file = path
            if file.suffix in self.config.suffix:
                self.execute_for_file(file)


@click.command()
@click.option("--mode", type=click.Choice(['auto', 'hide', 'restore', 'debug'], case_sensitive=False), help='The mode of operation. Default: auto', default="auto")
@click.option("-e", "--encoding", default="utf-8", help='The encoding used to decode the file. Default: utf-8')
@click.option("-p", "--variable-prefix", default="#{{", help="The prefix of variable placeholder. Default: #{{")
@click.option("-s", "--variable-suffix", default="}}#", help="The suffix of variable placeholder. Default: }}#")
@click.option('--debug', is_flag=True, help="In debug mode, `stoken` won't modify files, only detect tokens.")
@click.option('--no-git', is_flag=True, help="By default, the program will detect if there is a git directory, and if so, it will ignore the files in .gitignore. Activate this option to detect all the files.")
@click.option("-v", "--version", is_flag=True, help="To get the current version of stoken.")
def main(mode: str, encoding: str, variable_prefix: str, variable_suffix: str, debug: bool, no_git: bool, version: bool):
    if version:
        return print(f"v{VERSION}")

    stoken = Stoken(mode, encoding, variable_prefix, variable_suffix, debug, no_git)
    stoken.execute()
    stoken.quit_with_info(f"{Fore.GREEN}stoken: finished!{Fore.RESET}")


if __name__ == '__main__':
    main()
