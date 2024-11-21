from PIL import Image
import numpy as np
from sympy import Matrix
import json
import time

start_time = time.time()

decrypted_image = "decrypted.jpg"

# load key from key.json
with open("key.json", "r") as f:
    key = json.load(f)
    vigenere_key = key["key"]
    hill_key = key["matrix"]
    inv_hill_key = np.array(Matrix(hill_key).inv_mod(256)).astype(np.int64)

fragment = 4

for c in range(fragment):
    img_a = Image.open("fragment_" + str(c) + ".bmp")
    pixels_a = img_a.load()
    if c == 0:
        merged_img = Image.new("RGB", (img_a.size[0], img_a.size[1]))
        pixels_merged = merged_img.load()
    for i in range(img_a.size[0]):
        for j in range(img_a.size[1]):
            rc, gc, bc = pixels_a[i, j]
            r, g, b = pixels_merged[i, j]
            r = r | rc
            g = g | gc
            b = b | bc
            pixels_merged[i, j] = (r, g, b)
    print("Fragment " + str(c) + " done")

counter = 0
for i in range(merged_img.size[0]):
    for j in range(merged_img.size[1]):
        r, g, b = pixels_merged[i, j]
        [r, g, b] = ((r - ord(vigenere_key[i % len(vigenere_key)])) % 256, (g - ord(vigenere_key[j % len(vigenere_key)])) % 256, (b - ord(vigenere_key[counter % len(vigenere_key)])) % 256)
        [r, g, b] = np.dot(inv_hill_key, [r, g, b]) % 256
        counter += 1
        pixels_merged[i, j] = (r, g, b)
merged_img.save(decrypted_image)

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.4f} seconds")