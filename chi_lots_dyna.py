# plot the chi for dynabead lots data for thesis
#
# Lexie Scholtz
# Created 2025.09.20 in portree, isle of skye

ver = 1.0
to_save = True

import sys
import numpy as np
from matplotlib import pyplot as plt
from qc_formats import *
from matplotlib import gridspec as gridspec

# laser warmup
path = '../../../../../armani_lab/research/qcMAP/qc_data/'

# chis: [100], [80], [60], [40]
chis = [
    [[1.2098, 1.1986, 1.2366], [1.0535, 1.1018, 1.1164], [1.1661, 0.5568, 0.6908], [1.1065, 1.2270, 1.0544]],
    [[0.9430, 1.1790, 1.1726], [0.6799, 0.9687, 1.0441], [0.9318, 0.9503, 0.7842], [0.8061, 1.1582, 0.9194]],
    [[1.0328, 1.0713, 1.0718], [0.8963, 1.1487, 1.0927], [1.1365, 1.0336, 0.9476], [1.0002, 0.6096, 0.5280]]
]

cs = [100, 80, 60, 40]

colors = [green, purple, pink, cyan]
markers = ['o', 'd', '^', 's']

fig = plt.figure(figsize=(6.5, 3), dpi=dpi_disp)
gs = gridspec.GridSpec(5, 2, height_ratios=[0.2, 1, 1, 1, 1])
leg_ax = fig.add_subplot(gs[0, :])
prep_legax([leg_ax])

axes = []
for i in range(4):
    axes.append(fig.add_subplot(gs[1+i, 0]))

for i in range(len(chis)):
    lot_chis = chis[i]

    for j in range(len(lot_chis)):
        conc_chi = lot_chis[j]
        ax = axes[j]
        # conc = [cs[j], cs[j], cs[j]]

        ax.plot([i, i, i], conc_chi, linestyle='none', marker=markers[j],
            color=colors[j], markeredgecolor=colors[j])

for ax in axes:
    ax.set_xlabel('Lot')
    ax.set_ylabel(r'$\chi_{eff}$')
    ax.set_xlim([-0.5, 2.5])
    ax.set_xticks([0, 1, 2])
    ax.set_ylim([0.5, 1.5])


# for k in range(len(cs)):
#     leg_ax.plot([], [], color=colors[k], label='{} µg/mL'.format(cs[k]))
# for k in range(3):
#     leg_ax.plot([], [], marker='s', linestyle='none', markerfacecolor=black,
#         alpha=1-k/3, label='Trial {}'.format(k+1), markeredgewidth=0)
# leg_ax.plot([], [], color='w', label=' ')
# for k in range(len(files)):
#     leg_ax.plot([], [], color=bead_colors[k], label=files[k][0])
# leg_ax.legend(loc='center', ncol=3, handlelength=h_length_short)

# --- SAVE FIG ---
plt.tight_layout(pad=pad_loose)
plt.subplots_adjust(hspace=0)
fig.align_ylabels()

img_name = '../subgraphics/chi_lots_dyna_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
