import os
import glob
import numpy as np
import cv2
import time
from calendar_audio_utils import get_weekly_schedule_with_audio  # カレンダーから予定を取得するためのインポート

COSINE_THRESHOLD = 0.363
NORML2_THRESHOLD = 1.128

# 12時間（秒単位）
THROTTLE_TIME = 12 * 60 * 60
last_called_time = 0  # 最後に呼び出した時間を初期化

def match(recognizer, feature1, dictionary):
    for element in dictionary:
        user_id, feature2 = element
        score = recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
        if score > COSINE_THRESHOLD:
            return True, (user_id, score)
    return False, ("", 0.0)

def call_function_when_recognized(user_id):
    global last_called_time
    current_time = time.time()
    
    # 最後に呼び出してから12時間経過しているかを確認
    if current_time - last_called_time >= THROTTLE_TIME:
        print(f"認識されました: {user_id}")
        
        # 予定を音声再生なしで取得
        schedule = get_weekly_schedule_with_audio(play_audio=False)
        print("予定:", schedule)
        
        # 予定を音声再生ありで取得
        schedule = get_weekly_schedule_with_audio(play_audio=True)
        print("音声で再生される予定:", schedule)
        
        # notice.wavファイル以外の.wavファイルを削除
        cleanup_audio_files(exclude_file="notice.wav")
        
        # 最後に呼び出した時間を更新
        last_called_time = current_time
    else:
        print("まだ12時間経過していないため、次の呼び出しは行われません。")

def cleanup_audio_files(exclude_file):
    """指定された.wavファイル以外の.wavファイルを削除する関数"""
    directory = os.getcwd()  # 現在のディレクトリを取得
    wav_files = glob.glob(os.path.join(directory, "*.wav"))  # すべての.wavファイルを取得

    for wav_file in wav_files:
        if os.path.basename(wav_file) != exclude_file:
            try:
                os.remove(wav_file)  # 指定されたファイル以外を削除
                print(f"削除しました: {wav_file}")
            except OSError as e:
                print(f"ファイル削除エラー: {wav_file}, {e}")

def main():
    directory = os.path.dirname(__file__)
    capture = cv2.VideoCapture(0)  # Use the default camera

    if not capture.isOpened():
        print("Error: The webcam could not be opened.")
        return

    dictionary = []
    files = glob.glob(os.path.join(directory, "*.npy"))
    for file in files:
        feature = np.load(file)
        user_id = os.path.splitext(os.path.basename(file))[0]
        dictionary.append((user_id, feature))

    weights = os.path.join(directory, "face_detection_yunet_2023mar.onnx")
    face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
    weights = os.path.join(directory, "face_recognizer_fast.onnx")
    face_recognizer = cv2.FaceRecognizerSF_create(weights, "")

    while True:
        result, image = capture.read()
        if not result:
            print("Error: No image from webcam.")
            break

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Ensure image is in RGB

        height, width, _ = image.shape
        face_detector.setInputSize((width, height))

        result, faces = face_detector.detect(image)
        faces = faces if faces is not None else []

        for face in faces:
            aligned_face = face_recognizer.alignCrop(image, face)
            feature = face_recognizer.feature(aligned_face)

            result, user = match(face_recognizer, feature, dictionary)

            if result and user[0] != "unknown":
                call_function_when_recognized(user[0])  # 顔が認識された時にカレンダーの予定取得を実行

        # 適当な待機時間を設けてリソースの使用を抑える
        time.sleep(1)

    capture.release()

if __name__ == '__main__':
    main()
