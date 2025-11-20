import numpy as np
import os

root = "./data/features/gtzan/train"
for genre in os.listdir(root):
    gdir = os.path.join(root, genre)
    if not os.path.isdir(gdir):
        continue
    f = next(x for x in os.listdir(gdir) if x.endswith(".npz"))
    path = os.path.join(gdir, f)
    with np.load(path) as d:
        print(path, d["mel_spec"].shape)
