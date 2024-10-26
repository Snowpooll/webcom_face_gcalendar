import cv2
import os
import argparse

def main():
    # コマンドライン引数を解析するパーサーを作成
    parser = argparse.ArgumentParser(description="Resize and save an image")
    parser.add_argument("image_path", help="Path to the image file")
    args = parser.parse_args()

    # 画像を読み込む
    image = cv2.imread(args.image_path)
    if image is None:
        print("画像が読み込めませんでした。")
        return

    # 画像の元の高さ、幅を取得
    height, width = image.shape[:2]

    # 新しい寸法を計算（元のサイズの1/4）
    new_width = width // 4
    new_height = height // 4

    # 画像をリサイズ
    resized_image = cv2.resize(image, (new_width, new_height))

    # 新しいファイル名を設定
    new_file_path = os.path.splitext(args.image_path)[0] + "_quarter.jpg"

    # リサイズした画像を保存
    cv2.imwrite(new_file_path, resized_image)
    print(f"リサイズされた画像が保存されました: {new_file_path}")

if __name__ == '__main__':
    main()
