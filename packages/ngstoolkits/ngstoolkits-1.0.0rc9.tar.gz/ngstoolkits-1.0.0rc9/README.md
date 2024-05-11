<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/ngstools.svg?branch=main)](https://cirrus-ci.com/github/<USER>/ngstools)
[![ReadTheDocs](https://readthedocs.org/projects/ngstools/badge/?version=latest)](https://ngstools.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/ngstools/main.svg)](https://coveralls.io/r/<USER>/ngstools)
[![PyPI-Server](https://img.shields.io/pypi/v/ngstools.svg)](https://pypi.org/project/ngstools/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/ngstools.svg)](https://anaconda.org/conda-forge/ngstools)
[![Monthly Downloads](https://pepy.tech/badge/ngstools/month)](https://pepy.tech/project/ngstools)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/ngstools)
-->

Author : Liubo <[Ben-unbelieveable](git@github.com:Ben-unbelieveable/package_ngstoolkits.git)>
# ngstools

> Useful toolkits for NGS analysis

## Main Class
### CPRA
一个最简化的突变对象，通过染色体位置完成对象的初始化，同时支持加载参考基因组和样本比对的Bam文件，来实现更多的个性化操作。
```python
from ngstoolkits import CPRA
# 初始化对象
mutsite=CPRA("chr6",159188398,"C","T")

# 加载bam文件
CPRA.loadBam("test_data/pancancer689__DX2083_sijuan_20S12590085_20B12590085__Cancer.realign.bam")
# 加载参考基因组
CPRA.loadReference("test_data/hg19.fa")

# 基于Bam文件获取突变支持信息
mutsite.get_suppot()
# 得到的突变支持信息
mutsite.support_reads # 支持突变的list，内容是pysam的AlignedSegment对象
mutsite.cover_readsID_list # 支持突变的reads的ID
mutsite.support_readsID_list # 覆盖突变的reads的ID
```

### Seq
序列处理相关的静态函数
#### Seq.reverse_complement
返回所提供序列的反向互补序列
```python
from ngstoolkits import Seq
Seq.reverse_complement("ATGC") # 返回 "GCAT"

```

