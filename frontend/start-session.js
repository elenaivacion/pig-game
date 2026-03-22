"use strict";

const API = "http://localhost:5000";

const inputUserIdEl = document.getElementById("input-user");
const btnEnterEl = document.getElementById("btn-enter");
const sessionErrorEl = document.getElementById("session-error");

const startSession = async function (userId) {
  const res = await fetch(`${API}/api/start-session`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId }),
  });

  if (!res.ok) throw new Error("Login failed!");
};

btnEnterEl.addEventListener("click", async function () {
  const userId = inputUserIdEl.value.trim();
  if (!userId) return;

  try {
    sessionErrorEl.classList.add("hidden");
    await startSession(userId);
    window.location.href = "index.html";
  } catch {
    sessionErrorEl.classList.remove("hidden");
  }
});
