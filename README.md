# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydot/\_\_init\_\_.py |        9 |        0 |        0 |        0 |    100% |           |
| src/pydot/core.py         |      687 |      114 |      304 |       31 |     81% |158, 201, 234, 251, 260, 264, 280-281, 349, 364, 376, 378, 396, 456-476, 542->532, 568, 573-607, 619, 624, 662, 668, 671, 730, 739, 743, 751, 831, 856, 862->878, 915, 927, 992, 1012, 1015, 1018, 1021-1026, 1034, 1037-1042, 1045, 1048-1053, 1069, 1092, 1099, 1110, 1117, 1170-1181, 1262-1285, 1298-1299, 1306->1322, 1377->1383, 1430->1434, 1432, 1438, 1478-1482, 1612->exit, 1649, 1813->1818, 1821-1822 |
| src/pydot/dot\_parser.py  |      272 |       44 |      134 |       23 |     80% |63-64, 73-74, 91, 105-110, 113, 119, 131->134, 136, 141, 145->154, 152, 154->144, 160, 163, 173->172, 221, 229, 243->245, 247->249, 251, 268, 277-283, 308-311, 319-326, 341, 357-358, 511-515 |
| src/pydot/exceptions.py   |        6 |        2 |        0 |        0 |     67% |    23, 26 |
| test/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| test/test\_pydot.py       |      394 |       18 |       50 |        6 |     94% |72, 107-116, 256-258, 367, 616, 623, 648 |
|                 **TOTAL** | **1368** |  **178** |  **488** |   **60** | **84%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/pydot/pydot/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydot/pydot/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fpydot%2Fpydot%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.