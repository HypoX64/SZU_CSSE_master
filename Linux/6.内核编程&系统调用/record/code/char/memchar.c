#include <linux/module.h> //1）1~22 行的头文件、全局变量、常量和数据结构；2）23~163 驱动程序主体部分；3）164~224 行是模块相关和设备初始化代码。
#include <linux/fs.h>
#include <linux/mm.h>
#include <linux/init.h>
#include <linux/cdev.h>
#include <asm/uaccess.h>
#include <linux/slab.h>
#define MEMCHAR_SIZE 0x1000     /*设备所使用的内存大小 4KB*/
#define MEM_CLEAR 0x1           /*对所占内存清零*/
#define MEMCHAR_MAJOR 199       /* memchar 的主设备号*/
static int memchar_major = MEMCHAR_MAJOR;
struct memchar_dev              /*memchar 设备结构体*/
{
    struct cdev cdev;           /*cdev 结构体*/
    unsigned char mem[MEMCHAR_SIZE];     /*设备所用内存*/
};
struct memchar_dev *memchar_devp;      /* memchar 设备结构体指针*/
/*--------------------------------------------------------------------------memchar设备文件的open函数*/
int memchar_open(struct inode *inode, struct file *filp)
{
    filp->private_data = memchar_devp;  /*将设备结构体指针赋值给文件私有数据指针*/
    return 0;
}
/*------------------------------------------------------------------------------  文件释放函数*/
int memchar_release(struct inode *inode, struct file *filp)
{
    return 0;
}
/*------------------------------------------------------------------------------     ioctl 设备控制函数 */
static  long memchar_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
{
    struct memchar_dev *dev = filp->private_data;   /*获得设备结构体指针*/
    switch (cmd)
    {
    case MEM_CLEAR:
        memset(dev->mem, 0, MEMCHAR_SIZE);
        printk(KERN_INFO "memchar is set to zero\n");
        break;
    default:
        return - EINVAL;
    }
    return 0;
}
/*------------------------------------------------------------------------------      读函数*/
static ssize_t memchar_read(struct file *filp, char __user *buf, size_t size, loff_t *ppos)
{
    unsigned long p = *ppos;
    unsigned int count = size;
    int ret = 0;
    struct memchar_dev *dev = filp->private_data;    /*获得设备结构体指针*/
    /*分析和获取有效的写长度*/
    if (p >= MEMCHAR_SIZE)
        return count ? - ENXIO: 0;
    if (count > MEMCHAR_SIZE - p)
        count = MEMCHAR_SIZE - p;
    /*内核空间→用户空间*/
    if (copy_to_user(buf, (void*)(dev->mem + p), count))
    {
        ret = - EFAULT;
    }
    else
    {
        *ppos += count;
        ret = count;
        printk(KERN_INFO "read %d bytes(s) from %ld\n", count, p);
    }
    return ret;
}
/*------------------------------------------------------------------------------       写函数*/
static ssize_t memchar_write(struct file *filp, const char __user *buf, size_t size, loff_t *ppos)
{
    unsigned long p = *ppos;
    unsigned int count = size;
    int ret = 0;
    struct memchar_dev *dev = filp->private_data;    /*获得设备结构体指针*/
    /*分析和获取有效的写长度*/
    if (p >= MEMCHAR_SIZE)
        return count ? - ENXIO: 0;
    if (count > MEMCHAR_SIZE - p)
        count = MEMCHAR_SIZE - p;
    /*用户空间→内核空间*/
    if (copy_from_user(dev->mem + p, buf, count))
        ret = - EFAULT;
    else
    {
        *ppos += count;
        ret = count;
        printk(KERN_INFO "written %d bytes(s) from %ld\n", count, p);
    }
    return ret;
}
/*------------------------------------------------------------------------------      seek 文件定位函数 */
static loff_t memchar_llseek(struct file *filp, loff_t offset, int orig)
{
    loff_t ret = 0;
    switch (orig)
    {
    case 0:           /*相对文件开始位置偏移*/
        if (offset < 0)
        {
            ret = - EINVAL;
            break;
        }
        if ((unsigned int)offset > MEMCHAR_SIZE)
        {
            ret = - EINVAL;
            break;
        }
        filp->f_pos = (unsigned int)offset;
        ret = filp->f_pos;
        break;
    case 1:           /*相对文件当前位置偏移*/
        if ((filp->f_pos + offset) > MEMCHAR_SIZE)
        {
            ret = - EINVAL;
            break;
        }
        if ((filp->f_pos + offset) < 0)
        {
            ret = - EINVAL;
            break;
        }
        filp->f_pos += offset;
        ret = filp->f_pos;
        break;
    default:
        ret = - EINVAL;
        break;
    }
    return ret;
}
/*------------------------------------------------------------------------------  文件操作函数列表结构体*/
static const struct file_operations memchar_fops =
{
    .owner = THIS_MODULE,
    .llseek = memchar_llseek,
    .read = memchar_read,
    .write = memchar_write,
    .unlocked_ioctl = memchar_ioctl,
    .open = memchar_open,
    .release = memchar_release,
};
/****************************************************        初始化并注册 cdev*/
static void memchar_setup_cdev(struct memchar_dev *dev, int index)
{
    int err, devno = MKDEV(memchar_major, index);
    cdev_init(&dev->cdev, &memchar_fops);
    dev->cdev.owner = THIS_MODULE;
    dev->cdev.ops = &memchar_fops;
    err = cdev_add(&dev->cdev, devno, 1);
    if (err)
        printk(KERN_NOTICE "Error %d adding LED%d", err, index);
}
/*------------------------------------------------------------------------------    设备驱动模块加载函数*/
int memchar_init(void)
{
    int result;
    dev_t devno = MKDEV(memchar_major, 0);
    /* 申请设备号*/
    if (memchar_major)
        result = register_chrdev_region(devno, 1, "memchar");
    else /* 动态申请设备号 */
    {
        result = alloc_chrdev_region(&devno, 0, 1, "memchar");
        memchar_major = MAJOR(devno);
    }
    if (result < 0)
        return result;
    /* 动态申请设备结构体的内存*/
    memchar_devp = kmalloc(sizeof(struct memchar_dev), GFP_KERNEL);
    if (!memchar_devp)          /*申请失败*/
    {
        result = - ENOMEM;
        goto fail_malloc;
    }
    memset(memchar_devp, 0, sizeof(struct memchar_dev));
    memchar_setup_cdev(memchar_devp, 0);
    return 0;
fail_malloc:
    unregister_chrdev_region(devno, 1);
    return result;
}
/*------------------------------------------------------------------------------       模块卸载函数*/
void memchar_exit(void)
{
    cdev_del(&memchar_devp->cdev);      /*注销 cdev*/
    kfree(memchar_devp);         /*释放设备结构体内存*/
    unregister_chrdev_region(MKDEV(memchar_major, 0), 1);  /*释放设备号*/
}
/*------------------------------------------------------------------------------        */
MODULE_AUTHOR("SZU HPC 2019");
MODULE_LICENSE("Dual BSD/GPL");
module_param(memchar_major, int, S_IRUGO);
module_init(memchar_init);
module_exit(memchar_exit);
