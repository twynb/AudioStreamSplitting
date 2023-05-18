<script setup lang="ts">
const handleClick = async () => {
  console.log('click')
  const test = await fetch('/foo')
  console.log(await test.json())
  console.log('1')
}
</script>

<template>
  <button @click="handleClick">Clickme</button>
</template>

<style>
button {
  padding-inline: 4rem;
  padding-block: 2rem;
  background-color: black;
  color: white;
}
</style>
