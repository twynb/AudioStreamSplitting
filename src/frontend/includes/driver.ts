import type { DriveStep } from 'driver.js'

export function getDashboardSteps() {
  const { t } = useI18n()
  const DASHBOARD_STEPS: DriveStep[] = [
    {
      element: '#new_project_btn',
      popover: {
        title: t('driver.project.new_project_title'),
        description: t('driver.project.new_project_description'),
      },
    },
    {
      element: '#create_project_name',
      popover: {
        title: t('driver.project.create_name_title'),
        description: t('driver.project.create_name_description'),
      },
    },
    {
      element: '#create_project_description',
      popover: {
        title: t('driver.project.create_description_title'),
        description: t('driver.project.create_description_description'),
      },
    },
    {
      element: '#create_project_files',
      popover: {
        title: t('driver.project.create_project_files_title'),
        description: t('driver.project.create_project_files_description'),
      },
    },
    {
      element: '#create_project_files_list',
      popover: {
        title: t('driver.project.create_project_files_list_title'),
        description: t('driver.project.create_project_files_list_description'),
      },
    },
    {
      element: '#create_project_create_btn',
      popover: {
        title: t('driver.project.new_project_title'),
        description: t('driver.project.new_project_description'),
      },
    },
  ]

  return DASHBOARD_STEPS
}

export function getRecordSteps() {
  const { t } = useI18n()
  const RECORD_STEPS: DriveStep[] = [
    {
      element: '#start_record_btn',
      popover: {
        title: t('driver.record.start_title'),
        description: t('driver.record.start_description'),
      },
    },
    {
      element: '#stop_record_btn',
      popover: {
        title: t('driver.record.stop_title'),
        description: t('driver.record.stop_description'),
      },
    },
    {
      element: '#download_record_btn',
      popover: {
        title: t('driver.record.download_title'),
        description: t('driver.record.download_description'),
      },
    },
    {
      element: '#media_control_btns',
      popover: {
        title: t('driver.record.control_title'),
        description: t('driver.record.control_description'),
      },
    },
    {
      element: '#delete_record_btn',
      popover: {
        title: t('driver.record.delete_title'),
        description: t('driver.record.delete_description'),
      },
    },
    {
      element: '#create_project_form',
      popover: {
        title: t('driver.record.create_project_title'),
        description: t('driver.record.create_project_description'),
      },
    },
  ]
  return RECORD_STEPS
}
