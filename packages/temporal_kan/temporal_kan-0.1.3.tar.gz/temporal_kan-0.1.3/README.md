# Temporal KAN: A Kolmogorov-Arnold-Network Variant for Time Series

Tensorflow package that implements different recurrent layers using the KAN architecture.

## Installation:

A [pypi package](https://pypi.org/project/temporal_kan/) is available for installation, .

## Usage:

The package implements the 4 layers described in the paper PUTLINKHERE. To use a layer you can either import the layer directly or use the `TemporalKAN` and give the layer name as a string before other parameters.

Unlike the original KAN paper, the layers accepts any activation and not only splines. You need to pass a list of activations function for your layer, the int and float paramters will automatically get transformed into the corresponding spline, but you can also pass tensorflow activation layer name, or a custom activation function.

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
