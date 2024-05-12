# pylint: disable=W0622
"""
This module provides a command-line interface (CLI) for the PDFMicroarray
library. It allows users to process, analyze, and plot text occurrences
extracted from PDF documents, enabling literature research through a terminal
interface.
"""

import click

from pdf_microarray.pdf_microarray import PDFMicroarray
from pdf_microarray.plot_microarray import PlotMicroarray

VERSION = "1.0.1"

DIR = click.Path(exists=True, dir_okay=True)
FILE = click.Path(exists=True, file_okay=True)


@click.group()
@click.version_option(version=VERSION)
def cli():
    """
    Command line interface for managing PDF data extraction, analysis, and
    visualization.
    """


P_INPUT = "Path to the directory containing the PDF documents."
P_OUTPUT = "Path where processed text segments will be stored."
P_THREADS = "Number of threads to use for concurrent processing. Defaults \
to using all available CPU cores (-1)."
P_FORCE = "If enabled, forces the processing of files that have already been \
processed. Defaults to False."


@cli.command()
@click.option("-i", "--input", type=DIR, required=True, help=P_INPUT)
@click.option("-o", "--output", type=DIR, required=True, help=P_OUTPUT)
@click.option("--threads", type=int, default=-1, help=P_THREADS)
@click.option("--force", is_flag=True, default=False, help=P_FORCE)
def process(input, output, threads, force):
    """
    Processes PDF documents by extracting plain text, text from images and
    text from embedded diagrams, saving the results in the specified output
    directory.
    """
    PDFMicroarray.process(input, output, threads=threads, force=force)


A_INPUT = "Path to the directory where processed segments are stored."
A_WORDS = "Path to the file containing the list of words to search for."
A_OUTPUT = "Path where the analysis results in CSV format will be saved."


@cli.command()
@click.option("-i", "--input", type=DIR, required=True, help=A_INPUT)
@click.option("-w", "--words", type=FILE, required=True, help=A_WORDS)
@click.option("-o", "--output", required=True, help=A_OUTPUT)
def analyze(input, words, output):
    """
    Analyzes extracted text from PDFs for specific word occurrences, using
    Levenshtein distance, and saves the results to a CSV file.
    """
    PDFMicroarray.analyze(input, words, output)


L_INPUT = "Path to the CSV file containing data to be visualized."
L_WIDTH = "Width of the generated plot in inches. Defaults to 60."
L_THRESHOLD = "Minimum score (0-100) to consider a word match using \
Levenshtein distance. Defaults to 90."
L_EMPTY = "If enabled, shows all rows where no word matches have been found. \
Defaults to False."
L_SPLIT = "Maximum number of rows each generated plot should have. \
Defaults to 60."
L_HEIGHT = "Height of the generated plot in inches. Defaults to 30."
L_OUTPUT = "Optional path to save the generated plot image as a PNG file."


@cli.command()
@click.option("-i", "--input", type=FILE, required=True, help=L_INPUT)
@click.option("-o", "--output", default=None, help=L_OUTPUT)
@click.option("--threshold", type=int, default=90, help=L_THRESHOLD)
@click.option("--empty", is_flag=True, default=False, help=L_EMPTY)
@click.option("--split", type=int, default=60, help=L_SPLIT)
@click.option("--width", type=int, default=60, help=L_WIDTH)
@click.option("--height", type=int, default=30, help=L_HEIGHT)
def plot(input, output, threshold, empty, split, width, height):
    """
    Plots the analysis results from the given CSV file, visualizing the data
    in a microarray format.
    """
    PlotMicroarray.plot(
        input,
        image_path=output,
        threshold=threshold,
        empty=empty,
        split=split,
        width=width,
        height=height,
    )
