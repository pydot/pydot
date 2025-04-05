# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydot/\_\_init\_\_.py |       10 |        0 |        0 |        0 |    100% |           |
| src/pydot/classes.py      |       54 |        2 |       12 |        0 |     97% |     86-87 |
| src/pydot/core.py         |      653 |       87 |      264 |       30 |     84% |154, 161, 180, 231, 327, 342, 356, 358, 360, 376, 442-462, 536->526, 576->581, 580, 582, 619, 624, 633, 636, 690, 699, 703, 711, 797, 822, 828->844, 888, 905, 966, 986, 989, 992, 995-996, 1004, 1007-1008, 1011, 1014-1015, 1031, 1054, 1061, 1072, 1079, 1134-1145, 1228-1251, 1264-1265, 1272->1288, 1343->1349, 1409, 1412->1420, 1460-1464, 1600->exit, 1637, 1812->1817, 1820-1821 |
| src/pydot/dot\_parser.py  |      286 |       44 |      140 |       23 |     81% |67-68, 77-78, 128, 142-147, 150, 156, 170->173, 175, 180, 184->193, 191, 193->183, 203, 206, 216->215, 272, 280, 294->296, 298->300, 302, 319, 328-334, 359-362, 370-378, 393, 409-410, 542-546 |
| src/pydot/exceptions.py   |        6 |        2 |        0 |        0 |     67% |    23, 26 |
| test/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| test/conftest.py          |        9 |        0 |        0 |        0 |    100% |           |
| test/test\_api.py         |      291 |        0 |        6 |        0 |    100% |           |
| test/test\_classes.py     |       43 |        0 |        0 |        0 |    100% |           |
| test/test\_logging.py     |       11 |        0 |        0 |        0 |    100% |           |
| test/test\_parser.py      |       14 |        0 |        0 |        0 |    100% |           |
| test/test\_pydot.py       |      141 |       31 |       20 |        5 |     74% |49, 53-56, 76, 80-83, 98, 120, 158-173, 209, 216, 241 |
|                 **TOTAL** | **1518** |  **166** |  **442** |   **58** | **86%** |           |


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