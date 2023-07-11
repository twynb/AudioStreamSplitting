<script setup lang="ts">
import { onClickOutside } from '@vueuse/core'

const { t } = useI18n()

const foo = ref(false)
const button = ref<HTMLButtonElement>()
onClickOutside(button, () => foo.value = false)
</script>

<template>
  <ContentLayout :header="t('sidebar.dashboard')">
    <div class="grid grid-cols-2 gap-4">
      <div class="col-span-2 flex-center cursor-pointer border border-border rounded-sm p-3">
        <div class="flex flex-col items-center gap-y-1 font-bold">
          {{ t('dashboard.project.new') }}
          <span class="i-carbon-add text-lg" />
        </div>
      </div>

      <div v-for="i in 5" :key="i" class="relative border border-border rounded-sm p-3 space-y-1">
        <header class="space-y-1">
          <div class="flex items-center justify-between">
            <p class="font-bold">
              Some Name
            </p>
            <BaseButton ref="button" variant="ghost" class="aspect-square !p-0" @click="foo = true">
              <span class="i-carbon-overflow-menu-vertical" />
            </BaseButton>

            <Transition
              enter-active-class="transition-all origin-top-right"
              leave-active-class="transition-all origin-top-right"
              enter-from-class="opacity-100 scale-100"
              leave-to-class="opacity-0 scale-90"
            >
              <div v-if="foo" class="absolute right-2 top-2 border border-border rounded-sm bg-background py-1">
                <ul>
                  <li class="px-1">
                    <BaseButton variant="ghost" class="w-full gap-x-2 !justify-start">
                      <span class="i-carbon-edit" />
                      {{ t('dashboard.project.edit') }}
                    </BaseButton>
                  </li>
                  <li class="px-1">
                    <BaseButton variant="ghost" class="w-full gap-x-2 !justify-start">
                      <span class="i-carbon-trash-can" />
                      {{ t('dashboard.project.delete') }}
                    </BaseButton>
                  </li>
                </ul>
              </div>
            </Transition>
          </div>
          <p class="text-muted-foreground">
            Lorem ipsum dolor sit amet consectetur adipisicing elit.
          </p>
        </header>
      </div>
    </div>
  </ContentLayout>
</template>
