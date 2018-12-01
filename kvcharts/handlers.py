import datetime
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import TiBenchResult, TiMethod


def do_raise(request):
    foo = bar
    return HttpResponse("ok")


@csrf_exempt
def put_result(request):
    """
    POST body demo:
    {
        "method": "level::method_name",
        "args": "{\ factory:\ RocksEngine,\ get_count:\ 1000,\ ...}",
        "estimates": "{\"mean\": ..., \"median\": ...}",
        "ts": "2018-12-01 12:18:56"
    }
    """
    if request.method != 'POST':
        return HttpResponse(status=400, content='post is needed')

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400, content='not a valid json')
    if not isinstance(data, dict):
        return HttpResponse(status=400, content='json data should be a dict')
    if 'method' not in data:
        return HttpResponse(status=400, content='key not found: method')

    try:
        level, method_name = data['method'].split('::')
    except:
        return HttpResponse(status=400, content='invalid method name')

    method, _ = TiMethod.objects.get_or_create(name=method_name, level=level)

    kwargs = {'method': method}
    kwargs['args'] = json.loads(data.get('args', '{}'))
    try:
        kwargs['ts'] = datetime.datetime.strptime(data['ts'], '%Y-%m-%d %H:%M:%S')
    except:
        return HttpResponse(status=400, content='invalid ts value')

    # debug only:
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop('ts')
    kwargs_copy.pop('method')
    print(json.dumps(kwargs_copy, indent=4))

    obj = TiBenchResult.objects.create(**kwargs)
    return HttpResponse("ok: {}".format(method.id))
