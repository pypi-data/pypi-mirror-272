# -*- coding: utf-8 -*-
import json
import numpy
import torch
import pickle
import numpy as np

from utils import datasets_load_preprocess, src_load_preprocess


def tsd_src_inference(src, net, device, pkl_path, length=8192, probability_output=False, confidence=0.5):
    """
    模型对数据进行推理
    :param src: read_local_file()的结果
    :param net: 实例化后的模型
    :param device: 使用'CPU'或'GPU'来推理
    :param pkl_path: 标准器文件路径
    :param length: 模型推理时使用的信号长度
    :param probability_output: 是否 开启概率值输出. True,表示输出是某一类别的概率表示
    :param confidence: 置信度.当probability_output=False时生效.默认为0.5,当预测的类别概率值>=0.5时,才认为预测正确;否则,算作相反类别.
    :return: 推理结果
    """
    data = src_load_preprocess(src, length)
    # 标准化处理
    with open(pkl_path, "rb") as f:
        scaler = pickle.load(f)
    data = data.reshape(1, -1)
    data = scaler.transform(data)
    # 修改输入形状为(batch_size, 1, 序列长度)
    test_data = torch.from_numpy(data[:, np.newaxis, :])

    # 设置模型为评估模式
    net.eval()

    test_data = test_data.to(device)  # 将 数据移到 device

    # 推理
    outputs = net(test_data)

    if probability_output:
        sample_classes = torch.sigmoid(outputs).argmax(dim=1)  # 将输出通过sigmoid函数转换为概率
        probability_values = torch.sigmoid(outputs).max(dim=1).values

        if sample_classes.item() == 0:
            result = ['normal', round(probability_values.item(), 4)]
        elif sample_classes.item() == 1:
            result = ['fault', round(probability_values.item(), 4)]
        else:
            raise ValueError("输出不在已知分类中!")

        result_json = {
            "status": f"{result[0]}",
            "probability": f"{result[1]}"
        }

    else:
        predictions = torch.sigmoid(outputs).argmax(dim=1)  # 将输出通过sigmoid函数转换为概率
        mask = torch.sigmoid(outputs).max(dim=1).values >= confidence
        predictions[~mask] = 1 - predictions[~mask]

        if predictions.item() == 0:
            result = 'normal'
        elif predictions.item() == 1:
            result = 'fault'
        else:
            raise ValueError("输出不在已知分类中!")

        result_json = {
            "status": f"{result}"
        }

    result_json = json.dumps(result_json, indent=4)  # 转换为 JSON 格式的字符串

    return result_json


def tsd_inference(file_path, net, device, pkl_path, length=8192, probability_output=False, confidence=0.5):
    """
    模型对信号进行诊断
    :param file_path: 待诊断文件夹路径
    :param net: 实例化后的模型
    :param device: 使用'CPU'或'GPU'来推理
    :param pkl_path: 标准器文件路径
    :param length: 模型推理时使用的信号长度
    :param probability_output: 是否 开启概率值输出. True,表示输出是某一类别的概率表示
    :param confidence: 置信度.当probability_output=False时生效.默认为0.5,当预测的类别概率值>=0.5时,才认为预测正确;否则,算作相反类别.
    """
    data, name_list = datasets_load_preprocess(file_path, length, target_mode='inference')
    # 标准化处理
    with open(pkl_path, "rb") as f:
        scaler = pickle.load(f)

    json_obj = {}
    outputs_list = []
    outputs = None

    # 设置模型为评估模式
    net.eval()

    if isinstance(data, numpy.ndarray):
        data = scaler.transform(data)

        # 修改输入形状为(batch_size, 1, 序列长度)
        test_data = torch.from_numpy(data[:, np.newaxis, :])

        test_data = test_data.to(device)  # 将 数据移到 device
        # 推理
        outputs, _ = net(test_data)
    else:
        for item in data:
            data = scaler.transform(item)

            # 修改输入形状为(batch_size, 1, 序列长度)
            test_data = torch.from_numpy(data[:, np.newaxis, :])

            test_data = test_data.to(device)  # 将 数据移到 device
            # 推理
            outputs, _ = net(test_data)

            outputs_list.append(outputs)

    if probability_output:  # 输出类别和概率
        if len(outputs_list):  # 多个文件预测
            for out_item in zip(outputs_list, name_list):
                sample_class = torch.sigmoid(out_item[0]).argmax(dim=1)  # sigmoid将输出转换为概率,再选择概率最大的类别
                probability_values = torch.sigmoid(out_item[0]).max(dim=1).values

                result = {
                    f"{out_item[1]}": {
                        "status": [],
                        "probability": [],
                        "average_probability": []
                    },
                }

                average_list = []
                for item in zip(sample_class.tolist(), probability_values.tolist()):
                    if item[0] == 0:
                        mark = "normal"
                    elif item[0] == 1:
                        mark = "fault"
                    else:
                        raise ValueError("输出不在已知分类中!")

                    result[f"{out_item[1]}"]["status"].append(mark)
                    result[f"{out_item[1]}"]['probability'].append(round(item[1], 4))

                    average_list.append(round(item[1], 4))

                average_probability = sum(average_list) / len(average_list)
                result[f"{out_item[1]}"]['average_probability'].append(average_probability)

                json_obj.update(result)
        else:
            # 单个文件预测
            sample_class = torch.sigmoid(outputs).argmax(dim=1)  # sigmoid将输出转换为概率,再选择概率最大的类别
            probability_values = torch.sigmoid(outputs).max(dim=1).values

            for name in name_list:
                result = {
                    f"{name}": {
                        "status": [],
                        "probability": [],
                        "average_probability": []
                    },
                }
                average_list = []
                for item in zip(sample_class.tolist(), probability_values.tolist()):
                    if item[0] == 0:
                        mark = "normal"
                    elif item[0] == 1:
                        mark = "fault"
                    else:
                        raise ValueError("输出不在已知分类中!")

                    result[f"{name}"]["status"].append(mark)
                    result[f"{name}"]['probability'].append(round(item[1], 4))

                    average_list.append(round(item[1], 4))

                average_probability = sum(average_list) / len(average_list)
                result[f"{name}"]['average_probability'].append(average_probability)

                json_obj.update(result)

    else:  # 只输出类别
        if len(outputs_list):  # 多个文件预测
            for out_item in zip(outputs_list, name_list):
                sample_class = torch.sigmoid(out_item[0]).argmax(dim=1)  # sigmoid将输出转换为概率,再选择概率最大的类别
                mask = torch.sigmoid(out_item[0]).max(dim=1).values >= confidence
                sample_class[~mask] = 1 - sample_class[~mask]

                result = {
                    f"{out_item[1]}": {
                        "status": []
                    },
                }

                for item in sample_class.tolist():
                    if item == 0:
                        mark = "normal"
                    elif item == 1:
                        mark = "fault"
                    else:
                        raise ValueError("输出不在已知分类中!")

                    result[f"{out_item[1]}"]["status"].append(mark)

                json_obj.update(result)
        else:
            # 单个文件预测
            sample_class = torch.sigmoid(outputs).argmax(dim=1)  # sigmoid将输出转换为概率,再选择概率最大的类别
            mask = torch.sigmoid(outputs).max(dim=1).values >= confidence
            sample_class[~mask] = 1 - sample_class[~mask]

            for name in name_list:
                result = {
                    f"{name}": {
                        "status": []
                    },
                }

                for item in sample_class.tolist():
                    if item == 0:
                        mark = "normal"
                    elif item == 1:
                        mark = "fault"
                    else:
                        raise ValueError("输出不在已知分类中!")

                    result[f"{name}"]["status"].append(mark)

                json_obj.update(result)

    result_json = json.dumps(json_obj, indent=4)  # 转换为 JSON 格式的字符串

    return result_json


