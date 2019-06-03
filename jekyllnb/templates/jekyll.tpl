{% extends 'markdown.tpl' %}

{%- block header -%}
---
{%- for key, value in resources['metadata']['jekyll'].items() %}
{{ key }}: {{ value }}
{%- endfor %}
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

{%- block data_html -%}
{{ output.data['text/html'] }}
{%- endblock data_html -%}

{%- block data_png -%}
![png]({{ output.metadata.filenames['image/png'] | jekyllpath }}){: .center-image }
{%- endblock data_png -%}

{% block markdowncell scoped %}
{{ cell.source }}
{% endblock markdowncell %}
