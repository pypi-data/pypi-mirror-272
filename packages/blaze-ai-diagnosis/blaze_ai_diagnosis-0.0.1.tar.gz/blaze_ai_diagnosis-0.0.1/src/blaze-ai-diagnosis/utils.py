# -*- coding: utf-8 -*-
import os
import glob
import json
import yaml
import torch
import warnings

import numpy as np
import pandas as pd
from torch import nn
import seaborn as sns
from scipy import stats
import torch.cuda as cuda
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from model import WDCNN
from read_util.read import read_local_file


# 如果存在GPU，返回GPU对象，否则返回cpu()
def try_gpu():
    """
    检查GPU,调用可以使用的GPU;否则使用CPU
    """
    device = torch.device("cuda" if cuda.is_available() else "cpu")

    i = 0
    if device.type == "cuda":
        # 获取所有可用 GPU 设备的数量
        num_gpus = cuda.device_count()

        # 查找当前空闲的 GPU 设备
        for i in range(num_gpus):
            gpu_utilization = cuda.max_memory_allocated(i) - cuda.memory_allocated(i)
            if gpu_utilization == 0:
                device = torch.device("cuda:" + str(i))
                # 打印显卡名称
                print("Training/Testing on ", device, "(", torch.cuda.get_device_name(), ")\n")

                break

    else:
        print("GPU is not available. Training/Testing on CPU.\n")

        device = torch.device("cpu")

    return device


def assign_gpu(number=1):
    """
    指定使用第几块GPU,如果空闲就使用这块.
    """
    # 检查是否有可用的GPU
    if torch.cuda.is_available():
        device_count = torch.cuda.device_count()
        if device_count >= 2:  # 至少有两块GPU
            specified_gpu_index = number  # 指定第二块GPU的索引（索引从0开始）
            specified_gpu_available = torch.cuda.is_available() and torch.cuda.device_count() > specified_gpu_index
            if specified_gpu_available:
                # 检查指定的第二块GPU是否空闲
                specified_gpu_memory_allocated = torch.cuda.memory_allocated(specified_gpu_index)
                if specified_gpu_memory_allocated == 0:
                    # 使用指定的第二块GPU
                    device = torch.device("cuda:" + str(specified_gpu_index))
                    # 打印显卡名称
                    print("Training/Testing on ", device, "(", torch.cuda.get_device_name(), ")")
                else:
                    raise ValueError("指定的GPU正在使用")
            else:
                raise ValueError(f"第{number+1}块GPU不存在")
        else:
            raise ValueError(f"第{number+1}块GPU不存在")

        return device

    else:
        print("GPU is not available. Training on CPU.")

        return torch.device("cpu")


def plot_confusion_matrix(path, real_labels, predictive_labels, class_names=None):
    """
    根据 真实标签 和 预测标签 计算混淆矩阵
    :param path: 保存路径
    :param real_labels: 真实标签
    :param predictive_labels: 预测标签
    :param class_names: 类别名
    :return:
    """
    # normalize:归一化类型, 如果为 None, 则返回混淆矩阵中的原始计数, 如果为 'true', 则返回每个类别预测正确的比例,
    # 如果为 'pred', 则返回每个类别实际出现的比例, 如果为 'all', 则返回所有样本的比例.
    cmtx = confusion_matrix(real_labels, predictive_labels, normalize=None)

    # 打印混淆矩阵
    print(f"TP={cmtx[0, 0]}, FN={cmtx[0, 1]}")
    print(f"FP={cmtx[1, 0]}, TN={cmtx[1, 1]}\n")

    print(f"Accuracy:{round((cmtx[0, 0]+cmtx[1, 1])/(cmtx[0, 0]+cmtx[0, 1]+cmtx[1, 0]+cmtx[1, 1]), 4) * 100}%")
    print(f"Precision:{round(cmtx[0, 0]/(cmtx[0, 0]+cmtx[1, 0]), 4) * 100}%")
    print(f"Recall:{round(cmtx[0, 0]/(cmtx[0, 0]+cmtx[0, 1]), 4) * 100}%\n\n")

    if class_names is None:
        class_names = np.unique(real_labels)

    plt.figure(figsize=(16, 12))
    sns.heatmap(cmtx, annot=True, fmt="d", cmap="Blues", cbar=False,
                annot_kws={"fontsize": 20}, xticklabels=class_names, yticklabels=class_names)
    plt.xlabel("Predicted", fontsize=20)
    plt.ylabel("Real", fontsize=20)
    plt.title("Confusion Matrix", fontsize=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.savefig(path)
    plt.close()


def normal_distribution_check(data, xlim_range=8193):
    """
    检查信号是否符合正态分布
    :param data: 一维数组
    :param xlim_range: x轴显示范围,从1-8193
    :return:
    """
    # 正态性检验
    data_mean = data.mean()  # 均值
    data_std = data.std()  # 标准差
    print('\n均值为: %.3f, 标准差为: %.3f' % (data_mean, data_std))

    # 绘制数据密度曲线和异常值分析图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    # 绘制数据的密度曲线
    sns.kdeplot(data, label='Data', ax=ax1)
    # 执行Kolmogorov-Smirnov检验
    stats.kstest(data, 'norm', args=(data_mean, data_std))

    # 异常值分析
    error = data[np.abs(data - data_mean) > 3 * data_std]
    data_c = data[np.abs(data - data_mean) <= 3 * data_std]
    print('异常值共%i个' % len(error))

    # 筛选出异常值error、剔除异常值之后的数据data_c
    ax2.scatter(np.indices(data_c.shape), data_c, color='b', marker='.', alpha=0.3, label='normal data')
    ax2.scatter(np.indices(error.shape), error, color='r', marker='.', alpha=0.5, label='abnormal data')
    ax2.set_xlim([-10, xlim_range])
    ax2.grid()
    ax2.legend()
    plt.show()


def load_hyps(yaml_path: str):
    with open(f"{yaml_path}", 'r') as hyps:
        hyp = yaml.safe_load(hyps)

    return hyp


def load_json(json_path: str):
    with open(f"{json_path}", 'r') as file:
        json_info = json.load(file)

    return json_info


def traversal_raw_files(path):
    # csv、aiff、gz、txt文件类型的通配符模式
    file_types = ['**/*.csv', '**/*.aiff', '**/*.gz', '**/*.txt']
    files_path_list = []
    type_mark = 0
    for file_type in file_types:
        pattern = os.path.join(path, file_type)
        file_list = glob.glob(pattern, recursive=True)
        files_path_list.extend(file_list)
        if file_list:
            type_mark += 1

    if not type_mark:
        raise ValueError("没有找到 csv、aiff、gz、txt 中的任何一种文件类型!")
    else:
        if type_mark >= 2:
            warnings.warn("警告: 存在 大于等于 两种类型的文件,请注意文件类型是否正确.", UserWarning)

        return files_path_list


def read_files_demean(path, files_type='csv', file_skip_rows=0):
    """
    读取振动文件时,去掉振幅的平均值
    Parameters
    ----------
    path: 文件路径
    files_type: 支持读取 csv、aiff、gz、txt 文件
    file_skip_rows: 读取文本时,从首行开始需要跳过的行数

    Returns
    -------

    """
    if files_type == 'csv' or files_type == 'txt':
        data = np.loadtxt(path, delimiter=',', skiprows=file_skip_rows)

    elif files_type == 'aiff' or files_type == 'gz':
        data = read_local_file(path).data
    else:
        raise ValueError("无法读取的数据类型")

    data = data - np.mean(data)

    return data.astype(np.float32)


def read_files(path, files_type='csv', file_skip_rows=0):
    """
    Parameters
    ----------
    path: 文件路径
    files_type: 支持读取 csv、aiff、gz、txt 文件
    file_skip_rows: 读取文本时,从首行开始需要跳过的行数

    Returns
    -------
    """
    if files_type == 'csv' or files_type == 'txt':
        data = np.loadtxt(path, delimiter=',', skiprows=file_skip_rows)

    elif files_type == 'aiff' or files_type == 'gz':
        data = read_local_file(path).data
    else:
        raise ValueError("无法读取的数据类型")

    data = np.array(data)

    return data.astype(np.float32)


def overlap_divide(signal, window_size=4096):
    # 重叠长度,按 50% 重叠划分
    overlap_length = int(window_size * 0.5)

    segments = []
    for i in range(0, len(signal) - window_size + 1, window_size - overlap_length):
        start_index = i  # 起始索引
        end_index = i + window_size  # 结束索引
        segment = signal[start_index:end_index]

        segments.append(segment)

    segments = np.array(segments)

    return segments


def datasets_load_preprocess(file_path, length, target_mode='train'):
    if target_mode == 'inference':
        files_path = traversal_raw_files(file_path)

        data_list = []
        file_name_list = []
        for path in files_path:
            name_extension = path.split('.')[-1]  # 扩展名
            file_name = path.split('\\')[-1]  # 文件名

            data = read_files(path, name_extension, file_skip_rows=0)
            # #
            # data = data[:length]
            # #
            data_length = len(data)

            if data_length < length:
                raise ValueError(f"数据长度为{data_length},不满足要求长度{length}.")
            elif data_length > length:
                if data_length // length == 1:
                    warnings.warn(f"\n警告: 数据长度为{data_length},已截取为{length}.", UserWarning)
                    data = data[:length]
                if data_length // length >= 2:
                    warnings.warn(f"\n警告: 数据长度为{data_length},已截取为多段{length}.", UserWarning)
                    data = overlap_divide(data, window_size=4096)
            else:
                data = data

            # # 检查波形是否类似正态分布
            # random.seed(42)
            # if len(data.shape) == 1:
            #     normal_distribution_check(data, xlim_range=length + 1)
            # else:
            #     random_data = data[np.random.choice(data.shape[0], size=3, replace=False)]
            #     for x in random_data:
            #         normal_distribution_check(x, xlim_range=length+1)

            #
            data_list.append(data)
            file_name_list.append(file_name)

        if len(data_list) == 1:
            return data_list[0], file_name_list
        else:
            return data_list, file_name_list

    elif target_mode == 'train':
        files_path = traversal_raw_files(file_path)

        data_list = []
        label_list = []
        for path in files_path:
            name_extension = path.split('.')[-1]  # 扩展名
            type_name = path.split('_')[-1].split('.')[0]  # 文件名

            data = read_files(path, name_extension, file_skip_rows=0)

            # # 检查波形是否类似正态分布
            # random.seed(42)
            # random_data = data[np.random.choice(data.shape[0], size=3, replace=False)]
            # for x in random_data:
            #     normal_distribution_check(x, xlim_range=8193)

            if type_name == 'normal':
                label_list.extend([0] * data.shape[0])
            elif type_name in ['ball', 'cage', 'compound', 'inner', 'outer']:
                label_list.extend([1] * data.shape[0])
            else:
                raise ValueError(f"标签错误!请检查标签:{type_name}")

            data_list.append(data)

        data_arr = np.concatenate(data_list, axis=0)

        # 使用 train_test_split 进行分层抽样划分
        train_x, test_x, train_y, test_y = train_test_split(data_arr, label_list, test_size=0.1, stratify=label_list,
                                                            random_state=42)
        train_x, val_x, train_y, val_y = train_test_split(train_x, train_y, test_size=0.1, stratify=train_y,
                                                          random_state=42)

        # 检查每个子集中的类别比例是否大致相同
        train_type_numbers = [train_y.count(label) for label in set(train_y)]
        print("Train各子类别数量:", [train_y.count(label) for label in set(train_y)])
        print("Val各子类别数量:", [val_y.count(label) for label in set(val_y)])
        print("Test各子类别数量:", [test_y.count(label) for label in set(test_y)], '\n\n')

        # 计算类别权重  (反类频率权重)
        train_weights = torch.tensor(train_type_numbers)
        train_weights = 1 / train_weights
        train_weights = train_weights / train_weights.sum()  # 归一化权重

        # 标准化处理
        between_scaler = StandardScaler()  # 标准化器对象
        train_x_scaled = between_scaler.fit_transform(train_x)
        val_x_scaled = between_scaler.transform(val_x)
        test_x_scaled = between_scaler.transform(test_x)

        return train_weights, between_scaler, train_x_scaled, train_y, val_x_scaled, val_y, test_x_scaled, test_y

    else:
        raise ValueError(f"不支持的处理类型:{target_mode}")


def src_load_preprocess(src, length):
    data = src.data
    data_length = len(data)

    if data_length < length:
        raise ValueError(f"数据长度为{data_length},不满足要求长度{length}.")
    elif data_length > length:
        warnings.warn(f"\n警告: 数据长度为{data_length},已截取为{length}.", UserWarning)
        data = data[:length]
    else:
        data = data

    data_temp = data - np.mean(data)
    data_temp = data_temp.astype(np.float32)

    return data_temp


def activation_function_init(str_name):
    if str_name == "ReLU":
        ac_func = nn.ReLU
    elif str_name == "LeakyReLU":
        ac_func = nn.LeakyReLU
    elif str_name == "Tanh":
        ac_func = nn.Tanh
    elif str_name == "Sigmoid":
        ac_func = nn.Sigmoid
    elif str_name == "RReLU":
        ac_func = nn.RReLU
    elif str_name == "PReLU":
        ac_func = nn.PReLU
    elif str_name == "ELU":
        ac_func = nn.ELU
    elif str_name == "CELU":
        ac_func = nn.CELU
    elif str_name == "SELU":
        ac_func = nn.SELU
    elif str_name == "GELU":
        ac_func = nn.GELU
    elif str_name == "SiLU":
        ac_func = nn.SiLU
    elif str_name == "Softplus":
        ac_func = nn.Softplus
    elif str_name == "Softsign":
        ac_func = nn.Softsign
    else:
        ac_func = nn.ReLU

    return ac_func


def inference_instantiate_model(pth_path, rpm=None, activation_function='ReLU'):
    """
    :param pth_path: 权重文件路径
    :param rpm: 转速
    :param activation_function: 激活函数. 应与训练时一致
    :return: 实例化后的模型
    """
    device = try_gpu()  # 检查GPU
    ac = activation_function_init(activation_function)  # 模型使用的激活函数
    # 加载模型
    net = WDCNN(in_channel=1, out_channel=2, activation_function=ac)
    net.load_state_dict(torch.load(pth_path, map_location=device))

    return net, device





