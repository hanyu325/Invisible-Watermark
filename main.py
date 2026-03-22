import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def embed_watermark(host_path, wmk_path, alpha_factor=10.0):
    if not os.path.exists(host_path): raise FileNotFoundError(f"找不到底圖：{host_path}")
    if not os.path.exists(wmk_path): raise FileNotFoundError(f"找不到Logo：{wmk_path}")

    # 1. 讀取載體影像並轉為浮點數
    host = cv2.imread(host_path, cv2.IMREAD_GRAYSCALE)
    host_float = np.float32(host)
    rows, cols = host_float.shape

    # 2. 智慧讀取 Logo (處理透明背景 PNG 的問題)
    wmk_img = cv2.imread(wmk_path, cv2.IMREAD_UNCHANGED)
    if len(wmk_img.shape) == 3 and wmk_img.shape[2] == 4:
        # 如果有透明通道，直接拿透明通道當作圖案遮罩
        wmk_gray = wmk_img[:, :, 3]
    else:
        # 否則正常轉灰階
        wmk_gray = cv2.imread(wmk_path, cv2.IMREAD_GRAYSCALE)

    # 將 Logo 二值化為 0 與 1
    _, wmk_binary = cv2.threshold(wmk_gray, 127, 1.0, cv2.THRESH_BINARY)
    
    # 3. DFT 轉換
    dft = cv2.dft(host_float, flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    mag = cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1])
    phase = cv2.phase(dft_shift[:,:,0], dft_shift[:,:,1])

    # 4. 定位與縮放
    block_h, block_w = rows // 8, cols // 8
    wmk_resized = cv2.resize(wmk_binary, (block_w, block_h))

    cy, cx = rows // 2, cols // 2
    offset_y, offset_x = rows // 4, cols // 4

    # 5. 頻域對稱嵌入
    alpha = alpha_factor * np.mean(mag[cy - offset_y : cy - offset_y + block_h, cx - offset_x : cx - offset_x + block_w])
    mag_modified = mag.copy()

    mag_modified[cy - offset_y : cy - offset_y + block_h, cx - offset_x : cx - offset_x + block_w] += alpha * wmk_resized
    mag_modified[cy + offset_y - block_h : cy + offset_y, cx + offset_x - block_w : cx + offset_x] += alpha * cv2.flip(wmk_resized, -1)

    # 6. IDFT 反轉換
    real_modified = mag_modified * np.cos(phase)
    imag_modified = mag_modified * np.sin(phase)
    dft_shift_modified = np.stack((real_modified, imag_modified), axis=2)
    dft_modified = np.fft.ifftshift(dft_shift_modified)
    
    # 【關鍵修復】加入 cv2.DFT_SCALE 讓數值縮放回正常比例！
    img_back = cv2.idft(dft_modified, flags=cv2.DFT_SCALE | cv2.DFT_COMPLEX_OUTPUT)
    wmk_img_float = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])

    # 現在可以安心使用 clip 了，不會變全黑
    wmk_img_clipped = np.clip(wmk_img_float, 0, 255).astype(np.uint8)
    cv2.imwrite('watermarked.png', wmk_img_clipped)
    return 'watermarked.png'

def extract_watermark(wmk_img_path, host_path, alpha_factor=10.0):
    host_float = np.float32(cv2.imread(host_path, cv2.IMREAD_GRAYSCALE))
    wmk_float = np.float32(cv2.imread(wmk_img_path, cv2.IMREAD_GRAYSCALE))
    rows, cols = host_float.shape

    # 雙雙轉換至頻域
    dft_shift_host = np.fft.fftshift(cv2.dft(host_float, flags=cv2.DFT_COMPLEX_OUTPUT))
    mag_host = cv2.magnitude(dft_shift_host[:,:,0], dft_shift_host[:,:,1])

    dft_shift_wmk = np.fft.fftshift(cv2.dft(wmk_float, flags=cv2.DFT_COMPLEX_OUTPUT))
    mag_wmk = cv2.magnitude(dft_shift_wmk[:,:,0], dft_shift_wmk[:,:,1])

    cy, cx = rows // 2, cols // 2
    offset_y, offset_x = rows // 4, cols // 4
    block_h, block_w = rows // 8, cols // 8

    alpha = alpha_factor * np.mean(mag_host[cy - offset_y : cy - offset_y + block_h, cx - offset_x : cx - offset_x + block_w])

    # 減法提取
    extracted_diff = (mag_wmk[cy - offset_y : cy - offset_y + block_h, cx - offset_x : cx - offset_x + block_w] - 
                      mag_host[cy - offset_y : cy - offset_y + block_h, cx - offset_x : cx - offset_x + block_w]) / alpha
    
    # 【關鍵修復】先將提取出的微小數值正規化放大，再搭配 Otsu 自動門檻化找尋最佳黑白切分點
    extracted_norm = cv2.normalize(extracted_diff, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    _, extracted_final = cv2.threshold(extracted_norm, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return extracted_final

if __name__ == "__main__":
    # 確保檔名與你的圖片一致
    host_img_path = "host.png"  # 你的芙莉蓮圖片
    wmk_logo_path = "wmk.png"  # 你的 Cisco Logo

    print("🚀 正在執行頻域浮水印嵌入...")
    result_path = embed_watermark(host_img_path, wmk_logo_path, alpha_factor=15.0) # 強度稍微調高確保抗存檔破壞
    
    print("🔍 正在提取浮水印...")
    extracted = extract_watermark(result_path, host_img_path, alpha_factor=15.0)

    # 繪製結果
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 4, 1); plt.imshow(cv2.imread(host_img_path, 0), cmap='gray'); plt.title('1. Original Host')
    plt.subplot(1, 4, 2); plt.imshow(cv2.imread(wmk_logo_path, cv2.IMREAD_UNCHANGED), cmap='gray'); plt.title('2. Secret Logo')
    plt.subplot(1, 4, 3); plt.imshow(cv2.imread(result_path, 0), cmap='gray'); plt.title('3. Watermarked')
    plt.subplot(1, 4, 4); plt.imshow(extracted, cmap='gray'); plt.title('4. Extracted Logo')
    plt.tight_layout()
    plt.show()