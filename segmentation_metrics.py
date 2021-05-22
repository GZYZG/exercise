"""
图像分割的评价指标
"""
import numpy as np
import matplotlib.pyplot as plt
import itertools


def confusion_matrix(label, predict, n):
    """
    计算混淆矩阵
    :param label: 标签，np.array类型。形状可以是(n_sample,) 或者 (n_sample, n_classes)，当为第二种形状时可以表示多标签分类的情况
    :param predict: 预测值，与 `label` 同理
    :param n: 类别数目
    :return: 混淆矩阵，np.array类型。shape 为 (n, n)。$cm_{ij}$表示真实标签为 $i$，预测标签为 $j$ 的样本个数
    """
    k = (label >= 0) & (label < n)
    # bincount()函数用于统计数组内每个非负整数的个数
    # 详见 https://docs.scipy.org/doc/numpy/reference/generated/numpy.bincount.html
    return np.bincount(n * label[k].astype(int) + predict[k], minlength=n ** 2).reshape(n, n)


def mIoU(label, predict, class_n):
    """
    计算mIoU，mean Intersection over Union
    $IoU = TP / (TP + FP + TN)$
    $mIoU = \frac{1}{C} \sum_{i = 1}^{C} IoU_i$
    :param label: 标签
    :param predict: 预测值
    :param class_n: 类别数
    :return: mIoU
    """
    cm = confusion_matrix(label, predict, class_n)

    miou = np.diag(cm) / (cm.sum(axis=1) + cm.sum(axis=1) - np.diag(cm))

    miou = np.nanmean(miou)

    return miou


def plot_confusion_matrix(cm, classes, normalized=False, title="Confusion matrix", cmap=plt.cm.Blues):
    """
    画混淆矩阵
    :param cm: 混淆矩阵
    :param classes: 类别列表。classes[i] 表示 i 所对应的类名
    :param normalized: 是否进行归一化
    :param title: str，表头
    :param cmap:
    :return:
    """
    if normalized:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print("Confusion matrix with out normalization")

    print(cm)

    plt.imshow(cm, interpolation="nearest", cmap=cmap)
    plt.title(title, fontsize=14)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalized else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()


if __name__ == "__main__":
    label = np.array([0, 0, 1, 1])  # np.array([[0, 1, 1], [1, 1, 0], [0, 0, 1]])
    predict = np.array([0, 0, 1, 1])  # np.array([[0, 1, 0], [1, 0, 1], [0, 0, 0]])
    cm = confusion_matrix(label, predict, 2)
    plot_confusion_matrix(cm, [0,1], title="Confusion Matrix")
    print(f"Confusion Matrix: \n{cm}")

    print(f"mIoU: {mIoU(label, predict, 2)}")
