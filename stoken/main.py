import sys
from pathlib import Path

import yaml
import colorama
from colorama import Fore

import click
from model import Config

README_URL = "https://github.com/laorange/stoken"
BASE_DIR = Path(sys.argv[0]).parent.resolve()
colorama.just_fix_windows_console()


def quit_with_info(info: str = None):
    info = info + '\n\n' if info else ''
    input(f"{info}Press ENTER to exist: ")
    sys.exit(1)


@click.command()
@click.option("--mode", type=click.Choice(['auto', 'hide', 'restore', 'debug'], case_sensitive=False), help='The mode of operation.', default="auto")
@click.option("-e", "--encoding", default="utf-8", help='The encoding used to decode the file.')
@click.option("-p", "--variable-prefix", default="#{{", help="The prefix of variable placeholder.")
@click.option("-s", "--variable-suffix", default="}}#", help="The suffix of variable placeholder.")
@click.option('--debug', is_flag=True, help="In debug mode, `stoken` won't modify files, only detect tokens.")
def entry(mode: str, encoding: str, variable_prefix: str, variable_suffix: str, debug: bool):
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

    for file in BASE_DIR.glob("**/*"):
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
    entry()
