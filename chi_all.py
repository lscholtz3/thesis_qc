# plot the chi for all MNPs for thesis
#
# Lexie Scholtz
# Created 2025.09.28

ver = 1.1
to_save = True

import sys
import numpy as np
from matplotlib import pyplot as plt
from qc_formats import *
from matplotlib import gridspec as gridspec
from scipy.stats import linregress

# laser warmup
path = '../../../../../armani_lab/research/qcMAP/qc_data/'

# order given in labels
files = [
    ['SB', [4.5390, 4.2330, 4.3991], [4.0411, 3.9834, 3.9852], [3.6423, 3.4971, 3.4971], [3.0359, 2.8756, 2.9334]], # speedbead
    ['BD-2', [4.4124, 4.1228, 4.2719], [4.0964, 3.9435, 3.9039], [3.6002, 3.4428, 3.4182], [2.8203, 2.7247, 2.7923]], # biodynami 2
    ['C1', [4.2972, 4.1538, 4.1489], [3.7710, 3.7127, 3.8298], [3.1780, 3.2652, 3.2733], [2.6974, 2.8244, 2.7765]], # dy myone c1
    ['BD-3', [4.2287, 4.1348, 4.1800], [3.9223, 3.7326, 3.8294], [3.4125, 3.3902, 3.2957], [3.1781, 3.0421, 2.7787]], # biodynami 3
    ['BD-1', [4.2965, 4.0717, 4.0859], [3.9145, 3.6592, 3.7009], [3.3628, 3.3189, 3.3514], [2.7022, 3.0075, 2.9305]], # biodynami 1
    ['T1', [3.8680, 3.9787, 3.8539], [3.3483, 3.5955, 3.5906], [2.6669, 3.1809, 3.1692], [2.2827, 2.8246, 2.7846]], # dy myone t1
    ['AMP', [3.1437, 3.1912, 3.2796], [2.7412, 3.1051, 2.9845], [2.9971, 2.7717, 2.7306], [1.7762, 2.3993, 1.9013]], # ampure
    ['SM', [2.9210, 2.7516, 2.8778], [2.5510, 2.4461, 2.4030], [2.3799, 2.2971, 2.3184], [2.0624, 2.0341, 1.9753]], # sera-mag
    ['PG', [1.9261, 1.9436, 2.0810], [1.8082, 1.8332, 1.7370], [1.0653, 1.0017, 1.6294], [1.5292, 1.4042, 1.3193]], # dy protein G
    ['CA', [1.5573, 1.6924, 1.7793], [1.5378, 1.6185, 1.7452], [1.4638, 1.5556, 1.0102], [1.4269, 1.3791, 1.3608]], # dy carb acid
    ['270', [1.6844, 1.6761, 1.8383], [1.4534, 1.1898, 1.5277], [1.2991, 1.0589, 1.0393], [1.1861, 1.0898, 1.1164]], # dy m-270 strep
    ['280-1', [1.2098, 1.1986, 1.2366], [1.0535, 1.1018, 1.1164], [1.1661, 0.5568, 0.6908], [1.1065, 1.2270, 1.0544]], # dy m-280 lot 1
    ['280-3', [1.0328, 1.0713, 1.0718], [0.8963, 1.1487, 1.0927], [1.1365, 1.0336, 0.9476], [1.0002, 0.6096, 0.5280]], # dy m-280 lot 3
    ['280-2', [0.9430, 1.1790, 1.1726], [0.6799, 0.9687, 1.0441], [0.9318, 0.9503, 0.7842], [0.8061, 1.1582, 0.9194]], # dy m-280 lot 2
]
colors = [darker_blue, darker_blue, darker_blue, dark_blue, cyan, teal, green, yellow,
    orange, red, pink, pink, pink, purple]
conc_colors = [purple, cyan, orange, red]
labels = [f[0] for f in files]

fig = plt.figure(figsize=(5.5, 3.5), dpi=dpi_disp)
gs = gridspec.GridSpec(1, 1)
ax = fig.add_subplot(gs[0, 0])

for i in range(len(files)):
    conc_series = files[i][1:]

    for fi in range(len(conc_series)):
        conc_chis = conc_series[fi]
        c = conc_colors[fi]
        avg = np.mean(conc_chis)
        std = np.std(conc_chis)
        ax.errorbar(i, avg, std, linestyle='none',
            marker='o', markeredgecolor=c,
            capsize=m_size-1, ecolor=c, elinewidth=l_width)

ax.set_xlabel('MNP')
ax.set_ylabel(r'$\chi_{eff}$')
ax.set_ylim([0, 5])
ax.set_yticks([0, 1, 2, 3, 4, 5])
ax.set_xlim([-0.5, len(files)-0.5])
ax.set_xticks(range(len(files)), labels, rotation=45)

for k in range(4):
    c = conc_colors[k]
    ax.errorbar(-10, -10, 10, linestyle='none', marker='o', markeredgecolor=c,
        capsize=m_size-1, ecolor=c, elinewidth=l_width,
        label='{:d} µg/mL'.format(cs[k]))
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=4)

# --- SAVE FIG ---
plt.tight_layout(pad=pad_loose)

img_name = '../subgraphics/' + sys.argv[0][:-3] + '_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
