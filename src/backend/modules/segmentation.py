import os
from enum import Enum
from itertools import pairwise
from os import path

import numpy as np
from scipy import signal
import librosa
from librosa import feature

from audio_stream_io import readAudiofileToStream, saveNumPyAsAudioFile, overlappingStream


# TODO: Implement debugging mode (plots, prints) ?


class Feature(Enum):
    """
    This enum represent the different features we can extract and use for splitting.
    """
    CHROMA = 1
    SPECTRAL = 2
    MFCC = 3


# TODO: (Optional) Rework this to Preset and set more values than down-sampling
class Downsampling(Enum):
    """
    This enum represent the Downsampling for the SSM.
    """
    STRICT = 4
    NORMAL = 8
    LENIANT = 16
    EXTRA_LENIANT = 32
    # CUSTOM = 0 this should be specified by the user


def create_checkerboard_kernel(n: int):
    """
      Computes a checkerboard kernel to detect edges and corners in a matrix.

      :param n: length of one quadrant in the resulting kernel

      :returns: checkerboard kernel of length 2 * n + 1
    """

    axis = np.arange(-n, n+1)
    kernel = np.outer(np.sign(axis), np.sign(axis))
    return kernel


def create_gaussian_checkerboard_kernel(n: int, var=1.0, normalize=True):
    """
        Computes a gaussian checkerboard kernel to smooth and detect edges and corners in a matrix.
        This is a combination of a basic checkerboard kernel and a gauss filter kernel.

        :param n: length of one quadrant in the resulting kernel
        :param var: the variance of the resulting kernel (default: 1.0)
        :param normalize: whether the resulting kernel should be normalized or not (default: True)

        :returns: gaussian checkerboard kernel of length 2 * n + 1
    """

    taper = np.sqrt(0.5) / (n * var)
    axis = np.arange(-n, n+1)
    gaussian_1d = np.exp(-taper**2 * (axis**2))
    gaussian_2d = np.outer(gaussian_1d, gaussian_1d)
    kernel_box = np.outer(np.sign(axis), np.sign(axis))

    kernel = kernel_box * gaussian_2d
    if normalize:
        kernel = kernel / np.sum(np.abs(kernel))

    return kernel


def smooth_downsample_feature_sequence(x, sr, filt_len, down_sampling):
    """
        Smooths and down-samples a given feature-sequence and its samplerate.

        :param x: the feature sequence to smooth and down-sample
        :param sr: the samplerate of the feature sequence
        :param filt_len: length of the smoothing filter
        :param down_sampling: down-sampling rate

        :returns: the smoothed and down-sampled feature sequence, the down-sampled samplerate
    """

    filt_kernel = np.expand_dims(signal.get_window('boxcar', filt_len), axis=0)
    x_smooth = signal.convolve(x, filt_kernel, mode='same') / filt_len
    x_smooth = x_smooth[:, ::down_sampling]
    sr_feature = sr / down_sampling

    return x_smooth, sr_feature


def median_downsample_feature_sequence(x, sr, filt_len, down_sampling):
    """
        Smooths and down-samples a given feature-sequence and its samplerate using a median filter.

        :param x: the feature sequence to smooth and down-sample
        :param sr: the samplerate of the feature sequence
        :param filt_len: length of the median filter
        :param down_sampling: down-sampling rate

        :returns: the smoothed and down-sampled feature sequence, the down-sampled samplerate
    """

    if filt_len % 2 != 1:
        filt_len = filt_len + 1

    filt_len = [1, filt_len]
    x_smooth = signal.medfilt2d(x, filt_len)
    x_smooth = x_smooth[:, ::down_sampling]
    sr_feature = sr / down_sampling

    return x_smooth, sr_feature


def normalize_feature_sequence(x):
    """
        Normalized a given feature sequence.

        :param x: the feature sequence to normalize

        :returns: the normalized feature sequence
    """

    k, n = x.shape
    x_norm = np.zeros((k, n))

    v = np.ones(k, dtype=np.float64) / np.sqrt(k)
    for i in range(n):
        s = np.sqrt(np.sum(x[:, i] ** 2))
        if s > 0.001:
            x_norm[:, i] = x[:, i] / s
        else:
            x_norm[:, i] = v

    return x_norm


def compute_self_similarity(feature, sr, filter_len=41, down_sampling=8):
    """
        Computes the self similarity matrix for a given feature sequence.
        Stacks the feature sequence with delay, smooths and down-samples it and finally normalizes the sequence before
        calculating the ssm.

        :param feature: the feature sequence
        :param sr: the sample-rate
        :param filter_len: length for the filter kernel, needs to be odd ()
        :param down_sampling: down-sampling rate for feature sequence (default: 32)

        :returns: the self similarity matrix, the resulting sample-rate
    """

    # stack feature on top of itself, with a delay
    chroma = librosa.feature.stack_memory(feature, n_steps=4, delay=8)
    # feature smoothing
    chroma, down_sampled_sr = smooth_downsample_feature_sequence(chroma, sr, filt_len=filter_len, down_sampling=down_sampling)
    # normalization
    chroma = normalize_feature_sequence(chroma)

    # compute self similarity matrix
    ssm = np.dot(np.transpose(chroma), chroma)

    # Debug Plotting
    # plt.imshow(ssm, cmap='magma')
    # plt.colorbar()
    # plt.show()

    return ssm, down_sampled_sr


def compute_novelty_ssm(ssm, kernel=None, n=8, var=0.5, exclude=False):
    """
        Computes the novelty function for the given self similarity matrix.

        :param ssm: the self similarity matrix
        :param kernel: the kernel for edge / corner detection (default: gaussian checkerboard)
        :param n: length of one quadrant of the kernel (default: 10)
        :param var: variance for the gaussian checkerboard kernel (default: 0.5)
        :param exclude: whether to exclude the start and end of the resulting novelty function.
                        If True this sets both the start and end to 0. (default: False)

        :returns: the resulting novelty function. Peaks indicate edges / corners (transitions).
    """

    if kernel is None:
        kernel = create_gaussian_checkerboard_kernel(n, var=var)

    N = ssm.shape[0]
    M = 2 * n + 1
    nov = np.zeros(N)
    s_padded = np.pad(ssm, n, mode='reflect')

    for i in range(N):
        nov[i] = np.sum(s_padded[i:i + M, i:i + M] * kernel)

    # Normalize to [0.0 - 1.0]
    nov = (nov - np.min(nov)) / (np.max(nov) - np.min(nov))

    if exclude:
        right = np.min([n, N])
        left = np.max([0, N - n])
        nov[0:right] = 0
        nov[left:N] = 0

    return nov


# TODO: Needs more research (maybe adaptive thresholding)
def select_peaks(novelty, peak_threshold=0.5, down_sampling=32, offset=0.0):
    """
        Selects the peak of the given function based on the given threshold.

        :param novelty: the function to find peaks in
        :param peak_threshold: the threshold to filter with
        :param down_sampling: the down-sampling-rate used for the feature sequence

        :returns: all indexes where the function peaks
    """

    # Find peaks
    # peaks = librosa.util.peak_pick(x=novelty, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.5, wait=10)
    peaks, _ = signal.find_peaks(novelty, prominence=peak_threshold)

    # Adaptive Thresholding ##################################################
    # novelty = ndimage.gaussian_filter1d(novelty, sigma=4.0)
    # novelty = (novelty - np.min(novelty)) / (np.max(novelty) - np.min(novelty))
    # threshold_local = ndimage.median_filter(novelty, size=16) + novelty.mean() * peak_threshold
    # peaks = []
    # for i in range(1, novelty.shape[0] - 1):
    #     if novelty[i - 1] < novelty[i] and novelty[i] > novelty[i + 1]:
    #         if novelty[i] > threshold_local[i]:
    #             peaks.append(i)
    # peaks = np.array(peaks)
    ###########################################################################

    # Add start and end of segment
    # peaks = np.insert(peaks, 0, 0)
    # peaks = np.append(peaks, len(novelty))

    # Debug plotting
    # plt.plot(novelty)
    # for x in peaks:
    #     plt.vlines(x, ymin=0, ymax=0.01, colors='red', label=f'Peak: {x}')
    # plt.show()

    peaks *= down_sampling
    peaks += int(offset)
    return peaks


def extract_chroma(x, sr, hop_length, fft_window=2048):
    """
    Extracts the chroma feature vector from the given sequence.

    :param x: The sequence to work on.
    :param sr: The sample-rate of the sequence
    :param hop_length: The hop-length of the sequence.
    :param fft_window: The Window size for the fast-fourier-transformation (default: 2048)

    :return: The chroma feature vector.
    """
    # convert to mono
    x_mono = librosa.to_mono(x)
    # extract chroma feature
    return librosa.feature.chroma_stft(y=x_mono, sr=sr, hop_length=hop_length, center=False, n_fft=fft_window)


def extract_spectro(x, sr, hop_length, fft_window=2048):
    """
    Extracts the mel-spectrogram feature vector from the given sequence.

    :param x: The sequence to work on.
    :param sr: The sample-rate of the sequence
    :param hop_length: The hop-length of the sequence.
    :param fft_window: The Window size for the fast-fourier-transformation (default: 2048)

    :return: The mel-spectrogram feature vector.
    """
    # convert to mono
    x_mono = librosa.to_mono(x)
    # extract mel-spectrogram
    return librosa.feature.melspectrogram(y=x_mono, sr=sr, hop_length=hop_length, center=False, n_fft=fft_window)


# TODO: Reevaluate this; didn't seem to work well
def extract_mfcc(x, sr):
    # convert to mono
    x_mono = librosa.to_mono(x)
    # extract mffc
    return librosa.feature.mfcc(y=x_mono, sr=sr)


def segment_block(block, sr, hop_length, feature: Feature, filter_len=41, down_sampling=8, threshold=0.7, offset=0.0):
    """
        Segments a data array into segments, where each segment represents a different part in the audio.

        :param block: the current block of the audio stream
        :param sr: sample rate of the audio stream
        :param hop_length: hop length of the audio stream

        :returns: a list of indexes, where transitions should be
    """

    # Spectral worked best so far
    if feature == Feature.CHROMA:
        feature_seq = extract_chroma(block, sr, hop_length, fft_window=2048)
    elif feature == Feature.SPECTRAL:
        feature_seq = extract_spectro(block, sr, hop_length, fft_window=2048)
    elif feature == Feature.MFCC:
        feature_seq = extract_mfcc(block, sr)
    else:
        raise TypeError("Illegal Feature Value.")

    ssm, _ = compute_self_similarity(feature_seq, sr, filter_len=filter_len, down_sampling=down_sampling)
    nov = compute_novelty_ssm(ssm, n=8, exclude=False)
    return select_peaks(nov, peak_threshold=threshold, down_sampling=down_sampling, offset=offset)


def filter_peaks(peaks, n=3):
    """
    Filters a given vector to values that appear at least n times.

    :param peaks: The given vector
    :param n: The minimum number of times a value has to appear

    :return: The filtered vector
    """
    unique, counts = np.unique(peaks, return_counts=True)
    return np.sort([k for k, v in dict(zip(unique, counts)).items() if v >= n])


def segment_file(path, down_sampling=Downsampling.NORMAL):
    """
    Segments a given file into a generator.

    :param path: The path to the File
    :param down_sampling: The down-sampling rate for the SSM see: :class:`Downsampling`

    :return: A generator that iterates over the found segments, the start time and duration for the original file
    """
    block_len = 4096
    stream, sr, hop_length = readAudiofileToStream(path, block_len=block_len)

    transitions = np.zeros(1)
    last_frame_in_audiofile = 0
    for (idx, block) in enumerate(overlappingStream(stream)):
        if np.unique(block).size == 1:
            print("skipping")
            continue

        offset = idx * block_len * 0.25
        transitions = np.append(transitions,
                                segment_block(block, sr, hop_length, Feature.SPECTRAL,
                                              down_sampling=down_sampling.value, threshold=0.7, offset=offset))

        last_frame_in_audiofile = librosa.core.samples_to_frames(block.shape[1], hop_length=hop_length) + offset

    # Filter peaks and insert boundaries
    transitions = filter_peaks(transitions, n=3)
    transitions = np.insert(transitions, 0, 0)
    transitions = np.append(transitions, last_frame_in_audiofile - 1)

    for start, end in pairwise(transitions):
        start_time = librosa.core.frames_to_time(start, sr=sr, hop_length=hop_length, n_fft=2048)
        duration = librosa.core.frames_to_time(end - start, sr=sr, hop_length=hop_length, n_fft=2048)

        yield librosa.load(current_track, mono=False, sr=sr, offset=start_time, duration=duration), start_time, duration


# TODO: Move this elsewhere
if __name__ == '__main__':
    # TODO: This whole segment is only for testing purposes and should be refactored
    ####################################################################################################################
    for f in os.listdir('../../../test_output/'):
        os.remove(os.path.join('../../../test_output/', f))

    file_parent_path = path.abspath('../../../../../Music/Stuff/')

    album = "full_album.mp3"      # 1h 6m 30s    13 songs
    hiphop = "hiphop.mp3"         # 15m 30s      4 songs
    edm = "modern_edm.mp3"        # 20m 40s      5 songs
    pop = "old_pop.mp3"           # 19m 45s      5 songs
    rock = "rock.mp3"             # 15m 40s      4 songs
    crackle = "with_crackle.mp3"  # 12m          3 songs

    current_track = path.join(file_parent_path, crackle)
    ####################################################################################################################

    for (segment, sr), start, duration in segment_file(current_track, Downsampling.NORMAL):
        start_m, start_s = divmod(int(start), 60)
        m, s = divmod(int(duration), 60)
        song_name = f'Song_{start_m:02d}m{start_s:02d}s_{m:02d}m{s:02d}s'
        # probably not how this would work
        # tags = identify(segment)
        # song_name = tags.name
        # tag_audio_file(tags)

        output_path = path.abspath('../../../test_output/')
        saveNumPyAsAudioFile(segment, song_name, output_path, int(sr))

        print(f'Successfully written {song_name} to {output_path} with a ' +
              f'duration of {m:02d}m {s:02d}s.')