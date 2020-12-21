import {mixins, Doughnut} from 'vue-chartjs'

export default {
    extends: Doughnut,
    mixins: [mixins.reactiveProp],
    data: () => ({
        props: ['chartData'],
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: '各類型資產統計'
            }
        }
    }),
    mounted() {
        // this.chartData is created in the mixin.
        // If you want to pass options please create a local options object
        this.renderChart(this.chartData, this.options)
    }
}
