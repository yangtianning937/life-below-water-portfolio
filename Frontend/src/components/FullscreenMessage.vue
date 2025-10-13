<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from "vue"

const props = withDefaults(defineProps<{
  modelValue?: boolean
  title?: string
  message?: string
  icon?: string
  confirmText?: string
  cancelText?: string
  persistent?: boolean   // When true, disables clicking outside/ESC to close
}>(), {
  modelValue: true,
  title: "Message",
  message: "",
  icon: "ℹ️",
  confirmText: "",
  cancelText: "Cancel",
  persistent: false
})

const emit = defineEmits<{
  (e: "update:modelValue", v: boolean): void
  (e: "close"): void
  (e: "confirm"): void
}>()

const open = ref(!!props.modelValue)
watch(() => props.modelValue, v => { open.value = !!v })

function close() {
  if (props.persistent) return
  open.value = false
  emit("update:modelValue", false)
  emit("close")
}

function confirm() {
  emit("confirm")
  if (!props.persistent) close()
}

// Keyboard ESC
function onKey(e: KeyboardEvent) { if (e.key === "Escape") close() }
onMounted(() => window.addEventListener("keydown", onKey))
onBeforeUnmount(() => window.removeEventListener("keydown", onKey))

// Prevent background scrolling + focus to panel
const panel = ref<HTMLElement | null>(null)
watch(open, (v) => {
  document.body.classList.toggle("overflow-hidden", v)
  if (v) setTimeout(() => panel.value?.focus(), 0)
})

// Accessibility: auto-generate id
const ids = {
  title: `msg-title-${Math.random().toString(36).slice(2)}`,
  desc: `msg-desc-${Math.random().toString(36).slice(2)}`
}
</script>

<template>
<Transition
    enter-active-class="duration-200 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="duration-150 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="open" class="fixed inset-0 z-[9999] flex items-center justify-center p-6"
         @click.self="close">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

      <!-- Panel -->
      <section
        ref="panel"
        role="dialog" aria-modal="true" :aria-labelledby="ids.title" :aria-describedby="ids.desc"
        class="relative w-full max-w-lg rounded-2xl bg-white shadow-2xl ring-1 ring-black/10  focus:outline-none"
        tabindex="-1"
      >
        <header class="flex items-center gap-3 border-b border-black/5 px-6 py-4">
          <div v-if="icon" class="size-9 rounded-full bg-blue-100 flex items-center justify-center">{{ icon }}</div>
          <h2 :id="ids.title" class="text-lg font-semibold">{{ title }}</h2>
          <button v-if="!persistent"
                  class="ml-auto rounded-xl p-2 hover:bg-black/5 focus:outline-none focus:ring"
                  @click="close" aria-label="Close">✕</button>
        </header>

        <div :id="ids.desc" class="px-6 py-5 text-sm/6 text-black-700">
          <slot>{{ message }}</slot>
        </div>

        <footer class="flex items-center justify-end gap-3 border-t border-black/5 px-6 py-4">
          <button v-if="!persistent"
                  class="rounded-xl px-4 py-2 text-sm hover:bg-black/5 focus:outline-none focus:ring"
                  @click="close">{{ cancelText }}</button>
          <button v-if="confirmText"
                  class="rounded-xl bg-blue-600 px-4 py-2 text-sm text-white hover:bg-blue-700 focus:outline-none focus:ring"
                  @click="confirm">{{ confirmText }}</button>
        </footer>
      </section>
    </div>
  </Transition>
</template>

<style scoped>

</style>