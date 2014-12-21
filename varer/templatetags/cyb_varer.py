from django import template
from django.template.defaultfilters import stringfilter
import json

register = template.Library()

@register.filter
@stringfilter
def revision(value):
    with open('varer/static_build/rev-manifest.json') as f:
        json_data = json.load(f)

    if value not in json_data:
        raise Exception('Missing static file: ' + value)

    return json_data[value]
