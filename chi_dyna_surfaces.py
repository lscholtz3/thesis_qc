# plot the chi for dynabead streptavidin product lines data for thesis
#
# Lexie Scholtz
# Created 2025.09.22 in Stornoway, Isle of Lewis, Scotland

ver = 2.0
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
# rows:  M-270 carb,  protein G, M-270 strep,,
chis = [
    [[1.5573, 1.6924, 1.7793], [1.5378, 1.6185, 1.7452], [1.4638, 1.5556, 1.0102], [1.4269, 1.3791, 1.3608]],
    [[1.9261, 1.9436, 2.0810], [1.8082, 1.8332, 1.7370], [1.0653, 1.0017, 1.6294], [1.5292, 1.4042, 1.3193]],
    [[1.6844, 1.6761, 1.8383], [1.4534, 1.1898, 1.5277], [1.2991, 1.0589, 1.0393], [1.1861, 1.0898, 1.1164]],
]

df = ['1', '2', '3'] # default
alt = ['4', '5', '6']
files = [
    ['Carboxylic Acid', '2025.04.29/dca_2', df, df, df, df],
    ['Protein G', '2025.05.01/dpg_2', df, ['1-ex', '2-ex', '3-ex'], df, df],
    ['M-270 Streptavidin', '2025.04.29/dm7_2', df, df, df, df],
]

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

print(avg_chis)

for j in range(4):
    conc = cs[j]
    print('for conc {} µg/mL:'.format(conc))
    for i in range(3):
        for k in range(i+1, 3):
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
    [0, 1, 2, 3],
]
for ax in axes:
    ax.set_xlim([-0.5, 2.5])
    ax.set_ylabel(r'$\chi_{eff}$')
    ax.set_ylim(yranges[0][0]-0.3, yranges[0][-1]+0.3)
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
    for i in range(3):
        for k in range(i+1, 3):
            res = ttest(chis[i][j], chis[k][j])
            if res.pvalue < 0.05:
                print('*', end='')
            if res.pvalue < 0.005:
                print('*', end='')
            if res.pvalue < 0.0005:
                print('*', end='')
            print('for lot {}/{}: t-stat: {}, p value {}'.format(i, k, res.statistic, res.pvalue))

yranges = [
    [0, 15, 30],
]
i = 0
for ax in time_axes:
    ax.set_ylabel('Response Time (s)')
    ax.set_ylim(yranges[0][0]-3, yranges[0][-1]+3)
    ax.set_yticks(yranges[0])
    ax.set_xlabel('Surface Coating')
    ax.set_xlim([-0.5, 2.5])
    ax.set_xticks([0, 1, 2], ['CA', 'PG', 'ST'])

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

img_name = '../subgraphics/chi_dyna_surfaces_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
