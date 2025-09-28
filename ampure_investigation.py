# plot the analysis of ampure beads for thesis
#
# Lexie Scholtz
# Created 2025.09.28 back in boise

ver = 1.0
to_save = True

import sys
import numpy as np
from matplotlib import pyplot as plt
from qc_formats import *
from matplotlib import gridspec as gridspec
from scipy.stats import linregress
from matplotlib.legend_handler import HandlerLine2D, HandlerTuple

# laser warmup
path = '../../../../../armani_lab/research/qcMAP/qc_data/'

# label, dir, file_prefix, ws, xs, ys, zs
df = ['1', '2', '3'] # default
alt = ['4', '5', '6']
# rows:  ampure xp, sera-mag, speedbead
chis = [
    [[3.1437, 3.1912, 3.2796], [2.7412, 3.1051, 2.9845], [2.9971, 2.7717, 2.7306], [1.7762, 2.3993, 1.9013]],
    [[2.9210, 2.7516, 2.8778], [2.5510, 2.4461, 2.4030], [2.3799, 2.2971, 2.3184], [2.0624, 2.0341, 1.9753]],
    [[4.5390, 4.2330, 4.3991], [4.0411, 3.9834, 3.9852], [3.6423, 3.4971, 3.4971], [3.0359, 2.8756, 2.9334]],
]

df = ['1', '2', '3'] # default
alt = ['4', '5', '6']
files = [
    ['AMPure XP', '2025.05.09/amp_2', df, df, alt, df],
    ['Sera-Mag', '2025.05.13/sera_2', df, df, df, df],
    ['Speedbead', '2025.05.13/spbd_2', df, df, df, df],
]

c_ids = ['w', 'x', 'y', 'z']
cs = [100, 80, 60, 40]

colors = [purple, cyan, teal, magenta]
bead_colors = [pink, darker_blue, teal]

fig = plt.figure(figsize=(6.5, 2.5), dpi=dpi_disp)
gs = gridspec.GridSpec(2, 3, height_ratios=[0.1, 1])
leg_ax = fig.add_subplot(gs[0, :])
prep_legax([leg_ax])

ax1 = fig.add_subplot(gs[1, 0])
ax1_in = ax1.inset_axes([0.45, 0.2, 0.45, 0.45])
ax2 = fig.add_subplot(gs[1, 1])
ax3 = fig.add_subplot(gs[1, 2])

# ax 1: plot the 100 µg/mL map data files
for i in range(len(files)):
    series = files[i]
    series_name = series[0]
    dir = series[1]
    c_id = c_ids[0]
    conc_series = series[2]
    c0 = cs[0]
    for fi in range(len(conc_series)):
        data = np.genfromtxt(path + dir + c_id + conc_series[fi] + '.txt')

        time = data[:, 0] / 60 # convert to min
        lux = data[:, 1] / 1000 # convert to klx

        ax1.plot(time, lux, color=bead_colors[i], alpha=1-fi/3)

        conc = calibrate(lux, c0)
        ax1_in.plot(time, conc, color=bead_colors[i], alpha=1-fi/3, zorder=2)

# calculate response times
resp_times = []
for i in range(len(files)):
    series = files[i]
    series_name = series[0]
    dir = series[1]
    suffixes = series[2:]
    series_times = []

    for ci in range(len(suffixes)):
        conc_series = suffixes[ci]
        c_id = c_ids[ci]
        c0 = cs[ci]

        conc_times = []
        for fi in range(len(conc_series)):
            resp_time = calculate_resp_time(path + dir + c_id + conc_series[fi] + '.txt')
            conc_times.append(resp_time)

        series_times.append(conc_times)
    resp_times.append(series_times)

# ax 2+3 plot chis and response times
avg_chis = np.zeros([len(chis), 4])
std_chis = np.zeros([len(chis), 4])
avg_rts = np.zeros([len(resp_times), 4])
std_rts = np.zeros([len(resp_times), 4])

for i in range(len(chis)):
    lot_chis = chis[i]
    lot_rts = resp_times[i]
    for j in range(len(lot_chis)):
        # find avgs and stds
        avg_chis[i, j] = np.mean(lot_chis[j])
        std_chis[i, j] = np.std(lot_chis[j])

        avg_rts[i, j] = np.mean(lot_rts[j])
        std_rts[i, j] = np.std(lot_rts[j])

for i in range(len(chis)):
    ax2.errorbar(cs, avg_chis[i], std_chis[i], linestyle='none',
        marker=trial_markers[i], markeredgecolor=bead_colors[i],
        capsize=m_size-1, ecolor=bead_colors[i], elinewidth=l_width)
    res = linregress(cs, avg_chis[i])
    xs = [30, 110]
    ys = [x * res.slope + res.intercept for x in xs]
    ax2.plot(xs, ys, linestyle=':', color=bead_colors[i], alpha=0.5)

    ax3.errorbar(cs, avg_rts[i], std_rts[i], linestyle='none',
        marker=trial_markers[i], markeredgecolor=bead_colors[i],
        capsize=m_size-1, ecolor=bead_colors[i], elinewidth=l_width)
    res = linregress(cs, avg_rts[i])
    xs = [30, 110]
    ys = [x * res.slope + res.intercept for x in xs]
    ax3.plot(xs, ys, linestyle=':', color=bead_colors[i], alpha=0.5)

ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Illum. (klx)')
ax1.set_xlim([0, 5])
ax1.set_xticks([0, 2.5, 5])
ax1.set_ylim([-2, 32])

ax1_in.set_ylabel('c (µg/mL)', labelpad=-0.5)
ax1_in.set_xlim([0, 1])
ax1_in.set_ylim([-10, 110])
ax1_in.tick_params(axis='both', pad=0.5)

for ax in [ax2, ax3]:
    ax.set_xlabel('Concentration (µg/mL)')
    ax.set_xlim([30, 110])
    ax.set_xticks([40, 60, 80, 100])

ax2.set_ylabel(r'$\chi_{eff}$')
ax2.set_ylim([0, 5])
ax2.set_yticks([0, 2.5, 5])

ax3.set_ylabel('Response Time (s)')
ax3.set_ylim([0, 120])
ax3.set_yticks([0, 40, 80, 120])

handles = []
labels = []
for k in range(len(files)):
    h1, = leg_ax.plot([], [], color=bead_colors[k])
    h2 = leg_ax.errorbar(-100, -100, 10,  linestyle='none',
        marker=trial_markers[k], markeredgecolor=bead_colors[k],
        capsize=m_size-1, ecolor=bead_colors[k], elinewidth=l_width)
    handles.append((h1, h2))
    labels.append(files[k][0])

    h3, = leg_ax.plot([], [], marker='s', linestyle='none', markerfacecolor=black,
        alpha=1-k/3, markeredgewidth=0)
    handles.append(h3)
    labels.append('Trial {}'.format(k+1))
leg_ax.legend(handles, labels, loc='center', ncol=3, handlelength=h_length_dotted,
    handler_map={tuple: HandlerTuple(ndivide=None)})
leg_ax.set_xlim([0, 1])
leg_ax.set_ylim([0, 1])

# --- SAVE FIG ---
plt.tight_layout(pad=pad_loose, h_pad=2)

img_name = '../subgraphics/ampure_investigation_' + str(ver) + '.png'

if not to_save:
    # show fig - previews only
    print('displaying ' + img_name)
    plt.show()
else:
    # save fig
    plt.savefig(img_name, dpi=dpi_save)
    print('saved file as: ' + img_name)
