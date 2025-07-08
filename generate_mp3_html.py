import os

# 입력 mp3 폴더 & 출력 HTML 폴더
audio_dir = "frontend/static/audio"
output_dir = "sound_only_pages"
os.makedirs(output_dir, exist_ok=True)

# HTML 템플릿
template = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>소리만 재생</title>
  <style>
    body {{
      background-color: black;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }}
    .text {{
      color: white;
      font-size: 24px;
      margin-bottom: 20px;
    }}
    button {{
      padding: 10px 20px;
      font-size: 18px;
      cursor: pointer;
    }}
  </style>
</head>
<body>
  <div class="text">재생하려면 클릭하세요</div>
  <button onclick="playAudio()">재생</button>
  <audio id="quiz-audio" src="{audio_path}"></audio>
  <script>
    function playAudio() {{
      const audio = document.getElementById("quiz-audio");
      audio.play();
    }}
  </script>
</body>
</html>
"""

# mp3 파일마다 HTML 생성
for filename in sorted(os.listdir(audio_dir)):
    if filename.endswith(".mp3"):
        number = os.path.splitext(filename)[0].split("-")[-1]
        audio_path = f"static/audio/{filename}"
        html = template.format(audio_path=audio_path)
        with open(os.path.join(output_dir, f"question-{number}.html"), "w", encoding="utf-8") as f:
            f.write(html)

print("✅ MP3 기반 HTML 생성 완료!")
