# plot the raw control data for thesis
#
# Lexie Scholtz
# Created 2025.09.28

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
files = [
    ['DPBS', '2025.04.24/424ctl0', ['7', '8', '9']],
    ['Fluospheres', '2025.05.13/fluo1', df, df, df, df],
]

colors = [purple, cyan, teal, magenta]

fig = plt.figure(figsize=(4.5, 3), dpi=dpi_disp)
gs = gridspec.GridSpec(2, 2, height_ratios=[0.1, 1])
leg_ax = fig.add_subplot(gs[0, :])
prep_legax([leg_ax])

in_ax_coords = [0.25, 0.1, 0.65, 0.3]
ax1 = fig.add_subplot(gs[1, 0])
ax1_in = ax1.inset_axes(in_ax_coords)
ax2 = fig.add_subplot(gs[1, 1])
axes = [ax1, ax2]
ax2_in = ax2.inset_axes(in_ax_coords)
in_axes = [ax1_in, ax2_in]

for i in range(len(files)):
    ax = axes[i]
    in_ax = in_axes[i]
    series = files[i]
    series_name = series[0]
    dir = series[1]
    suffixes = series[2:]

    for ci in range(len(suffixes)):
        conc_series = suffixes[ci]
        print('{}{}'.format(dir, conc_series))
        c_id = c_ids[ci]
        c0 = cs[ci]

        for fi in range(len(conc_series)):
            if i == 0:
                c_id = ''
            data = np.genfromtxt(path + dir + c_id + conc_series[fi] + '.txt')

            time = data[:, 0] / 60 # convert to min
            lux = data[:, 1] / 1000 # convert to klx

            c = colors[ci]
            if i == 0:
                c = rainbow_grey
            ax.plot(time, lux, color=c, alpha=1-fi/3)
            in_ax.plot(time, lux, color=c, alpha=1-fi/3)

for ax in axes:
    ax.set_xlabel('Time (min)')
    ax.set_ylabel('Illum. (klx)')
    ax.set_xlim([0, 5])
    ax.set_xticks([0, 2.5, 5])
    ax.set_ylim([-2, 32])
    ax.set_yticks([0, 10, 20, 30])
for in_ax in in_axes:
    in_ax.tick_params(axis='both', pad=0.5)
    in_ax.set_xlim([0, 1])
ax1_in.set_ylim([27.5, 28])
ax1_in.set_yticks([27.5, 28])
ax2_in.set_ylim([22, 23])
ax2_in.set_yticks([22, 22.5, 23])

for k in range(len(cs)):
    leg_ax.plot([], [], color=colors[k], label='{} µg/mL'.format(cs[k]))
for k in range(3):
    leg_ax.plot([], [], marker='s', linestyle='none', markerfacecolor=black,
        alpha=1-k/3, label='Trial {}'.format(k+1), markeredgewidth=0)
leg_ax.plot([], [], color='w', label=' ')
leg_ax.legend(loc='center', ncol=5, handlelength=h_length_short)

# --- SAVE FIG ---
plt.tight_layout(pad=pad_loose, h_pad=2)

img_name = '../subgraphics/' + sys.argv[0][:-3] + '_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
