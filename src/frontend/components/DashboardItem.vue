<script setup lang="ts">
import { onClickOutside } from '@vueuse/core'
import type { Project } from '../models/types'

defineProps<{
  project: Project
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
  <div
    tabindex="0"
    class="group relative h-full flex flex-col cursor-pointer border border-border rounded-sm p-3 transition-border-color hover:border-accent-foreground"
  >
    <div>
      <div class="flex items-center justify-between">
        <p class="font-medium">
          {{ project.name }}
        </p>

        <BaseMenuButton :length="1">
          <template #button>
            <span class="i-carbon-overflow-menu-vertical" />
          </template>
          <template #content>
            <li class="px-1">
              <BaseButton variant="ghost" class="w-full gap-x-2 !justify-start" @click.prevent.stop="emits('delete', project.id)">
                <span class="i-carbon-trash-can" />
                {{ t('button.delete') }}
              </BaseButton>
            </li>
          </template>
        </BaseMenuButton>
      </div>

      <p class="text-balance text-muted-foreground -mt-2">
        {{ project.description }}
      </p>
    </div>

    <ul class="my-5">
      <li v-for="{ fileName } in project.files" :key="fileName" class="flex text-sm">
        <div class="basis-1/2">
          {{ fileName }}
        </div>
      </li>
    </ul>

    <div class="mt-auto text-sm italic text-muted-foreground space-x-1">
      <span>
        {{ t('dashboard.project.create_at') }}
      </span>

      <span>
        {{ useDateFormat(project.createAt, 'DD/MM/YYYY') }}
      </span>
    </div>

    <BaseBadge v-if="!project.visited" class="absolute -right-1 -top-1 !h-3 !w-3" />
  </div>
</template>
