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

{% block markdowncell scoped %}
{{ cell.source | wrap_text(80) }}
{% endblock markdowncell %}
