from django.http import HttpResponse
from .models import TiBenchResult


def put_result(request):
    """
    POST body demo:
    {
        "method": "xxx::yyy",
        "args": "{\ factory:\ RocksEngine,\ get_count:\ 1000,\ ...}",
        "min": 1,
        "max": 2,
        "avg": 1.5,
        "ts": "20181201:121856"
    }
    """
    if request.method != "POST":
        return HttpResponse(status=400, content="post is needed")
    return HttpResponse("ok.")
