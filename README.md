# 数字图像处理 - 车牌检测项目

本项目是《数字图像处理》课程的期末课程设计，实现了一个基于深度学习的车牌检测模型。

## 项目简介

本项目不依赖现成的检测框架（如 Ultralytics YOLOv8），而是使用 PyTorch 从零搭建了一个轻量级的 `SimpleYOLO` 网络结构，用于实现车牌的定位与检测。

主要包含以下内容：
1. **数据预处理**：解压和处理车牌数据集及标注文件。
2. **模型构建**：实现了一个简化的卷积神经网络。
3. **模型训练**：自定义损失函数（包含坐标损失、置信度损失、分类损失）并进行模型训练。
4. **结果验证**：可视化检测结果。

## 目录结构

```
.
├── 模型代码.ipynb          # 主要代码文件
├── requirements.txt      # 依赖包列表
├── dataset.yaml          # 数据集配置文件
├── README.md             # 项目说明文档
├── .gitignore            # Git 忽略配置
│
│   # 以下文件/文件夹需自行准备 (不包含在仓库中)
├── license_plate_dataset/ # [需自行准备] 图片数据集
├── 车牌标注_processed_v2/ # [需自行准备] 标注文件
└── yolov8n.pt            # [可选] YOLOv8 预训练权重
```

## 环境安装

建议使用 Python 3.8+ 环境。

1. 克隆仓库：
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 数据集说明

出于版权和隐私考虑，本仓库**不包含**原始图片数据集。

## 快速开始

本项目的所有逻辑都封装在 `模型代码.ipynb` 中。

1. 启动 Jupyter Notebook：
   ```bash
   jupyter notebook
   ```

2. 打开 `模型代码.ipynb`。

3. 从上到下运行代码单元格即可。
   - 脚本会自动检查解压数据集。
   - 构建模型并加载数据。
   - 开始训练并展示验证结果。

## 模型架构

`SimpleYOLO` 模型结构如下：
- **Backbone**: 由 5 个卷积块组成，每个块包含 Conv + BatchNorm + LeakyReLU + MaxPool。
- **Head**: 检测头输出维度为 `anchors * (5 + num_classes)`，输出 13x13 的特征图。

## 许可证

MIT License
