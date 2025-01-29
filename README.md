# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydot/\_\_init\_\_.py |       10 |        0 |        0 |        0 |    100% |           |
| src/pydot/classes.py      |       54 |        2 |       12 |        0 |     97% |     86-87 |
| src/pydot/core.py         |      653 |       87 |      264 |       30 |     84% |155, 162, 181, 232, 328, 343, 357, 359, 361, 377, 441-461, 535->525, 575->580, 579, 581, 618, 623, 632, 635, 689, 698, 702, 710, 796, 821, 827->843, 887, 904, 965, 985, 988, 991, 994-995, 1003, 1006-1007, 1010, 1013-1014, 1030, 1053, 1060, 1071, 1078, 1133-1144, 1227-1250, 1263-1264, 1271->1287, 1342->1348, 1408, 1411->1419, 1459-1463, 1599->exit, 1636, 1811->1816, 1819-1820 |
| src/pydot/dot\_parser.py  |      288 |       44 |      142 |       23 |     81% |67-68, 77-78, 128, 142-147, 150, 156, 170->173, 175, 180, 184->193, 191, 193->183, 199, 202, 212->211, 268, 276, 294->296, 298->300, 302, 321, 330-336, 363-366, 372-380, 395, 411-412, 560-564 |
| src/pydot/exceptions.py   |        6 |        2 |        0 |        0 |     67% |    23, 26 |
| test/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| test/conftest.py          |        9 |        0 |        0 |        0 |    100% |           |
| test/test\_api.py         |      291 |        0 |        6 |        0 |    100% |           |
| test/test\_classes.py     |       43 |        0 |        0 |        0 |    100% |           |
| test/test\_logging.py     |       11 |        0 |        0 |        0 |    100% |           |
| test/test\_parser.py      |       14 |        0 |        0 |        0 |    100% |           |
| test/test\_pydot.py       |      102 |       14 |       16 |        5 |     82% |68, 103-112, 148, 155, 180 |
|                 **TOTAL** | **1481** |  **149** |  **440** |   **58** | **87%** |           |


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