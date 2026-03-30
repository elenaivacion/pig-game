# 🎲 Pig Game: API Testing & Automation Workflow

This repository documents my end-to-end testing process for the **"Pig Game"** API. I built this project to bridge the gap between manual testing and full CI/CD automation, ensuring that the game's logic remains robust through every update.

## 📌 Project Overview

The game's backend is built using **Flask** (utilizing _Flasgger_ for Swagger documentation). Because the game is self-contained, the backend is responsible for both serving the frontend UI and managing the core game mechanics through a series of RESTful endpoints.

---

## 1. API Structure & Categorization

I analyzed the Swagger documentation and organized the test suite into two logical categories:

### 🟢 Public Endpoints (No Auth Required)

| Endpoint      | Method | Description                                    |
| :------------ | :----- | :--------------------------------------------- |
| `/`           | `GET`  | Serves the main game interface (`index.html`). |
| `/api/status` | `GET`  | Health-check to verify the backend is active.  |

### 🔴 Private Endpoints (Requires Bearer Token)

These endpoints handle the "heavy lifting" of the game state:

- **Session Management:** `/api/start-session` (token generation) and `/api/end-session` (cleanup).
- **Game Mechanics:** `/api/init` (state reset), `/api/roll` (dice logic), and `/api/hold` (scoring).

---

## 2. Testing Strategy in Postman

My approach focused on moving beyond simple "status 200" checks to ensure the API is secure, stable, and logically consistent.

### A. Positive Testing ("The Happy Path")

For every endpoint, I implemented JavaScript validation scripts to confirm:

- **Functional Accuracy:** E.g., for `/api/roll`, I wrote scripts to ensure the `dice` value is always an integer between 1 and 6.
- **Data Integrity:** Verifying that the JSON response structure matches the Swagger schema exactly.

### B. Negative & Security Testing

To ensure the API is "bulletproof," I tested its limits:

- **Auth Gates:** I verified that private endpoints return `401 Unauthorized` when the token is missing or expired, ensuring no game data is leaked.
- **Logic Constraints:** I tested scenarios such as attempting a `hold` action before any `roll` has occurred to ensure the state machine doesn't break.

### C. Advanced Scripting (Pre-requests)

To achieve full automation, I used **Pre-request Scripts** to handle session dependencies. For example:

> Before the `/api/hold` test runs, a script automatically triggers `/api/start-session` and `/api/init` to ensure a valid environment, making each test modular and independent.

---

## 3. Automation & CI/CD Integration

To ensure high code quality with every commit, I integrated the following tools:

- **Newman:** Used as the command-line collection runner to execute Postman tests outside the GUI.
- **GitHub Actions:** I configured a `.yml` workflow that triggers the entire test suite on every `push` or `pull request`. This provides immediate feedback on whether new changes have caused regressions.

### 📊 Live Test Execution Status

To ensure transparency, the statistics below are pulled directly from the latest CI/CD pipeline run:

| Metric           | Status                                                                                                                                                                          |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Latest Build** | [![API Regression Tests](https://github.com/elenaivacion/pig-game/actions/workflows/postman-tests.yml/badge.svg?branch=main)](https://github.com/elenaivacion/pig-game/actions) |
| **Test Engine**  | ![Newman](https://img.shields.io/badge/Engine-Newman-orange)                                                                                                                    |
| **Environment**  | ![Ubuntu](https://img.shields.io/badge/OS-Ubuntu--Latest-blue)                                                                                                                  |

> **Note on Test Counts:** My current Postman collection covers **all core endpoints** defined in the Swagger documentation, including positive, negative, and edge-case scenarios. You can see the full execution breakdown by clicking the "Build Status" badge above to view the logs.

---

## 4. Roadmap & Future Improvements

- [ ] **Edge Case Coverage:** Adding tests for maximum score limits and rapid-fire requests.
- [ ] **Visual Reporting:** Integrating HTML-based reports (like Newman-reporter-htmlextra) into the CI/CD pipeline.
- [ ] **Frontend Automation:** Expanding my expertise into UI testing to cover the end-user experience.

---

### 🛠️ Tech Stack & Tools

![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
