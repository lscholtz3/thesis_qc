# plot the raw Dynabeads data for thesis
#
# Lexie Scholtz
# Created 2025.09.18

ver = 1.1
to_save = True

import sys
import numpy as np
from matplotlib import pyplot as plt
from qc_formats import *
from matplotlib import gridspec as gridspec

# laser warmup
path = '../../../../../armani_lab/research/qcMAP/qc_data/'

# label, dir, file_prefix, ws, xs, ys, zs
df = ['1', '2', '3'] # default
files = [
    ['M-280 Streptavidin lot 1', '2025.04.28/dm81_2', df, df, df, df],
    ['M-280 Streptavidin lot 2', '2025.04.28/dm82_2', df, df, df, df],
    ['M-280 Streptavidin lot 3', '2025.04.28/dm83_2', df, df, df, ['4', '5', '6']],
    ['M-270 Streptavidin', '2025.04.29/dm7_2', df, df, df, df],
    ['MyOne C1 Streptavidin', '2025.04.28/dc1_2', df, df, df, df],
    ['MyOne T1 Streptavidin', '2025.04.29/dt1_2', df, df, df, df],
    ['Carboxylic Acid', '2025.04.29/dca_2', df, df, df, df],
    ['Protein G', '2025.05.01/dpg_2', df, ['1-ex', '2-ex', '3-ex'], df, df]
]
dm83z_dir = '2025.04.28/dm83_2'

c_ids = ['w', 'x', 'y', 'z']
cs = [100, 80, 60, 40]

colors = [purple, cyan, teal, magenta]
bead_colors = [darker_blue, dark_blue, green, yellow, orange, red, pink, rainbow_grey]

fig = plt.figure(figsize=(6.5, 6), dpi=dpi_disp)
gs = gridspec.GridSpec(4, 3, height_ratios=[0.1, 1, 1, 1])
leg_ax = fig.add_subplot(gs[0, :])
prep_legax([leg_ax])

axes = []
conc_axes = []
for r in range(3):
    for c in range(3):
        # axes.append(fig.add_subplot(gs[r*2 + 1, c]))
        # conc_axes.append(fig.add_subplot(gs[r*2 + 2, c]))
        axes.append(fig.add_subplot(gs[r+1, c]))
        conc_axes.append(axes[-1].inset_axes([0.45, 0.2, 0.45, 0.45]))

        if len(axes) == 8:
            break
ax9 = fig.add_subplot(gs[3, 2])
ax9_in = ax9.inset_axes([0.45, 0.2, 0.45, 0.45])

for i in range(len(files)):
    ax = axes[i]
    conc_ax = conc_axes[i]

    series = files[i]
    series_name = series[0]
    dir = series[1]
    suffixes = series[2:]

    for ci in range(len(suffixes)):
        conc_series = suffixes[ci]
        print('{}{}'.format(dir, conc_series))
        c_id = c_ids[ci]
        c0 = cs[ci]

        if 'lot 3' in series_name and ci == 3:
            dir = dm83z_dir

        for fi in range(len(conc_series)):
            data = np.genfromtxt(path + dir + c_id + conc_series[fi] + '.txt')

            time = data[:, 0] / 60 # convert to min
            lux = data[:, 1] / 1000 # convert to klx

            ax.plot(time, lux, color=colors[ci], alpha=1-fi/3)

            conc = calibrate(lux, c0)
            conc_ax.plot(time, conc, color=colors[ci], alpha=1-fi/3)

            if fi == 0 and ci == 0:
                print(str(c0) + ',' + dir + c_id +conc_series[fi])
                ax9.plot(time, lux, color=bead_colors[i])
                ax9_in.plot(time, conc, color=bead_colors[i])

for ax in axes + [ax9]:
    ax.set_xlabel('Time (min)')
    ax.set_ylabel('Illum. (klx)')
    ax.set_xlim([0, 5])
    ax.set_ylim([-2, 32])

for cax in conc_axes + [ax9_in]:
    # cax.set_xlabel('Time (min)', labelpad=0.5)
    cax.set_ylabel('c (µg/mL)', labelpad=0.5)
    cax.set_xlim([0, 1])
    cax.set_ylim([-10, 110])
    cax.tick_params(axis='both', pad=0.5)

for k in range(len(cs)):
    leg_ax.plot([], [], color=colors[k], label='{} µg/mL'.format(cs[k]))
for k in range(3):
    leg_ax.plot([], [], marker='s', linestyle='none', markerfacecolor=black,
        alpha=1-k/3, label='Trial {}'.format(k+1), markeredgewidth=0)
leg_ax.plot([], [], color='w', label=' ')
for k in range(len(files)):
    leg_ax.plot([], [], color=bead_colors[k], label=files[k][0])
leg_ax.legend(loc='center', ncol=4, handlelength=h_length_short)

# --- SAVE FIG ---
plt.tight_layout(pad=pad_loose, h_pad=2)

img_name = '../subgraphics/map_dyna_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
