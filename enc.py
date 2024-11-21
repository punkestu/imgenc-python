from PIL import Image
import numpy as np
import json
import time

start_time = time.time()

input_image = "plain.jpg"

# load key from key.json
with open("key.json", "r") as f:
    key = json.load(f)
    vigenere_key = key["key"]
    hill_key = key["matrix"]

img = Image.open(input_image)
img = img.convert("RGB")
pixels = img.load()

fragment = 4
fragment_mask = [0b11000000, 0b00110000, 0b00001100, 0b00000011]

counter = 0
for i in range(img.size[0]):
    for j in range(img.size[1]):
        r, g, b = pixels[i, j]
        [r, g, b] = np.dot(hill_key, [r, g, b]) % 256
        [r, g, b] = [(r + ord(vigenere_key[i % len(vigenere_key)])) % 256, (g + ord(vigenere_key[j % len(vigenere_key)])) % 256, (b + ord(vigenere_key[counter % len(vigenere_key)])) % 256]
        counter += 1
        pixels[i, j] = (r, g, b)

for c in range(fragment):
    img_a = img.copy()
    pixels = img_a.load()
    counter = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            r = r & fragment_mask[c]
            g = g & fragment_mask[c]
            b = b & fragment_mask[c]
            pixels[i, j] = (r, g, b)
            counter += 1
    img_a.save("fragment_" + str(c) + ".bmp", format="BMP")
    print("Fragment " + str(c) + " done")

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Elapsed time: {elapsed_time:.4f} seconds")