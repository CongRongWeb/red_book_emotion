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
        legend: {
          top: '5%',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        series: [
          {
            name: 'Access From',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 40,
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: [
              { value: chartData[0], name: '消极' },
              { value: chartData[1], name: '中性' },
              { value: chartData[2], name: '积极' },
            ]
          }
        ]
      })
    }
  }
}
</script>
