[toc]
## Question1
设计一个DFA，使其接受2进制字符串w，并且所有w的逆都能被5整除。比如，该DFA接受二进制串11110，因为其逆为01111，代表十进制的15，所以可以被5整除。详述该DFA的设计。
### 1.1 思路
首先设计一个接受的二进制串能被5整除的的DFA，然后将整个DFA的状态反转使其接受的为符合条件的二进制的逆。
### 1.2 设计一个接受的二进制串能被5整除的DFA
* 将已扫描到的字符的余数作为当前状态，一共有5种情况，即5个状态：Q0:余数为0；Q1余数为1......根据规律列出状态转移表如下：<br>
<div align="center">    
<img src="./imgs/Q1状态转移图.jpg " alt="image" style="zoom:33%;" />
</div>
* 根据状态转移表绘制状态转移图：<br>
<div align="center">    
<img src="./imgs/Q1_5.jpg " alt="image" style="zoom:50%;" />
</div>
### 1.3 反转状态转移图
* 将1.2中的DFA的状态反转(将箭头反向并将起始状态与接受状态对调)并根据q0的转移函数添加起始状态qs以防止出现未输入任何字符就接受的情况：<br>
<div align="center">    
<img src="./imgs/Q1_5逆.jpg " alt="image" style="zoom:50%;" />
</div>

## Question2
使用归纳证明法证明对于任意的NFA M=(Q,Σ,δ,q0 ,F)，一定存在CFG G=(Q,Σ,P,S)，使得L(G)=L(M)。
### 2.1 思路
等价转化法：已知NFA与RE等价，故问题转化为对任意的正则表达式R，都可以用CFG G=(Q,Σ,P,S)来表示。即要证明L(R)=L(G)。<br>
### 2.2 文法设计
RE由运算符，字符集，以及'()'组成，故根据运算优先级可以得到文法G：<br>
```shell
S -> A                                  
A -> B|A"|"B                           # "|" 加（或）             
B -> C|BC                              # "" 乘（直接连接）,幂运算可由乘实现
C -> D|D"*"|D"+"|CD"*"|CD"+"           # "*"闭包  "+"正闭包
D -> E|F                                
E -> "a","b","c","d","e","f","g"...... #终结符
F -> "("A")"                           #括号递归
```
### 2.3 归纳法证明
对输入的正则表达式R的运算符数量进行归纳法证明。<br>
* 当n=1时:<br>
R = "a*" | "a|a" | "a+" | "aa" | "(aa)"......<br>
以R =(aa)为例的派生过程：<br>
S=>A=>B=>C=>D=>F=>"("A")"=>"("B")"=>"("BC")"=>"("CC")"=>"("CD")"=>"("DD")"=>"("DE")"=>"("EE")"=>"(""a""a"")"即S=>(aa)<br>
易知其他情况也满足。<br>
* 假设当运算符数量为n时，正则表达式R也是合法的G<br>
当运算符数量为n+1时:<br>
R' = "R*" | "R|a" | "R+" | "Ra" | "(Ra)"...<br>
由于G可以派生出R，故S=>A=>....R可得A=>R<br>
以R' ="R|a"的派生过程为例：<br>
S=>A=>A"|"B=>R"|"B=>R"|"C=>R"|"D=>R"|"E=>R"|""a"即S=>R‘,成立<br>
对其他情况依次进行归纳，均成立<br>
故对任意的正则表达式R，都可以由所定义的 G得到，即对于任意的NFA M=(Q,Σ,δ,q0 ,F)，一定存在CFG G=(Q,Σ,P,S)，使得L(G)=L(M)。

## Question3
正则表达式在信息检索中具有广泛的应用。请设计并编程实现一个基于正则表达式的英文单词检索系统，要求给定任意的正则表达式作为输入，将其转换为等价的自动机，并可以根据该自动机实现从输入文本中检测并输出所有符合正则表达式描述的单词。
例如，当输入文本文件input.txt包含以下英文文本及正则表达式```s{a,…,z}*n```时：
```
Shenzhen University (SZU, Chinese: 深圳大学) is a public university established in 1983 located in Nanshan district, Shenzhen, Guangdong, China. It is accredited by the State Council of the People's Republic of China and is funded by the Shenzhen City Government. The university took its first enrollment the same year at what Deng Xiaoping called "Shenzhen Speed". Deng also was named the "father of Shenzhen University." It is regarded as the fastest developing university in China, and also one of the "Top 100 Universities in China" and one of the top university which is listed in the World Top Ranking Universities.
```
输出：
```
Shenzhen
Shenzhen
Shenzhen
Shenzhen
Shenzhen
```
为所有符合该正则表达式描述得单词，注意，此处单词间以空格分隔，并且对大小写字母不敏感。请在提交报告中给出详细的设计方案、关键代码实现、以及实验测试结果。
### 3.1 思路
### 3.2 正则表达式引擎的设计
#### 3.2.1 整体流程
#### 3.2.2 NFA单个节点的定义
#### 3.2.3 语义分析
#### 3.2.4 NFA的构建

#### 3.2.3 词法分析即校验
### 3.3 实验测试结果
#### 3.3.1 正则表达式引擎基础测试
#### 3.3.2 测试input.txt


## Question4
请设计并编程实现一个简单分类器，要求各类别规则用正则表达式描述，实现输入任意一个字符串，自动给出该串的类别编号。例如定义 类别1：0*1*； 类别2: 1*0*。则给出串0011，程序将输出结果为类别1。

