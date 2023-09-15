/**
 * Generated by orval v6.17.0 🍺
 * Do not edit manually.
 * AudioStreamSplitting API
 * OpenAPI spec version: 1.0.0
 */
import axios from 'axios'
import type {
  AxiosRequestConfig,
  AxiosResponse,
} from 'axios'

export interface PostAudioStore200 {
  success?: boolean
}

export interface PostAudioStoreBody {
  filePath?: string
  targetDirectory?: string
  offset?: number
  duration?: number
  metadata?: Metadata
  /** The target file type. Defaults to "mp3" if not provided. */
  fileType?: string
  /** The file name template. Defaults to the one specified in .env if not provided. */
  nameTemplate?: string
}

export interface PostAudioGetSegmentBody {
  filePath?: string
  offset?: number
  duration?: number
}

export interface PostAudioSplit200SegmentsItem {
  offset?: number
  duration?: number
  metadataOptions?: Metadata[]
}

export interface PostAudioSplit200 {
  segments?: PostAudioSplit200SegmentsItem[]
  /** Offsets where the segment afterward had a song mismatch. */
  mismatchOffsets?: number[]
}

export interface PostAudioSplitBody {
  filePath?: string
}

export interface Metadata {
  title?: string
  album?: string
  artist?: string
  year?: string
}

export function getAudioStreamSplittingAPI() {
/**
 * @summary Split the file at the given file location.
 */
  const postAudioSplit = <TData = AxiosResponse<PostAudioSplit200>>(
    postAudioSplitBody: PostAudioSplitBody, options?: AxiosRequestConfig,
  ): Promise<TData> => {
    return axios.post(
      '/audio/split',
      postAudioSplitBody, options,
    )
  }

  /**
   * @summary Get the given segment for the given file.
   */
  const postAudioGetSegment = <TData = AxiosResponse<Blob>>(
    postAudioGetSegmentBody: PostAudioGetSegmentBody, options?: AxiosRequestConfig,
  ): Promise<TData> => {
    return axios.post(
      '/audio/get-segment',
      postAudioGetSegmentBody, {
        responseType: 'blob',
        ...options,
      },
    )
  }

  /**
   * @summary Store the given segment for the given file in the target directory. The file location will be "targetDirectory/metadata[title].mp3"
   */
  const postAudioStore = <TData = AxiosResponse<PostAudioStore200>>(
    postAudioStoreBody: PostAudioStoreBody, options?: AxiosRequestConfig,
  ): Promise<TData> => {
    return axios.post(
      '/audio/store',
      postAudioStoreBody, options,
    )
  }

  return { postAudioSplit, postAudioGetSegment, postAudioStore }
}
export type PostAudioSplitResult = AxiosResponse<PostAudioSplit200>
export type PostAudioGetSegmentResult = AxiosResponse<Blob>
export type PostAudioStoreResult = AxiosResponse<PostAudioStore200>
