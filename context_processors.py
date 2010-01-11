# http://www.djangosnippets.org/snippets/67/#c52

from django.conf import settings as _settings

def settings(request):
    return {'settings': _settings}