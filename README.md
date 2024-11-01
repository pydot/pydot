# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydot/\_\_init\_\_.py |       10 |        0 |        0 |        0 |    100% |           |
| src/pydot/classes.py      |       52 |        2 |       12 |        0 |     97% |     82-83 |
| src/pydot/core.py         |      657 |       92 |      266 |       29 |     83% |173, 216, 312, 327, 339, 341, 343, 359, 419-439, 505->495, 531, 543, 548, 586, 591, 600, 603, 662, 671, 675, 683, 763, 788, 794->810, 854, 871, 936, 956, 959, 962, 965-970, 978, 981-986, 989, 992-997, 1013, 1036, 1043, 1054, 1061, 1114-1125, 1206-1229, 1242-1243, 1250->1266, 1321->1327, 1385, 1388->1396, 1436-1440, 1580->exit, 1617, 1781->1786, 1789-1790 |
| src/pydot/dot\_parser.py  |      273 |       44 |      132 |       23 |     80% |64-65, 74-75, 92, 106-111, 114, 120, 132->135, 137, 142, 146->155, 153, 155->145, 161, 164, 174->173, 222, 230, 244->246, 248->250, 252, 269, 278-284, 309-312, 318-325, 340, 356-357, 510-514 |
| src/pydot/exceptions.py   |        6 |        2 |        0 |        0 |     67% |    23, 26 |
| test/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| test/conftest.py          |        4 |        0 |        0 |        0 |    100% |           |
| test/test\_classes.py     |       43 |        0 |        0 |        0 |    100% |           |
| test/test\_pydot.py       |      402 |       18 |       22 |        6 |     94% |72, 107-116, 256-258, 367, 636, 643, 668 |
|                 **TOTAL** | **1447** |  **158** |  **432** |   **58** | **86%** |           |


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