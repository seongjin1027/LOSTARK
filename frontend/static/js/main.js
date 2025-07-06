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
        nextQuestion(true); // 10초 이상 이탈 시 다음 문제 강제 진행
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
    window.location.href = `/result.html?score=${score}&wrong=${wrong}`;
    return;
  }

  const q = questions[currentIndex];
  document.getElementById("question-title").innerText = q.title;

  const audio = document.getElementById("audio");
  audio.src = q.url;
  audio.play();

  document.getElementById("answer-input").value = "";
}

// 정답 확인
function checkAnswer() {
  const input = document.getElementById("answer-input").value.trim().toLowerCase();
  const keywords = questions[currentIndex].keywords.map(k => k.toLowerCase());

  const isCorrect = keywords.some(keyword => input.includes(keyword));
  if (isCorrect) {
    score += 1;
  } else {
    // 틀린 문제 기록
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

  if (pause) {
    const remaining = questions.slice(currentIndex);
    shuffle(remaining);
    questions = questions.slice(0, currentIndex).concat(remaining);
  }
}

// 페이지 로드 완료 시
document.addEventListener("DOMContentLoaded", function () {
  console.log("main.js loaded");

  // 시작 버튼
  const startBtn = document.getElementById("start-btn");
  if (startBtn) {
    startBtn.addEventListener("click", function () {
      console.log("시작 버튼 클릭됨");
      window.location.href = "/quiz.html";
    });
  }

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
    document.getElementById("score-display").innerText = `당신의 점수: ${score} / 50`;
  }
});
