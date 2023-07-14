export const useDBStore = defineStore('db', () => {
  const items = ref<Item[]>([
    {
      id: '03c482a8-bad0-4e94-b5a2-070580d1fd93',
      name: 'Possibly',
      description: 'porch express enter silk packon walk specific',
      duration: 1024,
      expectedCount: 8,
      foundCount: 6,
      createAt: '08/19/2109',
    },
    {
      id: '60023849-8d18-418e-9eca-1fb66678ccd8',
      name: 'Meet',
      description: 'element perhaps sheep imagine image birth',
      duration: 896,
      expectedCount: 6,
      foundCount: 6,
      createAt: '11/12/2098',
    },
    {
      id: '0fefa8bb-69c4-419b-8a2f-d3ddb8baa59a',
      name: 'Gently',
      description: 'guide bark specific touch mistake element',
      duration: 512,
      expectedCount: 3,
      foundCount: 2,
      createAt: '06/27/2091',
    },
  ])

  function getItemById(itemId: string) {
    return items.value.find(({ id }) => id === itemId)
  }

  return {
    items,
    getItemById,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useDBStore, import.meta.hot))
