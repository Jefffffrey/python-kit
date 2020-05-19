def gen(title, x, totals, total_times, y1, y2):
    print((title, x, y1, y2))
    html = """<meta charset="UTF-8">
<script src="https://code.highcharts.com/highcharts.js"></script>
<script src="https://code.highcharts.com/modules/data.js"></script>

<div id="container"></div>

<style>
    .chart {
        min-width: 320px;
        max-width: 800px;
        height: 220px;
        margin: 0 auto;
    }
</style>
<!-- http://doc.jsfiddle.net/use/hacks.html#css-panel-hack -->
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
</style>

<script>
    ['mousemove', 'touchmove', 'touchstart'].forEach(function (eventType) {
        document.getElementById('container').addEventListener(
            eventType,
            function (e) {
                var chart,
                    point,
                    i,
                    event;
                for (i = 0; i < Highcharts.charts.length; i = i + 1) {
                    chart = Highcharts.charts[i];
                    event = chart.pointer.normalize(e);
                    point = chart.series[0].searchPoint(event, true);
                    if (point) {
                        point.highlight(e);
                    }
                }
            }
        );
    });
    Highcharts.Pointer.prototype.reset = function () {
        return undefined;
    };
    Highcharts.Point.prototype.highlight = function (event) {
        event = this.series.chart.pointer.normalize(event);
        this.onMouseOver(); // Show the hover marker
        this.series.chart.tooltip.refresh(this); // Show the tooltip
        this.series.chart.xAxis[0].drawCrosshair(event, this); // Show the crosshair
    };

    function syncExtremes(e) {
        var thisChart = this.chart;

        if (e.trigger !== 'syncExtremes') { // Prevent feedback loop
            Highcharts.each(Highcharts.charts, function (chart) {
                if (chart !== thisChart) {
                    if (chart.xAxis[0].setExtremes) { // It is null while updating
                        chart.xAxis[0].setExtremes(
                            e.min,
                            e.max,
                            undefined,
                            false,
                            {trigger: 'syncExtremes'}
                        );
                    }
                }
            });
        }
    }


    xData = %s;
    datasets = [
            {
            data: %s,
            name: "Query",
            type: "line",
            unit: "",
            valueDecimals: 0,
        },
                {
            data: %s,
            name: "S",
            type: "line",
            unit: "",
            valueDecimals: 0,
        },
        {
            data: %s,
            name: "QPS",
            type: "line",
            unit: "",
            valueDecimals: 0,
        },
        {
            data: %s,
            name: "平均响应时间",
            type: "line",
            unit: "ms",
            valueDecimals: 1,
        },
    ]

    datasets.forEach(function (dataset, i) {

        // Add X values
        dataset.data = Highcharts.map(dataset.data, function (val, j) {
            return [xData[j], val];
        });

        var chartDiv = document.createElement('div');
        chartDiv.className = 'chart';
        document.getElementById('container').appendChild(chartDiv);

        Highcharts.chart(chartDiv, {
            chart: {
                marginLeft: 40, // Keep all charts left aligned
                spacingTop: 20,
                spacingBottom: 20
            },
            title: {
                text: dataset.name,
                align: 'left',
                margin: 0,
                x: 30
            },
            credits: {
                enabled: false
            },
            legend: {
                enabled: false
            },
            xAxis: {
                crosshair: true,
                events: {
                    setExtremes: syncExtremes
                },
                labels: {
                    format: '{value}'
                }
            },
            yAxis: {
                title: {
                    text: null
                }
            },
            tooltip: {
                positioner: function () {
                    return {
                        // right aligned
                        x: this.chart.chartWidth - this.label.width,
                        y: 10 // align to title
                    };
                },
                borderWidth: 0,
                backgroundColor: 'none',
                pointFormat: '{point.y}',
                headerFormat: '',
                shadow: false,
                style: {
                    fontSize: '18px'
                },
                valueDecimals: dataset.valueDecimals
            },
            series: [{
                data: dataset.data,
                name: dataset.name,
                type: dataset.type,
                color: Highcharts.getOptions().colors[i],
                fillOpacity: 0.3,
                tooltip: {
                    valueSuffix: ' ' + dataset.unit
                }
            }]
        });
    })

</script>
    """ % (x, totals, total_times, y1, y2)
    with open(title + '.html', 'w')as fo:
        fo.write(html)
