# plot the raw Cytiva data for thesis
#
# Lexie Scholtz
# Created 2025.09.19 in amsterdam

ver = 1.0
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
alt = ['4', '5', '6']
files = [
    ['AMPure XP', '2025.05.09/amp_2', df, df, alt, ['1', '3', '4']],
]

c_ids = ['w', 'x', 'y', 'z']
cs = [100, 80, 60, 40]

colors = [purple, cyan, teal, magenta]
bead_colors = [orange]

fig = plt.figure(figsize=(4.75, 3), dpi=dpi_disp)
gs = gridspec.GridSpec(2, 2, height_ratios=[0.1, 1])
leg_ax = fig.add_subplot(gs[0, :])
prep_legax([leg_ax])

axes = []
conc_axes = []
for r in range(1):
    for c in range(1):
        # axes.append(fig.add_subplot(gs[r*2 + 1, c]))
        # conc_axes.append(fig.add_subplot(gs[r*2 + 2, c]))
        axes.append(fig.add_subplot(gs[r+1, c]))
        conc_axes.append(axes[-1].inset_axes([0.45, 0.15, 0.45, 0.45]))

        if len(axes) == 8:
            break
comp_ax = fig.add_subplot(gs[1, 1])
compax_in = comp_ax.inset_axes([0.45, 0.15, 0.45, 0.45])

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
        dir = series[1]

        for fi in range(len(conc_series)):
            if fi == 2 and ci == 3:
                print('found exception')
                dir = '2025.05.12/amp_2'
            data = np.genfromtxt(path + dir + c_id + conc_series[fi] + '.txt')

            time = data[:, 0] / 60 # convert to min
            lux = data[:, 1] / 1000 # convert to klx

            ax.plot(time, lux, color=colors[ci], alpha=1-fi/3)

            conc = calibrate(lux, c0)
            conc_ax.plot(time, conc, color=colors[ci], alpha=1-fi/3)

            if fi == 0 and ci == 0:
                comp_ax.plot(time, lux, color=bead_colors[i])
                compax_in.plot(time, conc, color=bead_colors[i])

for ax in axes + [comp_ax]:
    ax.set_xlabel('Time (min)')
    ax.set_ylabel('Illum. (klx)')
    ax.set_xlim([0, 5])
    ax.set_ylim([-2, 32])

for cax in conc_axes + [compax_in]:
    # cax.set_xlabel('Time (min)', labelpad=0.5)
    cax.set_ylabel('c (µg/mL)', labelpad=0)
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
leg_ax.legend(loc='center', ncol=5, handlelength=h_length_short,
    bbox_to_anchor=(0.47, 0.5))

# --- SAVE FIG ---
plt.tight_layout(pad=pad_loose, h_pad=2)

img_name = '../subgraphics/map_ampure_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
