<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const text = ref('something')
const name = ref('')
const audioData = ref()

const handleSubmitName = async () => {
  const { data } = await axios.post<string>('/name', { name: text.value })
  name.value = data
}

const handleFileUpload = async (event: Event) => {
  audioData.value = undefined

  const formData = new FormData()
  formData.append('file', (event.target as HTMLInputElement).files[0])

  const { data } = await axios.post('/audio', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  audioData.value = data
}
</script>

<template>
  <div class="bg-slate-500 h-screen flex items-center justify-center">
    <div class="grid grid-cols-2 gap-10">
      <div class="space-y-2 border-2 border-red-500 p-5">
        <form @submit.prevent="handleSubmitName" class="space-y-2">
          <input type="text" v-model="text" class="py-2 pl-3 rounded-lg outline-none" />
          <p class="text-yellow-500">
            {{ name }}
          </p>

          <button type="submit" class="block px-6 py-2 bg-black text-white rounded-lg">Clickme</button>
        </form>
      </div>

      <div class="space-y-2 border-2 border-red-500 p-5 text-yellow-500">
        <input type="file" name="audio" class="py-2" @change="handleFileUpload" />

        <pre v-if="audioData">
          {{ audioData }}
        </pre>
      </div>
    </div>
  </div>
</template>
