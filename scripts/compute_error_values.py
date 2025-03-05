from decimal import Decimal, getcontext
getcontext().prec = 128
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from process_results_plot import latex_float


LSTYLES = ['dashed','dotted','dashdot','solid']


def error1(n, epsilon, approx=False):
    if approx:
        return Decimal(n) * Decimal(epsilon)
    else:
        return (Decimal(1) + Decimal(epsilon))**Decimal(n) - Decimal(1)


def error2(n, delta, epsilon, approx=False):
    if approx:
        return Decimal(delta) * Decimal(2**(n+1))
    else:
        error2 = Decimal(0)
        for j in range(n+1):
            error2 += Decimal(2**j) * (Decimal(1) + Decimal(epsilon)) ** Decimal(j)
        error2 *= Decimal(delta)
        return error2


def compute_error(n, delta, epsilon, approx=False):
    return error1(n, epsilon, approx) + error2(n, delta, epsilon, approx)


def suggest_delta(n, epsilon, error):
    return (Decimal(error) - Decimal(n) * Decimal(epsilon)) / Decimal(2**(n+1))


def plot_lines(lines_xs, lines_ys, labels, output_name, cosiness=1.7):
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

    fig.savefig(output_name)
    fig.clear()
    plt.close()


def plot_errors_deltas(ns, deltas, epsilon):
    """
    Plot 'n' vs error bound, for different values of delta and single epsilon.
    """
    lines_xs = []
    lines_ys = []
    legend = []
    for delta in deltas:
        errors = []
        for n in ns:
            error = compute_error(n, delta, epsilon)
            errors.append(float(error))
        lines_xs.append(np.array(ns))
        lines_ys.append(np.array(errors))
        legend.append(f"$\\delta = {latex_float(delta)}$")
    plot_lines(lines_xs, lines_ys, legend, f"experiments/error_deltas_plot.pdf")


def write_errors_1_and_2(ns, delta, epsilon):
    """
    Write errors for concrete parameters.
    """
    rows = []
    for n in ns:
        rows.append(
            {'n' : n,
             'epsilon' : f'{epsilon:.3e}',
             'delta' : f'{delta:.3e}',
             'error_1' : f'{error1(n, epsilon):.3e}',
             'error_2' : f'{error2(n, delta, epsilon):.3e}'})
    df = pd.DataFrame(rows)
    print(df)


def write_delta_suggestions(ns, epsilon, errors):
    """
    For each n, give largest value of delta that still bounds error to `error`.
    """
    rows = []
    for error in errors:
        for n in ns:
            rows.append(
                {'targ_error': f'{error:.3e}',
                 'n' : n,
                 'epsilon' : f'{epsilon:.3e}',
                 'delta' : f'{suggest_delta(n, epsilon, error):.3e}'})
    df = pd.DataFrame(rows)
    print(df)


def main():
    write_errors_1_and_2([10, 20, 30, 40, 50, 60], 1e-15, 1e-16)
    write_delta_suggestions([10, 20, 30, 40, 50, 60], 1e-16, [1e-3, 1e-6])
    plot_errors_deltas(ns=range(10,21), deltas=[1e-10, 1e-8, 1e-6], epsilon=1e-16)


if __name__ == '__main__':
    main()
