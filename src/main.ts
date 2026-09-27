import "./style.css";
import { GAME_TITLE, getStatusMessage } from "./core/status";

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) {
  throw new Error("#app が見つかりません");
}

app.innerHTML = `
  <div class="screen">
    <h1>${GAME_TITLE}</h1>
    <p>${getStatusMessage()}</p>
  </div>
`;
