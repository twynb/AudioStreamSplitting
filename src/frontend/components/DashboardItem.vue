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
    tabindex="1"
    class="group relative h-full flex flex-col cursor-pointer border border-border rounded-sm p-3 transition-border-color hover:border-accent-foreground"
  >
    <div>
      <div class="flex items-center justify-between">
        <p class="font-medium">
          {{ project.name }}
        </p>

        <BaseButton
          ref="moreBtn" variant="ghost" icon-only
          @click.stop="isMoreMenuOpen = true"
          @keydown.enter.stop="isMoreMenuOpen = true"
          @keydown.space.stop="isMoreMenuOpen = true"
          @keydown.escape.stop="isMoreMenuOpen = false"
        >
          <span class="i-carbon-overflow-menu-vertical" />
        </BaseButton>

        <Transition
          enter-active-class="transition-all origin-top-right"
          leave-active-class="transition-all origin-top-right"
          enter-from-class="opacity-0 scale-90"
          leave-to-class="opacity-0 scale-90"
        >
          <div v-if="isMoreMenuOpen" tabindex="2" class="absolute right-2 top-2 border border-border rounded-sm bg-background py-1">
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
  </div>
</template>
