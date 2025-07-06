window.onload = function () {
  const params = new URLSearchParams(window.location.search);
  const score = params.get("score");

  document.getElementById("score-display").innerText = `당신의 점수: ${score} / 50`;

  fetch("/api/submit/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      score: parseInt(score),
    }),
  });
};
