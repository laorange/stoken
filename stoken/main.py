import sys
from pathlib import Path

import yaml
import colorama

README_URL = "https://github.com/laorange/stoken"
BASE_DIR = Path(sys.argv[0]).parent
colorama.just_fix_windows_console()


def quit_with_info(info: str = None):
    info = info + '\n\n' if info else ''
    input(f"{info}Press ENTER to exist: ")
    sys.exit(1)


if __name__ == '__main__':
    YAML_PATH = BASE_DIR / "stoken.yaml"
    YAML_PATH = YAML_PATH if YAML_PATH.exists() else BASE_DIR / "stoken.yml"
    if not YAML_PATH.exists():
        quit_with_info(f"{colorama.Fore.RED}ERROR: Can't find configuration file! Create `stoken.yaml` in `{BASE_DIR}`. Please refer to {README_URL}.{colorama.Style.RESET_ALL}")

    with YAML_PATH.open("rt", encoding="utf-8") as yaml_file:
        try:
            config = yaml.load(yaml_file, Loader=yaml.SafeLoader)
        except Exception as e:
            quit_with_info(f"{colorama.Fore.RED}{e}\n\n"
                           f"Fail to read configuration file. Please refer to {README_URL} and modify the `{YAML_PATH}`.{colorama.Style.RESET_ALL}")

    print(config)

    entry()
