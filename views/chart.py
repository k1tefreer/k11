from django.shortcuts import render
from django.http import JsonResponse


def chart_list(request):
    """ 数据统计页面  """
    return render(request, 'chart_list.html')


def chart_bar(request):
    ''' 构造柱状图的数据 '''
    # 数据可以去数据库中获取
    legend = ['黄琮渊', '黄小帅']

    series_list = [
        {
            'name': '黄琮渊',
            'type': 'bar',
            'data': [5, 20, 36, 10, 10, 20]
        },
        {
            'name': '黄小帅',
            'type': 'bar',
            'data': [45, 10, 56, 10, 20, 10]
        }
    ]

    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def chart_pie(requset):
    """ 构造饼状图 """

    db_data_list = [
        {"value": 1048, "name": 'IT运维部门'},
        {"value": 735, "name": '销售部'},
        {"value": 580, "name": '游戏开发'},
        {"value": 484, "name": '企划部'},
        {"value": 300, "name": '新媒体'}
    ]

    result = {
        "status": True,
        "data": db_data_list,
    }

    return JsonResponse(result)


def chart_line(request):
    """ 构造折线图 """
    legend = ['成都', '重庆分公司', '浙江分公司', '江苏分公司', '上海分公司']

    series_list = [
        {
            'name': '成都',
            'type': 'line',
            'stack': 'Total',
            'data': [120, 132, 101, 134, 90, 230, 210]
        },
        {
            'name': '重庆分公司',
            'type': 'line',
            'stack': 'Total',
            'data': [220, 182, 191, 234, 290, 330, 310]
        },
        {
            'name': '浙江分公司',
            'type': 'line',
            'stack': 'Total',
            'data': [150, 232, 201, 154, 190, 330, 410]
        },
        {
            'name': '江苏分公司',
            'type': 'line',
            'stack': 'Total',
            'data': [320, 332, 301, 334, 390, 330, 320]
        },
        {
            'name': '上海分公司',
            'type': 'line',
            'stack': 'Total',
            'data': [820, 932, 901, 934, 1290, 1330, 1320]
        }
    ]

    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月','7月']

    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }
    return JsonResponse(result)


def highcharts(request):

    """ highcharts示例 """

    return render(request,'highcharts.html')
