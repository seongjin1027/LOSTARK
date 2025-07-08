let currentIndex = 0;
let questions = [];
let score = 0;
let pause = false;
let tabInactiveTime = 0;
let timer;
let wrongAnswers = [];

// 탭 이탈 감지
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    timer = setInterval(() => {
      tabInactiveTime += 1;
      if (tabInactiveTime >= 10) {
        nextQuestion(true);
      }
    }, 1000);
  } else {
    clearInterval(timer);
    tabInactiveTime = 0;
  }
});

// 배열 섞기
function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

// 퀴즈 문제 불러오기
function fetchQuestions() {
  fetch("/api/questions/")
    .then(res => res.json())
    .then(data => {
      questions = data;
      shuffle(questions);
      showQuestion();
    });
}

// 현재 문제 보여주기
function showQuestion() {
  if (currentIndex >= questions.length) {
    const wrong = encodeURIComponent(JSON.stringify(wrongAnswers));

    // ✅ 닉네임과 점수를 서버에 제출
    fetch("/api/submit/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        nickname: window.nickname || "익명",
        score: score
      }),
    })
      .then(res => res.json())
      .then(data => {
        console.log("서버 저장 완료:", data);
        // 결과 페이지 이동
        window.location.href = `/result.html?name=${encodeURIComponent(window.nickname)}&score=${score}&wrong=${wrong}`;
      })
      .catch(error => {
        console.error("서버 전송 실패:", error);
        alert("결과 저장에 실패했습니다.");
        window.location.href = `/result.html?name=${encodeURIComponent(window.nickname)}&score=${score}&wrong=${wrong}`;
      });

    return;
  }

  const q = questions[currentIndex];
  console.log("오디오 경로:", q.audio);

  const audio = document.getElementById("quiz-audio");
  audio.src = q.audio;
  audio.play();

  document.getElementById("answer-input").value = "";
}

// 정답 확인
function checkAnswer() {
  const input = document.getElementById("answer-input").value.trim().toLowerCase();
  const keywords = questions[currentIndex].answer.map(k => k.toLowerCase());

  const isCorrect = keywords.some(keyword => input.includes(keyword));
  if (isCorrect) {
    score += 1;
  } else {
    wrongAnswers.push({
      index: currentIndex + 1,
      input,
      keywords
    });
  }

  nextQuestion();
}

// 다음 문제로
function nextQuestion(force = false) {
  if (pause && !force) return;
  currentIndex += 1;
  showQuestion();
}

// 일시정지 & 재개
function togglePause() {
  pause = !pause;
  const overlay = document.getElementById("pause-overlay");
  overlay.style.display = pause ? "flex" : "none";
}

// 재생 버튼
function playAudio() {
  const audio = document.getElementById("quiz-audio");
  if (audio) {
    audio.play();
  } else {
    console.error("오디오 요소가 없습니다.");
  }
}

// 페이지 로드 시 실행
document.addEventListener("DOMContentLoaded", function () {
  console.log("main.js loaded");

  // 퀴즈 페이지
  if (document.getElementById("quiz-container")) {
    fetchQuestions();
    document.getElementById("submit-btn").onclick = checkAnswer;
    document.getElementById("pause-btn").onclick = togglePause;
    document.getElementById("resume-btn").onclick = togglePause;
  }

  // 결과 페이지
  if (document.getElementById("score-display")) {
    const params = new URLSearchParams(window.location.search);
    const score = params.get("score");
    const nickname = params.get("name");
    document.getElementById("score-display").innerText = `${nickname}님의 점수: ${score} / 50`;
  }
});

