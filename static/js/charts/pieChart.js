/*----------------------饼状图-----------------------*/

/**
 *
 * 经常消费的商铺
 *
 */
//环形图
(function(){

var pie1 = echarts.init(document.getElementById("pie1"));

option = {

	title : {
		text: "经常消费的商铺",
		x: 'center'
	},

    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b}: {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        x: 'left',
        data:['田老师红烧肉','麦当劳','肯德基','庆丰包子铺','和合谷']
    },
    series: [
        {
            name:'商铺名称',
            type:'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            label: {
                normal: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    show: true,
                    textStyle: {
                        fontSize: '30',
                        fontWeight: 'bold'
                    }
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data:[
                {value:335, name:'田老师红烧肉'},
                {value:310, name:'麦当劳'},
                {value:234, name:'肯德基'},
                {value:135, name:'庆丰包子铺'},
                {value:1548, name:'和合谷'}
            ]
        }
    ]
};

pie1.setOption(option);
})();

/**
 *
 * 日常生活
 *
 */
//嵌套环形图
(function(){

var pie2 = echarts.init(document.getElementById("pie2"));

option = {

	title : {
		text: "日常生活",
		x: 'center'
	},

    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b}: {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        x: 'left',
        data:['滴滴打车','乘坐地铁','外卖订单','医院看病','垃圾食品','飞机出行','酒店','购物','美食','其他']
    },
    series: [
        {
            name:'次数',
            type:'pie',
            selectedMode: 'single',
            radius: [0, '30%'],

            label: {
                normal: {
                    position: 'inner'
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data:[
                {value:335, name:'美食', selected:true},
                {value:679, name:'垃圾食品'},
                {value:1548, name:'外卖订单'}
            ]
        },
        {
            name:'次数',
            type:'pie',
            radius: ['40%', '55%'],

            data:[
                {value:335, name:'滴滴打车'},
                {value:310, name:'乘坐地铁'},
                {value:234, name:'购物'},
                {value:135, name:'医院看病'},
                {value:1048, name:'其他'},
                {value:251, name:'飞机出行'},
                {value:147, name:'酒店'}
            ]
        }
    ]
};
pie2.setOption(option);
})();

/**
 *
 * TOP5 消费区域
 *
 */
//饼状图
(function(){

var pie3 = echarts.init(document.getElementById("pie3"));

option = {
    title : {
        text: 'TOP5 消费区域',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data: ['北京','上海','深圳','广州','成都']
    },
    series : [
        {
            name: '城市消费',
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:[
                {value:335, name:'北京'},
                {value:310, name:'上海'},
                {value:234, name:'深圳'},
                {value:135, name:'广州'},
                {value:1548, name:'成都'}
            ],
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};

pie3.setOption(option);
})();

/**
 *
 * 钱都花在了这
 *
 */
//南丁格尔玫瑰图
(function(){

var pie4 = echarts.init(document.getElementById("pie4"));

option = {
    title : {
        text: '钱都花在了这',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        x : 'center',
        y : 'bottom',
        data:['rose','rose2','rose3','rose4','rose5','rose6','rose7','rose8']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {
                show: true,
                type: ['pie', 'funnel']
            },
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    series : [
        {
            name:'消费类型',
            type:'pie',
            radius : [20, 110],
            center : ['25%', '50%'],
            roseType : 'radius',
            label: {
                normal: {
                    show: false
                },
                emphasis: {
                    show: true
                }
            },
            lableLine: {
                normal: {
                    show: false
                },
                emphasis: {
                    show: true
                }
            },
            data:[
                {value:10, name:'rose'},
                {value:5, name:'rose2'},
                {value:15, name:'rose3'},
                {value:25, name:'rose4'},
                {value:20, name:'rose5'},
                {value:35, name:'rose6'},
                {value:30, name:'rose7'},
                {value:40, name:'rose8'}
            ]
        },
        {
            name:'消费类型',
            type:'pie',
            radius : [30, 110],
            center : ['75%', '50%'],
            roseType : 'area',
            data:[
                {value:10, name:'rose'},
                {value:5, name:'rose2'},
                {value:15, name:'rose3'},
                {value:25, name:'rose4'},
                {value:20, name:'rose5'},
                {value:35, name:'rose6'},
                {value:30, name:'rose7'},
                {value:40, name:'rose8'}
            ]
        }
    ]
};

pie4.setOption(option);
})();