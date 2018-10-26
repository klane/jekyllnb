{% extends 'markdown.tpl' %}

{% block header %}
---
layout: {{ resources['metadata']['layout'] }}
title: {{ resources['metadata']['title'] }}
permalink: {{ resources['metadata']['permalink'] }}
---
{% endblock header %}

{% block input %}
{{ '{% highlight python %}' }}
{{ cell.source  | wrap_text(80) }}
{{ '{% endhighlight %}' }}
{% endblock input %}

{% block data_png %}
![png]({{ output.metadata.filenames['image/png'] | jekyllpath }}){: .center-image }
{% endblock data_png %}

{% block markdowncell scoped %}
{{ cell.source | wrap_text(80) }}
{% endblock markdowncell %}
