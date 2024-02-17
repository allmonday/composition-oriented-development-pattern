import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: 'sample-1', name: 'sample1', component: () => import('pages/Sample1Page.vue') },
      { path: 'sample-2', name: 'sample2', component: () => import('pages/Sample2Page.vue') },
      { path: 'sample-3', name: 'sample3', component: () => import('pages/Sample3Page.vue') },
      { path: 'sample-4', name: 'sample4', component: () => import('pages/Sample4Page.vue') },
      { path: 'sample-5', name: 'sample5', component: () => import('pages/Sample5Page.vue') },
      { path: 'sample-6', name: 'sample6', component: () => import('pages/Sample6Page.vue') },
      { path: 'sample-7', name: 'sample7', component: () => import('pages/Sample7Page.vue') },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
