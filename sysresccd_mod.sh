#!/bin/sh

pushd /tmp/
unsquashfs /media/sysrescusb/sysrcd.dat

# mount-bind neccessary FS's

# create actual scripts to be run in chroot
chroot squashfs-root /bin/zsh

mksquashfs squashfs-root/* sysrcd.dat -comp lzo
rm -rf squashfs-root/
popd
