<template>
    <div class="q-ma-sm row">
        <div class="col">
            tasks (nested data):
            <pre>{{ tasks }} </pre>
        </div>
        <div class="col">
            stories (nested data):
            <pre>{{ stories }} </pre>
        </div>
        <div class="col">
            sprints (nested data):
            <pre>{{ sprints }} </pre>
        </div>
        <div class="col">
            teams (nested data):
            <pre>{{ teams }} </pre>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Sample1Service, Sample1SprintDetail, Sample1StoryDetail, Sample1TaskDetail, Sample1TeamDetail } from 'src/client'
import { onMounted, ref } from 'vue';

const tasks = ref<Sample1TaskDetail[]>([])
const sprints = ref<Sample1SprintDetail[]>([])
const stories = ref<Sample1StoryDetail[]>([])
const teams = ref<Sample1TeamDetail[]>([])

onMounted(async () => {
    tasks.value = await Sample1Service.getTasksWithDetail()
    stories.value = await Sample1Service.getStoriesWithDetail()
    sprints.value = await Sample1Service.getSprintsWithDetail()
    teams.value = await Sample1Service.getTeamsWithDetail()
})

</script>

<style scoped></style>