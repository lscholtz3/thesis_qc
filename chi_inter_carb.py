# plot the chi for streptavidin product lines data for thesis
#
# Lexie Scholtz
# Created 2025.09.27 in SeaTac gate A4

ver = 1.0
to_save = True

import sys
import numpy as np
from matplotlib import pyplot as plt
from qc_formats import *
from matplotlib import gridspec as gridspec
from scipy.stats import ttest_ind as ttest

# laser warmup
path = '../../../../../armani_lab/research/qcMAP/qc_data/'

# chis: [100], [80], [60], [40]
# rows:  dyna carb, ampure, biodynami x3
chis = [
    [[1.5573, 1.6924, 1.7793], [1.5378, 1.6185, 1.7452], [1.4638, 1.5556, 1.0102], [1.4269, 1.3791, 1.3608]],
    [[3.1437, 3.1912, 3.2796], [2.7412, 3.1051, 2.9845], [2.9971, 2.7717, 2.7306], [1.7762, 2.3993, 1.9013]],
    [[4.2965, 4.0717, 4.0859], [3.9145, 3.6592, 3.7009], [3.3628, 3.3189, 3.3514], [2.7022, 3.0075, 2.9305]],
    [[4.4124, 4.1228, 4.2719], [4.0964, 3.9435, 3.9039], [3.6002, 3.4428, 3.4182], [2.8203, 2.7247, 2.7923]],
    [[4.2287, 4.1348, 4.1800], [3.9223, 3.7326, 3.8294], [3.4125, 3.3902, 3.2957], [3.1781, 3.0421, 2.7787]]

]

df = ['1', '2', '3'] # default
alt = ['4', '5', '6']
files = [
    ['Carboxylic Acid', '2025.04.29/dca_2', df, df, df, df],
    ['AMPure XP', '2025.05.09/amp_2', df, df, alt, df],
    ['BioDyanmi Lot 1', '2025.05.12/bio1', alt, alt, df, df],
    ['BioDynami Lot 2', '2025.05.12/bio2', df, df, df, df],
    ['BioDynami Lot 3', '2025.05.12/bio3', df, df, df, df],

]
labels = ['DY', 'AMP', 'BD']
xs = [0, 1, 2, 2.33, 2.67]

c_ids = ['w', 'x', 'y', 'z']
cs = [100, 80, 60, 40]

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
            ax.plot(xs[i], conc_chi[k], linestyle='none', marker=trial_markers[k],
                markeredgecolor=trial_colors[k])

print('chis:\navgs:')
print(avg_chis)
print('stds:')
print(std_chis)

biodynami_chis = []
for col in range(4):
    bdx = chis[2][col] + chis[3][col] + chis[4][col]
    biodynami_chis.append(bdx)
ampure_chis = chis[1]
dyna_chis = chis[0]

agg_chis = [dyna_chis, ampure_chis, biodynami_chis]

for j in range(4):
    conc = cs[j]
    print('for conc {} µg/mL:'.format(conc))
    for i in range(len(agg_chis)):
        for k in range(i+1, len(agg_chis)):
            res = ttest(agg_chis[i][j], agg_chis[k][j])
            if res.pvalue < 0.05:
                print('*', end='')
            if res.pvalue < 0.005:
                print('*', end='')
            if res.pvalue < 0.0005:
                print('*', end='')
            print('for lot {}/{}: t-stat: {}, p value {}'.format(i, k, res.statistic, res.pvalue))

i = 0
yrange = [0, 3.5, 7]
yr = yrange[-1] * 0.1
for ax in axes:
    ax.set_xlim([xs[0]-0.5, xs[-1]+0.5])
    ax.set_ylabel(r'$\chi_{eff}$')
    ax.set_ylim(yrange[0]-yr, yrange[-1]+yr)
    ax.set_yticks(yrange)
    i += 1

avg_times = np.zeros([len(chis), 4])
std_times = np.zeros([len(chis), 4])
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
            ax.plot(xs[i], resp_time, linestyle='none', marker=trial_markers[fi],
                markeredgecolor=trial_colors[fi])
            conc_times.append(resp_time)

        series_times.append(conc_times)

        avg_times[i, ci] = np.mean(conc_times)
        std_times[i, ci] = np.std(conc_times)
    resp_times.append(series_times)


print('response times:\navgs:')
print(avg_times)
print('stds:')
print(std_times)

biodynami_rts = []
for col in range(4):
    bdrt = resp_times[2][col] + resp_times[3][col] + resp_times[4][col]
    biodynami_rts.append(bdrt)
ampure_rts = resp_times[1]
dyna_rts = resp_times[0]

agg_rts = [dyna_rts, ampure_rts, biodynami_rts]

print('\n\nRESPONSE TIMES')
for j in range(4):
    conc = cs[j]
    print('for conc {} µg/mL:'.format(conc))
    for i in range(len(agg_rts)):
        for k in range(i+1, len(agg_rts)):
            res = ttest(agg_rts[i][j], agg_rts[k][j])
            if res.pvalue < 0.05:
                print('*', end='')
            if res.pvalue < 0.005:
                print('*', end='')
            if res.pvalue < 0.0005:
                print('*', end='')
            print('for lot {}/{}: t-stat: {}, p value {}'.format(i, k, res.statistic, res.pvalue))

yrange = [0, 50, 100, 150]
yr = yrange[-1] * 0.1
i = 0
for ax in time_axes:
    ax.set_ylabel('Response Time (s)')
    ax.set_ylim(yrange[0]-yr, yrange[-1]+yr)
    ax.set_yticks(yrange)
    ax.set_xlabel('MNP')
    ax.set_xlim([xs[0]-0.5, xs[-1]+0.5])
    ax.set_xticks([0, 1, 2.33], labels)

    i += 1
for ax in axes + time_axes:
    ax.axvline(1.5, color=vib_grey, alpha=0.5)
    ax.axvline(0.5, color=vib_grey, alpha=0.5)

handles = []
labels = []
for i in range(3):
    h1, = leg_ax.plot([], [], linestyle='none', marker=trial_markers[i],
        color=trial_colors[i], label='Trial {}'.format(i+1))

leg_ax.legend(ncol=3, loc='center', bbox_to_anchor=(0.5, 1.0))

# --- SAVE FIG ---
plt.tight_layout(pad=pad_loose)
plt.subplots_adjust(hspace=0)
fig.align_ylabels()

img_name = '../subgraphics/chi_inter_carb_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
