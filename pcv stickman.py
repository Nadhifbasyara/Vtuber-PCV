import cv2
import mediapipe as mp
import time
import numpy as np

# =============================
#   Inisialisasi MediaPipe
# =============================
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
pTime = 0

print("Program berjalan. Tekan 'q' untuk keluar.")


# ==================================================
#   FUNGSI MENGGAMBAR STICKMAN (KEPALA BESAR + JARI)
# ==================================================
def draw_stickman(frame, lm):
    h, w, c = frame.shape

    # Fungsi untuk ambil koordinat landmark
    def C(part):
        p = lm[mp_pose.PoseLandmark[part].value]
        return int(p.x * w), int(p.y * h)

    # Titik tubuh
    head = C("NOSE")
    shoulder_r = C("RIGHT_SHOULDER")
    shoulder_l = C("LEFT_SHOULDER")
    elbow_r = C("RIGHT_ELBOW")
    elbow_l = C("LEFT_ELBOW")
    wrist_r = C("RIGHT_WRIST")
    wrist_l = C("LEFT_WRIST")
    hip_r = C("RIGHT_HIP")
    hip_l = C("LEFT_HIP")
    knee_r = C("RIGHT_KNEE")
    knee_l = C("LEFT_KNEE")
    ankle_r = C("RIGHT_ANKLE")
    ankle_l = C("LEFT_ANKLE")

    # =====================
    #      KEPALA BESAR
    # =====================
    cv2.circle(frame, head, 45, (255, 255, 255), 4)

    # Badan
    mid_shoulder = ((shoulder_r[0] + shoulder_l[0]) // 2,
                    (shoulder_r[1] + shoulder_l[1]) // 2)
    mid_hip = ((hip_r[0] + hip_l[0]) // 2,
               (hip_r[1] + hip_l[1]) // 2)
    cv2.line(frame, mid_shoulder, mid_hip, (255, 255, 255), 4)

    # Lengan
    cv2.line(frame, shoulder_r, elbow_r, (255, 255, 255), 4)
    cv2.line(frame, elbow_r, wrist_r, (255, 255, 255), 4)
    cv2.line(frame, shoulder_l, elbow_l, (255, 255, 255), 4)
    cv2.line(frame, elbow_l, wrist_l, (255, 255, 255), 4)

    # =====================
    #        JARI
    # =====================
    def draw_fingers(center):
        x, y = center
        length = 30
        offsets = [
            (-20, -10),
            (-10, -20),
            (0, -30),
            (10, -20),
            (20, -10)
        ]
        for ox, oy in offsets:
            cv2.line(frame, (x, y), (x + ox, y + oy), (255, 255, 255), 3)

    draw_fingers(wrist_r)
    draw_fingers(wrist_l)

    # Kaki
    cv2.line(frame, hip_r, knee_r, (255, 255, 255), 4)
    cv2.line(frame, knee_r, ankle_r, (255, 255, 255), 4)
    cv2.line(frame, hip_l, knee_l, (255, 255, 255), 4)
    cv2.line(frame, knee_l, ankle_l, (255, 255, 255), 4)

    return frame


# =============================
#        MAIN LOOP
# =============================
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert ke RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pose_res = pose.process(img_rgb)
    face_res = face_mesh.process(img_rgb)

    # ======================
    #       WINDOW UTAMA
    # ======================
    output = frame.copy()
    h, w, c = output.shape

    if pose_res.pose_landmarks:
        for lm in pose_res.pose_landmarks.landmark:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(output, (cx, cy), 5, (255, 0, 0), -1)

    if face_res.multi_face_landmarks:
        for f in face_res.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                output, f,
                mp_face.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(
                    thickness=1, circle_radius=1, color=(0, 255, 255)
                )
            )

    # ======================
    #       WINDOW STICKMAN
    # ======================
    stickman = np.zeros((600, 600, 3), dtype=np.uint8)

    if pose_res.pose_landmarks:
        stickman = draw_stickman(stickman, pose_res.pose_landmarks.landmark)

    # FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(output, f"FPS: {int(fps)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Tracking Asli", output)
    cv2.imshow("Stickman", stickman)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
