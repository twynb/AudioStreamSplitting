# Segmentation

This file provides all functions necessary to split an audio file into smaller segments.
Where each segment represents a distinct portion of the file. Segmentation works on mono
audio, if stereo is provided it will be transformed to mono.

If a file containing multiple songs is given, the resulting segments will represent the individual songs.
If a file containing one song is given, it may split the song into its multiple parts.

This segmentation is based on a computed self similarity matrix and its novelty function and may be faulty.
If there are no clear transitions or consecutive similar audio, splits may be missing. Generally this method
adds more splits than necessary, since songs often have strong dissimilarities within themselves.


## Contents

Classes:

- [``FeatureType``](#FeatureType)
- [``Preset``](#Preset)

Functions:

- [``extract_chroma``](#extract_chroma)
- [``extract_spectro``](#extract_spectro)
- [``smooth_downsample_feature_sequence``](#smooth_downsample_feature_sequence)
- [``median_downsample_feature_sequence``](#median_downsample_feature_sequence)
- [``normalize_feature_sequence``](#normalize_feature_sequence)
- [``create_gaussian_checkerboard_kernel``](#create_gaussian_checkerboard_kernel)
- [``compute_self_similarity``](#compute_self_similarity)
- [``compute_novelty_ssm``](#compute_novelty_ssm)
- [``select_peaks``](#select_peaks)
- [``filter_peaks``](#filter_peaks)
- [``segment_block``](#segment_block)
- [``segment_file``](#segment_file)


## Classes

### FeatureType

Enum containing all Features we would want to extract from the audio.

- ``CHROMA``:
- ``SPECTRAL``:

### Preset

Enum containing several presets of values used for splitting.
Set values are the length of the smoothing filter, downsampling factor and peak threshold.

- ``EXTRA_STRICT``
- ``STRICT``
- ``NORMAL``
- ``LENIENT``
- ``EXTRA_LENIENT``

NORMAL is the recommended Preset.
STRICT and EXTRA_STRICT may result in missing segments.
LENIENT and EXTRA_LENIENT may not only result in more segments but also in faultier ones.


## Functions

### extract_chroma

Computes a chromagram feature vector on the given sequence.

#### extract_chroma:Arguments

- ``feature``: The feature sequence
- ``samplerate``: The samplerate of the audio
- ``hop_length: int``: The amount of samples advanced between each frame in the audio
- ``fft_window: int``: The window size used for fast-fourier-transformation

#### extract_chroma:Returns

A chroma feature vector.


### extract_spectro

Computes a mel-scaled spectrogram feature vector on the given sequence.

#### extract_spectro:Arguments

- ``feature``: The feature sequence
- ``samplerate``: The samplerate of the audio
- ``hop_length: int``: The amount of samples advanced between each frame in the audio
- ``fft_window: int``: The window size used for fast-fourier-transformation

#### extract_spectro:Returns

A mel-scaled spectrogram feature vector.


### smooth_downsample_feature_sequence

Blur the given feature sequence and downsamples it by the given factor.

#### smooth_downsample_feature_sequence:Arguments

- ``feature``: The feature sequence
- ``samplerate``: The samplerate of the feature sequence
- ``filter_len: int``: The length of the smoothing filter. Has to be odd (if even will be incremented).
- ``downsampling: int``: The downsampling factor.

#### smooth_downsample_feature_sequence:Returns

The downsampled and smoothed feature sequence.


### median_downsample_feature_sequence

Compute a 2D median filter on the given feature sequence and downsample it by the given
factor.

#### median_downsample_feature_sequence:Arguments

- ``feature``: The feature sequence
- ``samplerate``: The samplerate of the feature sequence
- ``filter_len: int``: The length of the median filter. Has to be odd (if even will be incremented).
- ``downsampling: int``: The downsampling factor.

#### median_downsample_feature_sequence:Returns

The downsampled and smoothed feature sequence.


### normalize_feature_sequence

Normalize a given feature sequence using a L2-norm to a range of [0.0 - 1.0].

#### normalize_feature_sequence:Arguments

- ``feature``: The feature sequence to normalize.

#### normalize_feature_sequence:Returns

The normalized feature sequence.


### create_gaussian_checkerboard_kernel

Computes a checkerboard kernel convolved with a 2D gaussian.
Used to detect corners on the blurred self similarity matrix.

#### create_gaussian_checkerboard_kernel:Arguments

- ``n: int``: The resulting kernel length will be 2 * n + 1
- ``var: float``: The variance of the gaussian kernel
- ``normalize: bool``: Whether to normalize the kernel

#### create_gaussian_checkerboard_kernel:Returns

A 2D gaussian Kernel of length 2 * n + 1.


### compute_self_similarity

Computes a self similarity matrix on the given sequence using the dot-product.
This function will utilize [``smooth_downsample_feature_sequence``](#smooth_downsample_feature_sequence)
and [``normalize_feature_sequence``](#normalize_feature_sequence) before the actual computation.
Edges and corners in the SSM represent transitions between segments.

#### compute_self_similarity:Arguments

- ``feature``: The feature sequence
- ``samplerate``: The samplerate of the feature sequence
- ``filter_len: int``: The length of the filter used for smoothing. Has to be odd (if even will be incremented).
- ``downsampling: int``: The downsampling factor.

#### compute_self_similarity:Returns

An SSM (Self similarity matrix) for the given feature vector.


### compute_novelty_ssm

Computes a novelty function on the given SSM (Self Similarity Matrix) using
a given Corner detection kernel (or [create_gaussian_checkerboard_kernel](#create_gaussian_checkerboard_kernel)
by default).
The beginning and end of the resulting function will be inaccurate, since we mirror
the SSM for the convolution. These inaccurate parts may be excluded and set to 0.
This will result in a 1D representation of the SSM where peaks represent
transitions between segments.

#### compute_novelty_ssm:Arguments

- ``ssm``: The self similarity matrix to work with
- ``kernel``: The corner detection kernel to compute a novelty function with.
If None is specified, will default to [create_gaussian_checkerboard_kernel](#create_gaussian_checkerboard_kernel)
- ``n: int``: Influences the length of the default kernel
- ``var: float``: The variance of the default kernel
- ``exclude: bool``: Whether to exclude the first and last 2 * n + 1 values.
The edges of the ssm will be padded by reflection, which will result in inaccuracies.

#### compute_novelty_ssm:Returns

A novelty function of the given SSM


### select_peaks

Finds the Indices of peaks in the given novelty function,
which represent transitions.
Indices are in audio frames and will be upsampled (if previously downsampled)
and incremented by a given offset.

#### select_peaks:Arguments

- ``novelty``: The novelty function
- ``peak_threshold: float``: The threshold by which peaks are selected.
See [Librosa Docs](https://librosa.org/doc/latest/generated/librosa.util.peak_pick.html#librosa.util.peak_pick)
- ``downsampling: int``: The downsampling factor by which the ssm was previously downsampled
- ``offset: float``: An offset to increment resulting peaks by. This is useful for streamed audio, since each block of
the stream starts at 0

#### select_peaks:Returns

A list of peak indices (indices are audio frames, not samples).


### filter_peaks

Filters a given vector to only include values that occur more than n (by default 3)
times. This may be necessary when working with overlapping block in a stream, where
the same peaks may appear multiple times.

#### filter_peaks:Arguments

- ``peaks``: The list of peak indices
- ``n: int``: The number of times a values has to appear, for it to be relevant.

#### filter_peaks:Returns

The filtered list of peak indices.


### segment_block

Segments a block (see: [Librosa Docs](https://librosa.org/doc/latest/generated/librosa.stream.html#librosa.stream)).
This will extract a specified [``FeatureType``](#FeatureType) compute the SSM and Novelty Function
and finally search for Peaks.

#### segment_block:Arguments

- ``block``: A block of the streamed audio
- ``samplerate``: The samplerate of the audio
- ``hop_length: int``: The hop_length of the audio stream (amount of samples jumped between audio frames)
- ``feature: FeatureType``: The [``FeatureType``](#FeatureType) to use for segmentation
- ``filter_len: int``: The length of the smoothing filter. See [``smooth_downsample_feature_sequence``](#smooth_downsample_feature_sequence)
- ``downsampling: int``: The downsampling factor for the SSM. See [``smooth_downsample_feature_sequence``](#smooth_downsample_feature_sequence)
- ``threshold: float``: The peak threshold. See [``select_peaks``](#select_peaks)
- ``offset: float``: The offset by which peaks are incremented. See [``select_peaks``](#select_peaks)

#### segment_block:Returns

All peak indices found for the given block.


### segment_file

Creates a generator, where each step results in a start_time and duration, representing a segment.
This will stream over the audio in overlapping blocks and segment each block individually.
The resulting peaks will be filtered, to make sure the peaks are not just local maximums, before being pairwise iterated.

#### segment_file:Arguments

- ``path``: The path to the audio file.
- ``preset: Preset``: The preset of values used in segmentation.

#### segment_file:Returns

A generator over each segment of the audio file.
Each segment consists of start_time, duration and samplerate.
