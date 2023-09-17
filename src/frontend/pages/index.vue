<script setup lang="ts">
import CreateProjectModal from '@components/CreateProjectModal.vue'
import { useEventListener } from '@vueuse/core'
import type { Project } from 'models/types'
import { getDashboardSteps } from '../includes/driver'

const { getProjects, deleteProject, createProject } = useDBStore()
const { t } = useI18n()

const { execute } = usePost<Project>({
  url: '/project/create',
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
      files.forEach(file => formData.append('file', file))

      execute(formData)
      close()
    },
  },
})
const { driver, setConfig } = useDriver()
setConfig({
  async onNextClick() {
    if (driver.value.isFirstStep())
      await open()

    driver.value.moveNext()
  },
  async onPrevClick() {
    if (driver.value.getActiveIndex() === 1)
      await close()

    driver.value.movePrevious()
  },
  steps: getDashboardSteps(),
})

useEventListener('keydown', e => e.key === 'Escape' && !driver.value.isActive() && close())

const router = useRouter()

function handleToProject(id: string) {
  router.push(`/project/${id}`)
}
</script>

<template>
  <ContentLayout :header="t('sidebar.dashboard')">
    <template #header>
      <div class="flex items-center gap-x-3">
        <h1 class="text-4xl">
          {{ t('sidebar.dashboard') }}
        </h1>

        <BaseButton icon-only variant="ghost" title="Help" @click="driver.drive()">
          <span class="i-carbon:help-filled text-lg" />
        </BaseButton>
      </div>
    </template>

    <template #default>
      <template v-if="getProjects().length">
        <div class="grid grid-cols-1 gap-4 lg:grid-cols-3 md:grid-cols-2 xl:grid-cols-4">
          <div
            id="new_project_btn"
            tabindex="0"
            class="col-span-1 flex-center cursor-pointer border border-border rounded-sm p-3 transition-border-color lg:col-span-3 md:col-span-2 xl:col-span-4 hover:border-accent-foreground"
            @click="open"
            @keydown.enter.prevent="open"
            @keydown.space.prevent="open"
          >
            <div class="flex flex-col items-center gap-y-1 font-medium">
              {{ t('button.new_project') }}
              <span class="i-carbon-add text-lg" />
            </div>
          </div>

          <DashboardItem
            v-for="project in getProjects()"
            :key="project.id" :project="project"
            @keydown.enter.prevent="handleToProject(project.id)"
            @keydown.space.prevent="handleToProject(project.id)"
            @click="handleToProject(project.id)"
            @edit="handleToProject(project.id)"
            @delete="deleteProject"
          />
        </div>
      </template>

      <template v-else>
        <div class="justify- h-full flex flex-center flex-col -mt-20% lg:-mt-10%">
          <span class="i-carbon-3d-mpr-toggle text-xl" />

          <p class="mt-4 text-lg font-medium">
            {{ t('dashboard.project.no_project') }}
          </p>

          <p class="mt-2 text-center text-muted-foreground">
            {{ t('dashboard.project.add_new_project_prompt') }}
          </p>

          <BaseButton id="new_project_btn" class="mt-4 gap-1" @click="async () => await open() && driver.moveNext()">
            <span class="i-carbon-add" />
            {{ t('button.new') }}
          </BaseButton>
        </div>
      </template>
    </template>
  </ContentLayout>
</template>
