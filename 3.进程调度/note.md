#### 3-1 /proc/cpuinfo 信息
```bash
cat /proc/cpuinfo
```
![image](./record/pic/3-1.png)
CPU型号为Intel(R) Core(TM) i7-4710MQ CPU @ 2.50GHz,拥有四核心八线程
#### 3-2 top 命令的输出
```bash
top
```
![image](./record/pic/3-2.png)
其中 7.7 us 表示 7.7%的时间用于运行用户空间的代码,相应地有 sy 对应运行内核代码占用 CPU 时间的百分比、ni 表示低优先级用户态代码占用 CPU时间的百分比、id 表示空闲(运行 idle 任务进程)CPU 时间的百分比、wa 表示 IO 等待占用CPU 时间的百分比、hi 表示硬件中断(Hardware IRQ)占用 CPU 时间的百分比、si 表示软中断(Software Interrupts)占用 CPU 时间的百分比以及和虚拟化有关的 st(steal time)占用 CPU时间的百分比。
#### 3-3 top 命令的输出(展开 CPU 利用率)
![image](./record/pic/3-3.png)
#### 3-4&3-5 全系统的调度统计
```bash
cat /proc/sched_debug
cat /proc/schedstat
```
![image](./record/pic/3-4.png)
![image](./record/pic/3-5.png)
#### 3-6 ps –aux 查看进程状态
```bash
ps -aux
```
![image](./record/pic/3-6.png)
* R:TASK_RUNNING  可执行状态,包括就绪和正在 CPU 上执行
* S:TASK_INTERRUPTIBLE   可中断的睡眠状态,也是操作系统课程中所谓的阻塞状态
* D:TASK_UNINTERRUPTIBLE 不可中断的睡眠状态
* T:TASK_STOPPED 或 TASK_TRACED 暂停状态或跟踪状态
* Z:TASK_DEAD(-EXIT_ZOMBIE) 退出状态,且成为僵尸进程
* X:TASK_DEAD(-EXIT_DEAD)  退出状态,且进程即将被销毁
#### 3-7&3-8 就绪与阻塞
3-7 HelloWorld-loop-getchar 的运行输出
![image](./record/pic/3-7.png)<br>
3-8 用 ps 观察 HelloWorld-loop-getchar 进程调度状态变化
```bash
ps aux|grep HelloWorld-loop-getchar
```
![image](./record/pic/3-8.png)

#### 3-9&3-10 进程的调度统计
```bash
cat /proc/15366/status
```
![image](./record/pic/3-9.png)
进程主动切换的次数8,进程主动切换的次数213<br>

```bash
cat /proc/15363/stat
```
![image](./record/pic/3-10.png)

#### 3-11&3-12&3-13&3-14普通进程的 CFS 调度
* nice 命令可以用-xx 给出调整的数值(降低优先级 xx),也可以用“-n xx”方式直接设定 NICE 值(-
20~19)
* taskset -c 0　在命令前加上这条语句可以绑定进程运行在制定CPU<br>
3-11 执行 Run-NICE.sh 脚本并用 ps –a 查看
![image](./record/pic/3-11.png)<br>

3-12 用 top 观察优先权不同的两个进程
![image](./record/pic/3-12.png)
16460 号进程占用了 CPU 的 90.4%的时间,16461 号进程仅占用了 CPU 的 9.6%的时间。<br>

3-13 /proc/PID/sched
![image](./record/pic/3-13_1.png)
![image](./record/pic/3-13_2.png)<br>
3-14 /proc/PID/schedstat
![image](./record/pic/3-14.png)

#### 3-15&3-16创建实时进程
* 以 root 身份运行 RT-process-demo 进程,如果以普通用户运行 RT-process-demo 则会报告不允许创建实时进程。<br>

3-15 用 ps –al 观察 RT-process-demo 的四个观测点
![image](./record/pic/3-15a.png)
![image](./record/pic/3-15b.png)
![image](./record/pic/3-15c.png)
![image](./record/pic/3-15d.png)<br>
3-16 用/proc/PID/sched 观察 RT-process-demo 的四个观测点
![image](./record/pic/3-16a.png)<br>

![image](./record/pic/3-16b.png)<br>

![image](./record/pic/3-16c.png)<br>

![image](./record/pic/3-16d.png)<br>

#### 3-17 创建实时进程
```bash
sudo taskset -c 0 ./RR-FIFO.sh
```
经过多次测试发现实验结果无法在ubuntu18.04 多核处理(非虚拟机)器下复现,故改用centOS7进行实验<br>
top 命令查看高优先级实时进程10047 抢占 CPU
![image](./record/pic/3-17a.png)
![image](./record/pic/3-17b.png)
![image](./record/pic/3-17c.png)

3-17 运行脚本并查看三个实时进程的调度信息
```bash
# cat ./sched-10044; cat ./sched-10045; cat ./sched-10047
RR-FIFO-sched (10044, #threads: 1)
-------------------------------------------------------------------
nr_involuntary_switches                      :                  198
se.load.weight                               :                 1024
policy                                       :                    2
prio                                         :                    9
-------------------------------------------------------------------
nr_involuntary_switches                      :                  199
se.load.weight                               :                 1024
policy                                       :                    2
prio                                         :                    9
-------------------------------------------------------------------
nr_involuntary_switches                      :                   25
se.load.weight                               :                 1024
policy                                       :                    1
prio                                         :                    4
```
#### 3-20  ~ 3-26  CFS 进程的负载均衡
执行 HelloWorld-loop-nice+5/+15 并查看它们的负载权重.
![image](./record/pic/3-18.png)
可以发现负载权重相差了3*3=9倍

3-20 显示进程所在处理器编号的 top 输出
top命令后按 f 进入管理界面根据提示操作打开Last  Used Cpu
![image](./record/pic/3-20.png)

3-21 空闲系统上的即时负载情况
![image](./record/pic/3-21.png)

3-22 用 top 查看四个 NICE=-5 的进程所在 CPU
![image](./record/pic/3-22.png)
可以发现４个进程被分配在４个不同的CPU核心上运行

3-23 察看运行-5/0/+5/+10 四个进程后各处理器负载
![image](./record/pic/3-23.png)

3-24 从/proc/PID/sched 中查看进程的迁移次数
处理的进程数小于等于处理器核心数，基本不会进行调度
![image](./record/pic/3-24.png)

3-25 用 top 查看五个进程的处理器编号
在这个情况下处理的进程数大于处理器核心数，故会不断进行调度
![image](./record/pic/3-25a.png)
![image](./record/pic/3-25b.png)
![image](./record/pic/3-25c.png)

3-26 用/proc/PID/sched 查看进程迁移次数
![image](./record/pic/3-26.png)

