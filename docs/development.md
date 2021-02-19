# 开发人员手册

## QEMU + AARCH64 + GDB + GCC 配置

Refer to https://wiki.ubuntu.com/ARM64/QEMU

在 Ubuntu 20.04 环境下面，直接安装

    $ sudo apt install qemu-system-arm qemu-efi gcc-aarch64-linux-gnu

编译内核，输出文件 `arch/arm64/boot/zImage`:

    wget https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.20.tar.xz
    tar xJf linux-4.20.tar.xz
    cd linux-4.20
    make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- defconfig
    make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-

## 制作根文件系统

下载编译 `busybox`，为了简单起见，busybox配置为静态编译，如果不配置为静
态编译，则 `busybox` 的运行还需要依赖一些动态库，生成根文件系统的时候就
需要从交叉编译工具链环境中将需要的动态库拷贝过来

    wget http://www.busybox.net/downloads/busybox-1.32.1.tar.bz2

    tar xjf busybox-1.32.1.tar.bz2
    cd busybox-1.32.1

    # Change STATIC default value to y
    vi Config.in

    make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- defconfig

    make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-
    make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- install

准备相应的文件 `mkrootfs.sh`

```bash
workpath=$(pwd)
rootfs="rootfs"
busybox="busybox-1.32.1"

rm -rf $rootfs
mkdir $rootfs

cp -a /usr/aarch64-linux-gnu/lib $rootfs
cp $busybox/_install/* rootfs/ -rfa

mkdir $rootfs/proc
mkdir $rootfs/mnt
mkdir $rootfs/tmp
mkdir $rootfs/root
mkdir $rootfs/var

mkdir $rootfs/etc
mkdir $rootfs/etc/network
mkdir $rootfs/etc/init.d

mkdir $rootfs/dev
mknod $rootfs/dev/tty1 c 4 1
mknod $rootfs/dev/tty2 c 4 2
mknod $rootfs/dev/tty3 c 4 3
mknod $rootfs/dev/tty4 c 4 4
mknod $rootfs/dev/console c 5 1
mknod $rootfs/dev/null c 1 3

cat << EOF > $rootfs/etc/inittab
::sysinit:/etc/init.d/rcS
::respawn:-/bin/sh
::ctrlaltdel:/bin/umount -a -r
EOF

cat << EOF > $rootfs/etc/network/interfaces
auto eth0
iface eth0 inet static
   address 10.0.2.15
   netmask 255.255.255.0
   gateway 10.0.2.2
EOF

cat << EOF > $rootfs/etc/init.d/rcS
#!/bin/sh
mount -t proc proc /proc
mount -t 9p -o trans=virtio hostfolder /mnt
ifconfig eth0 10.0.2.15 netmask 255.255.255.0 up
route add default gateway 10.0.2.2 eth0
EOF
chmod 755 $rootfs/etc/init.d/rcS

(cd $rootfs; find . | cpio -o -H newc > $workpath/rootfs.cpio)
gzip -c rootfs.cpio > rootfs.cpio.gz
```


## 启动ARM64虚拟机

在主机上创建共享目录

    mkdir /opt/codebang/share

使用下面的命令启动

```bash
qemu-system-aarch64 -machine virt -cpu cortex-a57 -machine type=virt -nographic -m 2048 -smp 2 \
                    -kernel linux-4.20/arch/arm64/boot/zImage \
                    -fsdev local,security_model=passthrough,id=fsdev0,path=/opt/codebang/share \
                    -device virtio-9p-pci,fsdev=fsdev0,mount_tag=hostfolder \
                    -netdev user,id=n0,hostfwd=tcp::20600-:20600 -device e1000e,netdev=n0 \
                    -initrd rootfs.cpio.gz \
                    -append "root=/dev/ram0 rootfstype=ramfs rdinit=/linuxrc console=ttyAMA0"
```

使用 gdb 调试虚拟机里面的应用

    qemu-system-aarch64 -s -S ...

然后启动 gdb 连接虚拟机

    gdb-multiarch linux-4.20/vmlinux
    (gdb) target remote localhost:1234
    (gdb) c

## 编译 gdbserver for aarch64

    apt install g++-aarch64-linux-gnu

    wget https://ftp.gnu.org/gnu/gdb/gdb-9.2.tar.xz
    tar xJf gdb-9.2.tar.xz
    cd gdb-9.2

    cd gdb/gdbserver
    ./configure --host=aarch64-linux-gnu
    make
    make install DESTDIR=/opt/codebang/busybox-1.32.1/_install

### 使用 gdbserver 进行调试

启动虚拟机，在虚拟机里面运行

    /usr/local/bin/gdbserver 10.0.2.15:20600 /opt/codebang/share/a.out

    /usr/local/bin/gdbserver --multi 10.0.2.15:20600 &

在主机端使用 gdb-multiarch 连接

    gdb-multiarch /opt/codebang/share/a.out
    (gdb) target remote localhost:20600
    (gdb) c

    gdb-multiarch
    (gdb) target extended-remote localhost:20600
    (gdb) set remote exec-file /opt/codebang/share/a.out
    (gdb) run

## glibc arm64 调试

安装包含调试符号的开发包

    apt install libc6-dev-arm64-cross libc6-dbg-arm64-cross
    dpkg -L libc6-dbg-arm64-cross

目前的方式是替换 `/usr/aarch64-linux-gnu/lib/libc-2.31.so` 为调试版本
`/usr/aarch64-linux-gnu/lib/debug/lib/aarch64-linux-gnu/libc-2.31.so`

还需要把 `glibc-2.31` 的源码拷贝到 `/opt/codebang/build` 下面，然后在 `gdb` 中设
置 `sysroot` 和 `substitute-path` ，这样就可以正确显示符号

    (gdb) set debug aarch64 on
    (gdb) set sysroot /usr/aarch64-linux-gnu
    (gdb) set substitute-path /build/cross-toolchain-base-vwSSmv/cross-toolchain-base-43ubuntu3.1 /opt/codebang/build
    (gdb) file /opt/codebang/share/a.out
    (gdb) start

## gcc 显示中文错误信息

增加中文支持，修改 `/etc/locale.gen` ， 把 `zh_CN.UTF-8` 所在的行注释去掉，然后
运行

    locale-gen

因为默认使用的 `gcc-9` ，所以 `gcc` 总是去找 `gcc-9.mo` ，但是默认装的只有
`gcc.mo` ，所以需要人工创建一个连接

    cd /usr/share/locale-langpack/zh_CN/LC_MESSAGES/
    ln -s gcc.mo gcc-9.mo

这样总算会显示中文消息了
