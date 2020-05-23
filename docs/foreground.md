# 代码帮（CodeBang）项目前景文档

代码帮是一个用于学习 C/C++ 语言的在线教育平台。

代码帮的特点

* 使用自有产权的新一代知识语言 易科（yix） 来描述整个计算机/C/C++知识体系
* 使用具备人工智能模式的自学习平台，用户的学习过程基本不需要人工参与

代码帮的使命和目标

* 让学员掌握软件编程的思想，而不是仅仅掌握一门语言。 C 语言号称语言之
  王， C ++ 则是面向对象之祖，懂得了 C/C++，其他一切语言都能很快上手。

* 让具备初中文化水平的人和具备相关才能的人可以掌握 C/C++ 的编程思想，不是所有人都适合编写程序
* 成为中国大学的新一代计算机教材和新一代知识革命的领航者

什么是知识的革命，第一代知识以语言为载体，第二代语言以文字为载体，新一代语言以计算机为载体。

当然有很多公司在这个方向进行发展，有的人看到了这一点，有的人则只是跟着
直觉投入其中，但谁能真正的成为最后的统治者呢？

## 代码帮的应用

1. 帮助开发人员发现内存堆栈方面的问题。

这类问题使用普通调试器一般很难发现，代码帮可以应用于简单的用例，受运行速度的影响，
对于需要大量计算的复杂用例并不适用。

为了提高运行速度和性能，需要下载代码帮 App 在本地运行。

具体实例为 PyArmor 开发中遇到的堆栈问题，在使用新的包裹模式 2 加密的脚本，在
MacOS (10.14.6) 上的 Python 3.7.7 的环境下面运行总是出现崩溃现象

    Segmentation fault: 11

首先安装 pyarmor 6.0.2 ，然后编译一个有问题的动态库 `_pytransform.dylib` 。在 的
私有库 [pytransform](https://github.com/jondy/pytransform) 的上面使用了 tag
`codebang-crash` 专门保存了这个有问题的代码

    cd /path/to/pytransform/src
    git checkout codebang-crash
    make clean && make
    cp ../build/darwin_x86_64/.libs/_pytransform.dylib /path/to/pyarmor/platforms/darwin/x86_64

然后使用这个动态库加密一个简单的脚本 [foo.py](samples/crash/foo.py)

    cd /path/to/samples/crash
    pyarmor obfuscate --exact foo.py

运行加密脚本，会直接出现奔溃

    cd dist
    python3 foo.py

随后在编译一个解决了这个问题的版本，使用标签 `codebang-fixed` 指定的代码，这样加
密的脚本可以正常运行

    cd /path/to/pytransform/src
    git checkout codebang-fixed
    make clean && make
    cp ../build/darwin_x86_64/.libs/_pytransform.dylib /path/to/samples/crash/dist/pytransform

可以基于上面的示例程序展示代码帮如何发现内存堆栈导致的问题。

但是这个修正没有解决真正的问题，脚本 [queens.py](samples/crash/queens.py) 加密后
还是会崩溃，因为真正的问题是没有对 f_valuestack 进行相应的赋值，从而造成的真正的
代码执行完成之后，在使用下面的代码清空本层堆栈的时候，意外的把多余的两个影子堆栈
里面的元素推出堆栈，对其引用计数进行修改而导致的异常

```c
    assert(why != WHY_YIELD);
    /* Pop remaining stack entries. */
    while (!EMPTY()) {
        PyObject *o = POP();
        Py_XDECREF(o);
    }
```

解决这个问题的代码是在标签 `codebang-fixed-2` ，关键语句

    GET_FRAME_VALUESTACK(frame) = old_valuestack + 2;

1.1 图形化的显示内存数据

在调试 Python37-32 的超级模式的实例中，如果能够显示内存数据 _PyRuntime 的图形化
数据视图，并能够发现不正确的字段，例如，PyObject * 的字段指向的不是 PyObject 对
象等，将可以大大的提高发现问题的效率。

代码帮提供这样的功能，可以检查任意时刻的任意内存地址对应的图形化数据，可以根据已
知的所有数据类型自动识别对应的数据类型，也可以用户指定数据类型，用于查找其中的不
正确的字段，然后自动校正（例如，调整偏移量等）。

2. C 语言预处理，编译和运行的学习

使用 yix 把 cc1/cpp 的主要代码表示出来即可实现，使用 yix_transform_c 把 gcc 的源
代码直接转换

2.1 libc 的功能展示

使用 yix 把 glibc 的主要代码表示出来即可实现，使用 yix_transform_c 把 glibc 的源
代码直接转换

2.2. Python 解释器的核心工作原理（PyEval_EvalFrameEx)

使用 yix 把 Python 的核心代码 ceval.c 表示出来即可实现，使用 yix_transform_c 把
Python 相关源代码直接转换

## 项目现状

开始上线运营，发布地址: https://codebang.dashingsoft.com

融资目的

* 注册公司进行运营，目前是自然人运营方式
* 项目的宣传和推广

## 参考项目

* [CodePen](https://codepen.io)
* [pythonanywhere](https://www.pythonanywhere.com)
