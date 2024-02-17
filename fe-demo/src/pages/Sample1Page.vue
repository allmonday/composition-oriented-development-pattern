<template>
    <div>
        teams (nested data):
        <pre>{{ teams }} </pre>
    </div>
</template>

<script setup lang="ts">
import { Sample1Service, Sample1TeamDetail } from 'src/client'
import { onMounted, ref } from 'vue';

const teams = ref<Sample1TeamDetail[]>([])

onMounted(async () => {
    teams.value = await Sample1Service.getTeamsWithDetail()
})

</script>

<style scoped></style>