<template>
  <div :class="className" :style="{height:height,width:width,}" />
</template>

<script>
import * as echarts from 'echarts'
export default {
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '430px'
    },
    chartData: {
      required: true
    }
  },
  data() {
    return {
      chart: null,
      map: {}
    }
  },
  watch: {
    chartData: {
      deep: true,
      handler(val) {
        console.log(val,'asdasd')
        this.setOptions(val)
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  created() {

  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'statisticsxChart')
      this.setOptions(this.chartData)
    },
    setOptions(chartData) {
      const that = this
      let datas = []
      let percents =[]
      chartData.forEach(item=>{
        datas.push(item[0])
        percents.push(item[1])
      })
      this.chart.setOption({

        tooltip: {
          trigger: 'axis'
        },
        title: {
          x: 'center',
          text:"词频折线图",
          textStyle: {
            fontSize: 14,
            fontWeight: 'bolder',
            color: '#333' // 主标题文字颜色
          },
          top:'5%'
        },
        xAxis: [
          {
            type: 'category',
            data: datas,
            axisTick: {
              alignWithLabel: true
            }
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            name: '权重',
            type: 'bar',
            barWidth: '60%',
            data: percents
          }
        ]
      })
    }
  }
}
</script>
