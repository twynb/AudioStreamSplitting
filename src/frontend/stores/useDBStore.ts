import { useLocalStorage } from '@vueuse/core'

export const useDBStore = defineStore('db', () => {
  const projects = useLocalStorage<Project[]>('db', [], { deep: true })

  function getProjects() {
    return projects.value
  }

  function getProjectById(projectId: string) {
    return projects.value.find(({ id }) => id === projectId)
  }

  function createProject(project: Omit<Project, 'visited'>) {
    projects.value.unshift(project)
  }

  function deleteProject(projectId: string) {
    projects.value = projects.value.filter(({ id }) => id !== projectId)
  }

  function deleteAllProjects() {
    projects.value = []
  }

  return {
    getProjects,
    getProjectById,
    createProject,
    deleteProject,
    deleteAllProjects,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useDBStore, import.meta.hot))
