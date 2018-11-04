{% extends 'markdown.tpl' %}

{%- block header -%}
---
layout: {{ resources['metadata']['layout'] }}
title: {{ resources['metadata']['title'] }}
permalink: {{ resources['metadata']['permalink'] }}
---
{% endblock header %}

{%- block input -%}
{{ '```python' }}
{{ cell.source }}
{{ '```' }}
{% endblock input %}

{% block stream %}
{{ output.text | get_lines(end=-1) | indent }}
{% endblock stream %}

{%- block data_png -%}
![png]({{ output.metadata.filenames['image/png'] | jekyllpath }}){: .center-image }
{%- endblock data_png -%}

{% block markdowncell scoped %}
{{ cell.source }}
{% endblock markdowncell %}
