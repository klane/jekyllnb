{% extends 'markdown.tpl' %}

{% block header %}
---
layout: page
title: "{{resources['metadata']['title']}}"
permalink: {{resources['metadata']['permalink']}}
---
{% endblock header %}

{% block input %}
{{ '{% highlight python %}' }}
{{ cell.source  | wrap_text(80) }}
{{ '{% endhighlight %}' }}
{% endblock input %}

{% block data_svg %}
![svg]({{ output | base64image }})
{% endblock data_svg %}

{% block data_png %}
![png]({{ output | base64image }})
{% endblock data_png %}

{% block data_jpg %}
![jpeg]({{ output | base64image }})
{% endblock data_jpg %}

{% block markdowncell scoped %}
{{ cell.source | wrap_text(80) }}
{% endblock markdowncell %}
