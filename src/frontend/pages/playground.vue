<script setup lang="ts">
const { toast } = useToastStore()
const a = ref(1)

function foo() {
  toast({
    title: 'asf',
    content: 'Friday, February 10, 2023 at 5:57 PM',
    variant: 'destructive',
    duration: 10_000,
  })
  a.value++
}
</script>

<template>
  <ContentLayout header="Playground">
    <BaseButton @click="foo">
      Test
    </BaseButton>
  </ContentLayout>
</template>
