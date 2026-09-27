/** 1文字ずつ幅を測りながら、指定した幅を超えないように改行する。 */
export function wrapText(
  text: string,
  maxWidth: number,
  measure: (segment: string) => number,
): string[] {
  const lines: string[] = [];
  let current = "";

  for (const char of text) {
    if (char === "\n") {
      lines.push(current);
      current = "";
      continue;
    }
    const attempt = current + char;
    if (current.length > 0 && measure(attempt) > maxWidth) {
      lines.push(current);
      current = char;
    } else {
      current = attempt;
    }
  }
  lines.push(current);
  return lines;
}
