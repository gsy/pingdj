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
    kwargs['args'] = data.get('args', '{}')
    args = json.loads(kwargs['args'])
    kwargs['key_length'] = int(args.get('key_length', 0))
    kwargs['value_length'] = int(args.get('value_length', 0))

    estimates = json.loads(data.get('estimates', '{}'))
    mean = estimates['Mean']['point_estimate']
    lower_bound = estimates['Mean']['confidence_interval']['lower_bound']
    upper_bound = estimates['Mean']['confidence_interval']['upper_bound']
    kwargs['mean'] = mean
    kwargs['lower_bound'] = lower_bound
    kwargs['upper_bound'] = upper_bound

    try:
        kwargs['ts'] = datetime.datetime.strptime(data['ts'], '%Y-%m-%d %H:%M:%S')
    except:
        return HttpResponse(status=400, content='invalid ts value')

    # debug only:
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop('ts')
    kwargs_copy.pop('method')

    TiBenchResult.objects.create(**kwargs)
    return HttpResponse(json.dumps(kwargs_copy, indent=4))
