# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydot/\_\_init\_\_.py |       10 |        0 |        0 |        0 |    100% |           |
| src/pydot/classes.py      |       52 |        2 |       16 |        0 |     97% |     82-83 |
| src/pydot/core.py         |      673 |      109 |      296 |       29 |     81% |173, 216, 305, 320, 332, 334, 336, 352, 412-432, 498->488, 524, 529-563, 575, 580, 618, 623, 632, 635, 694, 703, 707, 715, 795, 820, 826->842, 886, 903, 968, 988, 991, 994, 997-1002, 1010, 1013-1018, 1021, 1024-1029, 1045, 1068, 1075, 1086, 1093, 1146-1157, 1238-1261, 1274-1275, 1282->1298, 1353->1359, 1417, 1420->1428, 1468-1472, 1612->exit, 1649, 1813->1818, 1821-1822 |
| src/pydot/dot\_parser.py  |      273 |       44 |      134 |       23 |     80% |64-65, 74-75, 92, 106-111, 114, 120, 132->135, 137, 142, 146->155, 153, 155->145, 161, 164, 174->173, 222, 230, 244->246, 248->250, 252, 269, 278-284, 309-312, 318-325, 340, 356-357, 510-514 |
| src/pydot/exceptions.py   |        6 |        2 |        0 |        0 |     67% |    23, 26 |
| test/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| test/conftest.py          |        4 |        0 |        2 |        0 |    100% |           |
| test/test\_classes.py     |       43 |        0 |       16 |        0 |    100% |           |
| test/test\_pydot.py       |      402 |       18 |       50 |        6 |     94% |72, 107-116, 256-258, 367, 636, 643, 668 |
|                 **TOTAL** | **1463** |  **175** |  **514** |   **58** | **85%** |           |


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