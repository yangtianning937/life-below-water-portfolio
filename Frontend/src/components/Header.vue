<script setup lang="ts">
const props = defineProps({
  title: String,
  subtitle: String,
})
</script>

<template>
  <header class="bg-gradient-to-r from-blue-600 to-cyan-600 text-white shadow-lg">
    <div class="container mx-auto px-4 py-6">
      <h1 class="text-3xl font-bold flex items-center gap-3">
        <span class="text-4xl">🌊</span>
        {{props.title}}
      </h1>
      <p class="mt-2 text-blue-100">{{props.subtitle}}</p>
    </div>
  </header>
</template>