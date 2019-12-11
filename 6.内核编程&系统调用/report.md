[toc]
## 实验目的
* 通过编程实践、观察，学习linux内核编程与系统调用的方法。
## 实验环境
* 硬件
1.Intel(R) Xeon(R) Bronze 3104 CPU @ 1.70GHz
2.DDR4 16G
* 软件
1.CentOS 7
2.VMware Workstation Pro 15

##  一、内核编程与实验环境
### 1.1.3  Linux 主机环境
安装CentOS7,查看内核版本
```bash
[hypo@localhost ~]$ uname -r
3.10.0-957.el7.x86_64
```
可以发现内核版本为3.10.0

### 1.2.1  yum 升级安装内核
在开始实验之前，我们需要更新内核版本至4.4.189并建立好内核编译环境以及调试环境。
* 执行以下命令安装yum 源elrepo
```bash
[root@localhost hypo]# rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
[root@localhost hypo]# rpm -Uvh http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm
Retrieving http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm
Retrieving http://elrepo.org/elrepo-release-7.0-4.el7.elrepo.noarch.rpm
Preparing...                          ################################# [100%]
	package elrepo-release-7.0-4.el7.elrepo.noarch is already installed
```
* 屏显 1-1 列出可安装的内核
```bash
[root@localhost hypo]# yum --disablerepo="*" --enablerepo="elrepo-kernel" list available
Loaded plugins: auto-update-debuginfo, fastestmirror, langpacks
Loading mirror speeds from cached hostfile
 * elrepo-kernel: hkg.mirror.rackspace.com
Available Packages
kernel-lt.x86_64                        4.4.205-1.el7.elrepo       elrepo-kernel
kernel-lt-devel.x86_64                  4.4.205-1.el7.elrepo       elrepo-kernel
kernel-lt-doc.noarch                    4.4.205-1.el7.elrepo       elrepo-kernel
kernel-lt-headers.x86_64                4.4.205-1.el7.elrepo       elrepo-kernel
kernel-lt-tools.x86_64                  4.4.205-1.el7.elrepo       elrepo-kernel
kernel-lt-tools-libs.x86_64             4.4.205-1.el7.elrepo       elrepo-kernel
kernel-lt-tools-libs-devel.x86_64       4.4.205-1.el7.elrepo       elrepo-kernel
kernel-ml.x86_64                        5.4.1-1.el7.elrepo         elrepo-kernel
kernel-ml-devel.x86_64                  5.4.1-1.el7.elrepo         elrepo-kernel
kernel-ml-doc.noarch                    5.4.1-1.el7.elrepo         elrepo-kernel
kernel-ml-headers.x86_64                5.4.1-1.el7.elrepo         elrepo-kernel
kernel-ml-tools.x86_64                  5.4.1-1.el7.elrepo         elrepo-kernel
kernel-ml-tools-libs.x86_64             5.4.1-1.el7.elrepo         elrepo-kernel
kernel-ml-tools-libs-devel.x86_64       5.4.1-1.el7.elrepo         elrepo-kernel
perf.x86_64                             5.4.1-1.el7.elrepo         elrepo-kernel
python-perf.x86_64                      5.4.1-1.el7.elrepo         elrepo-kernel
```
由于我们要安装4.4.205 版本的内核，因此使用命令yum --enablerepo=elrepo-kernel install
kernel-lt -y，如屏显 1-2 所示。如果用kernel-ml 则是mainline 当前最新的主线版本。
```bash
[root@localhost hypo]# yum --enablerepo=elrepo-kernel install kernel-lt -y
Loaded plugins: auto-update-debuginfo, fastestmirror, langpacks
Loading mirror speeds from cached hostfile
 * base: ap.stykers.moe
 * elrepo: mirror-hk.koddos.net
 * elrepo-kernel: mirror-hk.koddos.net
 * extras: centos.ustc.edu.cn
 * updates: ap.stykers.moe
Trying other mirror.
updates                                                  | 3.4 kB     00:00     
elrepo/primary_db                                          | 400 kB   00:00     
Resolving Dependencies
--> Running transaction check
---> Package kernel-lt.x86_64 0:4.4.205-1.el7.elrepo will be installed
--> Finished Dependency Resolution

Dependencies Resolved

================================================================================
 Package        Arch        Version                    Repository          Size
================================================================================
Installing:
 kernel-lt      x86_64      4.4.205-1.el7.elrepo       elrepo-kernel       39 M

Transaction Summary
================================================================================
Install  1 Package

Total download size: 39 M
Installed size: 180 M
Downloading packages:
kernel-lt-4.4.205-1.el7.elrepo.x86_64.rpm                  |  39 MB   00:47     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Warning: RPMDB altered outside of yum.
  Installing : kernel-lt-4.4.205-1.el7.elrepo.x86_64                        1/1 
  Verifying  : kernel-lt-4.4.205-1.el7.elrepo.x86_64                        1/1 

Installed:
  kernel-lt.x86_64 0:4.4.205-1.el7.elrepo                                       
Complete!
```
* 重启后查看内核版本
```bash
[hypo@localhost ~]$ uname -r
4.4.205-1.el7.elrepo.x86_64
```
### 1.2.2  内核源码安装方式
下载地址：https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.4.205.tar.xz
使用root权限打开nautilus
将文件下载到/usr/src/kernels
并用tar 解开

```bash
tar xvf linux-4.4.205.tar.xz
```
为了支持内核配置和编译，还需要安装少量额外工具包：
```bash
yum -y install gcc bc gcc-c++ ncurses ncurses-devel cmake elfutils-libelf-devel openssl-devel
```
配置文件.config 将指出哪些内核功能的是需要的，哪些功能是不需要的，哪些功能将编译成模块方式以便可以根据需要动态地加入到系统中。
为了生成.config 配置文件，需要用内核配置命令make config、make menuconfig、make xconfig 和make gconfig 几种方式。

make gconfig 需要依赖于GTK+ 2.0，make xconfig 需要依赖于QT
```bash
yum -y install qt #QT
yum -y install gtk2 gtk2-devel gtk2-devel-docs #GTK+ 2.0
```
* 屏显 1-3 Centos7 内核使用的配置文件
```bash
[hypo@localhost ~]$ ls /boot/config*
/boot/config-3.10.0-957.el7.x86_64  /boot/config-4.4.205-1.el7.elrepo.x86_64
```
将4.4.202版本中的配置文件内容拷贝到/usr/src/kernels/linux-4.4.202/.config作为我们的内核配置，并在该文件夹下执行make;make modules_install; make install三个命令完成编译安装.
* make
```bash
[root@localhost linux-4.4.205]# make -j4
  HOSTCC  scripts/basic/fixdep
  HOSTCC  scripts/kconfig/conf.o
  SHIPPED scripts/kconfig/zconf.tab.c
  SHIPPED scripts/kconfig/zconf.lex.c
......
  H16TOFW firmware/edgeport/down2.fw
  IHEX2FW firmware/whiteheat_loader.fw
  IHEX2FW firmware/whiteheat.fw
  IHEX2FW firmware/keyspan_pda/keyspan_pda.fw
  IHEX2FW firmware/keyspan_pda/xircom_pgs.fw

```
编译完成后即可安装内核模块，执行make modules_install
* 执行make modules_install前内核模块目录
```bash
[root@localhost linux-4.4.205]# ls /lib/modules
3.10.0-957.el7.x86_64  4.4.205-1.el7.elrepo.x86_64
```
* 执行make modules_install
```bash
[root@localhost linux-4.4.205]# make modules_install
  INSTALL Documentation/connector/cn_test.ko
  INSTALL arch/x86/crypto/aesni-intel.ko
  INSTALL arch/x86/crypto/blowfish-x86_64.ko
  INSTALL arch/x86/crypto/camellia-aesni-avx-x86_64.ko
  INSTALL arch/x86/crypto/camellia-aesni-avx2.ko
......
```
* 执行make modules_install后内核模块目录
```bash
[root@localhost linux-4.4.205]# ls /lib/modules
[root@localhost linux-4.4.205]# ls /lib/modules
3.10.0-957.el7.x86_64  4.4.205  4.4.205-1.el7.elrepo.x86_64
```
接着执行make install 安装内核
* 屏显 1-5 安装内核
```bash
[root@localhost linux-4.4.205]# make install
sh ./arch/x86/boot/install.sh 4.4.205 arch/x86/boot/bzImage \
	System.map "/boot"
[root@localhost linux-4.4.205]# ls /boot
config-3.10.0-957.el7.x86_64
config-4.4.205-1.el7.elrepo.x86_64
efi
grub
grub2
initramfs-0-rescue-e5acd5d39dc64925810753ecffa53aa5.img
initramfs-3.10.0-957.el7.x86_64.img
initramfs-3.10.0-957.el7.x86_64kdump.img
initramfs-4.4.205-1.el7.elrepo.x86_64.img
initramfs-4.4.205.img  #img
symvers-3.10.0-957.el7.x86_64.gz
symvers-4.4.205-1.el7.elrepo.x86_64.gz
System.map
System.map-3.10.0-957.el7.x86_64
System.map-4.4.205  #map
System.map-4.4.205-1.el7.elrepo.x86_64
vmlinuz
vmlinuz-0-rescue-e5acd5d39dc64925810753ecffa53aa5
vmlinuz-3.10.0-957.el7.x86_64
vmlinuz-4.4.205
vmlinuz-4.4.205-1.el7.elrepo.x86_64
```
安装后将在/boot 目录项更新System.map 和vmlinuz 两个文件，它们是软连接指向/boot/System.map-4.4.205 和/boot/vmlinuz-4.4.205。
* 屏显 1-6 /boot 目录下的System.map 和vmlinuz 文件
```bash
[hypo@localhost boot]$ ls -l System.map vmlinuz
lrwxrwxrwx. 1 root root 24 Dec  1 23:17 System.map -> /boot/System.map-4.4.205
lrwxrwxrwx. 1 root root 21 Dec  1 23:17 vmlinuz -> /boot/vmlinuz-4.4.205
```
*  vmlinuz 
编译生成的vmlinuz 是可引导的、压缩的内核，其中“vm”代表“Virtual Memory”，file命令查看到它是“Linux kernel x86 boot executable bzImage”，即bzip 压缩后的内核可执行映像。

* 屏显 1-7 file 查看vmlinuz-4.4.205
```bash
[hypo@localhost boot]$ file vmlinuz-4.4.205
vmlinuz-4.4.205: Linux kernel x86 boot executable bzImage, version 4.4.205 (root@localhost.localdomain) #1 SMP Sun Dec 1 22:54:42 , RO-rootFS, swap_dev 0x5, Normal VGA
```
未压缩的内核文件在源代码目录下，名为vmlinux。file 命令显示vmlinux 本质上是ELF 格式的文件。
* 屏显 1-8 vmlinux 和vmlinux.o 文件
```bash
[hypo@localhost boot]$ file /usr/src/kernels/linux-4.4.205/vmlinux
/usr/src/kernels/linux-4.4.205/vmlinux: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, BuildID[sha1]=404aa56b41453597972c678977c86cf38eafd6c3, not stripped
[hypo@localhost boot]$ file /usr/src/kernels/linux-4.4.205/vmlinux.o
/usr/src/kernels/linux-4.4.205/vmlinux.o: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), not stripped
[hypo@localhost boot]$ ls /usr/src/kernels/linux-4.4.205/vmlin* -l
-rwxr-xr-x. 1 root root 172192376 Dec  1 22:55 /usr/src/kernels/linux-4.4.205/vmlinux
-rw-r--r--. 1 root root 444773312 Dec  1 22:54 /usr/src/kernels/linux-4.4.205/vmlinux.o
```
* initramfs
initrd 是boot loader initialized RAM disk 的缩写，就是由 boot loader 初始化的内存盘。而initramfs 则是内存盘RAM disk 使用的映像文件.RedHat 类系统（包括Centos 和Fedora）从vmlinuz 核心引导后，会读取initrd.img 启动镜像，内涵、包含驱动模块等信息，其后才会从磁盘或其他介质挂载根文件系统。
mkinitrd 命令可建立映像文件，以供Linux 开机时载入ramdisk 中。由于其一部分文件来源于模块目录，如果命令中内核版本号不正确，将提示/lib/modules/下没有对应版本的内核模块目录。
* 屏显 1-9 生成initrd 影像
```bash
[root@localhost hypo]# mkinitrd myfs.img `uname -r`
[root@localhost hypo]# mkinitrd my4.4.205.img 4.4.205
[root@localhost hypo]# ls *.img
my4.4.205.img  myfs.img
```
用file 查看my4.4.205.img 文件，可以确认其类型为ASCII cpio archive (SVR4 with no CRC)。然后用cpio 将其内容提取出来，这就是内核启动时所使用的RAM disk 根文件系统结构，如屏显 1-10 所示。cpio 参数-i （等效于--extract），表示进入 copy-in 模式，也就是提取模式；参数-d（等效于 --make-directories），表示根据需要创建前导目录。zcat 是一个用于查看压缩文件的内容的程序，它将压缩文件扩展到标准输出而不是磁盘文件上。
* 屏显 1-10 内核的initrd 映像
```bash
[root@localhost ~]# file my4.4.205.img
my4.4.205.img: gzip compressed data, from Unix, last modified: Tue Dec 10 00:57:20 2019, max compression
[root@localhost ~]# mkdir my4.4.205-fs/
[root@localhost ~]# cd my4.4.205-fs/
[root@localhost my4.4.205-fs]# /usr/lib/dracut/skipcpio ../my4.4.205.img | zcat | cpio -ivd
.
tmp
usr
usr/bin
usr/bin/bash
usr/bin/sh
......
init
shutdown
125743 blocks
```
* System.map
System.map 文件是编译内核时生成的，它记录了内核中的符号列表，以及符号在内存中的虚拟地址。系统启动后，应用程序可以通过/proc/kallsyms 查找符号及其地址。
* 屏显 1-11 System.map 内核符号表文件（前10 行）
```bash
[root@localhost ~]# cd /
[root@localhost /]# cd boot
[root@localhost boot]# head System.map-4.4.205
0000000000000000 D __per_cpu_start
0000000000000000 D __per_cpu_user_mapped_start
0000000000000000 D irq_stack_union
0000000000000000 A xen_irq_disable_direct_reloc
0000000000000000 A xen_save_fl_direct_reloc
00000000000001c5 A kexec_control_code_size
0000000000004000 D vector_irq
0000000000004800 D unsafe_stack_register_backup
0000000000004840 D cpu_tss
0000000000006b00 d cpu_debug_store
```
### 1.2.3 启动菜单的内核选项
CentOS7 使用grub2 来做内核启动。
* 屏显 1-12 查看/boot/grub2/grub.cfg
```bash
[root@localhost ~]# awk -F\' '$1=="menuentry " {print i++ " : " $2}' /boot/grub2/grub.cfg
0 : CentOS Linux (4.4.205) 7 (Core)
1 : CentOS Linux (4.4.205-1.el7.elrepo.x86_64) 7 (Core)
2 : CentOS Linux (3.10.0-957.el7.x86_64) 7 (Core)
3 : CentOS Linux (0-rescue-e5acd5d39dc64925810753ecffa53aa5) 7 (Core)
```

* 屏显 1-13 修改新的内核作为默认启动，因此只需要修改/etc/default/grub 文件即可
```bash
[root@localhost ~]# cat /etc/default/grub
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
GRUB_CMDLINE_LINUX="crashkernel=auto rhgb quiet"
GRUB_DISABLE_RECOVERY="true"
#GRUB_DEFAULT 用于指定启动时默认使用的内核
#其中如果menuentry number 选0 则是我们刚从源代码编译安装的4.4.205 内核。
```
* 屏显 1-14 /boot/grub2/grubenv
```bash
[root@localhost ~]# cat /boot/grub2/grubenv
# GRUB Environment Block
saved_entry=CentOS Linux (3.10.0-957.el7.x86_64) 7 (Core)
```
### 1.3.1 内核配置

Linux 内核配置系统由3 个部分组成：
1.Makefile：分手在源代码的各个目录中，定义了内核编译规则
2.Kconfig: 用户可选择的功能
3..config 配置工具：包括配置命令解释器和配置用户界面（字符或图形界面），这些配置工具使用脚本语言（Tcl、TK 或perl）用户配置结果保存在.config 文件中

make命令基本使用方法
```bash
make menuconfig #基于curses 的文本窗口界面
make mrproper #清理所有编译生成的文件、 config 及某些备份文件
make clean #清理大多数编译生成的文件，但会保留config 文件等
```

## 二、内核编程示例
### 2.1.1  Hello 模块
为了展示内核模块的编写， 我们先在内核源码目录中新建一个子目录myKernelExp/helloModule，并且编写一个hello.c 文件和Makefile 文件。

#### 编译hello.ko 模块
* 代码 2-1 hello 模块源代码hello.c
```c
#include <linux/init.h>
#include <linux/module.h>
MODULE_LICENSE("Dual BSD/GPL");
static int hello_init(void)
{
    printk(KERN_ALERT " Hello World enter\n");
    return 0;
}
static void hello_exit(void)
{
    printk(KERN_ALERT " Hello World exit\n ");
    printk(KERN_ALERT " \n ");
}
module_init(hello_init);
module_exit(hello_exit);

MODULE_AUTHOR("Song Baohua");
MODULE_DESCRIPTION("A simple Hello World Module");
MODULE_ALIAS("a simplest module");
```

* 代码 2-2 hello 模块的Makefile
```Makefile
obj-m:=hello.o
```
* 屏显 2-2 编译hello 模块
```bash
# -C 选项的作用是指将当前的工作目录转移到指定的目录，即内核源码（KERN_DIR）目录，然后在$(pwd)给出的当前目录中查找模块源码，将其编译生成.ko 文件。
[root@localhost helloModule]# make -C /usr/src/kernels/linux-4.4.205 M=$(pwd) modules
make: Entering directory `/usr/src/kernels/linux-4.4.205'
  CC [M]  /usr/src/kernels/linux-4.4.205/myKernelExp/helloModule/hello.o
  Building modules, stage 2.
  MODPOST 1 modules
  CC      /usr/src/kernels/linux-4.4.205/myKernelExp/helloModule/hello.mod.o
  LD [M]  /usr/src/kernels/linux-4.4.205/myKernelExp/helloModule/hello.ko
make: Leaving directory `/usr/src/kernels/linux-4.4.205'
[root@localhost helloModule]# ls
hello.c   hello.mod.c  hello.o   modules.order
hello.ko  hello.mod.o  Makefile  Module.symvers
```
* 屏显 2-3 用file 和objdump 查看hello.ko
```bash
[root@localhost helloModule]# file hello.ko
hello.ko: ELF 64-bit LSB relocatable, x86-64, version 1 (SYSV), BuildID[sha1]=3d1e8d3e98d26bc16ff0576c7899cd2c341e8260, not stripped
[root@localhost helloModule]# objdump -h hello.ko

hello.ko:     file format elf64-x86-64

Sections:
Idx Name          Size      VMA               LMA               File off  Algn
  0 .note.gnu.build-id 00000024  0000000000000000  0000000000000000  00000040  2**2
                  CONTENTS, ALLOC, LOAD, READONLY, DATA
......
 16 .debug_frame  00000068  0000000000000000  0000000000000000  0000ee10  2**3
                  CONTENTS, RELOC, READONLY, DEBUGGING
```
#### 使用hello.ko 模块（restart into 4.4.205）
成功编译后，尝试用insmod 命令加载hello 内核模块
* 屏显 2-4 加载hello 模块后的内核输出信息
```bash
[root@localhost helloModule]# insmod hello.ko
[root@localhost helloModule]# dmesg | tail -2
[  190.446413] hello: loading out-of-tree module taints kernel.
[  190.447451]  Hello World enter
```
* 屏显 2-5 lsmod 查看hello 模块
```bash
#dmesg 命令从/var/log/messages 中读出printk 打印出来的信息，tail -2 显示了新的两行内容，正是hello 模块加载时的信息
[root@localhost helloModule]# dmesg | tail -2
[  190.446413] hello: loading out-of-tree module taints kernel.
[  190.447451]  Hello World enter
# 用lsmod 查看内核模块信息（并用tail -3 只显示前3行）
[root@localhost helloModule]# lsmod | head -3
Module                  Size  Used by
hello                  16384  0 
tcp_lp                 16384  0 
#hello 模块已经加载，占用16384 字节的内存空间，未被其他模块所引用（Used by为0）
```

* 屏显 2-6 /proc/modules 中hello 模块信息
```bash
#lsmod 命令的信息来源于/proc/modules，用cat 命令查看/proc/modules 文件可以看到相似的信息
[root@localhost helloModule]# cat /proc/modules |head -3
hello 16384 0 - Live 0xffffffffa05c8000 (O)#(O)标明是out-of-tree 外部模块
tcp_lp 16384 0 - Live 0xffffffffa05c3000
fuse 94208 3 - Live 0xffffffffa05ab000
```

* 屏显 2-7 /sys/module/hello 目录树
```bash
[root@localhost helloModule]# cd /sys/module/hello
# 用tree -a 命令（如未安装tree 工具，请先执行yum install tree）查看该目录结构
[root@localhost hello]# tree a
a [error opening dir]

0 directories, 0 files
[root@localhost hello]# tree -a
.
├── coresize
├── holders
├── initsize
├── initstate
├── notes
│   └── .note.gnu.build-id
├── refcnt
├── sections
│   ├── .gnu.linkonce.this_module
│   ├── __mcount_loc
│   ├── .note.gnu.build-id
│   ├── .rodata.str1.1
│   ├── .strtab
│   ├── .symtab
│   └── .text
├── srcversion
├── taint
└── uevent

3 directories, 15 files
```
* 屏显 2-8 查看hello 模块中.text 代码节的装载地址
```bash
[root@localhost hello]# cat sections/.text
0xffffffffa05c8000
```
* 屏显 2-9 卸载hello 模块时的输出信息
```bash
#用rmmod 命令卸载该模块，代码中的hello_exit()将为我们打印出退出时的提示信息
[root@localhost helloModule]# rmmod hello.ko
[root@localhost helloModule]# dmesg | tail -4
[ 1673.355682]  Hello World exit
 
[ 1673.355686]  
```
###  2.1.2 内核模块的代码结构
```c
//加载与卸载
//参数
//导出符号
//声明及其他描述
```

### 2.2 字符设备驱动程序
通过一小片内存来形成字符设备，以便用户程序可以对它进行读写操作。通过它把字符设备驱动程序的框架展示出来。下面先以样例代码入手，形成可运行的样例，然后再仔细分析内核和字符设备驱动程序之间的细节。
### 2.2.1. memchar 设备
#### 编写memchar 驱动
```bash
#创建目录辑/usr/src/kernels/linux-4.4.205/myKernelExp/memchar/memchar.c
[root@localhost myKernelExp]# mkdir memchar
[root@localhost myKernelExp]# cd memchar
```
```bash
#编译memchar.c
[root@localhost memchar]# cat memchar.c
#include <linux/module.h> 
#include <linux/fs.h>
#include <linux/mm.h>
#include <linux/init.h>
#include <linux/cdev.h>
#include <asm/uaccess.h>
#include <linux/slab.h>
#define MEMCHAR_SIZE 0x1000     /*设备所使用的内存大小 4KB*/
#define MEM_CLEAR 0x1           /*对所占内存清零*/
#define MEMCHAR_MAJOR 199       /* memchar 的主设备号*/
......
[root@localhost memchar]# cat Makefile
obj-m:=memchar.o
[root@localhost memchar]# make -C /usr/src/kernels/linux-4.4.205 M=$(pwd) modules
make: Entering directory `/usr/src/kernels/linux-4.4.205'
  CC [M]  /usr/src/kernels/linux-4.4.205/myKernelExp/memchar/memchar.o
  Building modules, stage 2.
  MODPOST 1 modules
  CC      /usr/src/kernels/linux-4.4.205/myKernelExp/memchar/memchar.mod.o
  LD [M]  /usr/src/kernels/linux-4.4.205/myKernelExp/memchar/memchar.ko
make: Leaving directory `/usr/src/kernels/linux-4.4.205'
[root@localhost memchar]# 
```
```bash
#安装memchar.ko
[root@localhost memchar]# insmod memchar.ko
[root@localhost memchar]# cat /proc/devices
Character devices:
  1 mem
  4 /dev/vc/0
  4 tty
  4 ttyS
  5 /dev/tty
  5 /dev/console
  5 /dev/ptmx
  7 vcs
......
189 usb_device
199 memchar #memchar 字符设备，主设备号为199。
202 cpu/msr
......
```

#### 读写测试
* 屏显 2-11 创建memchar 的设备节点
```bash
[root@localhost memchar]# mknod /dev/memchar c 199 0
[root@localhost memchar]# ls /dev/memchar -l
crw-r--r--. 1 root root 199, 0 Dec 10 05:02 /dev/memchar
[root@localhost memchar]# 
```
* 代码 2-3 memchar-write.c
```c
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
int main(int argc,char **argv)
{
    if(argc<2)
    { 
        perror("Usage: memchar-write XXXXXX (message to write)!\n");
        exit(1);
    }
    int fd;
    fd=open("/dev/memchar",O_RDWR|O_CREAT,0666);
    if(fd==-1)
    { 
        perror("open file mytest");
        exit(2);
    }
    write(fd,argv[1],strlen(argv[1]));
    close(fd);
    return 0;
}
```

* 代码 2-4 memchar-read.c
```c
#include <stdio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>

char buf_in[1024];

int main()
{
    int fd;
    fd=open("/dev/memchar",O_RDWR|O_CREAT,0666);
    if(fd==-1)
    { 
        perror("open file mytest");
        exit(1);
    }
    read(fd,buf_in,1024);
    printf("retrieved message is : %s !\n",buf_in);
    close(fd);
    return 0;
}
```
* 屏显 2-12 对/dev/memchar 设备的读写
```bash
[hypo@localhost linux]$ gcc memchar-write.c -o memchar-write
[hypo@localhost linux]$ gcc memchar-read.c -o memchar-read
[root@localhost linux]# ./memchar-write yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
[root@localhost linux]# ./memchar-read
retrieved message is : yyyyyyyyyyyyyyyyyyyyyyyyyyyyyy !

#用echo XXXX > /dev/memchar 的方式写入数据
[root@localhost linux]# echo hypo  > /dev/memchar
[root@localhost linux]# ./memchar-read
retrieved message is : hypo
yyyyyyyyyyyyyyyyyyyyyyyyy !
```
### 2.2.2  字符设备
字符设备驱动程序由cdev 结构体描述，其成员一部分和设备驱动模型相关。与具体功能相关的一个重要成员就是操作函数列表ops——在统一的文件操作接口之下封装了对硬件操作细节。
* 代码 2-6 cdev （linux-4.4/include/linux/cdev.h）
```bash
[root@localhost linux]# cat /usr/src/kernels/linux-4.4.205/include/linux/cdev.h
#ifndef _LINUX_CDEV_H
#define _LINUX_CDEV_H

#include <linux/kobject.h>
#include <linux/kdev_t.h>
#include <linux/list.h>
......
```
#### 设备的散列组织
每个字符设备使用一个cdev 结构体来表示（相应地块设备却使用genhd 来描述，而不是使用block_device）。为了快速地根据设备号找到cdev 或genhd，系统中有两个全局变量cdev_map 和bdev_map 组织了散列表，它们都是类型为kobj_map 结构体
* 代码 2-7 kobj_map (linux-4.4/drivers/base/map.c)
```bash
[root@localhost linux]# cat /usr/src/kernels/linux-4.4.205/drivers/base/map.c
......
struct kobj_map {
	struct probe {
		struct probe *next;
		dev_t dev;
		unsigned long range;
		struct module *owner;
		kobj_probe_t *get;
		int (*lock)(dev_t, void *);
		void *data;
	} *probes[255];
	struct mutex *lock;
};
......
```
* 代码 2-8 char_device_struct 及chrdevs[] (linux-4.4/fs/char_dev.c)
```bash
[root@localhost linux]# cat /usr/src/kernels/linux-4.4.205/fs/char_dev.c
......
static struct char_device_struct {
	struct char_device_struct *next;
	unsigned int major;
	unsigned int baseminor;
	int minorct;
	char name[64];
	struct cdev *cdev;		/* will die */
} *chrdevs[CHRDEV_MAJOR_HASH_SIZE];
......
```
#### 初始化与注册
  通常字符设备初始化代码（例如linux-4.4/drivers/char/raw.c中的raw_init()）通常完成以下步骤：
  1.先创建一个新的cdev对象；
  2.用register_chrdev_region()分配或注册一个设备号范围（使用代码4-7的chrdevs[]）；
  3.执行cdev_init()函数将cdev->ops 指向该字符设备专用的操作函数列表；
  4.然后通过cdev_add()将设备添加到字符设备数据库并激活；
  5.调用class_create()创建设备的类；
  6.调用device_create()创建device设备。
#### 打开字符设备
​    chrdev_open()的382行根据设备号inode->i_rdev 调用kobj_lookup()在cdev_map中查找kobject，进而找到包含它的cdev。在成功找到了该设备 cdev对象之后，将inode->i_cdev成员指向该字符设备对象。下次再对该设备文件节点进行操作时，就可以直接通 过 i_cdev 成员得到设备节点所对应的字符设备对象，而无须再通过cdev_map进行查找。
​    然后用cdev->ops替换file->f_op从而使用字符设备驱动自己提供的file_operations。最后，调用该字符设备驱动提供的open方法，完成设备初始化等工作。
​    在字符设备对象初始化时调用cdev_init()函数将字符设备对象 cdev->ops 指向该本设备的文件操作函数表 file_operations。
* 代码 2-9 chrdev_open() (linux-3.13/fs/char_dev.c)
```bash
[root@localhost linux]# cat /usr/src/kernels/linux-4.4.205/fs/char_dev.c
......
static int chrdev_open(struct inode *inode, struct file *filp)
{
	const struct file_operations *fops;
	struct cdev *p;
	struct cdev *new = NULL;
	int ret = 0;

	spin_lock(&cdev_lock);
	p = inode->i_cdev;
	if (!p) {
		struct kobject *kobj;
		int idx;
		spin_unlock(&cdev_lock);
		kobj = kobj_lookup(cdev_map, inode->i_rdev, &idx);
		if (!kobj)
			return -ENXIO;
		new = container_of(kobj, struct cdev, kobj);
		spin_lock(&cdev_lock);
		/* Check i_cdev again in case somebody beat us to it while
		   we dropped the lock. */
		p = inode->i_cdev;
		if (!p) {
			inode->i_cdev = p = new;
			list_add(&inode->i_devices, &p->list);
			new = NULL;
		} else if (!cdev_get(p))
			ret = -ENXIO;
	} else if (!cdev_get(p))
		ret = -ENXIO;
	spin_unlock(&cdev_lock);
	cdev_put(new);
	if (ret)
		return ret;

	ret = -ENXIO;
	fops = fops_get(p->ops);
	if (!fops)
		goto out_cdev_put;

	replace_fops(filp, fops);
	if (filp->f_op->open) {
		ret = filp->f_op->open(inode, filp);
		if (ret)
			goto out_cdev_put;
	}

	return 0;

 out_cdev_put:
	cdev_put(p);
	return ret;
}
......
```

## 三、系统调用
### 3.1. 添加系统调用
### 3.1.1. mysyscall 系统调用
* 添加系统调用号
/usr/src/kernels/linux-4.4.205/arch/x86/entry/syscalls/syscall_64.tbl添加如下一行，声明新的系统调用
```tbl
325	common	mlock2			sys_mlock2
#	my_call
326	common	mysyscall		sys_mysyscall
#
```

* 系统调用函数声明
/usr/src/kernels/linux-4.4.205/include/linux/syscalls.h添加如下一行，完成系统调用服务函数的声明。
```h
......
asmlinkage long sys_mlock2(unsigned long start, size_t len, int flags);
//my_call
asmlinkage long sys_mysyscall(int input_num);
#endif
```

* 添加系统调用号
原则上来说系统调用的服务函数可以在内核源码的任意地方实现，但是处于方便考虑，直接在kernel/sys.c 中实现了mysyscall()

```c
SYSCALL_DEFINE1(mysyscall,int,input_num){
    int result=input_num*2;
    printk("The result is %d\n",result);
    return result;
}
```
### 3.1.2  重新编译内核
执行make; make modules_install; make install 编译并安装新的内核，最后重启系统让新添加的系统调用生效。此时检查/boot/System.map-4.4.205 中的符号表可以发现mysyscall 相关的符号。而原来的系统符号表则保存到/boot/ System.map-4.4.205.old
* 屏显 4-1 System.map-4.4.189 中新增mysyscall 相关的符号
```bash
[hypo@localhost boot]$ cat System.map-4.4.205 | grep mysyscall
ffffffff81098df0 T SyS_mysyscall
ffffffff81098df0 T sys_mysyscall
ffffffff81adc1a0 d event_exit__mysyscall
ffffffff81adc240 d event_enter__mysyscall
ffffffff81adc2e0 d __syscall_meta__mysyscall
ffffffff81adc320 d args__mysyscall
ffffffff81adc328 d types__mysyscall
ffffffff81d9e508 t __event_exit__mysyscall
ffffffff81d9e510 t __event_enter__mysyscall
ffffffff81da0638 t __p_syscall_meta__mysyscall
```
### 4.1.3  测试验证
* 代码 4-4 mysyscall_test.c 测试程序
```c
#include <stdio.h>
#include <stdlib.h>
int main(int argc,void **argv)
{   int input_num,result;
    input_num= atoi(argv[1]);
    result=syscall(326,input_num);
    printf("result of mysyscall(%d) is: .\n",&input_num,&result);
    return 0;
}
```

* 在旧内核运行中运行mysyscall_test
```bash
[hypo@localhost linux]$ ./mysyscall_test 12
result of mysyscall(12) is: -1.
#strace 跟踪
[hypo@localhost linux]$ strace ./mysyscall_test 12
execve("./mysyscall_test", ["./mysyscall_test", "12"], [/* 49 vars */]) = 0
......
copy_file_range(12, 0xa, 0, [139715105483232], 140721734837005, 1426342264) = -1 ENOSYS (Function not implemented)
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 1), ...}) = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f11f55de000
write(1, "result of mysyscall(12) is: .\n", 30result of mysyscall(12) is: .
) = 30
exit_group(0)                           = ?
+++ exited with 0 +++
[hypo@localhost linux]$ 

```

* 在新内核上运行mysyscall_test
```bash
[root@localhost linux]# ./mysyscall_test 12
result of mysyscall(12) is: 24.
[root@localhost linux]# dmesg | tail -1
[ 2447.884291] The result is 24
#strace 跟踪
[root@localhost linux]# strace ./mysyscall_test 12
execve("./mysyscall_test", ["./mysyscall_test", "12"], [/* 49 vars */]) = 0
......
copy_file_range(12, 0xa, 0, [139825941932512], 140732992373542, 4093950248) = 24
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 2), ...}) = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f2bc3bbe000
write(1, "result of mysyscall(12) is: 24.\n", 32result of mysyscall(12) is: 24.
) = 32
exit_group(0)                           = ?
+++ exited with 0 +++
```

