<script setup lang="ts">
import { onClickOutside } from '@vueuse/core'
import type { Item } from 'pages/index.vue'

defineProps<{
  item: Item
}>()

const emits = defineEmits<{
  (e: 'edit', id: string): void
  (e: 'delete', id: string): void
}>()

const { t } = useI18n()

const isMoreMenuOpen = ref(false)
const moreBtn = ref<HTMLButtonElement>()
onClickOutside(moreBtn, () => isMoreMenuOpen.value = false)
</script>

<template>
  <div class="relative h-full flex flex-col cursor-pointer border border-border rounded-sm p-3 hover:border-accent-foreground">
    <header class="space-y-1">
      <div class="flex items-center justify-between">
        <p class="font-medium">
          {{ item.name }}
        </p>
        <BaseButton ref="moreBtn" variant="ghost" icon-only @click="isMoreMenuOpen = true">
          <span class="i-carbon-overflow-menu-vertical" />
        </BaseButton>

        <Transition
          enter-active-class="transition-all origin-top-right"
          leave-active-class="transition-all origin-top-right"
          enter-from-class="opacity-0 scale-90"
          leave-to-class="opacity-0 scale-90"
        >
          <div v-if="isMoreMenuOpen" class="absolute right-2 top-2 border border-border rounded-sm bg-background py-1">
            <ul>
              <li class="px-1">
                <BaseButton variant="ghost" class="w-full gap-x-2 !justify-start" @click="emits('edit', item.id)">
                  <span class="i-carbon-edit" />
                  {{ t('global.edit') }}
                </BaseButton>
              </li>
              <li class="px-1">
                <BaseButton variant="ghost" class="w-full gap-x-2 !justify-start" @click="emits('delete', item.id)">
                  <span class="i-carbon-trash-can" />
                  {{ t('global.delete') }}
                </BaseButton>
              </li>
            </ul>
          </div>
        </Transition>
      </div>
      <p class="text-balance text-muted-foreground">
        {{ item.description }}
      </p>
    </header>

    <div class="my-5">
      <div aria-valuemax="100" aria-valuemin="0" role="progressbar" data-state="indeterminate" data-max="100" class="relative h-4 w-full overflow-hidden rounded-full bg-secondary">
        <div data-state="indeterminate" data-max="100" class="h-full w-full bg-primary transition-all" :style="{ transform: `translateX(${(item.foundCount * 100 / item.expectedCount) - 100}%)` }" />
      </div>
    </div>

    <div class="mt-auto text-sm italic text-muted-foreground space-x-1">
      <span>
        {{ t('dashboard.project.create_at') }}
      </span>

      <span>
        {{ item.createAt }}
      </span>
    </div>
  </div>
</template>
