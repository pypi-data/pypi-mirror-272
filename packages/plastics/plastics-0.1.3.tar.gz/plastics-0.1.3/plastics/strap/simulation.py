# -*- coding: utf-8 -*-
"""
"""
from plastics import strap as sp
from warnings import filterwarnings, warn
from biosteam.utils import GG_colors, CABBI_colors
import biosteam as bst
import numpy as np
import pandas as pd
import os
from thermosteam.units_of_measure import format_units
from thermosteam.utils import roundsigfigs
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from colorpalette import Color
import yaml

__all__ = ('run_monte_carlo', 'plot_spearman', 'plot_kde',
           'plot_MSP_GWP_across_dissolution_capacity_boiling_point',
           'run_monte_carlo_across_polymer_composition',
           'plot_MSP_across_polymer_composition',
           'plot_spearman_both',
           'sobol_analysis')

results_folder = os.path.join(os.path.dirname(__file__), 'results')
images_folder = os.path.join(os.path.dirname(__file__), 'images')

def sobol_file(name, extention='xlsx'):
    filename = name + '_sobol'
    filename += '.' + extention
    return os.path.join(results_folder, filename)

def monte_carlo_file(name, extention='xlsx'):
    filename = name + '_monte_carlo'
    filename += '.' + extention
    return os.path.join(results_folder, filename)

def spearman_file(name):
    filename = name + '_spearman'
    filename += '.xlsx'
    return os.path.join(results_folder, filename)

def autoload_file_name(name):
    filename = name
    return os.path.join(results_folder, filename)

def set_font(size=8, family='sans-serif', font='Arial'):
    import matplotlib
    fontkwargs = {'size': size}
    matplotlib.rc('font', **fontkwargs)
    params = matplotlib.rcParams
    params['font.' + family] = font
    params['font.family'] = family

def set_figure_size(width=None, aspect_ratio=None, units=None): 
    # units default to inch
    # width defaults 6.614 inches
    # aspect ratio defaults to 0.65
    if aspect_ratio is None:
        aspect_ratio = 0.65
    if width is None:
        width = 6.6142
    elif width == 'half':
        width = 6.6142 / 2
    else:
        if units is not None:
            from thermosteam.units_of_measure import convert
            width = convert(width, units, 'inch')
    import matplotlib
    params = matplotlib.rcParams
    params['figure.figsize'] = (width, width * aspect_ratio)

def get_spearman_names(parameters):
    from plastics.strap import SingleDissolutionSTRAPModel
    pm = SingleDissolutionSTRAPModel(simulate=False)
    name = 'name'
    full_name = 'full_name'
    spearman_labels = {
        i: full_name for i in parameters
    }
    spearman_labels[pm.set_IRR] = 'IRR'
    
    def with_units(f, name, units=None):
        d = f.distribution
        dname = type(d).__name__
        if units is None: units = f.units
        if dname == 'Triangle':
            distribution = ', '.join([format(j, '.3g')
                                      for j in d._repr.values()])
        elif dname == 'Uniform':
            distribution = ' $-$ '.join([format(j, '.3g')
                                         for j in d._repr.values()])
        if units is None:
            return f"{name}\n[{distribution}]"
        else:
            return f"{name}\n[{distribution} {format_units(units)}]"
        
    def get_full_name(f):
        a = f.element_name
        if a == 'Cofermentation':
            a = 'Co-Fermentation'
        b = f.name
        if b == 'GWP': 
            return f"{a} {b}"
        else:
            return f"{a} {b.lower()}"
        
    for i, j in tuple(spearman_labels.items()):
        if j == name:
            spearman_labels[i.index] = with_units(i, i.name)
        elif j == full_name:
            spearman_labels[i.index] = with_units(i, get_full_name(i))
        elif isinstance(j, tuple):
            spearman_labels[i.index] = with_units(i, *j)
        elif isinstance(j, str):
            spearman_labels[i.index] = with_units(i, j)
        else:
            raise TypeError(str(j))
        del spearman_labels[i]
    
    return spearman_labels

def plot_spearman_both(**kwargs):
    set_font(size=10)
    set_figure_size(aspect_ratio=0.8)
    labels = ['TEA', 'LCA']
    pm = sp.SingleDissolutionSTRAPModel(simulate=False, **kwargs)
    rhos = []
    file = spearman_file(pm.name)
    df = pd.read_excel(file, header=[0, 1], index_col=[0, 1])
    names = get_spearman_names(pm.model.parameters)
    names = [names[i] for i in df.index]
    metric_names = []
    for label in labels:
        if label == 'TEA':
            metric = pm.MSP
            metric_name = metric.name
            values = df[metric.index]
            for i in pm.model.parameters:
                if i not in pm.general_parameters: 
                    values[i.index] = 0
        elif label == 'LCA':
            metric = pm.GWP
            metric_name = r'GWP$_{\mathrm{mass}}$'
            values = df[metric.index]
            for i in pm.model.parameters:
                if i not in pm.general_parameters: 
                    values[i.index] = 0
        else:
            raise ValueError(f"invalid label '{label}'")
        rhos.append(values)
        metric_names.append(metric_name)
    color_wheel = [Color(fg='#0c72b9'), Color(fg='#d34249')]
    fig, ax = bst.plots.plot_spearman_2d(rhos, index=names,
                                         color_wheel=color_wheel,
                                         name=metric_name,
                                         cutoff=0.20,
                                         xlabel="Spearman's rank correlation coefficient",
                                         **kwargs)
    legend_kwargs = {'loc': 'lower left'}
    plt.legend(
        handles=[
            mpatches.Patch(
                color=color_wheel[i].RGBn, 
                label=metric_names[i],
            )
            for i in range(len(labels))
        ], 
        **legend_kwargs,
    )
    return fig, ax

def plot_spearman(kind=None, **kwargs):
    set_font(size=10)
    set_figure_size(aspect_ratio=0.8)
    if kind is None: kind = 'TEA'
    pm = sp.SingleDissolutionSTRAPModel(simulate=False, **kwargs)
    if kind == 'TEA':
        metric = pm.MSP
        metric_name = metric.name
    elif kind == 'LCA':
        metric = pm.GWP
        metric_name = r'GWP$_{\mathrm{mass}}$'
    else:
        raise ValueError(f"invalid kind '{kind}'")
    rhos = []
    file = spearman_file(pm.name)
    df = pd.read_excel(file, header=[0, 1], index_col=[0, 1])
    rhos = df[metric.index]
    names = get_spearman_names(pm.model.parameters)
    index = [names[i] for i in rhos.index]
    color_wheel = [GG_colors.orange, GG_colors.blue]
    fig, ax = bst.plots.plot_spearman_2d([rhos], index=index,
                                         color_wheel=color_wheel,
                                         xlabel="Spearman's rank correlation coefficient",
                                         cutoff=0.06,
                                         **kwargs)
    return fig, ax

def run_monte_carlo(
        N, rule='L',
        sample_cache={},
        autosave=True,
        autoload=True,
        optimize=True,
        **kwargs
    ):
    filterwarnings('ignore', category=bst.exceptions.DesignWarning)
    filterwarnings('ignore', category=bst.exceptions.CostWarning)
    pm = sp.SingleDissolutionSTRAPModel(simulate=False, **kwargs)
    pm.model.exception_hook = 'raise'
    file = monte_carlo_file(pm.name)
    N_notify = min(int(N/10), 20)
    autosave = N_notify if autosave else False
    autoload_file = autoload_file_name(pm.name)
    np.random.seed(1)
    samples = pm.model.sample(N, rule)
    pm.model.load_samples(samples, optimize=optimize)
    convergence_model = bst.ConvergenceModel(
        # Recycle loop prediction will be based on model parameters
        predictors=pm.model.parameters,
    )
    pm.model.evaluate(
        notify=int(N/10),
        autosave=autosave,
        autoload=autoload,
        file=autoload_file,
        convergence_model=convergence_model,
    )
    pm.model.table.to_excel(file)
    pm.model.table = pm.model.table.dropna(how='all', axis=1)
    for i in pm.model.metrics:
        if i.index not in pm.model.table: pm.model._metrics.remove(i)
    pm.model.table = pm.model.table.dropna(how='any', axis=0)
    rho, p = pm.model.spearman_r(filter='omit nan')
    file = spearman_file(pm.name)
    rho.to_excel(file)

def sobol_analysis():
    from SALib.analyze import sobol
    filterwarnings('ignore', category=bst.exceptions.DesignWarning)
    filterwarnings('ignore', category=bst.exceptions.CostWarning)
    pm = sp.SingleDissolutionSTRAPModel(simulate=False)
    pm.model.exception_hook = 'raise'
    for kind, params, metric in [('tea', pm.tea_parameters, pm.MSP), ('lca', pm.lca_parameters, pm.GWP)]:
        file = sobol_file('_'.join([pm.name, kind]))
        pm.model.parameters = params
        convergence_model = bst.ConvergenceModel(predictors=params)
        samples = pm.model.sample(N=2**(len(pm.tea_parameters) - 4), rule='sobol', seed=0)
        pm.model.load_samples(samples)
        pm.model.evaluate(
            notify=int(len(samples)/10),
            convergence_model=convergence_model
        )
        problem = pm.model.problem()
        Y = pm.model.table[metric.index].values
        results = sobol.analyze(problem, Y)
        for i, j in results.items(): results[i] = j.tolist()
        with open(file, 'w') as file:
            yaml.dump(results, file)

def plot_sobol(names, categories, df, colors=None, hatches=None,
               bold_label=True, format_total=None, legend=False,
               legend_kwargs=None, **kwargs):
    colors, hatches = bst.plots.default_colors_and_hatches(len(names), colors, hatches)
    N_categories = len(categories)
    if format_total is None: format_total = lambda x: format(x, '.3g')
    if bold_label:
        bar_labels = [r"$\mathbf{" f"{format_total(i.total)}" "}$" "\n"
                      "$\mathbf{[" f"{format_units(i.units, '', False)}" "]}$"
                      for i in categories]
    else:
        bar_labels = [f"{format_total(i.total)}\n[{format_units(i.units)}]"
                      for i in categories]
    df.T.plot(kind='bar', stacked=True, edgecolor='k', **kwargs)
    locs, labels = plt.xticks()
    plt.xticks(locs, ['\n['.join(i.get_text().split(' [')) for i in labels])
    if legend: plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(rotation=0)
    fig = plt.gcf()
    ax = plt.gca()
    ax.set_ylabel('Cost and Utility Breakdown [%]')
    values = df.values
    negative_values = np.where(values < 0., values, 0.).sum(axis=0)
    lb = min(0., 20 * np.floor(negative_values.min() / 20))
    plt.ylim(lb, 100)
    bst.plots.style_axis(top=False, yticks=np.arange(lb, 101, 20))
    xticks, _ = plt.xticks()
    xlim = plt.xlim()
    y_twin = ax.twiny()
    plt.sca(y_twin)
    y_twin.tick_params(axis='x', top=True, direction="in", length=0)
    y_twin.zorder = 2
    plt.xlim(xlim)
    if len(xticks) != len(bar_labels): xticks = xticks[1:]
    plt.xticks(xticks, bar_labels, va='baseline')
    N_marks = N_categories
    axes = np.array([ax])
    if legend_kwargs is None: legend_kwargs = {}
    bst.plots.modify_stacked_bars(axes, N_marks, names, colors, hatches, 
                                  legend, **legend_kwargs)
    return fig, axes
    

def MSP_GWP_at_dissolution_capacity_boiling_point(
        boiling_point, capacity, process_model, convergence_model
    ):
    process_model.set_dissolution_capacity.setter(capacity)
    process_model.set_boiling_point.setter(boiling_point)
    with convergence_model.practice([capacity, boiling_point]):
        process_model.system.simulate()
    return np.array([process_model.MSP(), process_model.GWP()])

def plot_MSP_GWP_across_dissolution_capacity_boiling_point(load=True):
    bst.plots.set_font(size=10, family='sans-serif', font='Arial')
    pm = sp.SingleDissolutionSTRAPModel(simulate=False)
    xlim = np.array(pm.set_boiling_point.bounds)
    ylim = np.array(pm.set_dissolution_capacity.bounds)
    params = (pm.set_boiling_point, pm.set_dissolution_capacity)
    convergence_model = bst.ConvergenceModel(predictors=params)
    X, Y, Z = bst.plots.generate_contour_data(
        MSP_GWP_at_dissolution_capacity_boiling_point,
        file=os.path.join(results_folder, 'MSP_dissolution_capacity_boiling_point.npy'),
        load=load, save=True,
        xlim=xlim, ylim=ylim,
        args=(pm, convergence_model),
        n=20,
    )
    # Plot contours
    ylabel = "Dissolution capacity\n[% $\mathrm{wt}\ \mathrm{polymer} \cdot \mathrm{solvent}^{\mathrm{-1}}$]"
    xlabel = "Normal boiling point [K]"
    yticks = [1, 2, 4, 6, 8, 10]
    xticks = [360, 365, 370, 375, 380, 385, 390, 395, 400, 405]
    metric_bars = [
        bst.plots.MetricBar(
            'MSP', '$[\mathrm{USD} \cdot \mathrm{kg}^{\mathrm{-1}}]$', plt.cm.get_cmap('viridis_r'), 
            bst.plots.rounded_tickmarks_from_data(Z[:, :, 0], 5, 0.02, expand=0, p=0.02), 
            15, 2
        ),
        bst.plots.MetricBar(
            'GWP', '$[\mathrm{kgCO2e} \cdot \mathrm{kg}^{\mathrm{-1}}]$', plt.cm.get_cmap('inferno_r'), 
            bst.plots.rounded_tickmarks_from_data(Z[:, :, 1], 5, 0.01, expand=0, p=0.01), 
            15, 1
        )
    ]
    fig, axes, CSs, CB, other_axes = bst.plots.plot_contour_2d(
        X, Y, Z[:, :, :, None], xlabel, ylabel, xticks, yticks, metric_bars,  
        fillcolor=None, styleaxiskw=dict(xtick0=False), label=True,
    )
    
def run_monte_carlo_across_polymer_composition(N=None, autosave=True, autoload=True):
    filterwarnings('ignore', category=bst.exceptions.DesignWarning)
    filterwarnings('ignore', category=bst.exceptions.CostWarning)
    pm = sp.SingleDissolutionSTRAPModel(simulate=False)
    if N is None: N = 100
    pm.model.exception_hook = 'raise'
    coordinate = [0]
    pm.model.parameters = [i for i in pm.model.parameters if i is not pm.set_mass_fraction]
    np.random.seed(0)
    samples = pm.model.sample(N, rule='L')
    pm.model.load_samples(samples)
    def evaluate(**kwargs):
        autoload_file = autoload_file_name(f"{pm.name}_{coordinate[0]}")
        coordinate[0] += 1
        # kwargs['convergence_model'] = bst.ConvergenceModel(predictors=pm.model.parameters)
        pm.model.evaluate(
            autosave=autosave, 
            autoload=autoload,
            file=autoload_file,
            **kwargs,
        )
    
    pm.model.evaluate_across_coordinate(
        name='Polymer mass fraction',
        notify=int(N/10),
        f_evaluate=evaluate,
        f_coordinate=pm.set_mass_fraction,
        coordinate=np.linspace(0.05, 0.95, 15),
        notify_coordinate=True,
        xlfile=monte_carlo_file(pm.name + '_polymer_mass_fraction'),
    )
    
def plot_MSP_across_polymer_composition():
    pm = sp.SingleDissolutionSTRAPModel(simulate=False)
    file = monte_carlo_file(pm.name + '_polymer_mass_fraction')
    df = pd.read_excel(file, sheet_name=pm.MSP.short_description, index_col=0)
    df = df.dropna()
    composition = np.array(df.columns) * 100
    plt.ylabel(f"MSP\n[{format_units('USD/kg')}]")
    bst.plots.plot_montecarlo_across_coordinate(
        composition, df, 
        fill_color=CABBI_colors.green_dirty.tint(50).RGBn,
        median_color=CABBI_colors.green_dirty.shade(10).RGBn,
        p5_color=CABBI_colors.green_dirty.RGBn,
        smooth=1,
    )
    
def get_monte_carlo(name, features, cache={}):
    index = [i.index for i in features]
    key = name
    if key in cache:
        df = cache[key]
    else:
        file = monte_carlo_file(key)
        cache[key] = df = pd.read_excel(file, header=[0, 1], index_col=[0])
        df = df[index]
    mc = df.dropna(how='all', axis=0)
    return mc
    
def plot_kde():
    set_font(size=10)
    set_figure_size(width='half', aspect_ratio=1.1)
    pm = sp.SingleDissolutionSTRAPModel(simulate=False)
    metrics = [pm.GWP, pm.MSP]
    Xi, Yi = metrics
    df = get_monte_carlo(pm.name, metrics)
    y = df[Yi.index].values
    x = df[Xi.index].values
    yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    xticks = [0, 1, 2, 3, 4, 5]
    ax = bst.plots.plot_kde(
        y=y, x=x, xticks=xticks, yticks=yticks,
        xticklabels=True, yticklabels=True,
        xbox_kwargs=dict(light=CABBI_colors.orange.RGBn, dark=CABBI_colors.orange.shade(60).RGBn),
        ybox_kwargs=dict(light=CABBI_colors.blue.RGBn, dark=CABBI_colors.blue.shade(60).RGBn),
        xbox_width=400,
        aspect_ratio=1.1,
    )
    plt.sca(ax)
    plt.ylabel('MSP $[\mathrm{USD} \cdot \mathrm{kg}^{\mathrm{-1}}]$')
    plt.xlabel('GWP $[\mathrm{kgCO2e} \cdot \mathrm{kg}^{\mathrm{-1}}]$')
    plt.subplots_adjust(
        hspace=0.05, wspace=0.05,
        top=0.98, bottom=0.15,
        left=0.15, right=0.98,
    )