简体中文 | [English](readme.md)

# FaceAlbumMind

> **FaceAlbumMind** 是一个基于人脸识别的智能相册管理工具，能够自动分析相册中的人物，进行人脸检测、向量生成，并根据人脸特征进行聚类，从而帮助用户轻松整理和管理照片。

## 目录

- [1. 介绍](#1)
- [2. 功能概览](#2)
- [3. 安装](#3)
  - [3.1 克隆项目](#3.1)
  - [3.2 依赖安装](#3.2)
- [4. 快速开始](#4)
  - [4.1 新建相册](#4.1)
  - [4.2 上传照片](#4.2)
  - [4.3 自动归类](#4.3)
  - [4.4 查看结果](#4.4)
- [5. 使用的技术](#5)
- [6. 下一步开发](#6)
- [7. 支持与反馈](#7)

<a name="1"></a>

## 1. 介绍

**FaceAlbumMind** 是一款基于深度学习的人脸识别工具，专为自动整理和管理相册中的人物照片设计。无论您有多少张照片，FaceAlbumMind 都能通过人脸识别技术自动将人物进行归类，方便您对照片进行搜索和管理。

### 核心功能：
- **人脸检测**：使用先进的深度学习算法检测相片中的人脸。
- **人脸向量**：每张照片中的人脸将被转化为特征向量，用于人物归类。
- **人脸聚类**：根据人脸特征自动将相似的人物归类在一起，轻松管理相册。
- **便捷操作**：通过 Streamlit 提供的简洁用户界面，轻松上传图片、查看归类结果。

<div align="center">
  <img src="./images/demo.gif" alt="FaceAlbumMind Demo">
</div>

<a name="2"></a>

## 2. 功能概览

FaceAlbumMind 提供了以下核心功能：

- **人脸检测与识别**：支持批量处理相册照片，检测和提取照片中的人脸。
- **人脸聚类**：基于人脸向量的聚类算法，将相似的面孔分到同一个分类中。
- **向量搜索**：未来计划与 Milvus 集成，实现更大规模的照片搜索和相似度匹配。
- **简单易用的界面**：基于 Streamlit 构建的交互式界面，用户可以轻松上传和管理照片。

<a name="3"></a>

## 3. 安装

你可以按照以下步骤安装并运行 FaceAlbumMind。

<a name="3.1"></a>

### 3.1 克隆项目

首先，克隆该项目到你的本地环境：

```bash
git clone https://github.com/chenwr727/FaceAlbumMind.git
cd FaceAlbumMind
```

<a name="3.2"></a>

### 3.2 依赖安装

FaceAlbumMind 使用 Python 进行开发，请确保你已安装 Python 3.7 及以上版本。接着，使用以下命令安装所需依赖：

```bash
pip install --upgrade -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

依赖列表包括但不限于：
- [InsightFace](https://github.com/deepinsight/insightface): 用于人脸检测和特征提取。
- [Streamlit](https://github.com/streamlit/streamlit): 用于创建交互式前端界面。
- [Milvus](https://github.com/milvus-io/milvus)（未来计划）: 用于高效的向量搜索和管理。

<a name="4"></a>

## 4. 快速开始

安装完成后，你可以通过以下命令启动 FaceAlbumMind：

```bash
python -m streamlit run main.py
```

此时，FaceAlbumMind 的用户界面将运行在本地浏览器中。接下来，按照以下步骤体验核心功能。

<a name="4.1"></a>

### 4.1 新建相册

点击 `New Album` 按钮，创建一个新的相册来管理你的照片。你可以为相册指定名称和描述，方便日后查找。

<div align="center">
  <img src="./images/add_new_group.png" alt="新建相册">
</div>

<a name="4.2"></a>

### 4.2 上传照片

在相册中点击 `Upload Photos`，你可以选择上传多张照片。上传的照片将被自动处理，提取人脸特征。

<div align="center">
  <img src="./images/upload_pictures.png" alt="上传照片">
</div>

<a name="4.3"></a>

### 4.3 自动归类

上传照片后，FaceAlbumMind 将自动进行人脸检测和特征提取。完成后，照片会按照人物归类显示。你可以点击每个类别查看该人物的所有照片。

<div align="center">
  <img src="./images/show_pictures.png" alt="自动归类">
</div>

<a name="4.4"></a>

### 4.4 查看结果

系统会为每个归类生成一个相册分类。用户可以点击分类查看归类后的照片列表，方便检索和管理。

<a name="5"></a>

## 5. 使用的技术

FaceAlbumMind 基于以下技术构建：

- **[InsightFace](https://github.com/deepinsight/insightface)**：用于人脸检测与特征提取。
- **[Streamlit](https://github.com/streamlit/streamlit)**：提供快速构建 Web 界面的工具，用户可以通过浏览器轻松操作。
- **[Pandas](https://pandas.pydata.org/)**：用于数据管理和处理。
- **[Milvus](https://github.com/milvus-io/milvus)**：未来用于向量检索，处理大规模人脸聚类。

<a name="6"></a>

## 6. 下一步开发

FaceAlbumMind 未来的开发方向包括：

- **Milvus 集成**：实现高效的向量搜索，支持更大规模的照片数据。
- **更多聚类算法**：支持 DBSCAN 等更多的人脸聚类算法。
- **多种分类模式**：除了人物分类，还将支持根据场景、日期等维度分类照片。
- **增强的用户体验**：增加更丰富的交互功能，如图片批量处理、标签管理等。

<a name="7"></a>

## 7. 支持与反馈

如果你在使用过程中遇到问题，或者有任何建议，请通过以下方式与我们联系：

- 提交 [Issue](https://github.com/chenwr727/FaceAlbumMind/issues)

我们会尽快回应您的反馈，并持续改进项目！
