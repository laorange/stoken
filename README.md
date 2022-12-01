# stoken 

>  substitute-token

**以变量替换代码中密码等敏感信息**的命令行工具

---

使用方法：

1. 在release页面中下载，并添加到环境变量中 (或者 `pip install stoken` )

2. 在项目的根目录下创建 **`stoken.yaml`**：

```yaml
suffix:
  - .py
  - .js
  	
token:
  SECRET_TOKEN: qwertyuiop123456789
  MY_PASSWORD: poiuytrewq987654321
```

3. 假设有以下代码：

```python
# demo.py
token = "qwertyuiop123456789"
password = "poiuytrewq987654321"
print(f"{token=}, {password=}")
```

4. 执行 `stoken --hide` ，将会根据配置进行替换：

```python
# demo.py
token = "#{{{SECRET_TOKEN}}}#"
password = "#{{{MY_PASSWORD}}}#"
print(f"{token=}, {password=}")
```

5. 执行 `stoken --restore` ，将会根据配置进行复原。
