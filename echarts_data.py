def get_echarts_html(symbol,trade_data, boll_data,signal_data):
    echarts_data = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>ECharts</title>
        <!-- 引入 echarts.js -->
        <script src="https://cdn.bootcss.com/echarts/4.2.0-rc.2/echarts.min.js"></script>
        <style type="text/css">
            html,body,div{
                margin: 0;
                padding: 0;
                height: 100%%;
            }
        </style>
    </head>
    <body>
        <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
        <div id="main"></div>
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
            var data0 = splitData(%s) // 1            
            var data1 = %s // 2


        option = {
            title: {
                text: '%s', // 3
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
                    res +='close' +' : '+data0.values[params[0].dataIndex][1]+'</br>';
                    res +='low' +' : '+data0.values[params[0].dataIndex][2]+'</br>';
                    res +='high' +' : '+data0.values[params[0].dataIndex][3]+'</br>';
                    res +='upper' +' : '+data1[0][params[0].dataIndex]+'</br>';
                    res +='median' +' : '+data1[2][params[0].dataIndex]+'</br>';
                    res +='lower' +' : '+data1[1][params[0].dataIndex]+'</br>';
                    res +='volume' +' : '+data1[3][params[0].dataIndex]+'</br>';
                    res +='ema_short' +' : '+data1[4][params[0].dataIndex]+'</br>';
                    res +='ema_long' +' : '+data1[5][params[0].dataIndex]+'</br>';
                    return res;
                }                
            },
            legend: {
                data: ['k线', 'upper', 'lower', 'median', 'ema_short', 'ema_long']
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
                    name: 'k线',
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
                    markPoint: {    
                        label: {    
                            normal: {   
                                show:true,
                                
                                formatter: function (param) {   
                                    return param != null ? Math.round(param.value) : '';
                                }
                            }
                        },
                        data: %s //4
                        tooltip: {     
                            formatter: function (param) {
                                return param.name + '<br>' + (param.data.coord || '');
                            }
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
                {
                    name: 'ema_short',
                    type: 'line',
                    data: data1[4],
                    smooth: true,
                    lineStyle: {
                        normal: {opacity: 0.5}
                    }
                },    
                {
                    name: 'ema_long',
                    type: 'line',
                    data: data1[5],
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
    """%(trade_data,boll_data,symbol,signal_data)
    return echarts_data


