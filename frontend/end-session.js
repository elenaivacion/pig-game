"use strict";

const res = await fetch("end-session.html");
const html = await res.text();
document.body.insertAdjacentHTML("beforeend", html);

const btnEndSession = document.querySelector(".btn--end-session");
const dialogEl = document.getElementById("dialog-end-session");
const btnConfirmEnd = document.getElementById("btn-confirm-end");
const btnCancelEnd = document.getElementById("btn-cancel-end");

const endSession = async function () {
  const token = localStorage.getItem("token");
  const res = await fetch(`${API}/api/end-session`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!res.ok) throw new Error("Login failed!");
  localStorage.removeItem("token");
};

btnEndSession.addEventListener("click", function () {
  dialogEl.classList.remove("hidden");
});

btnCancelEnd.addEventListener("click", function () {
  dialogEl.classList.add("hidden");
});

btnConfirmEnd.addEventListener("click", async function () {
  await endSession();
  window.location.href = "start-session.html";
});
