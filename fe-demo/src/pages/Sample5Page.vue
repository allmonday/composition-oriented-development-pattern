<template>
    <div class="q-ma-sm">
        <q-btn @click="q(1)" class="q-mr-sm">team 1</q-btn>
        <q-btn @click="q(2)">team 2</q-btn>
        <div>
            page info (context)

            <pre>{{ page }}</pre>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Sample5Service, Sample5Root } from 'src/client'
import { onMounted, ref } from 'vue';

const page = ref<Sample5Root>()

onMounted(async () => {
    page.value = await Sample5Service.getPageInfo(1)
})

const q = async (id: number) => {
    page.value = await Sample5Service.getPageInfo(id)
}

</script>

<style scoped></style>