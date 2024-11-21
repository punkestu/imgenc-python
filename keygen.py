import json
import numpy as np
from numpy.linalg import LinAlgError
from sympy import Matrix
import random

# generate a random matrix
while True:
    try:
        matrix = np.random.randint(0, 256, (3, 3))
        np.array(Matrix(matrix).inv_mod(256)).astype(np.int64)
        break
    except:
        pass
# generate a random key
key = "".join([chr(np.random.randint(0, 256)) for _ in range(10)])
# base64 encode the key
key = key.encode("utf-8").hex()

# save the key and matrix to a file
with open("key.json", "w") as f:
    json.dump({"key": key, "matrix": matrix.tolist()}, f)