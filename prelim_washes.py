# plot the preliminary data on washing MNPs for thesis
#
# Lexie Scholtz
# Created 2025.09.28

ver = 1.2
to_save = True

import sys
import numpy as np
from matplotlib import pyplot as plt
from qc_formats import *
from matplotlib import gridspec as gridspec

# laser warmup
path = '../../../../../armani_lab/research/qcMAP/qc_data/'

dir = '2025.03.07/'
unwashed = ['d82c4', 'd82c5', 'd82c6']
washed = ['d82wash1', 'd82wash2', 'd82wash3']
labels = ['Trial 1', 'Trial 2', 'Trial 3']
files = [unwashed, washed]
# label, dir, file_prefix, ws, xs, ys, zs

colors = [[red, magenta, pink], [darker_blue, dark_blue, cyan]]

fig = plt.figure(figsize=(4, 2.5), dpi=dpi_disp)
gs = gridspec.GridSpec(2, 2, height_ratios=[0.1, 1], width_ratios=[1, 0.6])
leg_ax = fig.add_subplot(gs[0, :])
prep_legax([leg_ax])

in_ax_coords = [0.45, 0.15, 0.45, 0.45]
ax1 = fig.add_subplot(gs[1, 0])
ax1_in = ax1.inset_axes(in_ax_coords)
ax2 = fig.add_subplot(gs[1, 1])

for i in range(len(files)):
    conc_series = files[i]
    for fi in range(len(conc_series)):
        data = np.genfromtxt(path + dir + conc_series[fi] + '.txt')

        time = data[:, 0] / 60 # convert to min
        lux = data[:, 1] / 1000 # convert to klx

        ms = 0.5
        ax1.plot(time, lux, color=colors[i][fi], linestyle='none', marker='.',
            markersize=ms)
        conc = calibrate(lux, 100)
        ax1_in.plot(time, conc, marker='.', linestyle='none', markersize=ms,
            color=colors[i][fi])

        delta = np.mean(lux[:-n]) - np.min(lux)
        print(delta)
        ax2.plot(i, delta, linestyle='none', marker=trial_markers[fi],
            markeredgecolor=colors[i][fi])

ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Illuminance (klx)')
ax1.set_xlim([0, 5])
ax1.set_xticks([0, 2.5, 5])
ax1.set_ylim([-2, 32])
ax1.set_yticks([0, 10, 20, 30])

ax1_in.set_ylabel('c (µg/mL)', labelpad=0.5)
ax1_in.tick_params(axis='both', pad=0.5)
ax1_in.set_xlim([0, 1])
ax1_in.set_ylim([-10, 110])
ax1_in.set_yticks([0, 50, 100])

ax2.set_xlabel('Condition')
ax2.set_xlim([-0.5, 1.5])
ax2.set_xticks([0, 1], ['Unwashed', 'Washed'])
ax2.set_ylabel(r'$\Delta$Illuminance (klx)')
ax2.set_ylim([0, 15])
ax2.set_yticks([0, 5, 10, 15])

leg_ax.plot([], [], linestyle='none', label='Unwashed')
leg_ax.plot([], [], linestyle='none', label='Washed')
for k in range(3):
    leg_ax.plot([], [], color=colors[0][k], label=labels[k])
    leg_ax.plot([], [], color=colors[1][k], label=labels[k])
leg_ax.legend(loc='center', ncol=4, handlelength=h_length_short)

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
