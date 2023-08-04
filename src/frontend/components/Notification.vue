<script setup lang="ts">
defineProps<{
  noti: AppNotification
}>()

const { removeNotification } = useNotificationStore()
</script>

<template>
  <li
    class="relative max-w-400px overflow-hidden border border-border rounded-md bg-background p-4 pr-8"
  >
    <slot>
      <div class="grid gap-3">
        <div class="font-semibold">
          {{ noti.title }}
        </div>

        <div class="text-sm opacity-90">
          {{ noti.content }}
        </div>
      </div>
    </slot>

    <BaseButton class="absolute right-1 top-1 scale-90" variant="ghost" icon-only @click="removeNotification(noti.id)">
      <span class="i-carbon-close" />
    </BaseButton>
  </li>
</template>
