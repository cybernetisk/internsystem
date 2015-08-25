from rest_framework import renderers

from cal.views import to_ics


class IcsRenderer(renderers.BaseRenderer):
    media_type = 'text/calendar'
    format = 'ics'
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response']

        if response.exception:
            return ''

        return to_ics(data)
