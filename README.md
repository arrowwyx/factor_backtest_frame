## 本项目实现了一个简易的本地日频因子测试平台。
数据部分，利用免费开源的akshare获取。~~data/dataAshare文件夹中目前自带2010-2023的A股日频行情数据，用LFS上传到git。~~

由于push大文件太麻烦，用户可自行在/data/data_Ashare/get_data_akshare.ipynb中获取A股日线数据。

因子部分，本项目的特色是因子的简便计算。使用functions.py中的操作函数，一行代码就可以实现绝大多数日频量价因子的计算。

因子分析部分，采用alphalens的框架，特点在于轻量，也便于使用者根据自己的需求自定义封装。
比如下图展示了本项目生成的IC时序变化图，并且可以在标题上展示因子的计算公式，方便之后人工查看筛选。

 ![ic图示例](ic_plots/correlation(rank(open),%20rank(volume),%2010).png)