# plot the chi for dynabead streptavidin product lines data for thesis
#
# Lexie Scholtz
# Created 2025.09.21 in Stornoway, Isle of Lewis, Scotland

ver = 1.2
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
# rows: M-280, M-270, T1, C1
chis = [
    [[1.2098, 1.1986, 1.2366], [1.0535, 1.1018, 1.1164], [1.1661, 0.5568, 0.6908], [1.1065, 1.2270, 1.0544]],
    [[1.6844, 1.6761, 1.8383], [1.4534, 1.1898, 1.5277], [1.2991, 1.0589, 1.0393], [1.1861, 1.0898, 1.1164]],
    [[3.8680, 3.9787, 3.8539], [3.3483, 3.5955, 3.5906], [2.6669, 3.1809, 3.1692], [2.2827, 2.8246, 2.7846]],
    [[4.2972, 4.1538, 4.1489], [3.7710, 3.7127, 3.8298], [3.1780, 3.2652, 3.2733], [2.6974, 2.8244, 2.7765]]
]

df = ['1', '2', '3'] # default
alt = ['4', '5', '6']
files = [
    ['M-280 Streptavidin lot 1', '2025.04.28/dm81_2', df, df, df, df],
    ['M-270 Streptavidin', '2025.04.29/dm7_2', df, df, df, df],
    ['MyOne T1 Streptavidin', '2025.04.29/dt1_2', df, df, df, df],
    ['MyOne C1 Streptavidin', '2025.04.28/dc1_2', df, df, df, df],
]

c_ids = ['w', 'x', 'y', 'z']

cs = [100, 80, 60, 40]

colors = [cyan, teal, pink, purple]
markers = ['o', 'D', 's', '^']

fig = plt.figure(figsize=(6.5, 3.5), dpi=dpi_disp)
gs = gridspec.GridSpec(3, 4, height_ratios=[0.35, 1, 1])
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
            ax.plot([i], conc_chi[k], linestyle='none', marker=markers[k],
                markeredgecolor=colors[k])

print(avg_chis)

for j in range(4):
    conc = cs[j]
    print('for conc {} µg/mL:'.format(conc))
    for i in range(4):
        for k in range(i+1, 4):
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
    [0, 2, 4, 6, 8],
]
for ax in axes:
    ax.set_xlim([-0.5, 3.5])
    ax.set_ylabel(r'$\chi_{eff}$')
    ax.set_ylim(yranges[0][0]-0.25, yranges[0][-1]+0.25)
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
            ax.plot(i, resp_time, linestyle='none', marker=markers[fi],
                markeredgecolor=colors[fi])
            conc_times.append(resp_time)

        series_times.append(conc_times)
    resp_times.append(series_times)

print('\n\nRESPONSE TIMES')
for j in range(4):
    conc = cs[j]
    print('for conc {} µg/mL:'.format(conc))
    for i in range(4):
        for k in range(i+1, 4):
            res = ttest(chis[i][j], chis[k][j])
            if res.pvalue < 0.05:
                print('*', end='')
            if res.pvalue < 0.005:
                print('*', end='')
            if res.pvalue < 0.0005:
                print('*', end='')
            print('for lot {}/{}: t-stat: {}, p value {}'.format(i, k, res.statistic, res.pvalue))

yranges = [
    [0, 50, 100, 150],
    [0, 60, 120],
    [0, 60, 120],
    [0, 60, 120],
]
i = 0
for ax in time_axes:
    ax.set_ylabel('Response Time (s)')
    ax.set_ylim(yranges[0][0]-20, yranges[0][-1]+20)
    ax.set_yticks(yranges[0])
    ax.set_xlabel('Product Number')
    ax.set_xlim([-0.5, 3.5])
    ax.set_xticks([0, 1, 2, 3], ['280', '270', 'T1', 'C1'])

    i += 1

handles = []
labels = []
for i in range(3):
    h1, = leg_ax.plot([], [], linestyle='none', marker=markers[i],
        color=colors[i], label='Trial {}'.format(i+1))
    # h2, = leg_ax.plot([], [], linestyle='none', marker=time_markers[i],
    #     color=time_colors[i])
    # handles.append((h1, h2))
    # labels.append('Trial {}'.format(i+1))
leg_ax.legend(ncol=3, loc='center', bbox_to_anchor=(0.5, 1.0),
    handler_map={tuple: HandlerTuple(ndivide=None)})

# --- SAVE FIG ---
plt.tight_layout(pad=pad_tight)
plt.subplots_adjust(hspace=0)
fig.align_ylabels()

img_name = '../subgraphics/chi_dyna_strep_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
