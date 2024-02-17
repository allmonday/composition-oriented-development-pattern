<template>
    <div>
        teams (add filter for dataloader):
        <pre>{{ teams }} </pre>
    </div>
</template>

<script setup lang="ts">
import {Sample2Service, Sample2TeamDetailMultipleLevel} from 'src/client'
import { onMounted, ref } from 'vue';

const teams = ref<Sample2TeamDetailMultipleLevel[]>([])

onMounted(async() => {
    teams.value = await Sample2Service.getTeamsWithDetailOfMultipleLevel()
})

</script>

<style scoped>

</style>