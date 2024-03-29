import type { PostAudioSplit200SegmentsItem, PostAudioSplitBodyPresetName } from '../models/api'

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
    presetName: PostAudioSplitBodyPresetName
    peaks?: number[][]
    segments?: ProjectFileSegment[]
  }[]
  createAt: string
}
export type ProjectSegmentItem = PostAudioSplit200SegmentsItem & { peaks?: number[][] }
export type ProjectFileSegment = ProjectSegmentItem & { metaIndex: number }
