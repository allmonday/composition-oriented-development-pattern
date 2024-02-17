<template>
    <div>
        teams: (loader instance)

        <pre>{{ teams }}</pre>
    </div>
</template>

<script setup lang="ts">
import {Sample7Service, Sample7TeamDetail} from 'src/client'
import { onMounted, ref } from 'vue';

const teams = ref<Sample7TeamDetail[]>([])

onMounted(async() => {
    teams.value = await Sample7Service.getUserStat()
})

</script>

<style scoped>

</style>