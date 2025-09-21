# plot the chi for dynabead lots data for thesis
#
# Lexie Scholtz
# Created 2025.09.20 in portree, isle of skye

ver = 1.3
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
chis = [
    [[1.2098, 1.1986, 1.2366], [1.0535, 1.1018, 1.1164], [1.1661, 0.5568, 0.6908], [1.1065, 1.2270, 1.0544]],
    [[0.9430, 1.1790, 1.1726], [0.6799, 0.9687, 1.0441], [0.9318, 0.9503, 0.7842], [0.8061, 1.1582, 0.9194]],
    [[1.0328, 1.0713, 1.0718], [0.8963, 1.1487, 1.0927], [1.1365, 1.0336, 0.9476], [1.0002, 0.6096, 0.5280]]
]

df = ['1', '2', '3'] # default
files = [
    ['M-280 Streptavidin lot 1', '2025.04.28/dm81_2', df, df, df, df],
    ['M-280 Streptavidin lot 2', '2025.04.28/dm82_2', df, df, df, df],
    ['M-280 Streptavidin lot 3', '2025.04.28/dm83_2', df, df, df, ['4', '5', '6']],
]
dm83z_dir = '2025.04.28/dm83_2'
c_ids = ['w', 'x', 'y', 'z']

cs = [100, 80, 60, 40]

colors = [cyan, teal, pink, cyan]
markers = ['o', 'D', 's', '^']

time_colors = [dark_blue, green, purple]
time_markers = ['x', '+', '^']

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

avg_chis = np.zeros([3, 4])
std_chis = np.zeros([3, 4])

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
    res_a = ttest(chis[0][j], chis[1][j])
    print('for lot 1/2: t-stat: {}, p value {}'.format(res_a.statistic, res_a.pvalue))
    res_b = ttest(chis[1][j], chis[2][j])
    print('for lot 2/3: t-stat: {}, p value {}'.format(res_b.statistic, res_b.pvalue))
    res_c = ttest(chis[0][j], chis[2][j])
    print('for lot 1/3: t-stat: {}, p value {}'.format(res_c.statistic, res_c.pvalue))

for ax in axes:
    ax.set_xlabel('Lot')
    ax.set_ylabel(r'$\chi_{eff}$')
    ax.set_xlim([-0.5, 2.5])
    ax.set_xticks([0, 1, 2], [1, 2, 3])
    ax.set_ylim([0.35, 1.65])
    ax.set_yticks([0.5, 1.0, 1.5])

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

        if 'lot 3' in series_name and ci == 3:
            dir = dm83z_dir
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
    res_a = ttest(resp_times[0][j], resp_times[1][j])
    print('for lot 1/2: t-stat: {}, p value {}'.format(res_a.statistic, res_a.pvalue))
    res_b = ttest(resp_times[1][j], resp_times[2][j])
    print('for lot 2/3: t-stat: {}, p value {}'.format(res_b.statistic, res_b.pvalue))
    res_c = ttest(resp_times[0][j], resp_times[2][j])
    print('for lot 1/3: t-stat: {}, p value {}'.format(res_c.statistic, res_c.pvalue))


for ax in time_axes:
    ax.set_xlabel('Lot')
    ax.set_xlim([-0.5, 2.5])
    ax.set_xticks([0, 1, 2], [1, 2, 3])
    ax.set_ylabel('Response Time (s)')
    ax.set_ylim([23, 37])
    ax.set_yticks([25, 30, 35])

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
plt.tight_layout(pad=pad_loose)
plt.subplots_adjust(hspace=0)
fig.align_ylabels()

img_name = '../subgraphics/chi_lots_dyna_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
