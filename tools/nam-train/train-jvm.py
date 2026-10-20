# 作曲ソフト用の NAM（学習式アンプ）のモデルを、録音データから学習する（2026-10-21）。CPU では 1 周 3 分ほど。tkinter の無い環境では空の tkinter を PYTHONPATH に置く。
# マーシャル JVM410H のデータ（Miklánek ほか、CC BY 4.0、doi:10.5281/zenodo.7970723）から、NAM（学習式アンプ）のモデルを作る。
# 使い方: PYTHONPATH=/tmp/namstub python3 train.py G4 30
import sys, json, pathlib, torch
from nam.train import full
g, epochs = sys.argv[1], int(sys.argv[2])
torch.set_num_threads(2)
out = pathlib.Path(f"/tmp/jvm/out-{g}"); out.mkdir(exist_ok=True)
SR = 48000; total = 395 * SR; vstart = int(total * 0.88)
data = {
  "train": {"ny": 8192, "stop_samples": vstart},
  "validation": {"ny": None, "start_samples": vstart, "require_input_pre_silence": False},
  "common": {"x_path": f"/tmp/jvm/train/{g}-input.wav", "y_path": f"/tmp/jvm/train/{g}-speakerout.wav", "delay": 0, "allow_unequal_lengths": True},
  "joint": [{"name": "nam.data.normalize_joint_dataset_output", "kwargs": {"level_rms_dbfs": -18.0}}],
}
# 「lite」相当の WaveNet（CPU で学習できる小ささ）
acts = [{"type": "LeakyReLU", "negative_slope": 0.01}] * 23
model = {
  "net": {"name": "WaveNet", "config": {"layers_configs": [
      {"input_size": 1, "condition_size": 1, "channels": 8,
       "kernel_sizes": [6]*14 + [15, 15] + [6]*7,
       "dilations": [1, 3, 7, 17, 41, 101, 239, 1, 3, 7, 17, 41, 101, 239, 1, 13, 1, 3, 7, 17, 41, 101, 239],
       "activation": "LeakyReLU", "gated": False, "head": {"out_channels": 1, "kernel_size": 16, "bias": True}}],
    "head_scale": 0.01}},
  "loss": {"val_loss": "esr", "mrstft_weight": 0.0005},
  "optimizer": {"lr": 0.004, "weight_decay": 3.17e-07},
  "lr_scheduler": {"class": "ExponentialLR", "kwargs": {"gamma": 0.99}},
}
learning = {"train_dataloader": {"batch_size": 16, "shuffle": True, "pin_memory": False, "drop_last": True, "num_workers": 0},
            "val_dataloader": {}, "trainer": {"max_epochs": epochs, "accelerator": "cpu"}}
full.main(data, model, learning, out, no_show=True, make_plots=False)
print("done", g)
