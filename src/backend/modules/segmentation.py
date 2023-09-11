from collections import namedtuple
from enum import Enum
from itertools import pairwise

import librosa
import numpy as np
from scipy import signal

from .audio_stream_io import (
    overlapping_stream,
    read_audio_file_to_stream,
)

# TODO: Implement debugging mode (plots, prints) -> needs UI as well


class FeatureType(Enum):
    """This enum represent the different features we can extract and use for splitting."""

    CHROMA = 1
    SPECTRAL = 2


class Preset(
    namedtuple("Preset", "name filter_length downsampling peak_threshold"), Enum
):
    """This enum represents a preset of values used for splitting.

    The values set in these presets are:

    - filter_length: the size of the median filter used for downsampling
    - downsampling: the factor to downsample the ssm
    - peak_threshold: a threshold by which peaks in the novelty function are selected

    Presets are:

                      filter_length,      downsampling,       peak_threshold
    - EXTRA_STRICT:     57,                 2,                0.6
    - STRICT:           49,                 4,                0.55
    - NORMAL:           41,                 8,                0.5
    - LENIENT:          33,                 16,               0.45
    - EXTRA_LENIENT:    25,                 32,               0.4

    Normal is the recommended preset, strict may result in too little segments and lenient may
    result in increasingly too many but inaccurate segments.
    """

    EXTRA_STRICT = "extra strict", 57, 2, 0.6
    STRICT = "strict", 49, 4, 0.55
    NORMAL = "normal", 41, 8, 0.5
    LENIENT = "lenient", 33, 16, 0.45
    EXTRA_LENIENT = "extra lenient", 25, 32, 0.4
    # Custom = 0, 0, 0


def extract_chroma(feature, samplerate, hop_length: int, fft_window=2048):
    """Extracts the chroma feature vector from the given sequence.
    :param feature: The sequence to work on.
    :param samplerate: The sample-rate of the sequence
    :param hop_length: The hop-length of the sequence.
    :param fft_window: The Window size for the fast-fourier-transformation
                       (default: 2048)
    :return: The chroma feature vector.
    """
    # convert to mono
    feature_mono = librosa.to_mono(feature)
    # extract chroma feature
    return librosa.feature.chroma_stft(
        y=feature_mono,
        sr=samplerate,
        hop_length=hop_length,
        center=False,
        n_fft=fft_window,
    )


def extract_spectro(feature, samplerate, hop_length: int, fft_window=2048):
    """Extracts the mel-spectrogram feature vector from the given sequence.
    :param feature: The sequence to work on.
    :param samplerate: The sample-rate of the sequence
    :param hop_length: The hop-length of the sequence.
    :param fft_window: The Window size for the fast-fourier-transformation
                       (default: 2048)
    :return: The mel-spectrogram feature vector.
    """
    # convert to mono
    feature_mono = librosa.to_mono(feature)
    # extract mel-spectrogram
    return librosa.feature.melspectrogram(
        y=feature_mono,
        sr=samplerate,
        hop_length=hop_length,
        center=False,
        n_fft=fft_window,
    )


def smooth_downsample_feature_sequence(
    feature, samplerate, filter_len: int, downsampling: int
):
    """Smooths and down-samples a given feature-sequence and its samplerate.
    :param feature: the feature sequence to smooth and down-sample
    :param samplerate: the samplerate of the feature sequence
    :param filter_len: length of the smoothing filter
    :param downsampling: down-sampling rate
    :returns: the smoothed and down-sampled feature sequence,
              the down-sampled samplerate.
    """
    if filter_len % 2 != 1:
        filter_len = filter_len + 1

    filter_kernel = np.expand_dims(signal.get_window("boxcar", filter_len), axis=0)
    feature_smooth = signal.convolve(feature, filter_kernel, mode="same") / filter_len
    feature_smooth = feature_smooth[:, ::downsampling]
    sr_feature = samplerate / downsampling

    return feature_smooth, sr_feature


def median_downsample_feature_sequence(
    feature, samplerate, filter_len: int, downsampling: int
):
    """Smooths and down-samples a given feature-sequence and its samplerate
    using a median filter.
    :param feature: the feature sequence to smooth and down-sample
    :param samplerate: the samplerate of the feature sequence
    :param filter_len: length of the median filter
    :param downsampling: down-sampling rate
    :returns: the smoothed and down-sampled feature sequence,
              the down-sampled samplerate.
    """
    if filter_len % 2 != 1:
        filter_len = filter_len + 1

    filter_len = [1, filter_len]
    feature_smooth = signal.medfilt2d(feature, filter_len)
    feature_smooth = feature_smooth[:, ::downsampling]
    sr_feature = samplerate / downsampling

    return feature_smooth, sr_feature


def normalize_feature_sequence(feature):
    """Normalize a given feature sequence.
    :param feature: the feature sequence to normalize
    :returns: the normalized feature sequence.
    """
    n, m = feature.shape
    feature_norm = np.zeros((n, m))

    v = np.ones(n, dtype=np.float64) / np.sqrt(n)
    for i in range(m):
        s = np.sqrt(np.sum(feature[:, i] ** 2))
        if s > 0.001:
            feature_norm[:, i] = feature[:, i] / s
        else:
            feature_norm[:, i] = v

    return feature_norm


def create_gaussian_checkerboard_kernel(n: int, var=1.0, normalize=True):
    """Computes a gaussian checkerboard kernel to smooth and detect edges and
    corners in a matrix.
    This is a combination of a basic checkerboard kernel and a gauss filter kernel.
    :param n: length of one quadrant in the resulting kernel
    :param var: the variance of the resulting kernel
                (default: 1.0)
    :param normalize: whether the resulting kernel should be normalized or not
                      (default: True)
    :returns: gaussian checkerboard kernel of length 2 * n + 1.
    """
    taper = np.sqrt(0.5) / (n * var)
    axis = np.arange(-n, n + 1)
    gaussian_1d = np.exp(-(taper**2) * (axis**2))
    gaussian_2d = np.outer(gaussian_1d, gaussian_1d)
    kernel_box = np.outer(np.sign(axis), np.sign(axis))

    kernel = kernel_box * gaussian_2d
    if normalize:
        kernel = kernel / np.sum(np.abs(kernel))

    return kernel


def compute_self_similarity(feature, samplerate, filter_len=41, downsampling=8):
    """Computes the self similarity matrix for a given feature sequence.
    Stacks the feature sequence with delay, smooths, down-samples
    and finally normalizes the sequence before calculating the ssm.
    :param feature: the feature sequence
    :param samplerate: the sample-rate
    :param filter_len: length for the filter kernel, needs to be odd (incremented by one if even)
    :param downsampling: down-sampling rate for feature sequence (default: 32)
    :returns: the self similarity matrix, the resulting sample-rate.
    """
    # stack feature on top of itself, with a delay
    chroma = librosa.feature.stack_memory(feature, n_steps=4, delay=8)
    # feature smoothing
    chroma, downsampled_sr = smooth_downsample_feature_sequence(
        chroma, samplerate, filter_len=filter_len, downsampling=downsampling
    )
    # normalization
    chroma = normalize_feature_sequence(chroma)

    # compute self similarity matrix
    ssm = np.dot(np.transpose(chroma), chroma)

    # Debug Plotting
    # plt.imshow(ssm, cmap='magma')
    # plt.colorbar()
    # plt.show()

    return ssm, downsampled_sr


def compute_novelty_ssm(ssm, kernel=None, n=8, var=0.5, exclude=False):
    """Computes the novelty function for the given self similarity matrix.
    :param ssm: the self similarity matrix
    :param kernel: the kernel for edge / corner detection
                   (default: gaussian checkerboard)
    :param n: length of one quadrant of the kernel (default: 10)
    :param var: variance for the gaussian checkerboard kernel (default: 0.5)
    :param exclude: whether to exclude the start and end of the resulting novelty
                    function.
                    If True this sets both the start and end to 0. (default: False)
    :returns: the resulting novelty function.
              Peaks indicate edges / corners (transitions).
    """
    if kernel is None:
        kernel = create_gaussian_checkerboard_kernel(n, var=var)

    N = ssm.shape[0]
    M = 2 * n + 1
    nov = np.zeros(N)
    ssm_padded = np.pad(ssm, n, mode="reflect")

    for i in range(N):
        nov[i] = np.sum(ssm_padded[i : i + M, i : i + M] * kernel)

    # Normalize to [0.0 - 1.0]
    nov = (nov - np.min(nov)) / (np.max(nov) - np.min(nov))

    if exclude:
        right = np.min([n, N])
        left = np.max([0, N - n])
        nov[0:right] = 0
        nov[left:N] = 0

    return nov


def select_peaks(novelty, peak_threshold=0.5, downsampling=32, offset=0.0):
    """Selects the peak of the given function based on the given threshold.
    :param novelty: the function to find peaks in
    :param peak_threshold: the threshold to filter with
    :param downsampling: the down-sampling-rate used for the feature sequence
    :param offset: offset of the original signal in frames
    :returns: all indexes where the function peaks.
    """
    # Find peaks
    wait = int(novelty.shape[0] / 10)
    peaks = librosa.util.peak_pick(
        x=novelty,
        pre_max=10,
        post_max=10,
        pre_avg=10,
        post_avg=10,
        delta=peak_threshold,
        wait=wait,
    )

    # Debug plotting
    # plt.plot(novelty)
    # # Plot vertical lines where detected peaks are
    # for x in peaks:
    #     plt.vlines(x, ymin=0, ymax=0.01, colors='red', label=f'Peak: {x}')
    # plt.show()

    # upsampling
    peaks *= downsampling
    peaks += int(offset)
    return peaks


def filter_peaks(peaks, n=3):
    """Filters a given vector to values that appear at least n times.
    :param peaks: The given vector
    :param n: The minimum number of times a value has to appear
    :return: The filtered vector.
    """
    unique, counts = np.unique(peaks, return_counts=True)
    return np.sort([k for k, v in dict(zip(unique, counts)).items() if v >= n])


def segment_block(
    block,
    samplerate,
    hop_length,
    feature: FeatureType,
    filter_len=41,
    downsampling=8,
    threshold=0.5,
    offset=0.0,
):
    """Segments a data array into segments, where each segment represents
    a different part in the audio.
    :param block: the current block of the audio stream
    :param samplerate: sample rate of the audio stream
    :param hop_length: hop length of the audio stream
    :param feature: the feature type to use, see: :class:`Downsampling`
    :param filter_len: the length of the median filter
    :param downsampling: the downsampling factor to use
    :param threshold: the threshold for peak selection
    :param offset: an offset (in audio frames) to calculate indices for consecutive
                   calls correctly
    :returns: a list of indexes, where transitions should be.
    """
    if feature == FeatureType.CHROMA:
        feature_seq = extract_chroma(block, samplerate, hop_length, fft_window=2048)
    elif feature == FeatureType.SPECTRAL:
        feature_seq = extract_spectro(block, samplerate, hop_length, fft_window=2048)
    else:
        raise TypeError("Illegal Feature Value.")

    ssm, _ = compute_self_similarity(
        feature_seq, samplerate, filter_len=filter_len, downsampling=downsampling
    )
    nov = compute_novelty_ssm(ssm, n=8, exclude=False)
    return select_peaks(
        nov, peak_threshold=threshold, downsampling=downsampling, offset=offset
    )


def segment_file(path, preset=Preset.NORMAL):
    """Segments a given file into a generator.
    :param path: The path to the File
    :param preset: The down-sampling rate for the SSM see: :class:`Preset`
    :return: A generator that iterates over the found segments,
             the start time and duration for the original file.
    """
    block_len = 4096
    stream, samplerate, hop_length = read_audio_file_to_stream(
        path, block_len=block_len
    )

    transitions = np.zeros(1)
    last_frame_in_audiofile = 0
    for idx, block in enumerate(overlapping_stream(stream)):
        # if the block is constant, we won't find anything, so skip
        if np.unique(block).size == 1:
            continue

        offset = idx * block_len * 0.25
        transitions = np.append(
            transitions,
            segment_block(
                block,
                samplerate,
                hop_length,
                FeatureType.SPECTRAL,
                filter_len=preset.filter_length,
                downsampling=preset.downsampling,
                threshold=preset.peak_threshold,
                offset=offset,
            ),
        )

        last_frame_in_audiofile = (
            librosa.core.samples_to_frames(block.shape[1], hop_length=hop_length)
            + offset
        )

    # Filter peaks and insert boundaries
    transitions = filter_peaks(transitions, n=3)
    transitions = np.insert(transitions, 0, 0)
    transitions = np.append(transitions, last_frame_in_audiofile - 1)

    # Generate the segments consisting of start_time and duration
    for start, end in pairwise(transitions):
        start_time = librosa.core.frames_to_time(
            start, sr=samplerate, hop_length=hop_length, n_fft=2048
        )
        duration = librosa.core.frames_to_time(
            end - start, sr=samplerate, hop_length=hop_length, n_fft=2048
        )

        # TODO decide whether to remove librosa.load() call for memory efficiency
        yield librosa.load(
            path, mono=False, sr=samplerate, offset=offset, duration=duration
        ), start_time, duration
