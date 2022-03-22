import numpy as np
import pandas as pd
from collections import namedtuple
from itertools import chain
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split


pd.options.mode.chained_assignment = None


def label_encode(df, cols=None):
    """
    Helper function to label-encode some features of a given dataset.
    Parameters:
    --------
    df  (pd.Dataframe)
    cols (list): optional - columns to be label-encoded
    Returns:
    ________
    val_to_idx (dict) : Dictionary of dictionaries with useful information about
    the encoding mapping
    df (pd.Dataframe): mutated df with Label-encoded features.
    """

    if cols == None:
        cols = list(df.select_dtypes(include=['object']).columns)
    
    val_to_idx = {}  # 记录每个类别特征的取值对应的数字：cat_feat_name => {cat_feat_val: idx}
    for c in cols:
        le = LabelEncoder()
        tmp = le.fit_transform(df[c])
        val_to_idx[c] = {e: i for i, e in enumerate(le.classes_)}
        df[c] = tmp

    return val_to_idx, df


def prepare_data(df, wide_cols, crossed_cols, embeddings_cols, continuous_cols, target,
    scale=False, def_dim=8, seed=1981):

    """Prepares a pandas dataframe for the WideDeep model.
    Parameters:
    ----------
    df (pd.Dataframe)
    wide_cols : list with the columns to be used for the wide-side of the model
    crossed_cols : list of tuples with the columns to be crossed
    embeddings_cols : this can be a list of column names or a list of tuples with
    2 elements: (col_name, embedding dimension for this column)
    continuous_cols : list with the continous column names
    target (str) : the target to be fitted
    scale (bool) : boolean indicating if the continuous columns must be scaled
    def_dim (int) : Default dimension of the embeddings. If no embedding dimension is
    included in the "embeddings_cols" input all embedding columns will use this value (8)
    seed (int) : Random State for the train/test split
    Returns:
    ----------
    wd_dataset (dict): dict with:
    train_dataset/test_dataset: tuples with the wide, deep and lable training and
    testing datasets
    encoding_dict : dict with useful information about the encoding of the features.
    For example, given a feature 'education' and a value for that feature 'Doctorate'
    encoding_dict['education']['Doctorate'] will return an the encoded integer.
    embeddings_input : list of tuples with the embeddings info per column:
    ('col_name', number of unique values, embedding dimension)
    deep_column_idx : dict with the column indexes of all columns considerd in the Deep-Side
    of the model
    """

    # If embeddings_cols does not include the embeddings dimensions it will be set as
    # def_dim
    if type(embeddings_cols[0]) is tuple:
        emb_dim = dict(embeddings_cols)
        embeddings_cols = [emb[0] for emb in embeddings_cols]
    else:
        emb_dim = {e:def_dim for e in embeddings_cols}
    deep_cols = embeddings_cols+continuous_cols  # deep 部分由类别特征和连续特征组成

    # Extract the target and copy the dataframe so we don't mutate it
    # internally.
    Y = np.array(df[target])
    all_columns = list(set(wide_cols + deep_cols + list(chain(*crossed_cols))))
    df_tmp = df.copy()[all_columns]

    # Build the crossed columns
    ## 构造组合特征，此处是将两个类别特征的取值进行拼接形成组合特征的取值。但是这样的作法存在一些问题：当测试数据中出现了训练数据中没出现过的组合特征取值怎么办？
    ## 一个办法是做两个类别特征的取值的笛卡尔乘积，作为新的组合特征的值域。
    crossed_columns = []
    for cols in crossed_cols:
        colname = '_'.join(cols)
        df_tmp[colname] = df_tmp[cols].apply(lambda x: '-'.join(x), axis=1)
        crossed_columns.append(colname)

    # Extract the categorical column names that can be one hot encoded later
    categorical_columns = list(df_tmp.select_dtypes(include=['object']).columns)

    # Encode the dataframe and get the encoding Dictionary only for the
    # deep_cols (for the wide_cols is uneccessary)
    encoding_dict, df_tmp = label_encode(df_tmp)
    encoding_dict = {k:encoding_dict[k] for k in encoding_dict if k in deep_cols}
    embeddings_input = []
    for k,v in encoding_dict.items():
        embeddings_input.append((k, len(v), emb_dim[k]))

    # select the deep_cols and get the column index that will be use later
    # to slice the tensors
    df_deep = df_tmp[deep_cols]
    deep_column_idx = {k:v for v,k in enumerate(df_deep.columns)}

    # The continous columns will be concatenated with the embeddings, so you
    # probably want to normalize them first
    if scale:
        scaler = StandardScaler()
        for cc in continuous_cols:
            df_deep[cc]  = scaler.fit_transform(df_deep[cc].values.reshape(-1,1))

    # select the wide_cols and one-hot encode those that are categorical
    df_wide = df_tmp[wide_cols+crossed_columns]
    del(df_tmp)
    dummy_cols = [c for c in wide_cols+crossed_columns if c in categorical_columns]
    df_wide = pd.get_dummies(df_wide, columns=dummy_cols)

    # train/test split
    X_train_deep, X_test_deep = train_test_split(df_deep.values, test_size=0.3, random_state=seed)
    X_train_wide, X_test_wide = train_test_split(df_wide.values, test_size=0.3, random_state=seed)
    y_train, y_test = train_test_split(Y, test_size=0.3, random_state=seed)

    # Building the output dictionary
    wd_dataset = dict()
    train_dataset = namedtuple('train_dataset', 'wide, deep, labels')
    test_dataset  = namedtuple('test_dataset' , 'wide, deep, labels')
    wd_dataset['train_dataset'] = train_dataset(X_train_wide, X_train_deep, y_train)
    wd_dataset['test_dataset']  = test_dataset(X_test_wide, X_test_deep, y_test)
    wd_dataset['embeddings_input']  = embeddings_input
    wd_dataset['deep_column_idx'] = deep_column_idx
    wd_dataset['encoding_dict'] = encoding_dict

    return wd_dataset