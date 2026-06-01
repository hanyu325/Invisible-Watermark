import os
import sys
from src.config import INPUT_DIR, OUTPUT_DIR
from src.apply_watermark import apply_watermark
from src.retrieve_watermark import retrieve_watermark

def get_input_file():
    """Handle the folder scanning and user confirmation logic."""
    while True:
        if not os.path.exists(INPUT_DIR):
            os.makedirs(INPUT_DIR)
            
        files = os.listdir(INPUT_DIR)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if image_files:
            filename = image_files[0]
            ans = input(f'Found "{filename}" in input_photo folder. Do you want to use this image? (y/n):\n').strip().lower()
            if ans == 'y':
                return os.path.join(INPUT_DIR, filename)
            # 如果輸入 n，會繼續往下觸發重試機制
        
        # 找不到檔案，或是剛剛使用者選擇不用該圖片
        ans = input('Didn\'t find any photo in folder. Please make sure you put the photo in the "input_photo" folder.\nEnter "r" to retry, "e" to exit:\n').strip().lower()
        if ans == 'e':
            sys.exit(0)

def main():
    # 確保資料夾存在
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Please enter the function you want to use: (Enter 1 or 2)")
    print("1. Apply watermark")
    print("2. Retrieve watermark")
    
    choice = input().strip()
    
    if choice == '1':
        img_path = get_input_file()
        text = input('Enter the watermark text you want to apply:\n')
        
        output_filename = "watermarked.png"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        apply_watermark(img_path, text, output_path)
        print(f'Already applied watermark, please check the output_photo folder. "{output_filename}".')
        
    elif choice == '2':
        img_path = get_input_file()
        watermark = retrieve_watermark(img_path)
        
        print(f'Already retrieved the watermark: {watermark}')
        
    else:
        print("Invalid choice, exiting.")

if __name__ == "__main__":
    main()