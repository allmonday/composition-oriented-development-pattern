<template>
    <div class="q-ma-sm">
        teams (read fields of ancestor):
        full_name
        <pre>{{ teams }} </pre>
    </div>
</template>

<script setup lang="ts">
import { Sample3Service, Sample3TeamDetail } from 'src/client'
import { onMounted, ref } from 'vue';

const teams = ref<Sample3TeamDetail[]>([])

onMounted(async () => {
    teams.value = await Sample3Service.getTeamsWithDetail()
})

</script>

<style scoped></style>