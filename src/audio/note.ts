const NOTE_OFFSETS: Record<string, number> = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };

/** "C4" のような音名をMIDIノート番号にする（C4=60、A4=69）。 */
export function noteNameToMidi(name: string): number {
  const match = /^([A-G])([#b]?)(-?\d+)$/.exec(name);
  if (!match) {
    throw new Error(`不正な音名です: ${name}`);
  }
  const [, letter, accidental, octaveStr] = match;
  let semitone = NOTE_OFFSETS[letter];
  if (accidental === "#") {
    semitone += 1;
  } else if (accidental === "b") {
    semitone -= 1;
  }
  const octave = Number.parseInt(octaveStr, 10);
  return (octave + 1) * 12 + semitone;
}

/** MIDIノート番号を周波数（Hz）にする。 */
export function midiToFrequency(midiNote: number): number {
  return 440 * Math.pow(2, (midiNote - 69) / 12);
}

export function noteNameToFrequency(name: string): number {
  return midiToFrequency(noteNameToMidi(name));
}
