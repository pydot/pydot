# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydot/\_\_init\_\_.py |       10 |        0 |        0 |        0 |    100% |           |
| src/pydot/classes.py      |       56 |        2 |       12 |        0 |     97% |     85-86 |
| src/pydot/core.py         |      667 |       79 |      266 |       23 |     86% |155, 162, 181, 232, 328, 343, 357, 359, 361, 377, 443-463, 537->527, 581, 620-623, 628, 637, 640, 694, 703, 707, 715, 817, 848, 854->870, 988, 1008, 1011, 1014, 1017-1018, 1026, 1029-1030, 1033, 1036-1037, 1154-1165, 1248-1271, 1284-1285, 1292->1308, 1363->1369, 1618->exit, 1655, 1830->1835, 1838-1839 |
| src/pydot/dot\_parser.py  |      277 |       32 |      130 |       19 |     84% |71-72, 81-82, 132, 153-160, 174->177, 179, 184, 188->197, 195, 197->187, 207, 210, 220->219, 276, 284, 299->301, 303->305, 307, 324, 333-339, 344->347, 389-390, 514-518 |
| src/pydot/exceptions.py   |        7 |        2 |        0 |        0 |     71% |    25, 28 |
| test/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| test/conftest.py          |        9 |        0 |        0 |        0 |    100% |           |
| test/test\_api.py         |      307 |        0 |        6 |        0 |    100% |           |
| test/test\_classes.py     |       43 |        0 |        0 |        0 |    100% |           |
| test/test\_logging.py     |       11 |        0 |        0 |        0 |    100% |           |
| test/test\_parser.py      |       29 |        0 |        0 |        0 |    100% |           |
| test/test\_pydot.py       |      141 |       32 |       20 |        6 |     73% |49, 53-56, 76, 80-83, 98, 120, 143, 158-173, 209, 216, 241 |
|                 **TOTAL** | **1557** |  **147** |  **434** |   **48** | **88%** |           |


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