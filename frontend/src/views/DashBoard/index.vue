<template>
    <div style="min-height: 600px">
        <el-row type="flex" style="margin-bottom: 20px">
            <el-col :span="6" v-for="(infor, i) in inforCardData" :key="i">
                <el-card shadow="always" style="margin-right: 10px;height: 100px" :body-style="{ padding: '10px'}">
                    <el-row type="flex">
                        <el-col :span="6" align="center">
                            <i :class="infor.icon" style="font-size: 50px;margin: 10px" />
                        </el-col>
                        <el-col :span="18" align="right">
                            <p v-bind:style="{color:infor.color}">
                                {{ infor.title }}
                            </p>
                            <p>
                                {{ infor.count }}
                            </p>
                        </el-col>
                    </el-row>
                </el-card>
            </el-col>
        </el-row>
        <el-row type="flex">
            <el-col :span="16">
                <div class="mt-0">
                    <line-chart :chart-data="datacollection" />
                </div>
            </el-col>
            <el-col :span="6">
                <div class="small" style="margin-left: 20px">
                    <pie-chart :chart-data="pie" />
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script setup>
import LineChart from '../../Chart/LineChart'
import PieChart from '../../Chart/PieChart'
import { onMounted, ref } from 'vue'
import { getDashBoard } from '@/api/dashboard'

const datacollection = ref(null)
const pie = ref(null)
const data = ref({
  count: {
    asset: 12,
  },
})
const inforCardData = ref('')

function fillData() {
  datacollection.value = {
    labels: data.value.asset_data.label,
    datasets: [
      {
        label: '更新',
        backgroundColor: '#74f81d',
        data: data.value.asset_data.latest_data,
        fill: false,
        borderColor: '#74f81d',
      }, {
        label: '創建',
        data: data.value.asset_data.create_data,
        fill: false,
        borderColor: '#f87979',
      }
    ],
  }
}

function pieData() {
  pie.value = {
    hoverBackgroundColor: "red",
    hoverBorderWidth: 10,
    labels: data.value.asset_type.label,
    datasets: [
      {
        label: data.value.asset_type.label,
        data: data.value.asset_type.data,
        backgroundColor: ["#41B883", "#E46651", "#00D8FF"],
      }
    ],
  }
}

function getDash() {
  getDashBoard()
    .then((res) => {
      data.value = res.data
      inforCardData.value = res.data.count
      fillData()
      pieData()
    })
}

onMounted(() => {
  getDash()
})
</script>