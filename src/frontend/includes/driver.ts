import type { DriveStep } from 'driver.js'

export const DASHBOARD_STEPS: DriveStep[] = [
  {
    element: '#new_project_btn',
    popover: {
      title: 'Create a New Project',
      description: 'Click this button to start creating a new project.',
    },
  },
  {
    element: '#create_project_name',
    popover: {
      title: 'Project Name',
      description: 'Enter a unique name for your project here.',
    },
  },
  {
    element: '#create_project_description',
    popover: {
      title: 'Project Description',
      description: 'Provide a brief description of your project.',
    },
  },
  {
    element: '#create_project_files',
    popover: {
      title: 'Upload Project Files',
      description: 'Click here to upload files related to your project.',
    },
  },
  {
    element: '#create_project_files_list',
    popover: {
      title: 'Uploaded Files',
      description: 'View a list of files you have uploaded for your project.',
    },
  },
  {
    element: '#create_project_create_btn',
    popover: {
      title: 'Create Project',
      description: 'Click this button to create your project with the provided details.',
    },
  },
]

export const RECORD_STEPS: DriveStep[] = [
  {
    element: '#start_record_btn',
    popover: {
      title: 'Start Recording',
      description: 'Click this button to begin recording your media.',
    },
  },
  {
    element: '#stop_record_btn',
    popover: {
      title: 'Stop Recording',
      description: 'Click this button to stop recording your media.',
    },
  },
  {
    element: '#download_record_btn',
    popover: {
      title: 'Download Recorded Media',
      description: 'Click here to download the media you have recorded.',
    },
  },
  {
    element: '#media_control_btns',
    popover: {
      title: 'Media Control Buttons',
      description: 'Use these buttons to control your media playback.',
    },
  },
  {
    element: '#delete_record_btn',
    popover: {
      title: 'Delete Recorded Media',
      description: 'Click this button to delete the recorded media file.',
    },
  },
  {
    element: '#create_project_form',
    popover: {
      title: 'Create Project Form',
      description: 'Fill out this form to create a new project with the provided details.',
    },
  },
]
