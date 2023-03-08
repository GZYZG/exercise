# Exercise and practice when I'm learning :open_book:
这个项目用于记录我读研期间的一些练习，作为我的练兵场，记录我练习技能的场所！
:fire: :fire: :fire:

现在已经有的内容：
- [general_metrics.py](./general_metrics.py)，实现了混淆矩阵和混淆矩阵可视化；
- [segmentation_metrics.py](./segmentation_metrics.py)，只实现了 dice 系数和 IoU 的计算；
- [overlap.py](./overlap.py)：给定两个矩阵的左上、右下坐标，计算他们的重叠面积；
- [ml-examples](./ml-examples) 关于一些机器学习模型的例子
	- [Credit-card-fraud-detection.ipynb](./ml-examples/Credit-card-fraud-detection.ipynb)：信用卡欺诈检测，二分类任务
	- [dgl_link_predict.ipynb](./ml-examples/dgl_link_predict.ipynb)：使用 `dgl` 进行图上的链接预测任务
	- [FM.ipynb](./ml-examples/FM.ipynb)：FactorizationMachines 的实现；
	- [SparkML预测实战.ipynb](./ml-examples/SparkML预测实战.ipynb)：使用 SparkML 模块做机器学习任务；
	- [W&D.ipynb](./ml-examples/W&D.ipynb)、[WideNDeep_pt.py](./ml-examples/WideNDeep_pt.py)、[WideNDeep_tf.py](./ml-examples/WideNDeep_tf.py)：Wide&Deep 模型的实现；
	- [xgboost.ipynb](./ml-examples/xgboost.ipynb)：`xgboost` 做二分类、多分类、回归任务的示例，以及树模型的分析、可视化、xgb 的一些关键参数等；
-  [python](./python)：关于 `python` 的一些问题的探究
	- [decorator.py](./python/decorator.py)：python 中多重装饰器执行的顺序问题；
	- [file.py](./python/file.py)：使用 `shutil` 批量移动文件；
- [C++](./C++)：关于 `C++` 的一些问题的探究
	- [althttpd.c](./C++/althttpd.c)：纯 `c` 实现的 http 服务器；
	- [operator+.cpp](./C++/operator+.cpp)：一个例子直击 `operator+cpp` 的秘密 —— 具体调用哪个重载运算符！
- [others](./others)：其他的一些内容
- 