<template>
    <div class="q-ma-sm">
        teams: (loader instance), list top down from team to story of story_owner of user_id x

        <pre>{{ teams }}</pre>
        <div class="row">
            <div class="col-4">
                user id: <q-select outlined dense :options="[1, 2, 3, 4, 5, 6, 7]" v-model="userId"
                    @update:model-value="val => pick(val)"></q-select>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { Sample7Service, Sample7TeamDetail } from 'src/client'
import { onMounted, ref } from 'vue';

const teams = ref<Sample7TeamDetail[]>([])
const userId = ref(1)

onMounted(async () => {
    teams.value = await Sample7Service.getUserStat(userId.value)
})

const pick = async (id: number) => {
    teams.value = await Sample7Service.getUserStat(id)
}

</script>

<style scoped></style>