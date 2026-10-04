import { describe, expect, it } from "vitest";
import { createCamera, centerCameraOn } from "./camera";

describe("centerCameraOn", () => {
  it("マップが画面より十分大きいとき、対象を画面中央に映す", () => {
    const camera = createCamera(400, 200);
    const result = centerCameraOn(camera, 1000, 500, 2000, 1000);
    expect(result.x).toBe(1000 - 200);
    expect(result.y).toBe(500 - 100);
  });

  it("マップの左端・上端を超えないようにする", () => {
    const camera = createCamera(400, 200);
    const result = centerCameraOn(camera, 10, 10, 2000, 1000);
    expect(result.x).toBe(0);
    expect(result.y).toBe(0);
  });

  it("マップの右端・下端を超えないようにする", () => {
    const camera = createCamera(400, 200);
    const result = centerCameraOn(camera, 1990, 990, 2000, 1000);
    expect(result.x).toBe(2000 - 400);
    expect(result.y).toBe(1000 - 200);
  });

  it("マップが画面より小さいときは、マップを画面の中央に置く（家の中など）", () => {
    const camera = createCamera(400, 200);
    const result = centerCameraOn(camera, 50, 50, 100, 80);
    expect(result.x).toBe(-150);
    expect(result.y).toBe(-60);
  });
});

describe("カメラの位置は整数（タイルの継ぎ目に黒い線が出ないように）", () => {
  it("小数の座標を中心にしても、カメラの位置は整数になる", () => {
    const cam = centerCameraOn(createCamera(100, 80), 123.37, 90.62, 400, 300);
    expect(Number.isInteger(cam.x)).toBe(true);
    expect(Number.isInteger(cam.y)).toBe(true);
  });
});
