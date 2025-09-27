# plot the chi for streptavidin product lines data for thesis
#
# Lexie Scholtz
# Created 2025.09.27 in the air over the Washington-Canada border

ver = 1.1
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
# rows:  sera-mag, speedbead
chis = [
    [[3.8680, 3.9787, 3.8539], [3.3483, 3.5955, 3.5906], [2.6669, 3.1809, 3.1692], [2.2827, 2.8246, 2.7846]],
    [[4.2972, 4.1538, 4.1489], [3.7710, 3.7127, 3.8298], [3.1780, 3.2652, 3.2733], [2.6974, 2.8244, 2.7765]],
    [[2.9210, 2.7516, 2.8778], [2.5510, 2.4461, 2.4030], [2.3799, 2.2971, 2.3184], [2.0624, 2.0341, 1.9753]],
    [[4.5390, 4.2330, 4.3991], [4.0411, 3.9834, 3.9852], [3.6423, 3.4971, 3.4971], [3.0359, 2.8756, 2.9334]],
]

df = ['1', '2', '3'] # default
alt = ['4', '5', '6']
files = [
    ['MyOne T1 Streptavidin', '2025.04.29/dt1_2', df, df, df, df],
    ['MyOne C1 Streptavidin', '2025.04.28/dc1_2', df, df, df, df],
    ['Sera-Mag', '2025.05.13/sera_2', df, df, df, df],
    ['Speedbead', '2025.05.13/spbd_2', df, df, df, df],
]
labels = ['T1', 'C1', 'SM', 'SB']

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
            ax.plot([i], conc_chi[k], linestyle='none', marker=trial_markers[k],
                markeredgecolor=trial_colors[k])

print('chis:\navgs:')
print(avg_chis)
print('stds:')
print(std_chis)

for j in range(4):
    conc = cs[j]
    print('for conc {} µg/mL:'.format(conc))
    for i in range(len(chis)):
        for k in range(i+1, len(chis)):
            res = ttest(chis[i][j], chis[k][j])
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
    ax.set_xlim([-0.5, len(labels)-0.5])
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
            ax.plot(i, resp_time, linestyle='none', marker=trial_markers[fi],
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

print('\n\nRESPONSE TIMES')
for j in range(4):
    conc = cs[j]
    print('for conc {} µg/mL:'.format(conc))
    for i in range(len(chis)):
        for k in range(i+1, len(chis)):
            res = ttest(resp_times[i][j], resp_times[k][j])
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
    ax.set_xlim([-0.5, len(labels)-0.5])
    ax.set_xticks(range(len(labels)), labels)

    i += 1
for ax in axes + time_axes:
    ax.axvline(1.5, color=vib_grey, alpha=0.5)

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

img_name = '../subgraphics/chi_inter_strep_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
