# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                      |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|-------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydot/\_\_init\_\_.py |        9 |        0 |        0 |        0 |    100% |           |
| src/pydot/core.py         |      707 |      115 |      312 |       32 |     81% |158, 201, 234, 251, 260, 264, 280-281, 349, 364, 376, 378, 380, 396, 456-476, 542->532, 568, 573-607, 619, 624, 662, 667, 676, 679, 738, 747, 751, 759, 839, 864, 870->886, 930, 947, 1012, 1032, 1035, 1038, 1041-1046, 1054, 1057-1062, 1065, 1068-1073, 1089, 1112, 1119, 1130, 1137, 1190-1201, 1282-1305, 1318-1319, 1326->1342, 1397->1403, 1461, 1464->1472, 1512-1516, 1656->exit, 1693, 1857->1862, 1865-1866 |
| src/pydot/dot\_parser.py  |      272 |       44 |      134 |       23 |     80% |63-64, 73-74, 91, 105-110, 113, 119, 131->134, 136, 141, 145->154, 152, 154->144, 160, 163, 173->172, 221, 229, 243->245, 247->249, 251, 268, 277-283, 308-311, 319-326, 341, 357-358, 511-515 |
| src/pydot/exceptions.py   |        6 |        2 |        0 |        0 |     67% |    23, 26 |
| test/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| test/test\_pydot.py       |      394 |       18 |       50 |        6 |     94% |72, 107-116, 256-258, 367, 616, 623, 648 |
|                 **TOTAL** | **1388** |  **179** |  **496** |   **61** | **84%** |           |


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