# 🎭 VTuber Tracking Ultimate (Python + MediaPipe + OSC)

Proyek ini menyediakan sistem **full-body upper tracking + face tracking + finger tracking** menggunakan Python, MediaPipe, dan OSC (VMC Protocol).  
File utama: **vtuber selesai.py**

Tracking ini kompatibel dengan:

- **VCFace**
- **Virtual Motion Capture (VMC)**
- **Unity (VMC Receiver)**
- **VRChat (OSC Avatar Tracking)**
- Aplikasi lain yang mendukung `/VMC/Ext/...` protocol

---

## ✨ Fitur Utama

### 🧠 Face Tracking
- Head rotation (pitch, yaw, roll)
- Neck stabilization (gerakan lebih natural)
- Blink detection (EAR method)
- Iris & gaze tracking (left & right)
- Mouth tracking (open/close)

### 🦴 Body Tracking
- Spine roll & yaw
- Upper arm tracking
- Lower arm tracking
- Natural motion compensation

### ✋ Finger Tracking (Lengkap)
- Seluruh 10 jari + 3 bone per jari:
  - Proximal  
  - Intermediate  
  - Distal
- Thumb axis custom
- Finger curl detection berbasis landmark distance
- Sensitivity & axis sign configurable

### 🔧 Smoothing Pro
Menggunakan **Kalman Filter** untuk:
- Head tracking  
- Eye tracking  
- Spine  
- All 10 fingers (20 stabilizer instances)  

### 📡 OSC VMC Compatible Output
Semua bone dikirim sebagai:
```
/VMC/Ext/Bone/Pos
/VMC/Ext/Blend/Val
/VMC/Ext/Root/Pos
```

---

## 📥 Requirements

Instal semua dependensi berikut:

```bash
pip install opencv-python mediapipe python-osc numpy
```

Direkomendasikan Python **3.8 – 3.11**.

---

## ⚙ Konfigurasi Utama

### 🧾 OSC Settings
Atur IP dan PORT agar sesuai aplikasi penerima:

```python
OSC_IP = "10.4.65.149"
OSC_PORT = 39539
```

Contoh port:
- VCFace → 39539  
- VMC → 39540  
- Unity VMC Plugin → 39539  

### 🎥 Webcam

```python
WEBCAM_ID = 0
TARGET_FPS = 30
```

Jika kamera tidak muncul, coba 1 atau 2.

---

## 🔧 Kalibrasi Tracking

### 1. Lengan
```python
ARM_GAIN_XY = 1.2
ARM_GAIN_Z = 0.5
```

### 2. Jari (Finger Axis)
```python
FINGER_AXIS_L = 2   # Z
FINGER_AXIS_R = 2   # Z
```

### 3. Sign (arah rotasi)
```python
FINGER_SIGN_L = 1.0
FINGER_SIGN_R = -1.0
```

### 4. Jempol
```python
THUMB_AXIS_L = 1    # Y
THUMB_AXIS_R = 1
THUMB_SIGN_L = -1.0
THUMB_SIGN_R = 1.0
```

---

## ▶️ Cara Menjalankan

1. Hubungkan webcam.
2. Buka aplikasi penerima OSC (VCFace / VMC / Unity).
3. Jalankan:

```bash
python "vtuber selesai.py"
```

4. Tracking langsung aktif.
5. Tekan **Q** untuk keluar.

---

## 📡 OSC Output yang Dikirim

### Bone (Quaternion)
- Neck  
- Head  
- Spine  
- LeftUpperArm  
- LeftLowerArm  
- RightUpperArm  
- RightLowerArm  
- LeftEye  
- RightEye  

### Finger Bones
- LeftThumbProximal  
- LeftThumbIntermediate  
- LeftThumbDistal  
- RightIndexProximal, dsb...

### Blendshape Output
- `Blink_L`
- `Blink_R`
- `A` (mouth open)

Format pesan:
```
/VMC/Ext/Bone/Pos ["BoneName", px, py, pz, qx, qy, qz, qw]
/VMC/Ext/Blend/Val ["BlendName", value]
```

---

## 🧠 Penjelasan Internal

### Head Pose:
- SolvePnP → transformasi wajah → rotasi kepala
- Deadzone untuk mencegah jitter
- Neck ratio untuk memisahkan gerakan head & neck

### Iris Tracking:
Menggunakan landmark:
- 468 (left iris)
- 473 (right iris)

### Blink Detection:
EAR < 0.15 → blink  
EAR > 0.25 → open  

### Finger Tracking:
Menggunakan jarak:
```
tip → wrist
knuckle → wrist
```
 → lalu dihitung rasio curl

---

## 📚 Referensi File

Script utama:

```
vtuber selesai.py
```

---
