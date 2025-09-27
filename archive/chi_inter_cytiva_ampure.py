# plot the chi for cytiva product lines data for thesis
#
# Lexie Scholtz
# Created 2025.09.24 in Stornoway, Isle of Lewis, Scotland

ver = 1.0
to_save = True

import sys
import numpy as np
from matplotlib import pyplot as plt
from qc_formats import *
from matplotlib import gridspec as gridspec
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple
from scipy.stats import ttest_ind as ttest

# laser warmup
path = '../../../../../armani_lab/research/qcMAP/qc_data/'

# chis: [100], [80], [60], [40]
# rows:  sera-mag, speedbead, ampure xp
chis = [
    [[2.9210, 2.7516, 2.8778], [2.5510, 2.4461, 2.4030], [2.3799, 2.2971, 2.3184], [2.0624, 2.0341, 1.9753]],
    [[4.5390, 4.2330, 4.3991], [4.0411, 3.9834, 3.9852], [3.6423, 3.4971, 3.4971], [3.0359, 2.8756, 2.9334]],
    [[3.1437, 3.1912, 3.2796], [2.7412, 3.1051, 2.9845], [2.9971, 2.7717, 2.7306], [1.7762, 2.3993, 1.9013]]
]

df = ['1', '2', '3'] # default
alt = ['4', '5', '6']
files = [
    ['Sera-Mag', '2025.05.13/sera_2', df, df, df, df],
    ['Speedbead', '2025.05.13/spbd_2', df, df, df, df],
    ['AMPure XP', '2025.05.09/amp_2', df, df, alt, df]
]

c_ids = ['w', 'x', 'y', 'z']

cs = [100, 80, 60, 40]

colors = [cyan, teal, pink, purple]
markers = ['o', 'D', 's', '^']

fig = plt.figure(figsize=(6.5, 3.25), dpi=dpi_disp)
gs = gridspec.GridSpec(3, 4, height_ratios=[0.5, 1, 1])
leg_ax = fig.add_subplot(gs[0, :])
prep_legax([leg_ax])

axes = []
for i in range(4):
    axes.append(fig.add_subplot(gs[1, i]))

time_axes = []
for i in range(4):
    time_axes.append(fig.add_subplot(gs[2, i]))

avg_chis = np.zeros([len(chis), 4])
std_chis = np.zeros([len(chis), 4])

for i in range(len(chis)):
    lot_chis = chis[i]

    for j in range(len(lot_chis)):
        conc_chi = lot_chis[j]
        ax = axes[j]
        avg_chis[i, j] = np.mean(conc_chi)
        std_chis[i, j] = np.std(conc_chi)
        # conc = [cs[j], cs[j], cs[j]]
        for k in range(3):
            ax.plot([i], conc_chi[k], linestyle='none', marker=trial_markers[k],
                markeredgecolor=trial_colors[k])

print(avg_chis)

for j in range(4):
    conc = cs[j]
    print('for conc {} µg/mL:'.format(conc))
    for i in range(len(files)):
        for k in range(i+1, len(files)):
            res = ttest(chis[i][j], chis[k][j])
            if res.pvalue < 0.05:
                print('*', end='')
            if res.pvalue < 0.005:
                print('*', end='')
            if res.pvalue < 0.0005:
                print('*', end='')
            print('for lot {}/{}: t-stat: {}, p value {}'.format(i, k, res.statistic, res.pvalue))

i = 0
yranges = [
    [0, 3, 6],
]
for ax in axes:
    ax.set_xlim([-0.5, 2.5])
    ax.set_ylabel(r'$\chi_{eff}$')
    ax.set_ylim(yranges[0][0]-0.6, yranges[0][-1]+0.6)
    ax.set_yticks(yranges[0])
    i += 1

resp_times = []
for i in range(len(files)):
    series = files[i]
    series_name = series[0]
    dir = series[1]
    suffixes = series[2:]
    series_times = []

    for ci in range(len(suffixes)):
        ax = time_axes[ci]
        conc_series = suffixes[ci]
        c_id = c_ids[ci]
        c0 = cs[ci]

        conc_times = []
        for fi in range(len(conc_series)):
            resp_time = calculate_resp_time(path + dir + c_id + conc_series[fi] + '.txt')
            ax.plot(i, resp_time, linestyle='none', marker=trial_markers[fi],
                markeredgecolor=trial_colors[fi])
            conc_times.append(resp_time)

        series_times.append(conc_times)
    resp_times.append(series_times)

print('\n\nRESPONSE TIMES')
for j in range(4):
    conc = cs[j]
    print('for conc {} µg/mL:'.format(conc))
    for i in range(len(files)):
        for k in range(i+1, len(files)):
            res = ttest(chis[i][j], chis[k][j])
            if res.pvalue < 0.05:
                print('*', end='')
            if res.pvalue < 0.005:
                print('*', end='')
            if res.pvalue < 0.0005:
                print('*', end='')
            print('for lot {}/{}: t-stat: {}, p value {}'.format(i, k, res.statistic, res.pvalue))

yranges = [
    [0, 70, 140],
]
i = 0
for ax in time_axes:
    ax.set_ylabel('Response Time (s)')
    ax.set_ylim(yranges[0][0]-14, yranges[0][-1]+14)
    ax.set_yticks(yranges[0])
    ax.set_xlabel('MNP')
    ax.set_xlim([-0.5, 2.5])
    ax.set_xticks([0, 1, 2], ['SM', 'SB', 'AMP'])

    i += 1

handles = []
labels = []
for i in range(3):
    h1, = leg_ax.plot([], [], linestyle='none', marker=trial_markers[i],
        color=trial_colors[i], label='Trial {}'.format(i+1))

leg_ax.legend(ncol=3, loc='center', bbox_to_anchor=(0.5, 1.0),
    handler_map={tuple: HandlerTuple(ndivide=None)})

# --- SAVE FIG ---
plt.tight_layout(pad=pad_loose)
plt.subplots_adjust(hspace=0)
fig.align_ylabels()

img_name = '../subgraphics/chi_inter_cytiva_ampure_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
