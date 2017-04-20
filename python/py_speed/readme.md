### Function
```
def func(N):
    d = 0.0
    for i in range(N):
        d += (i % 3 - 1) * i
    return d
```
#### Anaconda Python 2.7.11, i5 3.2GHz x4, 7.7GB RAM

||Normal|JIT|JIT<br>nopython<br>nogil|Cython|Cython<br>nogil|
|---|---|:---:|:---:|:---:|:---:|
|Sequential<br>1 process|10.168<br>10.402<br>10.612|0.246<br>0.191<br>0.188|0.214<br>0.183<br>0.183|0.187<br>0.186<br>0.186|0.190<br>0.187<br>0.186|
|10 Threads|19.161<br>20.380<br>21.511|0.449<br>0.485<br>0.540|0.090<br>0.095<br>0.094|0.479<br>0.487<br>0.515|0.081<br>0.100<br>0.081|
|4 processes|3.208<br>3.248<br>3.229|0.567<br>0.698<br>0.691|0.536<br>0.670<br>0.654|0.144<br>0.141<br>0.147|0.149<br>0.151<br>0.144|
|4 processes<br>grouped|3.656<br>3.537<br>3.521|0.072<br>0.074<br>0.072|0.071<br>0.079<br>0.076|0.077<br>0.070<br>0.070|0.075<br>0.074<br>0.073|

#### Anaconda Python 3.5.1, i5 3.2GHz x4, 7.7GB RAM

||Normal|JIT|JIT<br>nopython<br>nogil|Cython|Cython<br>nogil|
|---|---|:---:|:---:|:---:|:---:|
|Sequential<br>1 process|17.917<br>18.070<br>18.290|0.377<br>0.187<br>0.187|0.220<br>0.188<br>0.185|0.187<br>0.185<br>0.186|0.188<br>0.185<br>0.186|
|10 Threads|25.489<br>25.529<br>26.120|0.321<br>0.346<br>0.357|0.071<br>0.067<br>0.072|0.312<br>0.524<br>0.556|0.070<br>0.071<br>0.071|
|4 processes|5.035<br>5.084<br>4.975|0.544<br>0.550<br>0.541|0.539<br>0.507<br>0.498|0.254<br>0.221<br>0.230|0.183<br>0.252<br>0.208|
|4 processes<br>grouped|5.858<br>5.686<br>5.717|0.072<br>0.069<br>0.068|0.074<br>0.069<br>0.068|0.075<br>0.070<br>0.068|0.070<br>0.068<br>0.069|
