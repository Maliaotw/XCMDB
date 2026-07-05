import { defineComponent } from 'vue'
import { Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  ArcElement,
  Title,
  Tooltip,
  Legend
)

export default defineComponent({
  name: 'PieChart',
  extends: Doughnut,
  props: ['chartData'],
  data() {
    return {
      options: {
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: true,
          text: '各類型資產統計'
        }
      }
    }
  },
  mounted() {
    this.renderChart(this.chartData, this.options)
  }
})