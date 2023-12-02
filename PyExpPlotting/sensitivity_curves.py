import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from dataclasses import dataclass
from typing import Any, Dict, Sequence, Tuple
from PyExpUtils.results.tools import subsetDF, splitByValue
from PyExpPlotting.colors import ColorPalette
from PyExpPlotting.tools import reduceCurve, CurveReducer, getBest

# TODO: some of these are true of all plots
# could set up an inheritance system
@dataclass
class SensitivityOptions:
    hypers: Sequence[str] | None = None
    style: str = 'solid'
    color: ColorPalette = ColorPalette()
    label: str | None = None
    width: float = 1.0
    height: float = 1.0
    legend: bool = True
    linewidth: float = 1.0
    log_x: int | None = None
    x_label: str | None = None
    y_label: str | None = None
    title: str | None = None

    prefer: str = 'big'
    curve_reducer: str | CurveReducer = 'auc'
    param_reducer: str = 'best'

def _getHypers(df: pd.DataFrame, param: str, metric: str):
    return set(df.columns) - {param, metric}

def sliceBestPerformance(df: pd.DataFrame, param: str, metric: str, options: SensitivityOptions):
    perf = reduceCurve(df, metric, options.curve_reducer)
    idx = getBest(perf, options.prefer)
    row = df.iloc[idx]

    hypers = options.hypers or _getHypers(df, param, metric)
    conds = { k: row[k] for k in hypers }
    parts = subsetDF(df, conds)

    param_vals = df[param].unique()
    param_vals.sort()

    out: Dict[Any, float] = {}
    for p in param_vals:
        sub = parts[parts[param] == p]
        out[p] = sub[metric]

    return out

def bestPerformanceEach(df: pd.DataFrame, param: str, metric: str, options: SensitivityOptions):
    df = df.copy()
    df['_perf'] = reduceCurve(df, metric, options.curve_reducer)

    out: Dict[Any, float] = {}
    for (p, sub) in splitByValue(df, param):
        idx = getBest(sub['_perf'], options.prefer)
        row = sub.iloc[idx]
        out[p] = row['_perf']

    return out

def plot_sensitivity(df: pd.DataFrame, ax: Axes, param: str, metric: str, options: SensitivityOptions):
    if options.param_reducer == 'slice':
        parts = sliceBestPerformance(df, param, metric, options)

    elif options.param_reducer == 'best':
        parts = bestPerformanceEach(df, param, metric, options)

    else:
        raise Exception('Unknown parameter reduction strategy')

    return plotSensitivityCurve(parts, ax, param=param, options=options)

def plotSensitivityCurve(parts: Dict[Any, float], ax: Axes, cis: Dict[Any, Tuple[float, float]] | None = None, param: str = '', options: SensitivityOptions = SensitivityOptions()):
    x = np.asarray(list(parts.keys()))
    y = np.asarray(list(parts.values()))

    idxs = np.argsort(x)
    x = x[idxs]
    y = y[idxs]

    ci = None
    if cis is not None:
        x_ci = np.asarray(list(cis.keys()))
        y_ci = np.asarray(list(cis.values()))

        idxs = np.argsort(x_ci)
        ci = y_ci[idxs]

    color = options.color.get(options.label)
    ax.plot(
        x, y,
        label=options.label,
        color=color,
        linewidth=options.linewidth,
    )

    if ci is not None:
        ax.fill_between(x, ci[:, 0], ci[:, 1], color=color, alpha=0.2)

    # TODO: make this a shared method
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    if options.log_x is not None:
        ax.set_xscale('log', base=options.log_x)

    if options.legend:
        ax.legend(frameon=False)

    if options.x_label is None:
        x_label = param.split('.')[-1]
        if options.log_x is not None:
            scale = options.log_x
            x_label += f' (log-{scale} scale)'

        ax.set_xlabel(x_label)

    elif options.x_label:
        ax.set_xlabel(options.x_label)

    if options.y_label:
        ax.set_ylabel(options.y_label)

    if options.title is not None:
        ax.set_title(options.title)
