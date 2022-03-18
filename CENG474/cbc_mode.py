import cv2
import numpy as np
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Random import get_random_bytes

mode = AES.MODE_CBC

keySize = 32
ivSize = AES.block_size

imageOrig = cv2.imread("cromernew.png")
rowOrig, columnOrig, depthOrig = imageOrig.shape

cv2.imshow("Original image", imageOrig)
cv2.waitKey()

imageOrigBytes = imageOrig.tobytes()

key = get_random_bytes(keySize)
iv = get_random_bytes(ivSize)

cipher = AES.new(key, AES.MODE_CBC, iv)
imageOrigBytesPadded = pad(imageOrigBytes, AES.block_size)
ciphertext = cipher.encrypt(imageOrigBytesPadded)

paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
void = columnOrig * depthOrig - ivSize - paddedSize
ivCiphertextVoid = iv + ciphertext + bytes(void)
imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype = imageOrig.dtype).reshape(rowOrig + 1, columnOrig, depthOrig)

cv2.imshow("Encrypted image", imageEncrypted)
cv2.imwrite("cromer_cbc.jpg", imageEncrypted)
cv2.waitKey()