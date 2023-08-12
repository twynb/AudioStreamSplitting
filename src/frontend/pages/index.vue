<script setup lang="ts">
import CreateProjectModal from '@components/dialogs/CreateProjectModal.vue'

const { getProjects, deleteProject, createProject } = useDBStore()
const { t } = useI18n()

const { execute } = usePost<Project>({
  url: '/create_project',
  axiosConfig: { headers: { 'Content-Type': 'multipart/form-data' } },
  onSuccess(project) {
    createProject(project)
  },
})

const { open, close } = useModal({
  component: CreateProjectModal,
  attrs: {
    onClose() { close() },
    onOk({ description, files, name }) {
      const formData = new FormData()

      formData.append('name', name)
      formData.append('description', description)
      files.forEach((file) => {
        formData.append('file', file)
      })

      execute(formData)
      close()
    },
  },
})

const router = useRouter()
</script>

<template>
  <ContentLayout :header="t('sidebar.dashboard')">
    <template v-if="getProjects().length">
      <div class="grid grid-cols-2 gap-4">
        <div class="col-span-2 flex-center cursor-pointer border border-border rounded-sm p-3 transition-border-color hover:border-accent-foreground" @click="open">
          <div class="flex flex-col items-center gap-y-1 font-medium">
            {{ t('button.new_project') }}
            <span class="i-carbon-add text-lg" />
          </div>
        </div>

        <DashboardItem
          v-for="project in getProjects()"
          :key="project.id" :project="project"
          @click="router.push(`/project/${project.id}`)"
          @edit="router.push(`/project/${project.id}`)"
          @delete="deleteProject"
        />
      </div>
    </template>

    <template v-else>
      <div class="justify- h-full flex flex-center flex-col -mt-10%">
        <span class="i-carbon-3d-mpr-toggle text-xl" />

        <p class="mt-4 text-lg font-medium">
          {{ t('dashboard.project.no_project') }}
        </p>

        <p class="mt-2 text-center text-muted-foreground">
          Add a new project and let our app automatically detect and <br> split songs in audio files.
        </p>

        <BaseButton class="mt-4 gap-1" @click="open">
          <span class="i-carbon-add" />
          {{ t('button.new') }}
        </BaseButton>
      </div>
    </template>
  </ContentLayout>
</template>
