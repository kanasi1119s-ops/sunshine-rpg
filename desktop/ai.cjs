// デスクトップ版の本体の側で、Claude に曲を書いてもらう（キーは本体の側だけにある）。
const Anthropic = require("@anthropic-ai/sdk").default;

const MODELS = new Set(["claude-opus-5-5", "claude-sonnet-5-5"]);
const EFFORTS = new Set(["low", "medium", "high"]);

async function composeWithClaude({ apiKey, model, effort, request, system, schema, history }) {
  if (!MODELS.has(model)) throw new Error("モデルの指定が違います");
  if (!EFFORTS.has(effort)) throw new Error("考える深さの指定が違います");
  if (typeof request !== "string" || !request.trim() || request.length > 20000) throw new Error("依頼の文を入れてください");
  if (typeof system !== "string" || typeof schema !== "object" || !schema) throw new Error("作曲の説明がありません");
  const client = new Anthropic({ apiKey });
  const messages = [...history, { role: "user", content: request }];
  const stream = client.beta.messages.stream({
    model,
    max_tokens: 64000,
    // 安全のための判定で断られたときは、サーバー側で別のモデルに引き継ぐ
    betas: ["server-side-fallback-2026-07-01"],
    fallbacks: "default",
    system: [{ type: "text", text: system, cache_control: { type: "ephemeral" } }],
    output_config: { effort, format: { type: "json_schema", schema } },
    messages,
  });
  let message;
  try {
    message = await stream.finalMessage();
  } catch (error) {
    throw new Error(describeError(error));
  }
  if (message.stop_reason === "refusal") throw new Error("この依頼は、AIに断られました。依頼の文を変えてみてください。");
  if (message.stop_reason === "max_tokens") throw new Error("曲が長すぎて、途中で切れました。もう少し短い曲を頼んでください。");
  const text = message.content.filter((b) => b.type === "text").map((b) => b.text).join("");
  messages.push({ role: "assistant", content: message.content });
  return { text, history: messages, usage: { input: message.usage.input_tokens, output: message.usage.output_tokens } };
}

function describeError(error) {
  if (error instanceof Anthropic.AuthenticationError) return "APIキーが正しくありません。Anthropic のコンソールで確かめてください。";
  if (error instanceof Anthropic.PermissionDeniedError) return "このAPIキーでは、このモデルを使えません。";
  if (error instanceof Anthropic.RateLimitError) return "短い時間に使いすぎました。少し待ってから、もう一度ためしてください。";
  if (error instanceof Anthropic.BadRequestError) return `依頼を受け付けてもらえませんでした: ${error.message}`;
  if (error instanceof Anthropic.APIConnectionError) return "インターネットにつながりませんでした。";
  if (error instanceof Anthropic.APIError) return `AIのサービスでエラーが起きました（${error.status ?? "?"}）: ${error.message}`;
  return String(error && error.message ? error.message : error);
}

module.exports = { composeWithClaude };
