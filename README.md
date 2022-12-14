# stoken 

[简体中文](https://github.com/laorange/stoken/blob/main/README.zh.md) | [English docs](https://github.com/laorange/stoken/blob/main/README.md)

The project name `stoken` means `substitute-token`. It's a code desensitization tool, which can substitute tokens (and other sensitive information) in your code. 

## Installation

### Method 1

If there's **python environment** on your device, you can run this command to install `stoken `:

```
pip install stoken
```

### Method 2

(Perhaps for other language developers) You can browse the [release page](https://github.com/laorange/stoken/releases/), download the `stoken.exe`, add its path to your system environment variables.

## Quick start

1. Here is demonstration code file, with the suffix `.py`：

```python
# demo.py
token = "qwertyuiop123456789"
password = "poiuytrewq987654321"
print(f"{token=}, {password=}")
```

2. In the root directory of your project, create **`stoken.yaml`** and edit it with [syntax of yaml](https://en.wikipedia.org/wiki/YAML).
   + `suffix` : the suffixes of the files you want to detect. **Don't forget there's a `.` before each suffix**.
   + `token` : the sensitive data you want to substitute. 

```yaml
suffix:
  - .py
  - .js
  	
token:
  SECRET_TOKEN: qwertyuiop123456789
  MY_PASSWORD: poiuytrewq987654321
```

3. Run `stoken --mode hide`, or run directly `stoken` with the default parameter `--mode auto`, the tokens will be substituted.

```python
# demo.py
token = "#{{SECRET_TOKEN}}#"
password = "#{{MY_PASSWORD}}#"
print(f"{token=}, {password=}")
```

4. Run `stoken --mode restore`, or run directly `stoken` with the default parameter `--mode auto`, the tokens will be restored.

## API

`stoken --help`

| options                     | description                                                  |
| --------------------------- | ------------------------------------------------------------ |
| `--mode`                    | The mode of operation. Default: `auto`                       |
| `-e` \| `--encoding`        | The encoding used to decode the file. Default: `utf-8`       |
| `-p` \| `--variable-prefix` | The prefix of variable placeholder. Default: `#{{`           |
| `-s` \| `--variable-suffix` | The suffix of variable placeholder. Default: `}}#`           |
| `--debug`                   | Activate this option to enter debug mode, as result, `stoken` won't modify files, only detect tokens. |
| `--no-git`                  | By default, the program will detect if there is a git directory, and if so, it will ignore the files in `.gitignore`. Activate this option to detect all the files. |
| `-v` | `--version`          | Show this version of `stoken`.                               |
| `--help`                    | Show this message and exit.                                  |

