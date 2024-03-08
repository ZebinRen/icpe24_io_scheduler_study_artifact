import matplotlib
import matplotlib.pyplot as plt
import pickle

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


# pickle
def pickle_load(filename):
    f = open(filename, 'rb')
    ret = pickle.load(f)
    f.close()
    print("{} loaded".format(filename))
    return ret


# Sampled
def sample_list(l, sample_size):
    if len(l) <= sample_size:
        return l
    return l[::len(l) // sample_size]
