<script setup lang="ts">
import { LangMap } from '../includes/constants'

const { t } = useI18n()

const { currentLocale } = useLocale()
const localOpts = Object.entries(LangMap).map(([key, value]) => ({ label: value, value: key }))

const { isDark, toggle } = useDarkToggle()

function handleToggleDark() {
  if (!document.startViewTransition)
    toggle()

  document.startViewTransition(() => toggle())
}
</script>

<template>
  <div>
    <h2 class="text-3xl">
      {{ t('settings.general.index') }}
    </h2>

    <BaseSeparator orientation="horizontal" />

    <div class="space-y-6">
      <div class="flex items-center justify-between">
        <div class="space-y-1">
          <h3>{{ t('settings.general.language') }}</h3>
          <p class="text-sm text-muted-foreground">
            {{ t('settings.general.hint.language') }}
          </p>
        </div>

        <BaseSelect
          v-model="currentLocale"
          :options="localOpts"
          class="w-200px"
        />
      </div>

      <div class="flex items-center justify-between">
        <div class="space-y-1">
          <h3>{{ t('settings.general.darkmode') }}</h3>
          <p class="text-sm text-muted-foreground">
            {{ t('settings.general.hint.darkmode') }}
          </p>
        </div>

        <BaseSwitch v-model="isDark" :on-switch="handleToggleDark" />
      </div>
    </div>
  </div>
</template>

<style>
::view-transition-group(root) {
  animation-duration: 1s;
}
::view-transition-new(root),
::view-transition-old(root) {
  mix-blend-mode: normal;
}

::view-transition-new(root) {
  animation-name: reveal-light;
}

::view-transition-old(root),
.dark::view-transition-old(root) {
  animation: none;
}
.dark::view-transition-new(root) {
  animation-name: reveal-dark;
}

@keyframes reveal-dark {
  from {
    clip-path: polygon(-30% 0, -30% 0, -15% 100%, -10% 115%);
  }
  to {
    clip-path: polygon(-30% 0, 130% 0, 115% 100%, -10% 115%);
  }
}

@keyframes reveal-light {
  from {
    clip-path: polygon(130% 0, 130% 0, 115% 100%, 110% 115%);
  }
  to {
    clip-path: polygon(130% 0, -30% 0, -15% 100%, 110% 115%);
  }
}
</style>
