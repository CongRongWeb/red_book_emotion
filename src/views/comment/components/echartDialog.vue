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
      this.chart.setOption({
        title: {
          x: 'center',
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
          data: ['乐','哀','好','怒','恶','惊','惧']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [chartData[0],chartData[1],chartData[2],chartData[3],chartData[4],chartData[5],chartData[6]],
            type: 'line'
          }
        ]
      })
    }
  }
}
</script>
