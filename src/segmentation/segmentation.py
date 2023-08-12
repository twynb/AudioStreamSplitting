import librosa
import numpy as np
from scipy import signal


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
    gaussian_1d = np.exp(-taper**2 * axis**2)
    gaussian_2d = np.outer(gaussian_1d, gaussian_1d)
    kernel_box = np.outer(np.sign(axis), np.sign(axis))

    kernel = kernel_box + gaussian_2d
    if normalize:
        kernel = kernel / np.sum(np.abs(kernel))

    return kernel


def smooth_downsample_feature_sequence(x, sr, filt_len, down_sampling, w_type='boxcar'):
    """
        Smooths and down-samples a given feature-sequence and its samplerate.

        :param x: the feature sequence to smooth and down-sample
        :param sr: the samplerate of the feature sequence
        :param filt_len: length of the smoothing filter
        :param down_sampling: down-sampling rate
        :param w_type: ???

        :returns: the smoothed and down-sampled feature sequence, the down-sampled samplerate
    """

    filt_kernel = np.expand_dims(signal.get_window(w_type, filt_len), axis=0)
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


def normalize_feature_sequence(x, threshold=0.0001, v=None):
    """
        Normalized a given feature sequence.

        :param x: the feature sequence to normalize
        :param threshold: ???
        :param v: ???

        :returns: the normalized feature sequence
    """

    k, n = x.shape
    x_norm = np.zeros((k, n))

    if v is None:
        v = np.ones(k, dtype=np.float64) / np.sqrt(k)

    for i in range(n):
        s = np.sqrt(np.sum(x[:, i] ** 2))
        if s > threshold:
            x_norm[:, i] = x[:, i] / s
        else:
            x_norm[:, i] = v

    return x_norm

# TODO: Currently takes a block and extracts chroma feature, should be changed so we can use this for all features
# TODO: Make more parameters customizable (normalization, ...)
def compute_self_similarity(x, sr, hop):
    """
        Computes the self similarity matrix for a given feature sequence.
        Stacks the feature sequence with delay, smooths and down-samples it and finally normalizes the sequence before
        calculating the ssm.

        :param x: the feature sequence
        :param sr: the sample-rate
        :param hop: the hop-length

        :returns: the self similarity matrix, the resulting sample-rate
    """

    x_mono = librosa.to_mono(x)

    # extract chroma feature
    chroma = librosa.feature.chroma_stft(y=x_mono, sr=sr, hop_lenght=hop, center=False)
    # stack feature on top of itself, with a delay
    chroma = librosa.feature.stack_memory(chroma, n_steps=4, delay=8)
    # feature smoothing
    chroma, sr = smooth_downsample_feature_sequence(chroma, sr, filt_len=41, down_sampling=27)
    # normalization
    chroma = normalize_feature_sequence(chroma, threshold=0.001)

    # compute self similarity matrix
    ssm = np.dot(np.transpose(chroma), chroma)

    return ssm, sr


def compute_novelty_ssm(ssm, kernel=None, n=10, var=0.5, exclude=False):
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
    s_padded = np.pad(ssm, n, mode='constant')

    for i in range(N):
        nov[i] = np.sum(s_padded[i:i + M, i:i + M] * kernel)

    if exclude:
        right = np.min([n, N])
        left = np.max([0, N - n])
        nov[0:right] = 0
        nov[left:N] = 0

    return nov


# TODO: Implement this
def select_peaks(novelty, threshold=0.5):
    """
        Selects the peak of the given function based on the given threshold.

        :param novelty: the function to find peaks in
        :param threshold: the threshold to filter with

        :returns: all indexes where the function peaks
    """

    peaks = []

    return peaks


def segment_block(block, sr, hop_length):
    """
        Computes the novelty function for the given self similarity matrix.

        :param block: the current block of the audio stream
        :param sr: sample rate of the audio stream
        :param hop_length: hop length of the audio stream

        :returns: the indexes where the audio stream transitions
    """

    ssm, sr = compute_self_similarity(block, sr, hop_length)
    nov = compute_novelty_ssm(ssm, n=16, exclude=True)

    idx = select_peaks(nov, threshold=0.2)

    return idx

