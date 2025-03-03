from decimal import Decimal, getcontext
getcontext().prec = 128
import numpy as np
import matplotlib.pyplot as plt
from process_results_plot import latex_float


LSTYLES = ['dashed','dotted','dashdot','solid']


def plot_lines(lines_xs, lines_ys, labels, cosiness=1.7):
    """
    Plot multiple lines (lines_xs and lines_ys should be 2D) with given labels (1D).
    """
    fig, ax = plt.subplots(layout='constrained')

    for i, (xs, ys, label) in enumerate(zip(lines_xs, lines_ys, labels)):
        ax.plot(xs, ys, label=label, linestyle=LSTYLES[i % len(LSTYLES)])
    
    # legend + axes
    ax.legend()
    ax.set_yscale('log')
    ax.set_xlabel('$n$')
    ax.set_ylabel('error bound')

    # squeeze/stretch
    fig.draw_without_rendering()
    tb = fig.get_tightbbox(fig.canvas.get_renderer())
    fig.set_size_inches(tb.width/cosiness, tb.height/cosiness)

    fig.savefig(f"experiments/error2_plot.pdf")
    fig.clear()
    plt.close()


def plot_error2(ns, deltas, epsilon):
    """
    Plot 'n' vs error bound, for different values of delta and single epsilon.
    """
    lines_xs = []
    lines_ys = []
    legend = []
    for delta in deltas:
        errors = []
        for n in ns:
            error = Decimal(0)
            for j in range(n+1):
                error += Decimal(2**j) * (Decimal(1) + Decimal(epsilon)) ** Decimal(j)
            error *= Decimal(delta)
            errors.append(float(error))
        lines_xs.append(np.array(ns))
        lines_ys.append(np.array(errors))
        legend.append(f"$\\delta = {latex_float(delta)}$")
    plot_lines(lines_xs, lines_ys, legend)


def main():
    plot_error2(ns=range(10,21), deltas=[1e-10, 1e-8, 1e-6], epsilon=1e-15)


if __name__ == '__main__':
    main()
