import os
import math
import torch
from torch import nn
from torch.utils.data import Dataset


class WDCNN(nn.Module):
    def __init__(
            self, in_channel=1, out_channel=2, linear_input=448,
            first_kernel_size=64, first_stride=16, first_padding=24,
            activation_function=nn.ReLU,
    ):
        super(WDCNN, self).__init__()
        self.out_channel = out_channel
        # 保存激活函数类型
        self.activation_function = activation_function

        # 输出长度计算公式：output_length = ((input_length + 2 * padding - kernel_size) / stride) + 1
        # ReLU, LeakyReLU(), Tanh()
        self.layer1 = nn.Sequential(
            nn.Conv1d(in_channels=in_channel, out_channels=16, kernel_size=first_kernel_size,
                      stride=first_stride, padding=first_padding),
            nn.BatchNorm1d(16),
            self.activation_function(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.layer2 = nn.Sequential(
            nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding='same'),
            nn.BatchNorm1d(32),
            self.activation_function(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.layer3 = nn.Sequential(
            nn.Conv1d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding='same'),
            nn.BatchNorm1d(64),
            self.activation_function(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.layer4 = nn.Sequential(
            nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding='same'),
            nn.BatchNorm1d(64),
            self.activation_function(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.layer5 = nn.Sequential(
            nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=0),
            nn.BatchNorm1d(64),
            self.activation_function(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.drop = nn.Dropout(0.5)

        self.fc = nn.Sequential(
            nn.Linear(linear_input, self.out_channel * 100),
            self.activation_function(),
            nn.Linear(self.out_channel * 100, self.out_channel)
        )

    def forward(self, x):
        x = self.layer1(x)  # (batch-size,16,128)
        x = self.layer2(x)  # (batch-size,32,64)
        x = self.layer3(x)  # (batch-size,64,32)
        x = self.layer4(x)  # (batch-size,64,16)
        x = self.layer5(x)  # (batch-size,64,7)
        x = self.drop(x)
        x = x.view(x.size(0), -1)  # (batch-size,64*7)
        x = self.fc(x)

        # nn.Softmax(dim=1) 使用torch里面的交叉熵计算loss时会自动给预测值添加softmax，因此这里不需要softmax层了
        return x


class WdcnnDataset(Dataset):
    def __init__(self, input_x, input_y):
        super(WdcnnDataset, self).__init__()
        self.input_x = input_x
        self.input_y = input_y

    def __getitem__(self, index):
        item = self.input_x[index]
        label = self.input_y[index]
        return item, label

    def __len__(self):
        return len(self.input_x)


class WdcnnMultiFeatureFrequencyScale(nn.Module):
    def __init__(
            self, in_channel=1, out_channel=2,
            first_kernel_size=64, first_stride=16, first_padding=24,
            rated_speed=1480,
            activation_function=nn.ReLU
    ):
        super(WdcnnMultiFeatureFrequencyScale, self).__init__()
        self.out_channel = out_channel
        self.activation_function = activation_function
        self.featurefrequency = [0.55686345, 3.8392105, 7.32621725, 10.9326654, 15.57416316,
                                 21.3058907, 28.9701581, 41.04637963, 54.25426667, 67.34573333]

        # Scale1
        self.feature_layer = nn.ModuleList()
        for i, frequency in enumerate(self.featurefrequency):
            kernel = math.ceil(rated_speed / 60 * frequency)

            feature_layer = nn.Sequential(
                nn.Conv1d(in_channels=in_channel, out_channels=1, kernel_size=kernel,
                          stride=kernel, padding=0),
                nn.BatchNorm1d(1),
                self.activation_function(),
            )
            self.feature_layer.append(feature_layer)

        # Scale2
        self.layer1 = nn.Sequential(
            nn.Conv1d(in_channels=in_channel, out_channels=16, kernel_size=first_kernel_size,
                      stride=first_stride, padding=first_padding),
            nn.BatchNorm1d(16),
            self.activation_function(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.layer2 = nn.Sequential(
            nn.Conv1d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding='same'),
            nn.BatchNorm1d(32),
            self.activation_function(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.layer3 = nn.Sequential(
            nn.Conv1d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding='same'),
            nn.BatchNorm1d(64),
            self.activation_function(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.layer4 = nn.Sequential(
            nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding='same'),
            nn.BatchNorm1d(64),
            self.activation_function(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.layer5 = nn.Sequential(
            nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=0),
            nn.BatchNorm1d(64),
            self.activation_function(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )

        self.drop = nn.Dropout(0.5)

    def forward(self, x):
        # scale1
        feature_outputs = []
        for feature_layer in self.feature_layer:
            f = feature_layer(x)
            feature_outputs.append(f)
        scale1_output = torch.cat(feature_outputs, dim=1)  # 连接所有输出
        scale1_output = torch.flatten(scale1_output, 1)  # 展平

        # scale2
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.layer5(x)
        x = self.drop(x)
        x = x.view(x.size(0), -1)

        combined_output = torch.cat([x, scale1_output], dim=1)
        output = nn.Linear(combined_output.size(1), self.out_channel * 100)
        output = self.activation_function(output)
        output = nn.Linear(output.size(0), self.out_channel)

        return output


class WdcnnMultiFeatureFrequencyScaleDataset(Dataset):
    def __init__(self, input_x, input_y):
        super(WdcnnMultiFeatureFrequencyScaleDataset, self).__init__()
        self.input_x = input_x
        self.input_y = input_y

    def __getitem__(self, index):
        item = self.input_x[index]
        label = self.input_y[index]
        return item, label

    def __len__(self):
        return len(self.input_x)


