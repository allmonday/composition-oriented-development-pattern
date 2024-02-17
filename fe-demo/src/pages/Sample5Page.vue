<template>
    <div>
        page info (context)

        <pre>{{ page }}</pre>
    </div>
</template>

<script setup lang="ts">
import {Sample5Service, Sample5Root} from 'src/client'
import { onMounted, ref } from 'vue';

const page = ref<Sample5Root>()

onMounted(async() => {
    page.value = await Sample5Service.getPageInfo(1)
})

</script>

<style scoped>

</style>