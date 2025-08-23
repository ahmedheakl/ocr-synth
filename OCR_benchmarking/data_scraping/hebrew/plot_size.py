import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import shutil

new_path = "benyehuda_epub_big"
old_path = "benyehuda_epub"
os.makedirs(new_path, exist_ok=True)
def plot_epub_sizes(folder):
    sizes = []
    for f in tqdm(os.listdir(folder)):
        if f.endswith(".epub"):
            size = os.path.getsize(os.path.join(folder, f))
            if size / (1024) > 50: continue
            sizes.append(size / (1024))
            
            # if sizes[-1] >= 10: 
            #     shutil.copy(os.path.join(folder, f), os.path.join(new_path, f))
    plt.hist(sizes, bins=20, edgecolor='black')
    plt.xlabel("File size (KB)")
    plt.ylabel("Count")
    plt.title("EPUB File Size Distribution")
    plt.savefig("sizes_dist.png")
    print(sum([int(s > 10) for s in sizes]))

plot_epub_sizes(new_path)
