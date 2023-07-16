export const useDBStore = defineStore('db', () => {
  const projects = ref<Project[]>([
    {
      id: '03c482a8-bad0-4e94-b5a2-070580d1fd93',
      name: 'Possibly',
      description: 'porch express enter silk packon walk specific',
      files: [
        {
          name: 'foobar',
          format: 'mp3',
          duration: 1024,
          size: 10500000,
          numChannels: 1234,
          numSamples: 986,
        },
      ],
      expectedCount: 1,
      foundCount: 1,
      createAt: '08/19/2109',
    },
  ])

  function getProjectById(itemId: string) {
    return projects.value.find(({ id }) => id === itemId)
  }

  return {
    projects,
    getProjectById,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useDBStore, import.meta.hot))
