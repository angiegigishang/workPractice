<template>
  <div style="width: 175px; height: 175px;"></div>
</template>

<script>
let echarts = require('echarts/lib/echarts')
// 引入柱状图组件
require('echarts/lib/chart/gauge')
export default {
  props: {
    planNum: {
      type: Number,
      default: 0
    },
    positive: {
      type: Number,
      default: 0
    },
    progressColor: {
      type: Array,
      default: () => []
    }
  },
  data () {
    return {
      myChart: null
    }
  },
  computed: {
    config () {
      return {
        axisLineWidth: 6, // 外圆宽度
        splitLineLength: 8, // 分割线长度
        detailSize: 40, // 详情文字大小
        positiveColor: this.progressColor[0],
        negativeColor: this.progressColor[1]
      }
    }
  },
  mounted () {
    this.initChart()
  },
  methods: {
    initChart () {
      let self = this
      let planNum = self.planNum
      self.myChart = echarts.init(self.$el)
      let options = {
        series: [
          {
            type: 'gauge', // 仪表盘
            radius: '80%', // 仪表盘半径
            center: ['50%', '50%'], // 仪表盘位置
            startAngle: 89.99, // 起始角度
            endAngle: -270, // 结束角度
            min: 0, // 最小值
            max: planNum, // 最大值
            data: [{ value: self.positive }],
            axisLine: { // 外圈圆
              lineStyle: {
                color: [[self.positive / planNum, self.config.positiveColor], [1, self.config.negativeColor]],
                width: self.config.axisLineWidth
              }
            },
            splitLine: { // 分隔线
              length: self.config.splitLineLength,
              lineStyle: {
                width: 1,
                color: '#b0b3b8'
              }
            },
            axisTick: {
              length: 3
            },
            axisLabel: { // 大刻度文字
              show: false
            },
            pointer: { // 指针
              show: false
            },
            detail: { // 仪表盘详情数据相关
              textStyle: {
                color: self.config.positiveColor,
                fontSize: self.config.detailSize,
                fontWeight: 'bolder'
              },
              offsetCenter: [0, '0%'],
              formatter: function (value) {
                let result = value / planNum * 100
                if (result !== 100 && result !== 0) {
                  result = result.toFixed(1)
                }
                return [
                  `{b|${result}%}`
                ].join('\n')
              },
              rich: {
                b: {
                  lineHeight: 70,
                  fontSize: self.config.detailSize,
                  color: self.config.positiveColor
                }
              }
            }
          }
        ]
      }
      this.myChart.setOption(options)
    },
    refresh (data) {
      let self = this
      if (!self.myChart) {
        return
      }
      let options = self.myChart.getOption()
      options.series[0].data[0].value = data
      options.series[0].axisLine.lineStyle = Object.assign({}, {
        color: [[data / self.planNum, self.config.positiveColor], [1, self.config.negativeColor]],
        width: self.config.axisLineWidth
      })
      options.series[0].detail = Object.assign({}, {
        textStyle: {
          color: self.config.positiveColor,
          fontSize: self.config.detailSize,
          fontWeight: 'bolder'
        },
        offsetCenter: [0, '0%'],
        formatter: function (value) {
          let result = value / self.planNum * 100
          if (result !== 100 && result !== 0) {
            result = result.toFixed(1)
          }
          return [
            `{b|${result}%}`
          ].join('\n')
        },
        rich: {
          b: {
            lineHeight: 70,
            fontSize: 40,
            color: self.config.positiveColor
          }
        }
      })
      this.myChart.setOption(options)
    }
  },
  watch: {
    positive (newVal) {
      this.refresh(newVal)
    }
  }
}
</script>

<style></style>
