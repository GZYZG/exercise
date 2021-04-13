"""
关于搜索问题的一个思路：
对于搜索问题，可以用一个状态变量state表示，搜索空间应该是由state取不同值组成的。
使state值发生变化的叫状态转移操作，state可以通过转移操作去不同的值 --- 即在搜索空间搜索。
关键是定义好用什么状态表示搜索问题、有哪些转移操作、搜索空间的约束条件即state应该满足的条件。
1）定义state用于表示搜索问题，确定问题的初始state，终止state；
2）确定搜索约束，state的取值约束；
3）确定转移操作，state经过转移操作可以取哪些值；
4）对空间进行遍历，遍历state的取值，使state的取值到达目标值。
"""

# # Solving MC problem by searching algorithms
#
# 在學習了眾多搜索算法之後，我們要用它們來解決MC problem這個經典問題。
#
# 1. 每個state可以用一個三元組$(m, c, b)$來表示左岸的傳教士、野人、和船的數目。傳教士和野人的總數目均為3 。船隻一首。由此，從數目守恆可以從左岸狀態$(m, c, b)$推論出右岸的狀態$(3-m, 3-c, 1-b)$.
# 2. Initial state = $(3, 3, 1)$, goal state = $(0, 0, 0)$。總共32個state，其中16個為不合法／不合理狀態。
# 3. 對每個state而言，有總共10個actions／Transition model（轉移模型）。其中部份是把原state轉移到一個不合理的state。因此，我們需要判斷一個state是不是合法的(legal)，以及對任一個state而言，其所有legal action以及對應的new states是什麼。
# 4. 當你能夠從一個state生成它所有legal transition後，你便能夠讓電腦自動為你建構整個搜索樹。
# 5. 當搜索樹成功生成後，你便能利用課堂中所教的uninformed感informed search algorithms來搜尋答案。
#
# 這個就是我們的期中考題目。內含幾個部份，因此我們分別計分，希望同學儘力把所有部份做出來。以下介紹各部份的要求。

# ## (a) legal states的判斷 (15%)
#
# 寫出一個python函數，名為`is_legal_state(state)`。輸入參數`state = [m, c, b]`為一個三元數列描述左岸的狀態。輸出為一個boolean數，代表`state`是不是合法的。
#
# ```python
# def is_legal_state(state):
#     m, c, b = state  # 左岸
#     mr, cr, br = 3-m, 3-c, 1-b  # 右岸
#     conditions = (...) and (...) and ....
#     ...
#     return conditions
# ```

# In[5]:


def is_legal_state(state):
    m, c, b = state  # 左岸
    if (not 0 <= m <= 3) or (not 0 <= c <= 3) or (not 0 <= b <= 1):
        return False
    mr, cr, br = 3 - m, 3 - c, 1 - b  # 右岸
    if m != 0 and c > m: return False
    if mr != 0 and cr > mr: return False
    if m == 0 and c == 0 and b == 1: return False
    if mr == 0 and cr == 0 and br == 1: return False
    if m == 3 and cr == 3 and b == 1: return False
    if mr == 3 and c == 3 and br == 1: return False
    return True


# ## (b) 生成所有legal states (15%)
#
# 由於傳教士人數 $m \in (0, 1, 2, 3)$, 野人人數 $c \in (0, 1, 2, 3)$, 船隻數 $b \in (0, 1)$，因此用多重python loop就可以生成所有狀態，再用上面的函數`is_legal_state`來把不合法的state刪除。

# In[6]:


def generate_all_legal_state():
    all_states = [(m, c, b) for m in range(4) for c in range(4) for b in range(2)]
    #     print(all_states)
    legal_states = list(filter(is_legal_state, all_states))

    return legal_states


generate_all_legal_state()


# ## (c) 生成所有legal transitions (15%)
#
# 再寫出另一個python函數名為`legal_transitions(state)`，其中輸入參數`state = [m ,c, b]`為原狀態。輸出結果為所有合法transition所得的states的list。
#
# ```python
# def legal_transitions(state):
#     transition = [[2, 0, 1], [0, 2, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]]  # 右岸往左岸移動
#     transition += [...]  # 左岸往右岸移動
#     ...
#     new_state = [state + transition for transition in transitions]
#     ...
#     return all_legal_new_states
# ```

# In[8]:


def legal_transitions(state):
    def tuple_add(x, y):
        assert len(x) == len(y)
        t = [x[i] + y[i] for i in range(len(x))]
        return tuple(t)

    transitions = [[2, 0, 1], [0, 2, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]]  # 右岸往左岸移動
    transitions += [[-2, 0, -1], [0, -2, -1], [-1, -1, -1], [-1, 0, -1], [0, -1, -1]]  # 左岸往右岸移動

    new_state = [tuple_add(state, transition) for transition in transitions]
    all_legal_new_states = list(filter(is_legal_state, new_state))
    return all_legal_new_states


legal_transitions((3, 3, 1))


# ## (d) 生成整個搜索樹 (30%)
#
# 利用上面的函數`legal_transitions`，加上合適的python for-loop，我們能夠從initial state $(3, 3, 1)$開始，把搜索樹中所有合法／合理的state都生成出來，並獲得對應的dictionary：
#
# ```python
# search_tree = {
#     '331': ['220', '310', '320'],
#     ...
#     ...
#     ...
# }
# ```
#
# 請把這個生成出的搜索樹和（b）部分所得到的所有legal state比較。它們是否一樣？如果有不一樣你是否能找到原因？

# In[ ]:


def state_to_str(state):
    return ''.join(map(str, state))


def str_to_state(s):
    return int(s[0]), int(s[1]), int(s[2])


def generate_search_tree(start_state, tree=dict()):
    # print(start_state)
    if start_state in tree:
        return
    else:
        transitions = legal_transitions(start_state)
        tree[start_state] = transitions
        for trans in transitions:
            generate_search_tree(trans, tree)
    items = tree.items()
    items = [(state_to_str(k), [state_to_str(e) for e in v]) for k, v in items]
    return dict(items)


print(generate_search_tree((3, 3, 1)))


# ## (e) 答案搜索 (25%)
#
# 這部分是整個project的重點，也是我在堂上講解得最多的地方，大家應該能駕輕就熟。請大家使用自己喜歡的informed search算法或是informed search算法來求解。如果你是用和cost有關的算法來解，請說明你的cost如何定義；如果你用informed search則heuristic function的定義請自行選擇並解釋。如果你不知道用什麼算法來求解，那麼你可以用iterative deepening search。（解釋文字可以用comment方式或者在自行新開markdown cell）

# In[ ]:
def search(start, end):
    stack = []
    state = start
    stack.append(state)
    visited = set()
    visited.add(start)
    adj = None
    tree = dict()
    paths = []

    while len(stack) > 0:
        state = stack[-1]
        # print(stack)
        if state == end:
            paths.append(tuple(stack.copy()))
            adj = stack.pop()
            visited.discard(adj)
            continue
            # break
        if tree.get(state, None) is None:
            successors = legal_transitions(state)
            tree[state] = successors
        else:
            successors = tree.get(state)
        next_nei = None
        idx = 0 if adj is None else successors.index(adj) + 1
        while idx < len(successors):
            if successors[idx] not in visited:
                next_nei = successors[idx]
                break
            idx += 1
        if next_nei is not None:
            stack.append(next_nei)
            visited.add(next_nei)
            adj = None
        else:
            # l = len(paths)
            # for i in range(l):
            #     path = paths[i]
            #     for successor in successors:
            #         if successor != start and successor in path and successor not in stack:
            #             if set(stack).intersection(set(path[path.index(successor):])).__len__() != 0:
            #                 continue
            #             if len(stack) != path.index(successor):
            #                 new_path = stack.copy()
            #                 new_path.extend(path[path.index(successor):])
            #                 paths.append(tuple(new_path))
            #             else:
            #                 flag = False
            #                 for e1, e2 in zip(stack, path[:path.index(successor)]):
            #                     if e1 != e2:
            #                         flag = True
            #                         break
            #                 if flag:
            #                     new_path = stack.copy()
            #                     new_path.extend(path[path.index(successor):])
            #                     paths.append(tuple(new_path))
            adj = stack.pop()
            visited.discard(adj)

    return set(paths)


paths = search((3, 3, 1), (0, 0, 0))
paths = [list(map(state_to_str, path)) for path in paths]

for path in paths:
    print(f"{' -> '.join(path)}")


# 331 -> 310 -> 321 -> 300 -> 311 -> 110 -> 221 -> 020 -> 031 -> 010 -> 111 -> 000
# 331 -> 310 -> 321 -> 300 -> 311 -> 110 -> 221 -> 020 -> 031 -> 010 -> 021 -> 000
# 331 -> 220 -> 321 -> 300 -> 311 -> 110 -> 221 -> 020 -> 031 -> 010 -> 111 -> 000
# 331 -> 220 -> 321 -> 300 -> 311 -> 110 -> 221 -> 020 -> 031 -> 010 -> 021 -> 000
#
