import type { PostAudioSplit200SegmentsItem } from '../models/api'

export interface Project {
  id: string
  name: string
  description: string
  path: string
  visited?: boolean
  files: {
    name: string
    fileType: string
    fileName: string
    filePath: string
    peaks?: number[][]
    segments?: PostAudioSplit200SegmentsItem[]
  }[]
  createAt: string
}
