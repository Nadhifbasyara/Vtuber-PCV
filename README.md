# 🎭 VTuber Tracking Ultimate

Skrip `vtuber selesai.py` adalah sistem pelacakan VTuber berbasis Python yang mengirimkan data tracking lewat OSC (VMC/Ext) ke software seperti **VCFace**, **Virtual Motion Capture (VMC)**, atau **Unity**.

---

## 🚀 Fitur Utama

- Face tracking (head rotation, eye movement, mouth)
- Blink detection (EAR)
- Iris/gaze tracking
- Upper body tracking (spine, shoulders, upper/lower arms)
- Full finger tracking (10 jari, 3 bone per jari)
- Kalman Filter stabilizer untuk smoothing
- Konfigurasi kalibrasi axis, sign, dan gain untuk lengan & jari
- Output OSC sesuai format `/VMC/Ext/...`

---

## 📦 Requirement

Pastikan Python 3.8–3.11 terpasang lalu install paket:

```bash
pip install opencv-python mediapipe python-osc numpy
