---
layout:     post
title:      "LossyCompress"
date:       2019-4-1 00:00:00
author:     "Borelset"
tags:
    - Algorithm
---

# 浮点数的有损压缩
前一段时间一直在研究有关浮点数有损压缩的一些算法，主要是关于SZ的算法。

----------------------------

### 简介
SZ Compressor是阿贡国家实验室开启的一个项目，主要用来处理科学计算中产生的海量浮点数数据。阿贡国家实验室数千台超级计算机每16秒产生的数据大约有130TB，一方面为了节省存储资源，另一方面也是为了节省写入数据的时间开销，所以对数据的压缩显得十分必要。但是传统的无损压缩技术面对浮点数的效果十分的有限，所以需要引入有损压缩技术。于是这个项目被开启了，经过项目的演进，发表了一系列论文，到了现在成为了压缩率最高的有损压缩算法。
有损压缩技术允许数据经过压缩和解压的过程后，会产生一定的误差。一般有两种常用的误差模式，分别是绝对误差和相对误差。绝对误差顾名思义就是对于任意一个浮点数，都允许一个固定值的误差范围；而相对误差，则是对于任意一个浮点数，都允许一个固定比例的误差范围。根据根据他们的研究，如果需要使用相对误差模式，那么可以对待压缩的数据进行一个对数变换，这样就将相对误差的有损压缩问题变为了绝对误差的有损压缩问题。这样实际上这两种模式都可以被归纳为一类问题，用一种方式来解决。在实际使用中，相对误差的应用更为广泛；而绝对误差一般只用在压缩坐标等信息上。
对于无损压缩而言，因为有信息论的相关理论，可以根据信息熵来推导压缩极限。与无损压缩不同的是，有损压缩很难得到一个理论上压缩的极限值。因为对于无损压缩而言，被压缩的数据是确定的，我们可以针对被压缩的数据来估算；然而对于有损压缩而言，被压缩的数据实际上是不确定的。根据对问题不同的抽象方式，我们会得到完全不同的待数据，因此也难以对于有损压缩的极限作出估计。这是有损压缩算法的困难之处，很难知道在压缩率方面是否还会有更有的方法。

--------------------------


### SZ的解决思路
有损压缩算法的核心是如何使用允许的误差来将需要保存的数据减少。SZ的思路是借助量化的方法，将一个浮点数的有损压缩问题变换为一个整数的无损压缩问题，然后再借助无损压缩的相关手段来进行压缩。

对于应用更为广泛的相对误差模式，SZ算法的整体流程大约分为四个部分。
**第一个部分是对数变换**
对于相对误差而言（假设相对误差比例是e），任意一个数值f,其允许的误差范围是
<p align="center">((1-e)f,(1+e)f)</p>
那么如果f经过了对数变换，那么可以知道log(f)允许的误差范围是
<p align="center">(log[(1-e)f], log[(1+e)f])</p>
也就是
<p align="center">(log(1-e)+log(f), log(1+e)+log(f))</p>
可以发现这个范围实际上是固定大小的。所以如果将所有数据都进行log变换，那么相对误差问题就可以转换为绝对误差问题。
所以这个步骤要将所有需要压缩的数据全部进行对数变换。由于对数只能处理正数，所以负数也都会被转化为正数，然后另外使用一个数组来记录每个数据的正负。另外0取对数之后会得到负无穷，所以这里也会有一些特殊的处理方法。遇到等于0的数据之后，并不会对它进行处理而是跳过，等到其他的数据都被处理完之后，统计出其他的数据经过变换之后最为接近0的值，然后计算出一个比这个最接近0的数更为接近0的值来当作一个特殊值，指定为0对应的对数，并将这个特殊值保存在压缩文件中。这样，所有的数据都经过了对数变换，之后可以按照绝对误差的方式来进行压缩。这个步骤大约占整体耗时的1/3。
**第二个部分是逐点处理**
逐点处理的过程中借鉴了差量压缩的思想，发展出了量化的方法。核心做法就是，对于某个数据fn的压缩，根据其之前的数据来获得一个fn'的预测值，然后查看实际值fn和预测值fn'的差值与绝对误差数值p的比例M，也就是
<p align="center">M=(fn-fn')/2p</p>
然后对M取整获得M'，M'就是fn对应的量化值。这种方法的主要原理是将除法取整的误差范围跟绝对误差的数值相匹配，让允许的绝对误差变为除法的取整误差，通过这种方法将浮点数数组变换为了整数数组，减少了需要保存的信息量。这个步骤大约占整体耗时的1/3。
**第三个部分是huffman编码**
这一部分就是对上一步得到的整数数组进行huffman编码，进一步减少占用的空间。第四部分使用其他的无损压缩算法中实际上也包含了huffman编码，但是那是自己字节级别的编码。量化值所组成的数组是整形数据，每个数字占4个字节，这里做的事情就是按照整型数值来进行huffman编码，以得到正好的压缩效果。这个步骤大约占整体耗时的1/3。
**第四个部分是使用其他的无损压缩方法**
这一部分是将前面所有需要保存的数据整合起来，一起进行一次无损的压缩。一般使用gzip或者zStandard等压缩算法来进行。

------------------------------

### 我们的优化
我们在相对误差的压缩流程上做了一个优化。我们看到在逐点处理的阶段上实际每个数据点都是做一个减法和一个除法，于是考虑省略掉第一个部分的对数变换，将其融入到逐点处理中，以节省对数处理的耗时。节省掉对数变换占总体1/3的耗时相当于将速度提升了50%，已经是一个比较大的提升了。
将对数变换带来的影响一起考虑进逐点处理的公式中，第二个部分逐点处理的方法如下
<p align="center">M=(log(fn)-log(fn'))/2log(1+e)</p>
观察这个式子，我们可以把它变为
<p align="center">fn/fn'=(1+e)^(2M-1+2d)</p>
其中0 < d < 1，等式的右边可以看到实际上和数据本身没有任何的关系，那么我们其实可以对右边的式子进行建表，然后每次只要计算出fn/fn'这样一个除法，然后再进行查表即可。
但是随之而来的问题是fn/fn'的结果是一个浮点数，如何对浮点数这样的结果进行建表也是一个挑战。这里我们为了应对这个挑战设计了被命名为Model A的初级建表方式和在此基础上演进出的Model B这样较为完善的建表方式。大体上原理如下图。
具体的实现细节比较复杂，这里就不介绍了。需要详细了解可以查看下方列出的相关文献。

------------------------------

### 相关文献
[1] Sheng Di, Franck Cappello, "Fast Error-bounded Lossy HPC Data Compression with SZ," to appear in International Parallel and Distributed Processing Symposium, 2016.  
[2] Sheng Di, Dingwen Tao, Xin Liang, and Franck Cappello, "Efficient Lossy Compression for Scientific Data based on Pointwise Relative Error Bound", in IEEE Transactions on Parallel and Distributed Systems (IEEE TPDS), 2018.  
[3] Xin Liang, Sheng Di, Dingwen Tao, Zizhong Chen, and Franck Cappello, "Efficient Transformation Scheme for Lossy Data Compression with Point-wise Relative Error Bound", in IEEE CLUSTER 2018.  
[4] Xin Liang, Sheng Di, Dingwen Tao, Zizhong Chen, Franck Cappello, "Error-Controlled Lossy Compression Optimized for High Compression Ratios of Scientific Datasets", in IEEE Bigdata, 2018.  
[5] Xiangyu Zou, Tao Lu, Wen Xia, Xuan Wang, Weizhe Zhang, Sheng Di, Dingwen Tao, Franck Cappello, "Accelerating Relative-error Bounded Lossy Compression for HPC datasets with Precomputation-Based Mechanisms", in Proceedings of the 35th International Conference on Massive Storage Systems and Technology (MSST '19), 2019.