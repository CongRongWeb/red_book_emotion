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
          datas.push(item.date)
          percents.push(item.percent)
      })
      this.chart.setOption({

        title: {
          x: 'center',
          text:"动态情感曲线图",
          textStyle: {
            fontSize: 14,
            fontWeight: 'bolder',
            color: '#333' // 主标题文字颜色
          },
          top:'5%'
        },
        color:['rgb(58,161,255)'],
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: datas
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: percents,
            type: 'line',
            smooth: true
          }
        ]
      })
    }
  }
}
</script>
