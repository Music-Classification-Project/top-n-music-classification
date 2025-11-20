import numpy as np
import os

# with np.load("sandbox/jonas/cnn_model/blues.00000_win0.npz") as d:
#     x = d["mel_spec"]
#     print(x.min(), x.max(), x.mean(), x.std())


root = "./data/features/gtzan/train"
for genre in os.listdir(root):
    gdir = os.path.join(root, genre)
    if not os.path.isdir(gdir):
        continue
    f = next(x for x in os.listdir(gdir) if x.endswith(".npz"))
    path = os.path.join(gdir, f)
    with np.load(path) as d:
        print(path, d["mel_spec"].shape)
