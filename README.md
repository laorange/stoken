# stoken 

>  substitute-token

[简体中文](https://github.com/laorange/stoken/blob/main/README.zh.md) | [English docs](https://github.com/laorange/stoken/blob/main/README.md)

A code desensitization tool, which can substitute tokens (and other sensitive information) in your code. 

---

## Quick start

1. Run: `pip install stoken` 

2. In the root directory of your project, create **`stoken.yaml`** and edit it with [syntax of yaml](https://en.wikipedia.org/wiki/YAML).
   + `suffix` : the suffix of the files you want to detect. **Don't forget there's a `.` before it**.
   + `token` : the sensitive data you want to substitute. 

```yaml
suffix:
  - .py
  - .js
  	
token:
  SECRET_TOKEN: qwertyuiop123456789
  MY_PASSWORD: poiuytrewq987654321
```

3. Here is demonstration code file, with the suffix `.py`：

```python
# demo.py
token = "qwertyuiop123456789"
password = "poiuytrewq987654321"
print(f"{token=}, {password=}")
```

4. Run `stoken --mode hide`, or run directly `stoken` with the default parameter `--mode auto`, the tokens will be substituted.

```python
# demo.py
token = "#{{SECRET_TOKEN}}#"
password = "#{{MY_PASSWORD}}#"
print(f"{token=}, {password=}")
```

5. Run `stoken --mode restore`, or run directly `stoken` with the default parameter `--mode auto`, the tokens will be restored.

## API

`stoken --help`

```
Options:
  --mode [auto|hide|restore|debug] The mode of operation. Default: auto.
  -e, --encoding TEXT              The encoding used to decode the file.
  -p, --variable-prefix TEXT       The prefix of variable placeholder.
  -s, --variable-suffix TEXT       The suffix of variable placeholder.
  --debug                          In debug mode, `stoken` won't modify files,
                                   only detect tokens.
  --help                           Show this message and exit.
```

