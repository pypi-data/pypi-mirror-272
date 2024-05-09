# rknntools

- rknn模型转换可能会用到的工具
- RKNNTOOLKIT2版本 >= 1.5.2

#### 代码说明


op_limit.py 包括函数check_op_limit，输入onnx模型，输出算子匹配情况


#### 其他说明
- 目前算子已经匹配实例中的模型，以及conformer、zipformer等，后续可能有补充
- 目前依赖onnx库，测试1.13.1可行

#### TODO
- ONNX模型输入输出信息打印
- 读取ONNX模型并初始化全0输入，保存输出至文件供精度比对
- 修复ONNX模型的输入shape，满足rknntoolkits的要求
- 提供PT->ONNX代码，返回其中不支持算子在代码中的具体位置