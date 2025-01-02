import os
import argparse
from moviepy import *

# 함수 정의
def create_video(image_folder, output_video_path):
    # 이미지 목록을 저장할 리스트
    image_files = []

    # 폴더에서 GIF와 PNG 파일을 읽어 목록에 추가
    for file in os.listdir(image_folder):
        if file.endswith('.gif') or file.endswith('.png'):
            image_files.append(os.path.join(image_folder, file))

    # 이미지 파일들을 이름 순으로 정렬
    image_files.sort()  # 알파벳 순으로 정렬

    if not image_files:
        print("이미지 파일이 폴더에 없습니다. GIF 또는 PNG 파일이 필요합니다.")
        return

    # 이미지 파일들을 비디오로 변환
    clips = []
    for img_file in image_files:
        print(img_file)
        clip = None  # clip 변수 초기화 (GIF 및 PNG 모두에 대해 사용될 수 있게)
        if img_file.endswith('.gif'):
            # GIF 파일을 비디오 클립으로 변환 (경로를 큰따옴표로 감싸서 전달)
            gif_clip = VideoFileClip(img_file)
            clip = gif_clip  # clip에 gif 클립 저장

            
        elif img_file.endswith('.png'):
            # PNG 이미지를 비디오 클립으로 변환 (1초 길이로 설정)
            clip = ImageClip(img_file)# 1초 동안 표시
            clip.duration = 5.0            
        else :
            continue
            
        if clip.size[0] +  clip.size[1] > 1500:
            resizedWidth = 1500 / (clip.size[0] +  clip.size[1]) * clip.size[0]
            clip = clip.with_effects([vfx.Resize(width=resizedWidth)])
        elif clip.size[0] +  clip.size[1] < 500:
            resizedWidth = 500 / (clip.size[0] +  clip.size[1]) * clip.size[0]
            clip = clip.with_effects([vfx.Resize(width=resizedWidth)])

        # 파일명을 자막으로 추가
        file_name = os.path.basename(img_file)  # 파일명 추출
        txt_clip = TextClip("NanumSquareB.ttf", method='caption', text=file_name, font_size=12, color='white', bg_color='black', size = [clip.size[0], None])

        # 텍스트 자막과 이미지 비디오 클립을 합침
        clip_with_text = CompositeVideoClip([clip, txt_clip])
        clip_with_text.duration = clip.duration
        clips.append(clip_with_text) # 마지막 클립에 텍스트 합침

    if not clips:
        print("클립을 생성하는 동안 문제가 발생했습니다. 이미지 파일들이 유효한지 확인하세요.")
        return

    # 모든 클립을 이어 붙이기
    final_clip = concatenate_videoclips(clips, method="compose")

    # 비디오 출력 (경로를 큰따옴표로 감싸서 처리)
    final_clip.write_videofile(output_video_path, codec='libx264', fps=24)
    print(f"비디오가 {output_video_path}에 저장되었습니다.")

# 커맨드라인 인자 처리
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GIF 및 PNG 파일들을 비디오로 변환")
    parser.add_argument("image_folder", type=str, help="GIF 및 PNG 파일들이 있는 폴더 경로")

    args = parser.parse_args()

    # 상대 경로를 절대 경로로 변환
    image_folder = os.path.abspath(args.image_folder)
    output_video_path = 'result.mp4'

    # 경로가 유효한지 확인
    if not os.path.exists(image_folder):
        print(f"지정된 이미지 폴더가 존재하지 않습니다: {image_folder}")
    else:
        # 비디오 생성 함수 호출
        create_video(image_folder, output_video_path)
