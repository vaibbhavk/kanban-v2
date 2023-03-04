<template>
    <div class="d-flex flex-column align-items-center col border border-secondary p-3">
        <span class="fs-4 d-inline-block text-truncate w-100 mb-4 border p-1">
            {{ s.list_name }}
        </span>

        <ul>
            <li class="mb-3">
                Completed/Total:&nbsp;<strong>{{ s.total_completed }}/{{ s.total }}</strong>
            </li>
            <li>
                Crossed deadline/Pending:&nbsp;<strong>{{ s.d_passed }}/{{ s.total_incomplete }}</strong>
            </li>
        </ul>

        <p v-if="s.date_count.length > 0">
            <BarChart :date_labels="s.date_labels" :date_data="s.date_data" />
        </p>
        <p v-else>No trends to show</p>
    </div>
</template>

<script>

import BarChart from '@/components/BarChart.vue'

export default {
    name: 'SummaryPerList',
    components: {
        BarChart
    },
    props: ['s'],
    data: function () {
        return {

        }
    },
    mounted: function () {

    },
    methods: {

    }

}
</script>
