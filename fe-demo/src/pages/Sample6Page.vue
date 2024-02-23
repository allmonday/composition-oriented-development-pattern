<template>
    <div class="q-ma-sm">
        page info (pick fields and hide fields)
        <pre>{{ page }}</pre>
    </div>
</template>

<script setup lang="ts">
import { Sample6Service, Sample6Root } from 'src/client'
import { onMounted, ref } from 'vue';

const page = ref<Sample6Root>()

onMounted(async () => {
    page.value = await Sample6Service.getPageInfo()
})

</script>

<style scoped></style>