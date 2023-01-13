---
layout: notebook
title: Hello World!
permalink: /hello/world/
---

# Hello World!

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import HTML, display
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

![png]({{ "/assets/images/hello-world/hello-world_4_0.png" | relative_url }}){: .center-image }

# Goodbye World!
