{% macro sum_fare_per_class(class_column, fare_column) %}

    {% set classes = ["First", "Second", "Steerage"] %}
    
    {% for class in classes %}
        sum(
            case
                when {{class_column}} = '{{class}}' then {{fare_column}}
            end
        ) as {{class | lower}}_total_fare

        {% if not loop.last %},{% endif %}
    {% endfor %}

{% endmacro %}