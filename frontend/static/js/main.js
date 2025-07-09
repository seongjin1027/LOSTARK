let currentIndex = 0;
let questions = [];
let score = 0;
let pause = false;
let tabInactiveTime = 0;
let timer;
let wrongAnswers = [];
let waitingForNext = false;

// 문제 번호 및 남은 문제 수 표시
function updateQuestionStatus() {
  const status = document.getElementById("question-number");
  const current = currentIndex + 1;
  const total = questions.length;
  const remaining = total - current;
  if (status) {
    status.textContent = `${current} / ${total}번째 문제 (남은 문제: ${remaining})`;
  }
}

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
  waitingForNext = false;

  const overlay = document.getElementById("feedback-overlay");
  if (overlay) overlay.style.display = "none";

  if (currentIndex >= questions.length) {
    const wrong = encodeURIComponent(JSON.stringify(wrongAnswers));
    fetch("/api/submit/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nickname: window.nickname || "익명",
        score: score
      }),
    })
      .then(res => res.json())
      .then(() => {
        window.location.href = `/result.html?name=${encodeURIComponent(window.nickname)}&score=${score}&wrong=${wrong}`;
      })
      .catch(() => {
        alert("결과 저장에 실패했습니다.");
        window.location.href = `/result.html?name=${encodeURIComponent(window.nickname)}&score=${score}&wrong=${wrong}`;
      });
    return;
  }

  updateQuestionStatus();

  const q = questions[currentIndex];
  const audio = document.getElementById("quiz-audio");
  audio.src = q.audio;
  audio.pause();
  audio.currentTime = 0;

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

  showFeedback(isCorrect);
}

// 정답/오답 피드백
function showFeedback(isCorrect) {
  const overlay = document.getElementById("feedback-overlay");
  const message = document.getElementById("feedback-message");
  message.textContent = isCorrect ? "✅ 정답입니다!" : "❌ 오답입니다!";
  overlay.style.display = "flex";
  waitingForNext = true;
}

// 다음 문제로 이동
function nextQuestion(force = false) {
  if ((pause && !force) || waitingForNext) return;
  currentIndex += 1;
  showQuestion();
}

// 일시정지
function togglePause() {
  pause = !pause;
  const overlay = document.getElementById("pause-overlay");
  overlay.style.display = pause ? "flex" : "none";

  const audio = document.getElementById("quiz-audio");
  if (pause && audio && !audio.paused) {
    audio.pause();
  }
}

// 재생 버튼
function playAudio() {
  const audio = document.getElementById("quiz-audio");
  if (audio) {
    audio.play();
  }
}

// 페이지 로딩 시
document.addEventListener("DOMContentLoaded", function () {
  if (document.getElementById("quiz-container")) {
    fetchQuestions();
    document.getElementById("submit-btn").onclick = checkAnswer;
    document.getElementById("pause-btn").onclick = togglePause;
    document.getElementById("resume-btn").onclick = togglePause;

    const nextBtn = document.getElementById("next-btn");
    if (nextBtn) {
      nextBtn.onclick = () => {
        const overlay = document.getElementById("feedback-overlay");
        if (overlay) overlay.style.display = "none";
        waitingForNext = false;
        currentIndex += 1;
        showQuestion();
      };
    }
  }

  if (document.getElementById("score-display")) {
    const params = new URLSearchParams(window.location.search);
    const score = params.get("score");
    const nickname = params.get("name");
    document.getElementById("score-display").innerText = `${nickname}님의 점수: ${score} / 50`;
  }
});
