<template>
    <div>
        teams (post hook):
        <pre>{{ teams }} </pre>
    </div>
</template>

<script setup lang="ts">
import {Sample4Service, Sample4TeamDetail} from 'src/client'
import { onMounted, ref } from 'vue';

const teams = ref<Sample4TeamDetail[]>([])

onMounted(async() => {
    teams.value = await Sample4Service.getTeamsWithDetail()
})

</script>

<style scoped>

</style>