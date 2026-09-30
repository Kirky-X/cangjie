# SKIPPED — 冒烟级离线测试未覆盖项说明

原则：副作用脚本（模型下载/GPU 推理/真实转码）不写假测试。以下为有意跳过的部分及原因。

## transcribe_diarize_fw.py

- `transcribe_with_diarization()`：需下载 faster-whisper `large-v3` 模型（数 GB，网络+磁盘副作用），
  并依赖 torch/cuda 探测。属典型副作用流程，只保留 `--help` 与缺文件退出码冒烟
  （校验发生在模型导入之前，见 test_cli_smoke.py），核心转写逻辑不做离线假测试。
- `detect_speaker_changes()`：依赖 librosa，本环境未安装且约束为离线不装依赖，
  能量分段算法无法真实执行，不 mock 伪造结果。
- 两个函数的参数默认值/auto 语言处理已在 test_transcribe_arg_handling.py 中通过
  mock 转写函数做真实测试（仅拦截调用，不伪造转写结果）。

## transcribe_with_diarization.py

- `transcribe_audio()`：需下载 `Qwen/Qwen3-ASR-1.7B` 模型，同上跳过；
  参数处理已覆盖，`--help`/缺文件退出码已冒烟。

## extract_audio.py

- 真实 ffmpeg 解出音轨：本环境无 ffmpeg，且真实转码属副作用；已用 mock subprocess.run
  覆盖命令参数构造（16kHz/mono/pcm_s16le）、输出路径推导与全部错误分支，
  不在测试中真的跑 ffmpeg。

## 覆盖口径

- 覆盖：纯函数真实行为（utils）、CLI 参数解析与分发校验（cangjie.py）、
  ffmpeg 命令构造与错误包装（extract_audio.py，mock）、转写入口参数处理（mock）、
  四入口 `--help` 与缺文件退出码（子进程冒烟）。
- 跳过：任何需要下载模型、GPU 推理、真实 ffmpeg 转码或 librosa 的路径（原因见上）。
