"""
图像分割的评价指标
"""
import numpy as np
import itertools


def IoU(label, predict, class_n):
    """
    计算各类的IoU， Intersection over Union
    $IoU = TP / (TP + FP + TN)$
    $mIoU = \frac{1}{C} \sum_{i = 1}^{C} IoU_i$
    :param label: 标签
    :param predict: 预测值
    :param class_n: 类别数
    :return: 各个类别的IoU
    """
    cm = confusion_matrix(label, predict, class_n)

    miou = np.diag(cm) / (cm.sum(axis=1) + cm.sum(axis=1) - np.diag(cm))

    # miou = np.nanmean(miou)

    return miou


def dice_coefficient(pred, target, smooth=1):
    """
    计算dice系数
    :param pred: 预测。shape为(batch_size, w, h)
    :param target: 目标。shape为(batch_size, w, h)
    :param smooth: 平滑系数，scalar，默认为1
    :return:
    """
    assert pred.shape[0] == target.shape[0]
    n = pred.shape[0]
    t1 = pred.reshape(n, -1)
    t2 = target.reshape(n, -1)

    intersection = (t1 * t2).sum()

    return 2. * intersection / (t1.sum() + t2.sum() + smooth)
