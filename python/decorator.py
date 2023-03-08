def AA(func):
    print('AA 1')  # 只会在装饰时执行

    def func_a(*args, **kwargs):
        print('AA 2')  # 每次调用时都会执行
        return func(*args, **kwargs)

    return func_a


def BB(func):
    print('BB 1')  # 只会在装饰时执行

    def func_b(*args, **kwargs):
        print('BB 2')  # 每次调用时都会执行
        return func(*args, **kwargs)

    return func_b


@BB
@AA
def f(x):
    print('F')
    return x * 10


print(f(1))