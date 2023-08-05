<script setup lang="ts">
const { toast } = useToastStore()
const a = ref(1)

function foo() {
  toast({
    title: `${a.value}`,
    content: 'Friday, February 10, 2023 at 5:57 PM',
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
