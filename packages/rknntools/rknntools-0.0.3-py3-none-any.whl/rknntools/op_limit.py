'''
rknn2模型转换工具代码一 输入onnx模型 输出初步算子匹配结果
'''
import onnx
import sys

def check_op_limit(modelname):
    '''
    :param modelname: onnx模型路径
    :return: 无返回，打印信息
    '''
    model = onnx.load(modelname)

    # Print all operations in the model
    operations = []

    for opset in model.opset_import:
        print("ONNX模型版本信息：\n")
        print(f"domain: {opset.domain} version: {opset.version}")

    for node in model.graph.node:
        # Only print operation if it is not already in the set
        if node.op_type not in operations:
            # print(f"Operation: {node.op_type}")
            operations.append(node.op_type)

    print("输入ONNX模型的操作列表：\n")
    print(operations)

    RK3566_152_NPUOPLIST = ['Add', 'Bias', 'Sub', 'Mul', 'Scale', 'Div', 'Max', 'Min', 'GlobalMaxPool',
                            'GlobalAveragePool', 'AveragePool',
                            'MaxPool', 'BatchNormalization', 'LayerNormalization', 'Clip', 'ReLU6', 'Elu', 'Gelu',
                            'Relu', 'LeakyRelu',
                            'PRelu', 'GRU', 'LSTM', 'Concat', 'Mish', 'Pad', 'ReduceMean', 'ReduceSum', 'Resize',
                            'Reshape', 'ReverseSequence',
                            'Sigmoid', 'HardSigmoid', 'Swish', 'HardSwish', 'Softplus', 'Softmax', 'Slice', 'Split',
                            'Tanh', 'Transpose', 'Convolution',
                            'DepthwiseConvolution', 'ConvTranspose', 'Deconvolution', 'Gemm', 'MatMul', 'Expand',
                            'Where', 'exGlu',
                            ]  # RKNN文档中的npu算子
    RK3566_152_NPUOPLIST = [item.upper() for item in RK3566_152_NPUOPLIST]

    RKNN_152_CPUOPLIST = ['ArgMin', 'ArgMax', 'Cast', 'Cos', 'DataConvert', 'DepthToSpace', 'Equal', 'Exp', 'Flatten',
                          'Gather', 'Greater', 'GreaterOrEqual',
                          'InstanceNormalization', 'Less', 'LessOrEqual', 'LogSoftmax', 'LpNormalization', 'LRN',
                          'MaxRoiPool', 'MaxUnpool', 'Mish', 'Min',
                          'Pad', 'Pow', 'Proposal', 'ReduceMax', 'ReduceMin', 'Reorg', 'Reshape', 'Resize', 'RoiAlign',
                          'RMSNorm', 'ScatterND', 'Sin', 'Slice',
                          'SpaceToDetph', 'Split', 'Sqrt', 'Squeeze', 'Tile', 'Upsample', 'Not']  # 文档中的CPU算子
    RKNN_152_CPUOPLIST = [item.upper() for item in RKNN_152_CPUOPLIST]

    RKNN_2_NEW_OP_LIST = ['And','GatherElements','Log']
    RKNN_2_NEW_OP_LIST = [item.upper() for item in RKNN_2_NEW_OP_LIST] #RKNN 2.0.0版本号后支持的新的算子

    ONNX_OP = ['Constant', 'Unsqueeze', 'Conv', 'Identity', 'ConstantOfShape', 'Shape','Erf']  # 文档中没有或者名称不匹配，但实际支持的算子
    ONNX_OP = [item.upper() for item in ONNX_OP]

    NO_SUPPORT_LIST = []
    for item in operations:
        if (item.upper() not in RK3566_152_NPUOPLIST) and (item.upper() not in RKNN_152_CPUOPLIST) and (item.upper() not in RKNN_2_NEW_OP_LIST) and (
                item.upper() not in ONNX_OP):
            NO_SUPPORT_LIST.append(item)

    if len(NO_SUPPORT_LIST) == 0:
        print("初步匹配该模型算子全部支持")
    else:
        print("不支持的操作列表：\n")
        print(NO_SUPPORT_LIST)



if __name__ =="__main__":
    check_op_limit(sys.argv[1])
    # check_op_limit('final.onnx')
