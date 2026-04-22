import cv2

cameras = [cv2.VideoCapture(i) for i in range(2)]

while True:
    for idx, cam in enumerate(cameras):
        ret, frame = cam.read()

    if not ret:
        break

    cv2.imshow(f"Kameras {idx}", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

for cap in cameras:
    cap.release()

cv2.destroyAllWindows()
print("Hello World")
