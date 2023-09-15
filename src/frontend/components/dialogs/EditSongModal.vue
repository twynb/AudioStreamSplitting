<script setup lang="ts">
import type { Metadata } from 'models/api'

const props = defineProps<{ metadatas: Metadata[]; opt: string }>()

const emits = defineEmits<{ (e: 'change', v: number): void }>()

const opts = props.metadatas.map((m, i) =>
  ({
    value: `${i}`,
    label: Object.values(m).map(v => v).join('_'),
  }))

const opt = ref(props.opt)
watch(opt, () => emits('change', +opt.value))
</script>

<template>
  <BaseSelect v-model="opt" :options="opts">
    <template #label>
      {{ opts[+opt].label }}
    </template>
  </BaseSelect>
</template>
