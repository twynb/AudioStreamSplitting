<script setup lang="ts">
const { t } = useI18n()
const router = useRouter()
</script>

<template>
  <div class="h-full flex-center">
    <div class="flex flex-col items-center">
      <h1 class="text-6xl tracking-widest">
        404
      </h1>

      <p class="text-primary/70">
        Not found page
      </p>

      <BaseButton class="mt-5" @click="router.push('/')">
        {{ t('button.back_to_dashboard') }}
      </BaseButton>
    </div>
  </div>
</template>
