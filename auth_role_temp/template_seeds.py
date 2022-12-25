
TEMPLATE = """
{% set id = 1  %}
{%- for  item in element.lista  -%}
   {% set outer_loop = loop  %}
{%- for  crud_name in element.names  -%}
- model: {{ item }}s.models.{{ item.capitalize() }}Model
  id: 1 
  fields:
    title: {{ crud_name }}{{ item }}
    label: {{ crud_name }}{{ item }}
{{'\n'}}
{{'\n'}}
{%- endfor -%}

{{'\n'}}
{{'\n'}}
{%- endfor -%}
{{'\n'}}


"""