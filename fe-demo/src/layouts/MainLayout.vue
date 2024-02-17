<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          Quasar App
        </q-toolbar-title>

        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
          Links
        </q-item-label>

        <q-item clickable tag="a" :to="{name: link.name}" v-for="link in links" :key="link.title">
          <q-item-section>
            <q-item-label>
              <span>{{ link.title }}</span>
            </q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';

type Link = {
  title: string
  name: string
}
const links: Link[] = [
  {
    title: 'Sample 1',
    name: 'sample1',
  },
  {
    title: 'Sample 2',
    name: 'sample2',
  },
  {
    title: 'Sample 3',
    name: 'sample3',
  },
  {
    title: 'Sample 4',
    name: 'sample4',
  },
  {
    title: 'Sample 5',
    name: 'sample5',
  },
  {
    title: 'Sample 6',
    name: 'sample6',
  },
  {
    title: 'Sample 7',
    name: 'sample7',
  },
];

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
</script>
