<script setup lang="ts">
import { onClickOutside } from '@vueuse/core'

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
    class="group relative h-full flex flex-col cursor-pointer border border-border rounded-sm p-3 transition-border-color hover:border-accent-foreground"
  >
    <header class="space-y-1">
      <div class="flex items-center justify-between">
        <p class="font-medium">
          {{ project.name }}
        </p>
        <BaseButton ref="moreBtn" variant="ghost" icon-only @click.stop="isMoreMenuOpen = true">
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
                <BaseButton variant="ghost" class="w-full gap-x-2 !justify-start" @click="emits('edit', project.id)">
                  <span class="i-carbon-edit" />
                  {{ t('button.edit') }}
                </BaseButton>
              </li>
              <li class="px-1">
                <BaseButton variant="ghost" class="w-full gap-x-2 !justify-start" @click="emits('delete', project.id)">
                  <span class="i-carbon-trash-can" />
                  {{ t('button.delete') }}
                </BaseButton>
              </li>
            </ul>
          </div>
        </Transition>
      </div>
      <p class="text-balance text-muted-foreground">
        {{ project.description }}
      </p>
    </header>

    <div class="my-5">
      <div aria-valuemax="100" aria-valuemin="0" role="progressbar" data-state="indeterminate" data-max="100" class="relative h-4 w-full overflow-hidden rounded-full bg-secondary">
        <div data-state="indeterminate" data-max="100" class="h-full w-full bg-primary transition-all" :style="{ transform: `translateX(${(project.foundCount * 100 / project.expectedCount) - 100}%)` }" />
      </div>
    </div>

    <div class="mt-auto text-sm italic text-muted-foreground space-x-1">
      <span>
        {{ t('dashboard.project.create_at') }}
      </span>

      <span>
        {{ project.createAt }}
      </span>
    </div>
  </div>
</template>
