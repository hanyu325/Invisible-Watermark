# Final Project: Invisible Watermark

本專案的目標是寫一個隱形浮水印文字嵌入器，使用者輸入原圖與文字，系統輸出已嵌入文字的圖片。

## Structure

```
Invisible-Watermark/
    README.md
    .gitignore
    requirements.txt
    input_photo/           # Directory for input images
    output_photo/          # Directory for output images
    src/
        main.py                # Main entry point (CLI)
        apply_watermark.py     # Watermark embedding module
        retrieve_watermark.py  # Watermark retrieval module
        qim.py                 # Core QIM algorithm
        utils.py               # Shared utilities (e.g., DFT / IDFT)
        config.py              # Global configurations and parameters
        benchmark.py           # Experimental Test
```

## 使用者體驗

系統開啟時，輸出:
```
Please enter the function you want to use: (Enter 1 or 2)
1. Apply watermark
2. Retrieve watermark
```
---

使用者輸入1，如果有在input_photo folder找到檔案，輸出:
```
Found "檔名" in input_photo folder. Do you want to use this image? (y/n):
```
否則輸出:
```
Didn't find any photo in folder. Please make sure you put the photo in the "input_photo" folder.
Enter "r" to retry, "e" to exit: 
```

使用者輸入y後，輸出:
```
Enter the watermark text you want to apply: 
```

使用者輸入後，輸出:
```
Already applied watermark, please check the output_photo folder. "watermarked.png".
```

---

使用者輸入2，如果有在input_photo folder找到檔案，輸出:
```
Found "檔名" in input_photo folder. Do you want to use this image? (y/n):
```
否則輸出:
```
Didn't find any photo in folder. Please make sure you put the photo in the "input_photo" folder.
Enter "r" to retry, "e" to exit: 
```

使用者輸入y後，系統輸出:
```
Already retrieved the watermark: // 這裡輸出提取的 watermark
```

## Methodology

### 加浮水印步驟
1. 將圖片(input_photo資料夾內的original.png)運用DFT轉換成頻域空間、將使用者輸入的文字加上EOF字符轉換成ASCII Code，再轉換成 binary string
2. 根據設定好的key(寫死在程式裡的)locate到目標位置，並利用QIM技術將轉換好的Binary Code嵌入原圖的頻域空間中
```
0: adjust the spectrum coefficient to the nearest even quantization step.
1: adjust to the nearest odd quantization step.
```
3. 利用IDFT技術將已嵌入文字的頻域空間轉換為圖片，即已加入浮水印之圖片，並輸出至output_photo資料夾內的watermarked.png

### 取出浮水印步驟
1. 將input_photo資料夾內的undecode.png運用DFT轉換成頻域空間
2. 根據設定好的key，找到位置並根據QIM將頻域空間藏的訊息轉換為Binary Code，直到碰到EOF字符
3. 將Binary Code 轉換為ASCII Code，再轉換為Text，並輸出