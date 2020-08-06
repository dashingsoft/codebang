# 代码帮（CodeBang）项目前景文档

代码帮是一个用于学习 C/C++ 语言的在线教育平台。

代码帮的使命和目标

* 成为中国大学的新一代计算机教材和新一代知识革命的领航者
* 让具备相关才能的人（不是所有人都适合编写程序）能够掌握 C/C++ 的编程思想，而不
  是仅仅掌握一门语言。 C 语言号称语言之王， C ++ 则是面向对象之祖，懂得了 C/C++，
  其他一切语言都能很快上手。

代码帮的特点

* 使用自有产权的新一代知识语言 易科（yix） 来描述整个计算机/C/C++知识体系，能够
  使用动画的形式展示任何 C/C++ 编写的应用程序或者系统（例如， Linux 内核）等的内
  部工作原理。

  也就是说，代码帮的后台系统可以把 C 语言的执行过程翻译成为普通人容易理解的动画
  过程。和传统的技术书籍相比较，书的编写是作者首先理解了代码，然后根据自己的理解
  编写而成。而代码帮则是根据源代码直接翻译过来，能够更加真实的表达代码和高效的自
  动转换。

* 使用具备人工智能模式的自学习平台，用户的学习过程基本不需要人工参与

什么是知识的革命，第一代知识以语言为载体，第二代语言以文字为载体，新一代语言以计
算机为载体。

当然有很多公司在这个方向进行发展，有的人看到了这一点，有的人则只是跟着直觉投入其
中，但谁能真正的成为最后的统治者呢？

## 代码帮的应用

1. C 语言预处理，编译和运行的学习

使用 yix 把 cc1/cpp 的主要代码表示出来即可实现，使用 yix_transform_c
把 gcc 的源代码直接转换

实例 1. Linux 内核原理的展示

Linux 内核就是一组 C 编写的代码，我们有时候需要根据代码把过程描述出来，
例如下面的这个项目就是使用文字的方式来描述 Linux 的内核

https://0xax.gitbooks.io/linux-insides/content/

但是 代码帮 可以使用更加直观的方式来展示内核，帮助人们了解 Linux 的内
部原理。

基本思路是定义内核相应的域，然后把代码直接转换过去，在代码帮引擎中执行
转换后的代码就可以动态的了解 Linux 内核执行过程。

使用 yix 把 linux 内核源码和 glibc 的主要代码表示出来即可实现，使用
yix_transform_c 把 glibc 的源代码直接转换

实例 2. Python 解释器的核心工作原理（PyEval_EvalFrameEx)

使用 yix 把 Python 的核心代码 ceval.c 表示出来即可实现，使用 yix_transform_c 把
Python 相关源代码直接转换

2. 帮助开发人员发现内存堆栈方面的问题。

这类问题使用普通调试器一般很难发现，代码帮可以应用于发现数据方面的问题。为了提高
运行速度和性能，需要下载代码帮 App 在本地运行。

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

2.1 图形化的显示内存数据

在调试 Python37-32 的超级模式的实例中，如果能够显示内存数据 _PyRuntime 的图形化
数据视图，并能够发现不正确的字段，例如，PyObject * 的字段指向的不是 PyObject 对
象等，将可以大大的提高发现问题的效率。

代码帮提供这样的功能，可以检查任意时刻的任意内存地址对应的图形化数据，可以根据已
知的所有数据类型自动识别对应的数据类型，也可以用户指定数据类型，用于查找其中的不
正确的字段，然后自动校正（例如，调整偏移量等）。

这种情况下代码帮是作为数据的显示视图，代码的执行需要在调试器 GDB 下运行，代码帮
和 GDB 进行通信（可能需要使用 Python 写一个 GDB 的扩展模块），获得内存，数据类型
等相关信息。

## 项目现状

开始上线运营，发布地址: https://codebang.dashingsoft.com

## 参考项目

* [CodePen](https://codepen.io)
* [SkyEye](http://www.digiproto.com/)
