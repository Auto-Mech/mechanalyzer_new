import click

from mechanalyzer.cli import run_sort, ste_mech, compare_rates


@click.group()
def main():
    """MechAnalyzer CLI"""
    pass


@main.command()
@click.option(
    "-m",
    "--mech",
    default="mechanism.dat",
    show_default=True,
    help="Input mechanism file name",
)
@click.option(
    "-s",
    "--spc",
    default="species.csv",
    show_default=True,
    help="Input species file name",
)
@click.option(
    "-t",
    "--therm",
    default="therm.dat",
    show_default=True,
    help="Input thermo file name",
)
@click.option(
    "-i",
    "--sort",
    default="sort.dat",
    show_default=True,
    help="Input sort file name",
)
@click.option(
    "-o",
    "--outmech",
    default="outmech.dat",
    show_default=True,
    help="Output mechanism file name",
)
@click.option(
    "-c",
    "--outspc",
    default="outspc.csv",
    show_default=True,
    help="Output species file name",
)
@click.option(
    "-g",
    "--outgroups",
    default="pes_groups.dat",
    show_default=True,
    help="Output PES groups file name",
)
def sort(
    mech: str = "mechanism.dat",
    spc: str = "species.csv",
    therm: str = "therm.dat",
    sort: str = "sort.dat",
    outmech: str = "outmech.dat",
    outspc: str = "outspc.csv",
    outgroups: str = "pes_groups.dat",
):
    """Sort the reactions in a mechanism"""
    run_sort.main(
        mech=mech,
        spc=spc,
        therm=therm,
        sort=sort,
        outmech=outmech,
        outspc=outspc,
        outgroups=outgroups,
    )

@main.command()
@click.option(
    "-m",
    "--mechs_yaml",
    default="mechs.yaml",
    show_default=True,
    help="yaml file, set up like:\\mech1:\\\trate_file: 'rate.ckin'\\\ttherm_file: 'therm.ckin'\\\tspecies_csv: 'species.csv'\\mech2: ...",
)
@click.option(
    "-o",
    "--plot_filename",
    default="rate_plot.pdf",
    show_default=True,
    help="name of output pdf of plots"
)
@click.option(
    "-f",
    "--out_txt_filename",
    default="ordering.txt",
    show_default=True,
    help="name of output text filename"
)
@click.option(
    "-d",
    "--job_path",
    default=".",
    show_default=True,
    help="directory for input/output files"
)
@click.option(
    "-t",
    "--temps_lst",
    default=None,
    type=lambda s: [float(temp) for temp in s.split(',')],
    show_default=True,
    help="array of temperatures, None defaults to 500--1500"
)
@click.option(
    "-p",
    "--pressures",
    default=None,
    type=lambda s: [float(press) for press in s.split(',')],
    show_default=True,
    help="array of pressures to plot, None defaults to (1, 10, 100)"
)
@click.option(
    "-s",
    "--sort_method",
    default="ratios",
    show_default=True,
    help="Sort the pdf plots by the ratio of the differences with 'ratios', or not at all with None"
)
@click.option(
    "-r",
    "--rev_rates",
    default=True,
    show_default=True,
    help="reverse rates of remaining mechanisms to make them match the direction in the first"
)
@click.option(
    "-l",
    "--remove_loners",
    default=True,
    show_default=True,
    help="True only plots rates that are in ALL mechanisms, False plots ALL rates in all mechanism"
)
def compare_mechanisms(
    mechs_yaml: str = 'mechs.yaml',
    plot_filename: str = 'rate_plot.pdf',
    out_txt_filename: str = 'ordering.txt',
    job_path: str = '.',
    temps_lst: list = [],
    pressures: list = [],
    sort_method: str = None,
    rev_rates: bool = True,
    remove_loners: bool = True,
    write_file: bool = False
):
    """Sort the reactions in a mechanism"""
    compare_rates.main(
        mechs_yaml=mechs_yaml,
        plot_filename=plot_filename,
        out_txt_filename=out_txt_filename,
        job_path=job_path,
        temps_lst=temps_lst,
        pressures=pressures,
        sort_method=sort_method,
        rev_rates=rev_rates,
        remove_loners=remove_loners,
        write_file=write_file,
    )
@main.command()
def expand():
    """Expand stereochemistry for a mechanism"""
    ste_mech.main()
