# FirstGlance

FirstGlance is a Python library created with the intention of being used for preliminary data analysis primarily within a notebook environment.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install FirstGlance.

```bash
pip install FirstGlance
```

## Usage

```python
From FirstGlance import report
```

```python
# Returns seaborn boxplots, histograms, and heatmap using the numeric columns
report.plot_analysis('example.csv')
```

```python
# Returns pandas dataframe with entry count, null count, datatype and descriptive statistics for each column
report.stats_report('example.csv')
```

## Dependencies

- [pandas](https://pandas.pydata.org/)
- [seaborn](https://seaborn.pydata.org/)

Before using this package, make sure you have installed the above dependencies. You can install them using pip:

```bash
pip install pandas seaborn
```

## License

MIT License

Copyright (c) 2024 Jordan Kanius

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.