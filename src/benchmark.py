import os
import time
import cv2
from skimage.metrics import structural_similarity as ssim

# 假設你已經按照先前的修改完成了動態 Delta 的版本
from src.apply_watermark import apply_watermark
from src.retrieve_watermark import retrieve_watermark

def run_benchmark():
    orig_path = "input_photo/original.png"
    watermarked_path = "output_photo/watermarked.png"
    secret_text = "frieren, 2026.06.01"  # 你可以換成任何你想測試的文字
    
    if not os.path.exists(orig_path):
        print(f"Please place an image at {orig_path} first.")
        return
    
    print("=== Starting benchmark analysis ===")
    
    # 1. 測試嵌入時間
    start_embed = time.time()
    apply_watermark(orig_path, secret_text, watermarked_path)
    end_embed = time.time()
    embed_time = end_embed - start_embed
    
    # 2. 測試提取時間與正確性
    start_extract = time.time()
    extracted_text = retrieve_watermark(watermarked_path)
    end_extract = time.time()
    extract_time = end_extract - start_extract
    
    # 3. 計算畫質指標
    img_orig = cv2.imread(orig_path)
    img_wm = cv2.imread(watermarked_path)
    psnr_val = cv2.PSNR(img_orig, img_wm)
    ssim_val = ssim(img_orig, img_wm, channel_axis=2)
    
    # 4. 計算最大容載量
    rows, cols, _ = img_orig.shape
    max_bits = (rows * cols) // 2 - 1
    max_chars = max_bits // 8

    # Output results (you can directly use this for reporting)
    print("\n=== Experimental Results ===")
    print(f"Test image resolution: {rows} x {cols}")
    print(f"Imperceptibility - PSNR: {psnr_val:.2f} dB")
    print(f"Imperceptibility - SSIM: {ssim_val:.4f}")
    print(f"Embedding time: {embed_time:.4f} seconds")
    print(f"Extraction time: {extract_time:.4f} seconds")
    print(f"Theoretical maximum capacity: {max_bits} bits ({max_chars} characters)")
    print(f"Extracted text: {extracted_text}")
    print(f"Extraction status: {'Success (100% correct)' if extracted_text == secret_text else 'Failure'}")

if __name__ == "__main__":
    run_benchmark()