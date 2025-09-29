# plot the preliminary data on concentration screen for thesis
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

# laser warmup
path = '../../../../../armani_lab/research/qcMAP/qc_data/'

# series name, dir1+prefix, dir2+prfix, suffix x6 (a-f)
df = ['a', 'b', 'c', 'd', 'e', 'f']
alt = ['a2', 'b', 'c', 'd', 'e', 'f2']
files = [
    ['Dynabeads M-280 Streptavidin', '2025.03.06/scd82a2', '2025.03.09/scd82b', '2025.03.07/d82c4', '2025.03.09/scd82d', '2025.03.09/scd82e', '2025.03.06/scd82f2'],
    ['Dynabeads M-270 Streptavidin', '2025.03.06/scd7k1a', '2025.03.10/scd7k1b', '2025.03.10/scd7k1c', '2025.03.10/scd7k1d', '2025.03.10/scd7k1e', '2025.03.06/scd7k1f'],
    ['Dynabeads MyOne C1 Streptavidin', '2025.03.06/scdck1a', '2025.03.10/scdck1b', '2025.03.10/scdck1c', '2025.03.10/scdck1d', '2025.03.10/scdck1e', '2025.03.06/scdck1f'],
    ['Dynabeads MyOne C1 Streptavidin', '2025.03.06/scdtk1a', '2025.03.09/scdtk1b', '2025.03.09/scdtk1c', '2025.03.09/scdtk1d', '2025.03.09/scdtk1e', '2025.03.09/scdtk1f2'],
    ['Dynabeads M-270 Carboxylic Acid', '2025.03.12/scdcaa3', '2025.03.12/scdcab', '2025.03.12/scdcac', '2025.03.12/scdcad', '2025.03.12/scdcae', '2025.03.12/scdcaf3'],
    ['Dynabeads Protein G', '2025.03.12/scdpga3', '2025.03.12/scdpgb', '2025.03.12/scdpgc', '2025.03.12/scdpgd', '2025.03.12/scdpge', '2025.03.12/scdpgf3'],
    ['Sera-Mag Streptavidin', '2025.03.07/scsm1a2', '2025.03.09/scsm1b', '2025.03.09/scsm1c', '2025.03.09/scsm1d', '2025.03.09/scsm1e', '2025.03.07/scsm1f2'],
    ['Sera-Mag SpeedBead Streptavidin', '2025.03.07/scspb1a2', '2025.03.09/scspb1b', '2025.03.09/scspb1c', '2025.03.09/scspb1d', '2025.03.09/scspb1e2', '2025.03.07/scspb1f2'],
    ['BioDynami', '2025.03.07/scbio1a2', '2025.03.09/scbio1b', '2025.03.09/scbio1c', '2025.03.09/scbio1d', '2025.03.09/scbio1e', '2025.03.07/scbio1f2'],
    # ['AMPure XP', ]
]
cs = [500, 250, 100, 75, 50, 25]
bead_colors = vib_full[1:]
conc_colors = [purple, cyan, teal, yellow, orange, red]

# set up axes
fig = plt.figure(figsize=(6.5, 5.5), dpi=dpi_disp)
gs = gridspec.GridSpec(4, 3, height_ratios=[0.1, 1, 1, 1])
leg_ax = fig.add_subplot(gs[0, :])
prep_legax([leg_ax])

in_ax_coords = [0.48, 0.18, 0.45, 0.42]
axes = []
conc_axes = []
for x in range(1, 4):
    for y in range(3):
        axes.append(fig.add_subplot(gs[x, y]))
        conc_axes.append(axes[-1].inset_axes(in_ax_coords))

fig2 = plt.figure(figsize=(5, 2.5), dpi=dpi_disp)
gs2 = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
leg2_ax = fig2.add_subplot(gs2[0, 0])
prep_legax([leg2_ax])
resp_ax = fig2.add_subplot(gs2[0, 1])
resp_inax = resp_ax.inset_axes([0.5, 0.1, 0.45, 0.35])

# sweep through files
deltas = np.zeros([len(files), len(cs)])
for i in range(len(files)):
    conc_series = files[i][1:]
    ax = axes[i]
    conc_ax = conc_axes[i]
    for fi in range(len(conc_series)):
        data = np.genfromtxt(path + conc_series[fi] + '.txt')

        time = data[:, 0] / 60 # convert to min
        lux = data[:, 1] / 1000 # convert to klx

        ms = 4
        ax.plot(time, lux, color=conc_colors[fi], linestyle='none', marker='.',
            markersize=ms, markeredgewidth=0, markerfacecolor=conc_colors[fi])
        conc = calibrate(lux, cs[fi])
        conc_ax.plot(time, conc, color=conc_colors[fi], linestyle='none', marker='.',
            markersize=ms, markeredgewidth=0, markerfacecolor=conc_colors[fi])

        delta = np.mean(lux[:-n]) - np.min(lux)
        deltas[i, fi] = delta

for i in range(len(files)):
    resp_ax.plot(cs, deltas[i], color=bead_colors[i], marker='o')
    resp_inax.plot(cs, deltas[i], color=bead_colors[i], marker='o')

for ax in axes:
    ax.set_xlabel('Time (min)', labelpad=1)
    ax.set_ylabel('Illuminance (klx)', labelpad=1)
    ax.set_xlim([0, 5])
    ax.set_xticks([0, 2.5, 5])
    ax.set_ylim([-3, 33])
    ax.set_yticks([0, 10, 20, 30])

for in_ax in conc_axes:
    in_ax.set_ylabel('c (µg/mL)', labelpad=0.5)
    in_ax.tick_params(axis='both', pad=0.5)
    in_ax.set_xlim([0, 1])
    in_ax.set_ylim([-10, 110])
    in_ax.set_yticks([0, 50, 100])

resp_ax.set_xlabel('Concentration (µg/mL)')
resp_ax.set_ylabel(r'$\Delta$Illuminance (klx)')
resp_ax.set_xlim([-20, 550])
resp_ax.set_ylim([-3, 33])
resp_ax.set_yticks([0, 10, 20, 30])

resp_inax.tick_params(axis='both', pad=0.5)
resp_inax.set_xlim([0, 125])
resp_inax.set_xticks([0, 50, 100])
resp_inax.set_ylim([-2, 27])
resp_inax.set_yticks([0, 12.5, 25])

for k in range(len(cs)):
    leg_ax.plot([], [], color=conc_colors[k], label='{:d} µg/mL'.format(cs[k]))
leg_ax.legend(loc='upper center', ncol=6, handlelength=h_length_short)

for k in range(len(files)):
    leg2_ax.plot([], [], color=bead_colors[k], marker='o', label=files[k][0])
leg2_ax.legend(loc='center left', bbox_to_anchor=(0, 0.4), handlelength=h_length_short)
# --- SAVE FIG ---
fig.tight_layout(pad=pad_loose, h_pad=2)
fig2.tight_layout(pad=pad_loose)

img_name = '../subgraphics/' + sys.argv[0][:-3] + '_' + str(ver)

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    fig.savefig(img_name + '-a.png', dpi=dpi_save)
    fig2.savefig(img_name + '-b.png', dpi=dpi_save)
    print('saved file as: ' + img_name)
