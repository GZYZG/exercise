#include <iostream>
using namespace std;

class A {
	int a;
public:
	A(int x=0): a(x){}
	void f(){cout << "operator+(int): " << a << endl;}
	A operator+(A op) {
        A T;
        T.a = a + op.a;
        return T;
    }
    friend A operator+(int op1, A op2) {
        A T;
        T.a = op1 + op2.a;

        return T;
    }
};

class B {
    int b;
public:
    B(int x=0): b(x) {}
    void f() {cout << "operator+(Obj): " << b << endl;}
    B operator+(B op) {
        B T;
        T.b = b + op.b;

        return T;
    }
};


int main()
{
    A a1, a2(2);
    B b1, b2(2);
    // operator+ 的参数为 A 时，int 型 op 作为第二操作数
    (a1 + 3).f(); // pass，operator+中，默认将 this 作为第一个参数，即 operator+(A) --> operator(A, A)，可以通过构造函数将 3 --> A(3)
    // operator+ 的参数为 A 时，int 型 op 作为第一操作数
    (3 + a1).f();  // failed，找不到合适的 operator+，即没有定义这样的函数：operator+(int, A)，如果定义了则 pass
    // operator+ 的参数为 A 时，A 型 op 作为操作数
    (a1 + a2).f();  // pass，很显然，定义的 operator+(A) 其实等价于 operator+(A, A)

    // operator+ 的参数为 int 时，int 型 op 作为第二操作数
    (b1 + 3).f();  // pass，很显然，定义的 operator+(int) 其实就是 operator+(B, int)
    // operator+ 的参数为 int 时，int 型 op 作为第一操作数
    (3 + b1).f();  // failed，找不到 operator+(int, B)
    // operator+ 的参数为 int 时，B 型 op 作为操作数
    (b1 + b2).f(); // failed，定义的 operator+(int) 其实是 operator(B, int)

    return 0;
}

/*
结论：

执行加法操作时，其实是根据两个操作数的类型来确定 operator+ 的函数签名，且由第一个参数确定在哪个函数空间查找该函数签名！
*/