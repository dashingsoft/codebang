workpath=$(pwd)
rootfs="rootfs"
busybox="busybox-1.32.1"

rm -rf $rootfs
mkdir $rootfs

cp $busybox/_install/* rootfs/ -rfa

# Runtime lib without debug symbol in remote server
cp -a /usr/aarch64-linux-gnu/lib $rootfs/
rm -rf $rootfs/lib/debug/

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

mkdir -p $rootfs/opt/codebang/data/users

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
mount -t 9p -o trans=virtio hostfolder /opt/codebang/data/users
ifconfig eth0 10.0.2.15 netmask 255.255.255.0 up
route add default gateway 10.0.2.2 eth0
/usr/local/bin/gdbserver --multi 10.0.2.15:20600 &
EOF
chmod 755 $rootfs/etc/init.d/rcS

(cd $rootfs; find . | cpio -o -H newc > $workpath/rootfs.cpio)
gzip -c rootfs.cpio > rootfs.cpio.gz

rm rootfs.cpio
mv rootfs.cpio.gz ../data/vm
