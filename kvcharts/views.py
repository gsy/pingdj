from django.shortcuts import render

from .models import TiBenchResult, TiMethod


def _get_charts(name, level):
    try:
        method = TiMethod.objects.get(name=name, level=level)
    except TiMethod.DoesNotExist:
        return [], [], [], []
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


def _get_group_data(level):
    data = {'group_name': level, 'charts': []}
    query = TiMethod.objects.filter(level=level).values('name').distinct()
    for item in query:
        name = item['name']
        timestaps, lower_bounds, upper_bounds, means = _get_charts(name, level)
        data['charts'].append(
            {
                'chart_name': '{}::{}'.format(level, name),
                'timestamps': timestaps,
                'lower_bounds': lower_bounds,
                'upper_bounds': upper_bounds,
                'means': means,
            }
        )
    return data


def index(request):
    query = TiMethod.objects.values('level').distinct()
    group_name_list = [x['level'] for x in query]

    groups = []
    for group_name in group_name_list:
        group_data = _get_group_data(group_name)
        groups.append(group_data)

    context = {"groups": groups}
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
    return render(request, 'kvcharts/demo.html', context)


def demo_with_children(request):
    data = {
        'timestamps': [1, 2, 3, 4, 5, 6],
        'children': [
            {
                'function_name': 'foo::method1',
                'points': [150, 232, 201, 154, 190, 330, 410],
            },
            {
                'function_name': 'foo::method2',
                'points': [820, 932, 901, 934, 1290, 1330, 1320]
            },
            {
                'function_name': 'foo::method3',
                'points': [320, 332, 301, 334, 390, 330, 320]
            },
        ],
    }
    context = {"data": data}
    return render(request, 'kvcharts/demo_with_children.html', context)
