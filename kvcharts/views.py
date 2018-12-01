from django.shortcuts import render


def charts(request):
    # x 轴是时间戳
    # y 轴是3条直线
    context = {
        "data": {
            "method_name": "foo",
            "timestamp": [1, 2, 3, 4, 5, 6],
            "min": [10, 5, 8, 3, 7, 4],
            "max": [100, 90, 80, 98, 102, 108],
            "avg": [51, 52, 57, 53, 43, 60],
        }
    }
    return render(request, 'kvcharts/index.html', context)
