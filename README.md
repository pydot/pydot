# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydot/\_\_init\_\_.py |       10 |        0 |        0 |        0 |    100% |           |
| src/pydot/classes.py      |       54 |        2 |       12 |        0 |     97% |     86-87 |
| src/pydot/core.py         |      658 |       92 |      268 |       30 |     83% |181, 232, 328, 343, 357, 359, 361, 377, 441-461, 535->525, 561, 573, 574->580, 578, 616, 621, 630, 633, 697, 706, 710, 718, 804, 829, 835->851, 895, 912, 977, 997, 1000, 1003, 1006-1011, 1019, 1022-1027, 1030, 1033-1038, 1054, 1077, 1084, 1095, 1102, 1157-1168, 1251-1274, 1287-1288, 1295->1311, 1366->1372, 1432, 1435->1443, 1483-1487, 1627->exit, 1664, 1839->1844, 1847-1848 |
| src/pydot/dot\_parser.py  |      274 |       44 |      132 |       23 |     80% |66-67, 76-77, 96, 110-115, 118, 124, 138->141, 143, 148, 152->161, 159, 161->151, 167, 170, 180->179, 236, 244, 262->264, 266->268, 270, 289, 298-304, 331-334, 340-348, 363, 379-380, 533-537 |
| src/pydot/exceptions.py   |        6 |        2 |        0 |        0 |     67% |    23, 26 |
| test/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| test/conftest.py          |        4 |        0 |        0 |        0 |    100% |           |
| test/test\_classes.py     |       43 |        0 |        0 |        0 |    100% |           |
| test/test\_pydot.py       |      402 |       18 |       22 |        6 |     94% |73, 108-117, 257-259, 368, 637, 644, 669 |
|                 **TOTAL** | **1451** |  **158** |  **434** |   **59** | **86%** |           |


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