# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydot/\_\_init\_\_.py |       10 |        0 |        0 |        0 |    100% |           |
| src/pydot/classes.py      |       54 |        2 |       12 |        0 |     97% |     86-87 |
| src/pydot/core.py         |      651 |       86 |      262 |       30 |     84% |181, 232, 328, 343, 357, 359, 361, 377, 441-461, 535->525, 564, 575->580, 579, 581, 618, 623, 632, 635, 689, 698, 702, 710, 793, 818, 824->840, 884, 901, 962, 982, 985, 988, 991-992, 1000, 1003-1004, 1007, 1010-1011, 1027, 1050, 1057, 1068, 1075, 1130-1141, 1224-1247, 1260-1261, 1268->1284, 1339->1345, 1405, 1408->1416, 1456-1460, 1596->exit, 1633, 1808->1813, 1816-1817 |
| src/pydot/dot\_parser.py  |      288 |       45 |      142 |       24 |     81% |66-67, 76-77, 96, 110-115, 118, 124, 138->141, 143, 148, 152->161, 159, 161->151, 167, 170, 180->179, 236, 244, 262->264, 266->268, 270, 289, 298-304, 331-334, 340-348, 363, 379-380, 406, 557-561 |
| src/pydot/exceptions.py   |        6 |        2 |        0 |        0 |     67% |    23, 26 |
| test/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| test/conftest.py          |        4 |        0 |        0 |        0 |    100% |           |
| test/test\_classes.py     |       43 |        0 |        0 |        0 |    100% |           |
| test/test\_pydot.py       |      410 |       18 |       22 |        6 |     94% |73, 108-117, 257-259, 381, 650, 657, 682 |
|                 **TOTAL** | **1466** |  **153** |  **438** |   **60** | **87%** |           |


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