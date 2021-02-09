if [[ "$1" == "debug" ]] ; then
	echo "Start debug vmlinux at port 20800"
	START_OPTS="-gdb tcp::20800 -S"
fi

KERNEL=/opt/codebang/data/vm/Image.gz
ROOTFS=/opt/codebang/data/vm/rootfs.cpio.gz
USERDATA=/opt/codebang/data/users
HOSTFWDS="hostfwd=tcp::20600-:20600,hostfwd=tcp::20601-:20601,hostfwd=tcp::20602-:20602,hostfwd=tcp::20603-:20603,hostfwd=tcp::20604-:20604,hostfwd=tcp::20605-:20605,hostfwd=tcp::20606-:20606,hostfwd=tcp::20607-:20607,hostfwd=tcp::20608-:20608,hostfwd=tcp::20609-:20609"

qemu-system-aarch64 ${START_OPTS} \
	-machine virt -cpu cortex-a57 -machine type=virt \
	-nographic -m 2048 -smp 2 \
        -kernel $KERNEL -initrd $ROOTFS \
        -fsdev local,security_model=passthrough,id=fsdev0,path=$USERDATA \
        -device virtio-9p-pci,fsdev=fsdev0,mount_tag=hostfolder \
        -netdev user,id=n0,$HOSTFWDS -device e1000e,netdev=n0 \
        -append "root=/dev/ram0 rootfstype=ramfs rdinit=/linuxrc console=ttyAMA0"

