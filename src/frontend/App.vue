<script setup lang="ts">
import { ref } from 'vue'
import { useFetch } from './composables/useFetch'
import TestComp from './components/TestComp.vue'

const handleClick = async () => {
  const { data, onFetchResponse } = useFetch('/foo').json()
  onFetchResponse(() => {
    console.log(data.value)
  })
}

const text = ref('Something')

const json = ref({})
</script>

<template>
  <TestComp />
  <!-- <div class="bg-slate-500 h-screen flex items-center justify-center">
    <div class="space-y-2">
      <div class="space-y-2">
        <input type="text" v-model="text" class="py-2 pl-3 rounded-lg outline-none" />
        <p class="pl-3 text-yellow-500">
          {{ text }}
        </p>
      </div>
      <button @click="handleClick" class="block px-6 py-2 bg-black text-white rounded-lg">Clickme</button>
      <pre>
        {{ json }}
      </pre>
    </div>
  </div> -->
</template>
