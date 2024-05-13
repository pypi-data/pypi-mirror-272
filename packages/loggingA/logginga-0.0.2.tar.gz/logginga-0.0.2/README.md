## 创作背景

> 每个项目都要配置一次日志，繁琐，故自定义了一个库

## 功能

- 将每一个级别的日志分别写入。相较于大杂烩，层次更清晰
- 开放日志实例名的定制
- 开放日志目录定制

## 安装

### 方式一： python

```
python3 setup.py install
```

### 方式二： pip

```
pip3 install loggingA
```

## 使用

```python
from loggingA.logger import get_logger

logger = get_logger("./", "flask")
logger.critical('This is a error message')
```