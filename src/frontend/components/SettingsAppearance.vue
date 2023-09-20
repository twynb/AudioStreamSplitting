<script setup lang="ts">
const { isDark, toggle } = useDarkToggle()
const { t } = useI18n()

function handleToggleDark() {
  if (!document.startViewTransition)
    toggle()

  document.startViewTransition(() => toggle())
}
</script>

<template>
  <div>
    <h2 class="text-3xl">
      {{ t('settings.appearance.index') }}
    </h2>

    <BaseSeparator orientation="horizontal" />

    <div class="space-y-5">
      <div class="flex items-center justify-between">
        <h3>
          {{ t('settings.appearance.darkmode') }}
        </h3>

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
