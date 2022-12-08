import sys
from pathlib import Path
from typing import List, Dict, Union

import pydantic
import yaml
import colorama
from colorama import Fore
import click
import git

README_URL = "https://github.com/laorange/stoken"
BASE_DIR = Path.cwd().resolve()
colorama.just_fix_windows_console()


class Config(pydantic.BaseModel):
    suffix: List[str]
    token: Dict[str, str]


def quit_with_info(info: str = None):
    info = info + '\n\n' if info else ''
    input(f"{info}Press ENTER to exist: ")
    sys.exit(1)


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


@click.command()
@click.option("--mode", type=click.Choice(['auto', 'hide', 'restore', 'debug'], case_sensitive=False), help='The mode of operation.', default="auto")
@click.option("-e", "--encoding", default="utf-8", help='The encoding used to decode the file.')
@click.option("-p", "--variable-prefix", default="#{{", help="The prefix of variable placeholder.")
@click.option("-s", "--variable-suffix", default="}}#", help="The suffix of variable placeholder.")
@click.option('--debug', is_flag=True, help="In debug mode, `stoken` won't modify files, only detect tokens.")
def main(mode: str, encoding: str, variable_prefix: str, variable_suffix: str, debug: bool):
    if mode == "debug":
        debug = True
        mode = "auto"

    YAML_PATH = BASE_DIR / "stoken.yaml"
    YAML_PATH = YAML_PATH if YAML_PATH.exists() else BASE_DIR / "stoken.yml"
    if not YAML_PATH.exists():
        quit_with_info(f"{Fore.RED}ERROR: Can't find configuration file! Create `stoken.yaml` in `{BASE_DIR}`. Please refer to {README_URL}.{colorama.Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}stoken: read {YAML_PATH}{Fore.RESET}")

    with YAML_PATH.open("rt", encoding="utf-8") as yaml_file:
        try:
            config = Config(**yaml.load(yaml_file, Loader=yaml.SafeLoader))
        except Exception as e:
            quit_with_info(f"{Fore.RED}{e}\n\n"
                           f"Fail to read configuration file. Please refer to {README_URL} and modify the `{YAML_PATH}`.{colorama.Style.RESET_ALL}")

    repo = get_git_repo()
    for file in BASE_DIR.glob("**/*"):
        if repo is not None and repo.ignored(file):
            print(f"{file.relative_to(BASE_DIR)} has been ignored.")
            continue

        if file.suffix in config.suffix:
            text_of_this_file = ""
            change_num = 0

            for line_num, line in enumerate(file.open(encoding=encoding)):
                content_of_this_line = line

                for key, token in config.token.items():
                    variable = f"{variable_prefix}{key}{variable_suffix}"

                    if mode == "auto":
                        if token in line:
                            mode = "hide"
                        elif variable in line:
                            mode = "restore"

                    if mode == "hide":
                        if token in line:
                            content_of_this_line = content_of_this_line.replace(token, variable)
                            change_num += 1

                    elif mode == "restore":
                        if variable in line:
                            content_of_this_line = content_of_this_line.replace(variable, token)
                            change_num += 1

                if content_of_this_line != line:
                    print(f"{file.relative_to(BASE_DIR)} line-{line_num + 1}: {Fore.RED}{line.strip()} {Fore.RESET}-> {Fore.GREEN}{content_of_this_line.strip()}{Fore.RESET}")

                text_of_this_file += content_of_this_line

            if change_num:
                if not debug:
                    with file.open("wt", encoding=encoding) as f:
                        f.write(text_of_this_file)
            else:
                print(f"{file.relative_to(BASE_DIR)}: No tokens were found.")

    print(f"{Fore.GREEN}stoken: finished!{Fore.RESET}")


if __name__ == '__main__':
    main()
