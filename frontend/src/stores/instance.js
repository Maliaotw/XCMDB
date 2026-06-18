import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { getInstance } from '@/api/instance'

export const useInstanceStore = defineStore('instance', () => {
  const datastore = ref([])
  const network = ref([])
  const host = ref([])
  const filterform = ref({})
  const tableData = ref([])
  const total = ref(0)
  const tableRef = ref(null)
  const loading = ref(false)

  function setDatasets(data) {
    if (data.datastore) datastore.value = data.datastore
    if (data.network) network.value = data.network
    if (data.host) host.value = data.host
  }

  function setFilterform(f) {
    filterform.value = f
  }

  function setTableRef(ref) {
    tableRef.value = ref
  }

  async function fetchData(page, size, params = {}) {
    loading.value = true
    try {
      const p = page === 1 ? 0 : page - 1
      const offset = p * size
      const response = await getInstance(offset, size, params)
      tableData.value = response.data.results
      total.value = response.data.count
      // Emit updated datasets to filter
      if (response.data.datastore || response.data.network || response.data.host) {
        setDatasets(response.data)
      }
      return response
    } catch (error) {
      console.error('Failed to fetch instance data:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // Watch filterform changes and auto-refresh table data
  watch(
    filterform,
    async () => {
      if (tableRef.value?.getInit) {
        // Access the ref's .value from the table instance refs
        const pageSizeVal = tableRef.value.pageSize?.value || 10
        tableRef.value.getInit(1, pageSizeVal)
      }
    },
    { deep: true }
  )

  return {
    datastore,
    network,
    host,
    filterform,
    tableData,
    total,
    tableRef,
    loading,
    setDatasets,
    setFilterform,
    setTableRef,
    fetchData
  }
})
