# pypi-lwabish

## 简介

本pypi库主要收集个人自用的python snippets，方便日常学习和开发。随着知识的扩充和实践的增多，可能不定期按需重构，且不保证向后兼容。

## 安装&使用

```commandline
# 安装最新版本
pip install git+https://github.com/lwabish/pypi-lwabish.git@master

# 安装指定版本(例如v0.0.2)
pip install git+https://github.com/luabish/luabish.git@v0.0.2
```

安装完成后即可像使用其他库一样import本模块

```python
import lwabish

...
```

## 内容

- lwabish.common: 未分类的或不好分类的通用工具函数
- lwabish.structureutils: 以各种数据结构为核心的类定义以及工具函数
- lwabish.finance: 金融相关的工具函数，比如各种收益率如xirr的计算等
- lwabish.crawler: 和爬虫相关的工具函数。该模块很久未维护。
- ...

## 注意

由于模块里功能比较分散且未成型，所以没有把依赖写进pypi安装包的install_requires里，如果遇到ImportError可自行安装相关的模块