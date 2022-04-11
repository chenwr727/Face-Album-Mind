# 人脸聚类

## 目录

* [1. 介绍](#1)
* [2. 安装](#2)
  * [2.1 程序结构](#2.1)
  * [2.2 安装依赖](#2.2)
* [3. 快速开始](#3)
  * [3.1 新建分组](#3.1)
  * [3.2 导入图片](#3.2)
  * [3.3 相册查看](#3.3)
* [4. 下一步](#4)

<a name="1"></a>

## 1. 介绍
`人脸聚类`，实现对相片进行智能分类，将属于同一人的相片自动归为一组。

- 人脸识别：[insightface](https://github.com/deepinsight/insightface)
- Web框架：[streamlit](https://github.com/streamlit/streamlit)

<a name="2"></a>

## 2. 安装

<a name="2.1"></a>

### 2.1 程序结构

    |-- InsightFace-Face-Cluster
        |-- modules
        |   |-- __init__.py
        |   |-- crud.py
        |   |-- database.py
        |   |-- models.py
        |   |-- schemas.py
        |-- utils
        |   |-- __init__.py
        |   |-- msyh.ttc
        |   |-- tools.py
        |-- main.py


<a name="2.2"></a>

### 2.2 安装依赖

```bash
pip3 install --upgrade -r requirements.txt -i https://mirror.baidu.com/pypi/simple
```

<a name="3"></a>

## 3. 快速开始

```bash
python3 -m streamlit run main.py 
```

<a name="3.1"></a>

### 3.1 新建分组
![](./images/add_new_group.png)

<a name="3.2"></a>

### 3.2 导入图片
![](./images/upload_pictures.png)

<a name="3.3"></a>

### 3.3 相册查看
![](./images/show_pictures.png)

<a name="4"></a>

## 4. 下一步

- 向量查询与检索：[milvus](https://github.com/milvus-io/milvus/)