import numpy as np

def qim_embed(value, bit, delta):
    """
    Embed a bit ('0' or '1') into a coefficient value using QIM with dynamic delta.
    """
    if bit == '0':
        return np.round(value / (2 * delta)) * (2 * delta)
    else:
        return np.round((value - delta) / (2 * delta)) * (2 * delta) + delta

def qim_extract(value, delta):
    """
    Extract a bit from a coefficient value using QIM with dynamic delta.
    """
    quantized_step = np.round(value / delta)
    return '0' if quantized_step % 2 == 0 else '1'