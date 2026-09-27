export interface DebugMenuState {
  open: boolean;
  cursor: number;
}

export function createDebugMenuState(): DebugMenuState {
  return { open: false, cursor: 0 };
}

export function toggleMenu(state: DebugMenuState, itemCount: number): DebugMenuState {
  const open = !state.open;
  return { open, cursor: open ? Math.min(state.cursor, Math.max(0, itemCount - 1)) : state.cursor };
}

export function moveMenuCursor(state: DebugMenuState, delta: number, itemCount: number): DebugMenuState {
  if (!state.open || itemCount === 0) {
    return state;
  }
  const cursor = (state.cursor + delta + itemCount) % itemCount;
  return { ...state, cursor };
}
