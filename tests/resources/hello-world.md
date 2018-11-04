---
layout: notebook
title: Hello World!
permalink: /hello/world/
---

# Hello World!

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, HTML
```

```python
print('Hello World!')
```

    Hello World!

```python
df = pd.DataFrame({'a': ['one', 'two'], 'b': [1, 2]})
display(HTML(df.to_html(index=False)))
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>a</th>
      <th>b</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>one</td>
      <td>1</td>
    </tr>
    <tr>
      <td>two</td>
      <td>2</td>
    </tr>
  </tbody>
</table>

```python
series = pd.Series(np.random.randn(1000))
series.plot.hist(edgecolor='black');
```

![png]({{ site.baseurl }}/assets/images/hello-world/hello-world_4_0.png){: .center-image }

# Goodbye World!
