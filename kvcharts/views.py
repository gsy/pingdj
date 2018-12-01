from django.shortcuts import render

from .models import TiBenchResult, TiMethod


def _get_charts(name, level):
    method = TiMethod.objects.get(name='get', level='engine')
    print(method)
    charts = TiBenchResult.objects.filter(
        method=method,
        value_length=64,
    ).order_by('ts')
    timestaps = []
    lower_bounds = []
    upper_bounds = []
    means = []
    for item in charts:
        timestaps.append(item.ts.strftime('%H:%M:%S'))
        lower_bounds.append(item.lower_bound)
        upper_bounds.append(item.upper_bound)
        means.append(item.mean)
    return timestaps, lower_bounds, upper_bounds, means


def index(request):
    timestaps_get, lower_bounds_get, upper_bounds_get, means_get = \
        _get_charts('get', 'engine')
    timestaps_put, lower_bounds_put, upper_bounds_put, means_put = \
        _get_charts('put', 'engine')

    groups = [
        {
            'group_name': 'engine',
            'charts': [
                {
                    'chart_name': 'engine::get',
                    'timestamps': timestaps_get,
                    'lower_bounds': lower_bounds_get,
                    'upper_bounds': upper_bounds_get,
                    'means': means_get,
                },
                {
                    'chart_name': 'engine::put',
                    'timestamps': timestaps_put,
                    'lower_bounds': lower_bounds_put,
                    'upper_bounds': upper_bounds_put,
                    'means': means_put,
                },
            ],
        },
    ]
    context = {"groups": groups}
    print(context)
    return render(request, 'kvcharts/index.html', context)


def demo(request):
    groups = [
        {
            'group_name': 'engine',
            'charts': [
                {
                    'chart_name': 'engine::get',
                    'timestamps': [1, 2, 3, 4, 5, 6],
                    'lower_bounds': [10, 5, 8, 3, 7, 4],
                    'upper_bounds': [100, 90, 80, 98, 102, 108],
                    'means': [51, 52, 57, 53, 43, 60],
                },
                {
                    'chart_name': 'engine::put',
                    'timestamps': [1, 2, 3, 4, 5, 6],
                    'lower_bounds': [20, 15, 18, 13, 17, 14],
                    'upper_bounds': [60, 90, 80, 88, 62, 48],
                    'means': [51, 52, 57, 53, 43, 30],
                },
            ],
        },
    ]
    context = {"groups": groups}
    print(context)
    return render(request, 'kvcharts/demo.html', context)
