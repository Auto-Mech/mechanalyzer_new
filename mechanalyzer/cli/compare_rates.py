""" Script for running a comparison of rate constants between mechanisms
"""

import os
import sys
import numpy
import yaml
import mechanalyzer.calculator.compare as compare
import mechanalyzer.plotter.rates as plot_rates
import mechanalyzer.plotter._util as util
import mechanalyzer.parser.new_spc as spc_parser
import mechanalyzer.parser.ckin_ as ckin_parser
from ioformat import pathtools


def read_mechs_yaml(mechs_yaml_file):
    """ read the yaml file that specifies each mechanism file
        for each mechanism, makes sure all files are given
    """
    def _mech_is_fully_specified(mech_data):
        """ make sure all files are given in yaml for mechanism
        """
        keys = ['rate_file', 'therm_file', 'species_csv']
        _fully_specified = True
        if not all(key in mech_data for key in keys):
            _fully_specified = False
            print(
                'missing in yaml: ', 
                ','.join([key for key in keys if key not in mech_data]))
        return _fully_specified

    with open(mechs_yaml_file, 'r') as file:
        mechs = yaml.safe_load(file)
    mechs =  {
        key: mech_files for key, mech_files in mechs.items() 
        if _mech_is_fully_specified(mech_files)}

    labels = []
    mech_files = []
    therm_files = []
    csv_files = []
    for key, mech in mechs.items():
        labels.append(key)
        mech_files.append(mech['rate_file'])
        therm_files.append(mech['therm_file'])
        csv_files.append(mech['species_csv'])

    return labels, mech_files, therm_files, csv_files


def main(
        mechs_yaml='mechs.yaml',
        plot_filename='rate_plot.pdf',
        out_txt_filename='ordering.txt',
        job_path='.',
        temps_lst=None, pressures=None,
        sort_method=None, rev_rates=True,
        remove_loners=True, write_file=False):

    labels, mech_files, therm_files, csv_files = read_mechs_yaml(mechs_yaml)
    if temps_lst is None or len(temps_lst) < 2:
        temps_lst = [numpy.linspace(500, 1000, 16)]
    else:
        temps_lst = [numpy.linspace(temps_lst[0], temps_lst[1], 16)]
    if pressures is None or len(pressures) < 1:
        pressures = [1, 10, 100]

    rxn_ktp_dcts = ckin_parser.load_rxn_ktp_dcts(
        mech_files, job_path, temps_lst, pressures)
    spc_therm_dcts = ckin_parser.load_spc_therm_dcts(
        therm_files, job_path, temps_lst[0])  # NOTE: taking first entry
    spc_dcts = spc_parser.load_mech_spc_dcts(csv_files, job_path)

    # Get the algn_rxn_ktp_dct
    temps = temps_lst[0]  # function receives a single Numpy array of temps
    algn_rxn_ktp_dct = compare.get_algn_rxn_ktp_dct(
        rxn_ktp_dcts, spc_therm_dcts, spc_dcts, temps, rev_rates=rev_rates,
        remove_loners=remove_loners, write_file=write_file)

    # Run the plotter
    figs = plot_rates.build_plots(
        algn_rxn_ktp_dct,
        mech_names=labels,
        ratio_sort=bool(sort_method == 'ratios'))
    util.build_pdf(figs, filename=plot_filename, path=job_path)

    # Write the ordered text file
    FSTR = compare.write_ordered_str(algn_rxn_ktp_dct, dct_type='rxn')
    pathtools.write_file(FSTR, job_path, out_txt_filename)

