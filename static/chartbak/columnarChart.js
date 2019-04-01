/*----------------------柱状图-----------------------*/

/**
 *
 * 微信红包
 *
 */

//坐标轴刻度与标签对齐
(function(){

var columnar1 = echarts.init(document.getElementById("columnar1"));

option = {

	title: {
		text: "微信红包",
		x:'left'
	},

    color: ['#3398DB'],
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis : [
        {
            type : 'category',
            data : ['收红包数', '发红包数', '收最大金额', '发最大金额', '转账次数', '转最大金额', '收最大金额'],
            axisTick: {
                alignWithLabel: true
            }
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'红包金额',
            type:'bar',
            barWidth: '60%',
            data:[10, 52, 200, 334, 390, 330, 220]
        }
    ]
};

columnar1.setOption(option);
})();


/**
 *
 * 半年消费分类
 *
 */
//堆叠条形图
(function(){

var columnar2 = echarts.init(document.getElementById("columnar2"));

option = {

	title : {
		text: "半年消费分类",
		x:'left'
	},

    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        data: ['美食', '交通','娱乐','生活','电子产品'],
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis:  {
        type: 'value'
    },
    yAxis: {
        type: 'category',
        data: ['1月','2月','3月','4月','5月','6月','7月']
    },
    series: [
        {
            name: '美食',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [320, 302, 301, 334, 390, 330, 320]
        },
        {
            name: '交通',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [120, 132, 101, 134, 90, 230, 210]
        },
        {
            name: '娱乐',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [220, 182, 191, 234, 290, 330, 310]
        },
        {
            name: '生活',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [150, 212, 201, 154, 190, 330, 410]
        },
        {
            name: '电子产品',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [820, 832, 901, 934, 1290, 1330, 1320]
        }
    ]
};

columnar2.setOption(option);
})();


/**
 *
 * 消费最高一周收支记录
 *
 */
//正负条形图
(function(){

var columnar3 = echarts.init(document.getElementById("columnar3"));

option = {

	title : {
		text: "消费最高一周收支记录",
		x:'left'
	},

    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        data:['支出', '收入']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis : [
        {
            type : 'value'
        }
    ],
    yAxis : [
        {
            type : 'category',
            axisTick : {show: false},
            data : ['周一','周二','周三','周四','周五','周六','周日']
        }
    ],
    series : [
        {
            name:'收入',
            type:'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true
                }
            },
            data:[320, 302, 341, 374, 390, 450, 420]
        },
        {
            name:'支出',
            type:'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'left'
                }
            },
            data:[-120, -132, -101, -134, -190, -230, -210]
        }
    ]
};


columnar3.setOption(option);
})();


/**
 *
 * 全年各月收支记录
 *
 */
//折柱混合
(function(){

var columnar4 = echarts.init(document.getElementById("columnar4"));


option = {

	title : {
		text: "全年各月收支记录",
		x: "left"
	},
	
    tooltip: {
        trigger: 'axis'
    },
    toolbox: {
        feature: {
            saveAsImage: {show: true}
        }
    },
    legend: {
        data:['支出','收入']
    },
    xAxis: [
        {
            type: 'category',
            data: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: '金额',
            min: 0,
            max: 250,
            interval: 1000,
            axisLabel: {
                formatter: '{value} ￥'
            }
        }
    ],
    series: [
        {
            name:'支出',
            type:'bar',
            data:[20, 49, 70, 32, 56, 67, 36, 22, 26, 50, 64, 33]
        },
        {
            name:'收入',
            type:'bar',
            data:[26, 59, 90, 264, 28, 707, 76, 182, 87, 88, 60, 23]
        }
    ]
};




columnar4.setOption(option);
})();
