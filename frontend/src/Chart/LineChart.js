import {Line, mixins} from 'vue-chartjs'

export default {
    extends: Line,
    mixins: [mixins.reactiveProp],
    data: () => ({
        props: ['chartData'],
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: true,
                text: '七天內資產'
            }
        }
    }),
    mounted() {
        // this.chartData is created in the mixin.
        // If you want to pass options please create a local options object
        this.renderChart(
            this.chartData,
            this.options
        )
    }
}
