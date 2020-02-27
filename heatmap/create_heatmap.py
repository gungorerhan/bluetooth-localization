import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import scipy
from matplotlib.colors import ListedColormap


# read base image
image_filename = 'floor_plan.png'
im = plt.imread(image_filename)

# convert to int
im = (im*255).astype('uint8')
plt.figure(figsize=(19.20,10.80))

# Api call for #visitor matrix 
# TODO reads csv's and create matrix manually for now
df = pd.read_csv('locs_new.csv').to_numpy()
locs = np.zeros((519,636))
for x,y in df:
    locs[x][y] += 1

# apply gaussian filter
hm = scipy.ndimage.gaussian_filter(locs, sigma=16)

# create colormap
cmap = sb.cubehelix_palette(rot=5, n_colors=8)
cmap = sb.color_palette(palette="Reds", n_colors=10)
cmap = ListedColormap(np.array(cmap))

# add heatmap to image
#plt.figure(figsize=(20,20))
plt.imshow(255 * hm, alpha=5, cmap=cmap)
plt.imshow(im)
plt.axis('off')
plt.savefig('heatmap.png', transparent=True)
plt.show()