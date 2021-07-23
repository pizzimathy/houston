
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as Axes3D
from charting import defaults


fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
defaults.style.format()

ax.plot([0,1], [0,1], [0,1])
ax.invert_zaxis()

plt.show()

