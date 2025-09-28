# plot the analysis of inter-manuf. carboxyl beads for thesis
#
# Lexie Scholtz
# Created 2025.09.28 back in boise

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
    ['Carboxylic Acid', '2025.04.29/dca_2', df, df, df, df],
    ['AMPure XP', '2025.05.09/amp_2', df, df, alt, ['1', '3', '4']],
    ['BioDyanmi Lot 1', '2025.05.12/bio1', alt, alt, df, df],
]

infl_points = [
    [10.273, 10.406, 10.141],
    [27.183, 24.704, 24.007],
    [20.906, 20.098, 19.798]
]


c_ids = ['w', 'x', 'y', 'z']
cs = [100, 80, 60, 40]

colors = [purple, cyan, teal, magenta]
bead_colors = [darker_blue, teal, pink]

fig = plt.figure(figsize=(6.5, 2.5), dpi=dpi_disp)
gs = gridspec.GridSpec(2, 3, height_ratios=[0.1, 1])
leg_ax = fig.add_subplot(gs[0, :])
prep_legax([leg_ax])

ax1 = fig.add_subplot(gs[1, 0])
ax1_in = ax1.inset_axes([0.45, 0.2, 0.45, 0.45])
ax2 = fig.add_subplot(gs[1, 1])
ax3 = fig.add_subplot(gs[1, 2])

for i in range(len(files)):
    series = files[i]
    series_name = series[0]
    dir = series[1]
    # suffixes = series[2:]
    c_id = c_ids[0]
    conc_series = series[2]
    c0 = cs[0]
    for fi in range(len(conc_series)):
        data = np.genfromtxt(path + dir + c_id + conc_series[fi] + '.txt')

        time = data[:, 0] / 60 # convert to min
        lux = data[:, 1] / 1000 # convert to klx

        ax1.plot(time, lux, color=bead_colors[i], alpha=1-fi/3)

        conc = calibrate(lux, c0)
        ax1_in.plot(time, conc, color=bead_colors[i], alpha=1-fi/3, zorder=2)

        infl_time = infl_points[i][fi]
        ax2.plot(i, infl_time, linestyle='none', marker=trial_markers[fi],
            markeredgecolor=bead_colors[i], alpha=1-fi/3)

        resp_time = calculate_resp_time(path + dir + c_id + conc_series[fi] + '.txt')
        ax3.plot(i, resp_time-infl_time, linestyle='none', marker=trial_markers[fi],
            markeredgecolor=bead_colors[i], alpha=1-fi/3)

ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Illum. (klx)')
ax1.set_xlim([0, 5])
ax1.set_xticks([0, 2.5, 5])
ax1.set_ylim([-2, 32])

ax1_in.set_ylabel('c (µg/mL)', labelpad=-0.5)
ax1_in.set_xlim([0, 1])
ax1_in.set_ylim([-10, 110])
ax1_in.tick_params(axis='both', pad=0.5)
ax1_in.axhline(10, linestyle='--', color=vib_grey, alpha=1, zorder=1)

for ax in [ax2, ax3]:
    ax.set_xlabel('MNP')
    ax.set_xlim([-0.5, 2.5])
    ax.set_xticks([0, 1, 2], ['DY', 'AMP', 'BD'])

ax2.set_ylabel('Inflection Point (s)')
ax2.set_ylim([0, 30])
ax2.set_yticks([0, 10, 20, 30])

ax3.set_ylabel(r'$\Delta$Response-Inflection (s)')
ax3.set_ylim([0, 45])
ax3.set_yticks([0, 15, 30, 45])

for k in range(len(files)):
    leg_ax.plot([], [], color=bead_colors[k], label=files[k][0])
    leg_ax.plot([], [], marker='s', linestyle='none', markerfacecolor=black,
        alpha=1-k/3, label='Trial {}'.format(k+1), markeredgewidth=0)
leg_ax.plot([], [], linestyle='--', color=vib_grey, alpha=1, label='90% response threshold')
leg_ax.legend(loc='center', ncol=4, handlelength=h_length+0.2)

# --- SAVE FIG ---
plt.tight_layout(pad=pad_loose, h_pad=2)

img_name = '../subgraphics/map_inter_carb_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
