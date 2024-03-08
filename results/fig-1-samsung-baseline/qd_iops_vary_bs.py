import argparse
import os.path
import subprocess

import fio

# Machine-dependent settings
all_bs = ['512', '1k', '2k', '4k', '8k', '16k', '32k', '64k']
all_qd = ['1', '2', '4', '8', '16', '32', '64', '128', '256']
cpus_allowed = 0

# Machine-dependent settings done

# settings
results_dir = 'results_qd_iops_vary_bs/fio_output'

# Read and parse results, throughput
global_rk = []
jobs_rk = [
    'read:lat_ns:mean', 'read:iops', 'read:lat_ns:stddev', 'read:iops_stddev',
    'usr_cpu', 'sys_cpu', 'read:bw'
]

iops_results = {}
iops_stddev = {}
avg_lat_results = {}
cpu_results = {}
bw_results = {}
for cur_bs in all_bs:
    iops_results[cur_bs] = []
    iops_stddev[cur_bs] = []
    avg_lat_results[cur_bs] = []
    cpu_results[cur_bs] = []
    bw_results[cur_bs] = []
    for cur_qd in all_qd:
        output_file = 'bs_{}_qd_{}.txt'.format(cur_bs, cur_qd)
        output_file = os.path.join(results_dir, output_file)
        _, j_res = fio.parse_experiment(output_file, global_rk, jobs_rk)
        j_res = j_res[0]
        iops_results[cur_bs].append(j_res['read:iops'] / 1000)
        iops_stddev[cur_bs].append(j_res['read:iops_stddev'] / 1000)
        avg_lat_results[cur_bs].append(j_res['read:lat_ns:mean'] / 1000)
        cpu_results[cur_bs].append((j_res['usr_cpu'] + j_res['sys_cpu']) / 100)
        bw_results[cur_bs].append(j_res['read:bw'] / 1024 / 1024)

import matplotlib
import matplotlib.pyplot as plt

# Switch to Type 1 Fonts.
matplotlib.rcParams['text.usetex'] = True
plt.rc('font', **{'family': 'serif', 'serif': ['Times']})

# matplotlib_color = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5']
# Check: https://personal.sron.nl/~pault/
# Paul Tol's "bright" color scheme -> Figure 1
matplotlib_color = ['#4477AA', '#228833', '#CCBB44', '#EE6677', '#AA3377', '#66CCEE', '#BBBBBB', '#332288']
m_color_index = 0


dot_style = [
    '+',
    'X',
    'o',
    'v',
    's',
    'P',
]


def get_next_color():
    global m_color_index
    c = matplotlib_color[m_color_index]
    m_color_index += 1

    return c


def reset_color():
    global m_color_index
    m_color_index = 0


# Global parameters
linewidth = 4
markersize = 15

datalabel_size = 36
datalabel_va = 'bottom'
axis_tick_font_size = 46
axis_label_font_size = 52
legend_font_size = 46

####################################
# Throughput: IOPS
####################################
if True:
    # Data, set unused value to none
    group_list = all_bs
    y_values_ax1 = avg_lat_results
    y_values_ax2 = cpu_results
    std_dev_ax1 = None
    std_dev_ax2 = None
    x_ticks = iops_results
    legend_label = {
        '512': '512',
        '1k': '1K',
        '2k': '2K',
        '4k': '4K',
        '8k': '8K',
        '16k': '16K',
        '32k': '32K',
        '64k': '64K'
    }

    title = None
    xlabel = 'Throughput (KIOPS)'
    ylabel_ax1 = 'Average latency ($\mu$s)'
    fig_save_path = 'fig-1a-qd-iops-vary-bs-throughput.pdf'

    reset_color()
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.set_xlabel(xlabel, fontsize=axis_label_font_size)
    ax.set_ylabel(ylabel_ax1, fontsize=axis_label_font_size)
    ax.grid(True)

    ax.tick_params(axis='both', which='major', labelsize=axis_tick_font_size)
    ax.xaxis.set_ticks([100, 200, 300, 400])
    ax.set_xlim([0, 400])
    ax.set_ylim([0, 1000])
    ax.yaxis.set_ticks([0, 250, 500, 750, 1000])
    ax.yaxis.set_ticklabels(['0', '250', '500', '750', '1,000'])

    # Throughput
    for (index, group_name) in zip(range(len(group_list)), group_list):
        # x, y, std_dev, data_label = data[group_name]
        if x_ticks:
            x = x_ticks[group_name]
        y = y_values_ax1[group_name]
        y = [i for i in y if i < 900]
        x = x[:len(y)]
        yerr = None
        if std_dev_ax1:
            yerr = std_dev_ax1[group_name]
        label = legend_label[group_name]
        # if group_name in ['8k', '16k', '32k', '64k']:
        #     label = None

        ax.errorbar(
            x,
            y,
            yerr=yerr,
            label=label,
            marker=dot_style[index % len(dot_style)],
            linewidth=linewidth,
            markersize=markersize,
            color=get_next_color(),
        )

        if not group_name in [
                '512',
                '1k',
                '2k',
        ]:
            # Add data label
            for i in range(len(x)):
                if i == 7:
                    ax.text(x[i]-50, y[i], all_qd[i], size=datalabel_size)
                elif i == 8:
                    ax.text(x[i]-10, y[i], all_qd[i], size=datalabel_size)
                elif i > 3:
                    ax.text(x[i]-20, y[i], all_qd[i], size=datalabel_size)

        if group_name in ['512', '8k']:
            for i in range(len(x)):
                if i <= 3:
                    ax.text(x[i], y[i], all_qd[i], size=datalabel_size)

    reset_color()
    x = x_ticks['512']
    y = y_values_ax1['512']
    y = [i for i in y if i < 900]
    x = x[:len(y)]
    ax.errorbar(
            x,
            y,
            yerr=None,
            marker=dot_style[0],
            linewidth=linewidth,
            markersize=markersize,
            color=get_next_color(),
    )
    
    leg = ax.legend(
        fontsize=legend_font_size,
        ncol=3,
        loc='upper left',
        handlelength=1.3,
        handletextpad=0.2,
        bbox_to_anchor=(-0.03, 1.02),
        columnspacing=0.15,
        labelspacing=0.05,
        borderpad=0.3,
    )
    
    for line in leg.get_lines():
        line.set_linewidth(6)


    # draw arrows
    plt.arrow(200, 500, 150, -280, width=10, head_width=20, color='black')
    plt.text(180, 520, '370 KIOPS', size=datalabel_size)
    plt.savefig(fig_save_path, bbox_inches='tight')