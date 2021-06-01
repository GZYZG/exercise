"""
1. 加载模型参数
2. 构建计算流程
3. inference
"""
from collections import OrderedDict
import numpy as np
import random
from pyspark.sql import SparkSession


def relu(x):
    x = np.array(x)
    x[x < 0] = 0
    return x


def sigmoid(x):
    x = np.array(x)
    return 1 / (1 + np.exp(-x))


class GCN:
    def __init__(self, config: OrderedDict):
        self.num_layers = config.get("num_layers")
        self.layers = []
        for i in range(self.num_layers):
            shape = config[f"layer_{i + 1}"]['in_dim'], config[f"layer_{i + 1}"]['out_dim']
            weight = np.zeros(shape=shape)
            if config[f"layer_{i + 1}"]['bias']:
                bias = np.zeros(shape=(config[f"layer_{i + 1}"]['out_dim'],))
            if config[f"layer_{i + 1}"]['activation'] == "relu":
                act = relu
            elif config[f"layer_{i + 1}"]['activation'] == 'sigmoid':
                act = sigmoid

            self.layers.append({"weight": weight, "bias": bias, "activation": act})

    def load_weights(self, weights):
        pass

    def forward(self, ndata, norm):
        h = ndata
        for idx, layer in enumerate(self.layers):
            h = np.matmul(norm, h)
            h = np.matmul(h, layer['weight'])
            if layer.get('bias', None) is not None:
                h += layer['bias']
            if layer.get('activation', None) is not None:
                h = layer.get('activation')(h)

        return h


def load_graph(path):
    data = np.load(path, allow_pickle=True)
    n = data['node_num']
    u = data['u']
    v = data['v']
    feat = data['feat']
    label = data['label']

    adj = np.zeros((n, n))
    adj[u, v] = 1

    return adj, feat, label


def cal_norm(adj):
    A = np.array(adj) + np.eye(len(adj))
    D = np.diag(A.sum(axis=1))
    t = D ** -.5
    norm = np.matmul(t, A)
    norm = np.matmul(norm, A)
    return norm


def gen_subgraph(vertexs, adj, order=2):
    vs = set(vertexs)
    for i in range(order):
        tmp = adj[vs, :]
        tmp = tmp.reshape(-1)
        vs = vs.union(set(tmp))

    return list(vs)


if __name__ == "__main__":
    config = OrderedDict()
    config['num_layers'] = 2

    config['layer_1'] = OrderedDict()
    config['layer_1']['in_dim'] = 16
    config['layer_1']['out_dim'] = 8
    config['layer_1']['bias'] = True
    config['layer_1']['activation'] = 'Relu'

    config['layer_2'] = OrderedDict()
    config['layer_2']['in_dim'] = 8
    config['layer_2']['out_dim'] = 4
    config['layer_2']['bias'] = True
    config['layer_2']['activation'] = 'Relu'

    # 加载图数据，包括图的邻接矩阵，特征矩阵
    path = ""
    g = load_graph(path)
    adj, feat, label = g
    n = adj.shape[0]

    test_n = 100
    test_idx = random.sample(range(n), test_n)

    sc = SparkSession.builder.appName("GCNInferenceWithSpark").getOrCreate()

    # 为每个测试结点，生成基于该顶点的子树。每个测试结点的计算作为一个task
    gcn = GCN(config)
    gcn.load_weights(None)
    subgraphs = [gen_subgraph(idx, adj, order=2) for idx in test_idx]
    subgraphs = [[feat[idx] for idx in sub] for sub in subgraphs]
    subgraphs = sc.paralize(subgraphs)
    subgraphs.map(lambda x: gcn.forward(x))

    test_embs = [subgraphs[idx][0] for idx in test_idx]
