import cv2
import numpy as np
from src.config import SEED, EOF_MARKER
from src.utils import text_to_binary, get_dft, get_idft
from src.qim import qim_embed

def apply_watermark(img_path, text, output_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not read image.")

    b_channel, g_channel, r_channel = cv2.split(img)
    dft = get_dft(b_channel)
    rows, cols = b_channel.shape
    
    # 【關鍵修改】：根據圖片總像素數量動態決定 QIM 的 Delta
    # 乘上 0.8 是為了確保訊號轉換回像素時，強度足以抵抗四捨五入，又不會嚴重影響畫質
    # 2026/06/07 嘗試將 0.8 改成 2.0、3.0 甚至 5.0
    dynamic_delta = rows * cols * 0.8
    
    binary_str = text_to_binary(text, EOF_MARKER)
    np.random.seed(SEED)
    
    coords = []
    # 原本是 range(1, rows // 2) 和 range(1, cols)
    # 縮小範圍，避開高頻區：
    for r in range(1, rows // 4): 
        for c in range(1, cols // 4):
            coords.append((r, c))
            
    np.random.shuffle(coords)
    
    if len(binary_str) > len(coords):
        raise ValueError("Text is too long to embed in this image.")
        
    for i, bit in enumerate(binary_str):
        r, c = coords[i]
        val = dft[r, c, 0]
        
        # 將 dynamic_delta 傳給 QIM
        new_val = qim_embed(val, bit, dynamic_delta)
        
        dft[r, c, 0] = new_val
        dft[rows - r, cols - c, 0] = new_val 

    idft_b = get_idft(dft)
    watermarked_b = np.clip(idft_b, 0, 255).astype(np.uint8)
    
    watermarked_img = cv2.merge((watermarked_b, g_channel, r_channel))
    cv2.imwrite(output_path, watermarked_img)