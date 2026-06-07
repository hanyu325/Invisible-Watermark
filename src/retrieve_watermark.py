import cv2
import numpy as np
from src.config import SEED, EOF_MARKER
from src.utils import binary_to_text, get_dft
from src.qim import qim_extract

def retrieve_watermark(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not read image.")

    b_channel, g_channel, r_channel = cv2.split(img)
    dft = get_dft(b_channel)
    rows, cols = b_channel.shape
    
    # 【關鍵修改】：提取時套用相同的動態 Delta 計算公式
    # 2026/06/07 嘗試將 0.8 改成 2.0、3.0 甚至 5.0
    dynamic_delta = rows * cols * 0.8
    
    np.random.seed(SEED)
    coords = []
    # 原本是 range(1, rows // 2) 和 range(1, cols)
    # 縮小範圍，避開高頻區：
    for r in range(1, rows // 4): 
        for c in range(1, cols // 4):
            coords.append((r, c))
            
    np.random.shuffle(coords)
    
    binary_str = ""
    for r, c in coords:
        val = dft[r, c, 0]
        
        # 將 dynamic_delta 傳給 QIM
        bit = qim_extract(val, dynamic_delta)
        binary_str += bit
        
        if len(binary_str) % 8 == 0:
            current_text = binary_to_text(binary_str)
            if current_text.endswith(EOF_MARKER):
                return current_text[:-len(EOF_MARKER)]
                
    return "Failed to retrieve: EOF marker not found."