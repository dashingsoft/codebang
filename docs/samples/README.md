# CodeBang 应用实例

PyArmor 开发中遇到的一个堆栈问题，在使用新的包裹模式 2 加密的脚本，在MacOS
(10.14.6) 上的 Python 3.7.7 的环境下面运行总是出现崩溃现象

    Segmentation fault: 11

## 环境配置

在 Linux 下面，使用下面的命令生成单独的调试信息 `.dwarf` 文件，例如

    gcc -g -gsplit-dwarf -o foo.so foo.c
    
    cp foo.so foo.dwo /path/to/dist/
    
在 Mac 下面，使用选项 `-g` 保存调试信息，然后使用 `dysym` 生成独立的调试信息目录
.dySYM，最好把动态库里面的调试信息删除

    gcc -g -shared -o foo.so foo.c
    dsymutil foo.so
    strip -x foo.so
    
    cp -a foo.so foo.so.dSYM /path/to/dist

    xcrun python3 lldb-proxy.py

## 代码版本

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

