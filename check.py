import cv2

# Create the LBPHFaceRecognizer
clf = cv2.face.LBPHFaceRecognizer_create()

print("Recognizer created successfully:", clf)
