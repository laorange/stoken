# stoken 

[English docs](https://github.com/laorange/stoken/blob/main/README.md) | [简体中文](https://github.com/laorange/stoken/blob/main/README.zh.md)

项目名 `stoken` 是指 `substitute-token`。这是**以变量替换代码中密码等敏感信息**的命令行工具。

## 安装

### 方法一

如果您的设备上有 `Python` 环境，可以使用 `pip` 指令来安装 `stoken ` :

```
pip install stoken
```

### 方法二

您也可以选择到[Release页面](https://github.com/laorange/stoken/releases/)下载 `stoken.exe`，并将该程序添加到环境变量中，以便在命令行中直接使用。

## 使用方法

1. 假设有以下代码：

```python
# demo.py
token = "qwertyuiop123456789"
password = "poiuytrewq987654321"
print(f"{token=}, {password=}")
```

2. 在项目的根目录下创建 **`stoken.yaml`**，参考：[yaml语法](https://zhuanlan.zhihu.com/p/145173920).
   + `suffix` : 需要检测代码文件的后缀名。⚠️别忘了，在格式名前面有个`.`；
   + `token` : 需要替换的密码

```yaml
suffix:
  - .py
  - .js
  	
token:
  SECRET_TOKEN: qwertyuiop123456789
  MY_PASSWORD: poiuytrewq987654321
```

3. 执行 `stoken --mode hide`，或直接执行`stoken` (默认参数：`--mode auto`)，所有敏感信息被替换。

```python
# demo.py
token = "#{{SECRET_TOKEN}}#"
password = "#{{MY_PASSWORD}}#"
print(f"{token=}, {password=}")
```

4. 执行 `stoken --mode restore`，或直接执行`stoken` (默认参数：`--mode auto`)，所有敏感信息被还原。

## API

可执行 `stoken --help` 查看参数提示：

| 参数                        | 描述                                                         |
| --------------------------- | ------------------------------------------------------------ |
| `--mode`                    | 操作模式。默认：`auto`                                       |
| `-e` \| `--encoding`        | 文件编码，默认`utf-8`                                        |
| `-p` \| `--variable-prefix` | 变量占位符前缀，默认`#{{`                                    |
| `-s` \| `--variable-suffix` | 变量占位符前缀，默认`}}#`                                    |
| `--debug`                   | 调试模式下，仅检测，不修改                                   |
| `--no-git`                  | 默认情况下，程序会检测是否由Git管理，如果是，在查找密钥时将会跳过`.gitignore`中的文件。使用该选项，可以强制检测所有文件。 |
| `-v` | `--version`          | 查看`stoken` 的版本号                                        |
| `--help`                    | 查看使用说明                                                 |

