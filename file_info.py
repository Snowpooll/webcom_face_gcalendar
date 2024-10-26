import cv2
import os
import argparse

def main():
    # コマンドライン引数を解析するパーサーを作成
    parser = argparse.ArgumentParser(description="Display image properties")
    parser.add_argument("image_path", help="Path to the image file")
    args = parser.parse_args()

    # 画像を読み込む
    image = cv2.imread(args.image_path)
    if image is None:
        print("画像が読み込めませんでした。")
        return

    # 画像の高さ、幅、チャンネル数を取得
    height, width, channels = image.shape
    print(f"画像の幅: {width} ピクセル")
    print(f"画像の高さ: {height} ピクセル")
    print(f"色チャネル数: {channels}")

    # ファイルサイズを取得
    file_size = os.path.getsize(args.image_path)
    print(f"ファイルサイズ: {file_size} バイト")

if __name__ == '__main__':
    main()

