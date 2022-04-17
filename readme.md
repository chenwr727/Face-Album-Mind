# Intelligent Gallery Album

* [1. Introduce](#1)
* [2. Install](#2)
  * [2.1 Program](#2.1)
  * [2.2 Requirements](#2.2)
* [3. Quick Start](#3)
  * [3.1 Add New Group](#3.1)
  * [3.2 Upload Pictures](#3.2)
  * [3.3 Show Labels](#3.3)
* [4. Next](#4)

<a name="1"></a>

## 1. Introduce
Intelligently categorize photos, automatically group photos belonging to the same person.

![](./images/demo.gif)

- [insightface](https://github.com/deepinsight/insightface)
- [streamlit](https://github.com/streamlit/streamlit)

<a name="2"></a>

## 2. Install

<a name="2.1"></a>

### 2.1 Program

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

### 2.2 Requirements

```bash
pip3 install --upgrade -r requirements.txt -i https://mirror.baidu.com/pypi/simple
```

<a name="3"></a>

## 3. Quick Start

```bash
python3 -m streamlit run main.py 
```

<a name="3.1"></a>

### 3.1 Add New Group
![](./images/add_new_group.png)

<a name="3.2"></a>

### 3.2 Upload Pictures
![](./images/upload_pictures.png)

<a name="3.3"></a>

### 3.3 Show Labels
![](./images/show_pictures.png)

<a name="4"></a>

## 4. Next

- Vector database built for scalable similarity search: [milvus](https://github.com/milvus-io/milvus/)