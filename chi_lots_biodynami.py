# plot the chi for dynabead lots data for thesis
#
# Lexie Scholtz
# Created 2025.09.21 in Stornoway, Isle of Lewis, Scotland

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
chis = [
    [[4.2965, 4.0717, 4.0859], [3.9145, 3.6592, 3.7009], [3.3628, 3.3189, 3.3514], [2.7022, 3.0075, 2.9305]],
    [[4.4124, 4.1228, 4.2719], [4.0964, 3.9435, 3.9039], [3.6002, 3.4428, 3.4182], [2.8203, 2.7247, 2.7923]],
    [[4.2287, 4.1348, 4.1800], [3.9223, 3.7326, 3.8294], [3.4125, 3.3902, 3.2957], [3.1781, 3.0421, 2.7787]]
]

df = ['1', '2', '3'] # default
alt = ['4', '5', '6']
files = [
    ['BioDyanmi Lot 1', '2025.05.12/bio1', alt, alt, df, df],
    ['BioDynami Lot 2', '2025.05.12/bio2', df, df, df, df],
    ['BioDynami Lot 3', '2025.05.12/bio3', df, df, df, df],
]

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
            ax.plot([i], conc_chi[k], linestyle='none', marker=time_markers[k],
                markeredgecolor=time_colors[k])

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

i = 0
yranges = [
    [3.5, 4.0, 4.5, 5.0, 5.5],
    [3.0, 3.5, 4.0, 4.5, 5.0],
    [3.0, 3.5, 4.0, 4.5, 5.0],
    [2.5, 3.0, 3.5, 4.0, 4.5]
]
for ax in axes:
    ax.set_xlabel('Lot')
    ax.set_ylabel(r'$\chi_{eff}$')
    ax.set_xlim([-0.5, 2.5])
    ax.set_xticks([0, 1, 2], [1, 2, 3])
    ax.set_ylim(yranges[i][0]-0.2, yranges[i][-1]+0.2)
    ax.set_yticks([yranges[i][0], yranges[i][2], yranges[i][4]])
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
            ax.plot(i, resp_time, linestyle='none', marker=time_markers[fi],
                markeredgecolor=time_colors[fi])
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

yranges = [
    [45, 55, 65],
    [50, 60, 70],
    [55, 65, 75],
    [60, 70, 80]
]
i = 0
for ax in time_axes:
    ax.set_xlabel('Lot')
    ax.set_xlim([-0.5, 2.5])
    ax.set_xticks([0, 1, 2], [1, 2, 3])
    ax.set_ylabel('Response Time (s)')
    ax.set_ylim(yranges[i][0]-2.5, yranges[i][-1]+2.5)
    ax.set_yticks(yranges[i])
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
plt.tight_layout(pad=pad_loose)
plt.subplots_adjust(hspace=0)
fig.align_ylabels()

img_name = '../subgraphics/chi_lots_biodynami_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
