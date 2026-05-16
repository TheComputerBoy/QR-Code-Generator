import cv2

# Load the image
image = cv2.imread("QRCODEGen_2026-05-16_15-00-20.png")

# Initialize the detector
detector = cv2.QRCodeDetector()

# Detect and decode the data
data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

# Output results
if vertices_array is not None:
    print(f"Decoded Data: {data}")
else:
    print("QR Code not detected.")
