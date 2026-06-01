import os

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, 'input_photo')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output_photo')

# Algorithm Parameters
# Delta 需設定夠大，才能抵抗轉換為圖片(0~255 uint8)時的失真
SEED = 12345       # 固定 Key，確保每次找的位置一致
EOF_MARKER = '<<EOF>>'