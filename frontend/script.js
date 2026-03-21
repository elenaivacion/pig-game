"use strict";

const API = "http://localhost:5000";

// Selecting elements
const player0El = document.querySelector(".player--0");
const player1El = document.querySelector(".player--1");
const score0El = document.querySelector("#score--0");
const score1El = document.getElementById("score--1");
const current0El = document.getElementById("current--0");
const current1El = document.getElementById("current--1");
const diceEl = document.querySelector(".dice");
const btnNew = document.querySelector(".btn--new");
const btnRoll = document.querySelector(".btn--roll");
const btnHold = document.querySelector(".btn--hold");

let scores, currentScore, activePlayer, playing;

// Starting conditions

function applyState(state) {
  switch (state.action) {
    case "new":
      score0El.textContent = 0;
      score1El.textContent = 0;
      current0El.textContent = 0;
      current1El.textContent = 0;
      diceEl.classList.add("hidden");
      player0El.classList.remove("player--winner");
      player1El.classList.remove("player--winner");
      player0El.classList.add("player--active");
      player1El.classList.remove("player--active");
      break;

    case "update":
      diceEl.classList.remove("hidden");
      diceEl.src = `dice-${state.dice}.png`;
      document.getElementById(`current--${state.activePlayer}`).textContent =
        state.currentScore;
      break;

    case "switch":
      diceEl.classList.remove("hidden");
      diceEl.src = `dice-${state.dice}.png`;
      score0El.textContent = state.scores[0];
      score1El.textContent = state.scores[1];
      document.getElementById(
        `current--${1 - state.activePlayer}`,
      ).textContent = 0;
      player0El.classList.toggle("player--active");
      player1El.classList.toggle("player--active");
      break;

    case "winner":
      score0El.textContent = state.scores[0];
      score1El.textContent = state.scores[1];
      diceEl.classList.add("hidden");
      document
        .querySelector(`.player--${state.winner}`)
        .classList.add("player--winner");
      document
        .querySelector(`.player--${state.winner}`)
        .classList.remove("player--active");
      break;
  }
}

const init = async function () {
  const res = await fetch(`${API}/api/init`, {
    method: "POST",
  });
  applyState(await res.json());
};
init();

// Rolling dice functionality
btnRoll.addEventListener("click", async function () {
  const res = await fetch(`${API}/api/roll`, {
    method: "POST",
  });
  applyState(await res.json());
});

btnHold.addEventListener("click", async function () {
  const res = await fetch(`${API}/api/hold`, {
    method: "POST",
  });
  applyState(await res.json());
});

btnNew.addEventListener("click", async function () {
  init();
});
