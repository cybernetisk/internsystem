from django import template
from django.template.defaultfilters import stringfilter
from cyb_oko.settings import BASE_DIR
import json

register = template.Library()

@register.filter
@stringfilter
def revision(value):
    with open(BASE_DIR + '/siteroot/static_build/rev-manifest.json') as f:
        json_data = json.load(f)

    if value not in json_data:
        raise Exception('Missing static file: ' + value)

    return json_data[value]
