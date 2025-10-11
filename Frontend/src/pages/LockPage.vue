<!-- src/pages/LockPage.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/assets/security/auth'

const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()
const { login } = useAuth()

async function submit(e?: Event) {
  e?.preventDefault()
  error.value = ''
  loading.value = true
  const ok = await login(password.value)
  loading.value = false
  if (ok) {
    const redirect = sessionStorage.getItem('redirect_after_login') || '/home'
    sessionStorage.removeItem('redirect_after_login')
    // Use Vue Router for navigation
    await router.replace(redirect)
  } else {
    error.value = 'Incorrect password'
  }
}
</script>

<template>
  <div class="min-h-screen grid place-items-center bg-gradient-to-b from-blue-50 to-cyan-50">
    <form class="bg-white w-[92%] max-w-md p-6 rounded-2xl shadow-lg border"
          @submit="submit" aria-describedby="err">
      <h1 class="text-2xl font-bold mb-4">Enter Password</h1>

      <label class="block text-sm font-medium mb-2" for="pwd">Password</label>
      <input id="pwd" type="password" v-model="password" required
             class="w-full rounded-xl border px-4 py-2 focus:ring-2 focus:ring-marine-400 outline-none"/>

      <p v-if="error" id="err" class="mt-2 text-sm text-red-600">{{ error }}</p>

      <button type="submit" :disabled="loading"
              class="mt-4 w-full rounded-xl bg-marine-500 text-white font-semibold py-2 disabled:opacity-60">
        {{ loading ? 'Checking...' : 'Unlock' }}
      </button>
    </form>
  </div>
</template>
