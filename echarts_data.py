def get_echarts_html(symbol,trade_data, boll_data):
    echarts_data = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>ECharts</title>
        <!-- 引入 echarts.js -->
        <script src="https://cdn.bootcss.com/echarts/4.2.0-rc.2/echarts.min.js"></script>
    </head>
    <body>
        <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
        <div id="main" style="width: 1200px;height:600px;"></div>
        <script type="text/javascript">

            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById('main'));
            var upColor = '#ec0000';
            var upBorderColor = '#8A0000';
            var downColor = '#00da3c';
            var downBorderColor = '#008F28';

            function splitData(rawData) {
                var categoryData = [];
                var values = []
                for (var i = 0; i < rawData.length; i++) {
                    categoryData.push(rawData[i].splice(0, 1)[0]);
                    values.push(rawData[i])
                }
                return {
                    categoryData: categoryData,
                    values: values
                };
            }
            var data0 = splitData(%s)
            var data1 = %s

        function calculateMA(dayCount) {
            var result = [];
            for (var i = 0, len = data0.values.length; i < len; i++) {
                if (i < dayCount) {
                    result.push('-');
                    continue;
                }
                var sum = 0;
                for (var j = 0; j < dayCount; j++) {
                    sum += data0.values[i - j][1];
                }
                result.push(sum / dayCount);
            }
            return result;
        }



        option = {
            title: {
                text: '%s',
                left: 0
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross'
                },
                formatter: function(params) {
                    res = ""                    
                    res +='open' +' : '+data0.values[params[0].dataIndex][0]+'</br>';
                    res +='high' +' : '+data0.values[params[0].dataIndex][1]+'</br>';
                    res +='low' +' : '+data0.values[params[0].dataIndex][2]+'</br>';
                    res +='close' +' : '+data0.values[params[0].dataIndex][3]+'</br>';
                    res +='upper' +' : '+data1[0][params[0].dataIndex]+'</br>';
                    res +='median' +' : '+data1[2][params[0].dataIndex]+'</br>';
                    res +='lower' +' : '+data1[1][params[0].dataIndex]+'</br>';
                    res +='volume' +' : '+data1[3][params[0].dataIndex]+'</br>';
                    return res;
                }                
            },
            legend: {
                data: ['15min', 'upper', 'lower', 'median', 'wd']
            },
            grid: {
                left: '10%%',
                right: '10%%',
                bottom: '15%%'
            },
            xAxis: {
                type: 'category',
                data: data0.categoryData,
                scale: true,
                boundaryGap : false,
                axisLine: {onZero: false},
                splitLine: {show: false},
                splitNumber: 20,
            },
            yAxis: {
                scale: true,
                splitArea: {
                    show: true
                }
            },
            dataZoom: [
                {
                    type: 'inside',
                    start: 50,
                    end: 100
                },
                {
                    show: true,
                    type: 'slider',
                    y: '90%%',
                    start: 50,
                    end: 100
                }
            ],
            series: [
                {
                    name: '15min',
                    type: 'candlestick',
                    data: data0.values,
                    itemStyle: {
                        normal: {
                            color: upColor,
                            color0: downColor,
                            borderColor: upBorderColor,
                            borderColor0: downBorderColor
                        }
                    },
                },
                {
                    name: 'upper',
                    type: 'line',
                    data: data1[0],
                    smooth: true,
                    lineStyle: {
                        normal: {opacity: 0.5}
                    },
                },
                {
                    name: 'lower',
                    type: 'line',
                    data: data1[1],
                    smooth: true,
                    lineStyle: {
                        normal: {opacity: 0.5}
                    }
                },
                {
                    name: 'median',
                    type: 'line',
                    data: data1[2],
                    smooth: true,
                    lineStyle: {
                        normal: {opacity: 0.5}
                    }
                },             
            ]
        };
                // 使用刚指定的配置项和数据显示图表。
                myChart.setOption(option);
                window.onresize = myChart.resize;

            </script>
        </body>
        </html>            
    """%(trade_data,boll_data,symbol)
    return echarts_data


