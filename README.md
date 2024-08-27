# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/pydot/pydot/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                               |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|----------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/pydot/\_\_init\_\_.py          |        9 |        0 |        0 |        0 |    100% |           |
| src/pydot/\_vendor/\_\_init\_\_.py |        0 |        0 |        0 |        0 |    100% |           |
| src/pydot/\_vendor/tempfile.py     |      489 |      234 |      178 |       30 |     49% |63, 77-82, 93, 96-99, 102, 110, 117->119, 119->124, 123, 128, 151, 178-179, 196->199, 199->195, 212-223, 236->239, 249, 257-266, 269, 274-277, 280-286, 293, 297, 307->310, 319, 350-357, 377, 385-394, 397, 418-428, 447->exit, 451-452, 457-460, 463->exit, 469, 493-506, 511-512, 517-519, 534-535, 571, 574, 590-597, 628-683, 695-704, 710-713, 716-728, 737-739, 742, 746, 749-756, 759, 763, 767, 771, 774-775, 778, 781, 785-788, 792-795, 799, 802, 805, 808, 811, 814, 817, 820, 823, 826, 829, 832-837, 840, 843-846, 849-852, 855, 892-921, 923, 926, 932-934, 943->exit, 947->exit |
| src/pydot/core.py                  |      687 |      114 |      304 |       31 |     81% |158, 201, 234, 251, 260, 264, 280-281, 349, 364, 376, 378, 396, 456-476, 542->532, 568, 573-607, 619, 624, 662, 668, 671, 730, 739, 743, 751, 831, 856, 862->878, 915, 927, 992, 1012, 1015, 1018, 1021-1026, 1034, 1037-1042, 1045, 1048-1053, 1069, 1092, 1099, 1110, 1117, 1170-1181, 1262-1285, 1298-1299, 1306->1322, 1377->1383, 1430->1434, 1432, 1438, 1478-1482, 1612->exit, 1649, 1813->1818, 1821-1822 |
| src/pydot/dot\_parser.py           |      272 |       44 |      134 |       23 |     80% |63-64, 73-74, 91, 105-110, 113, 119, 131->134, 136, 141, 145->154, 152, 154->144, 160, 163, 173->172, 221, 229, 243->245, 247->249, 251, 268, 277-283, 308-311, 319-326, 341, 357-358, 511-515 |
| src/pydot/exceptions.py            |        6 |        2 |        0 |        0 |     67% |    23, 26 |
| test/\_\_init\_\_.py               |        0 |        0 |        0 |        0 |    100% |           |
| test/test\_pydot.py                |      406 |       27 |       54 |        7 |     91% |73, 108-117, 257-259, 368, 617, 624, 649, 673-683, 687-689 |
|                          **TOTAL** | **1869** |  **421** |  **670** |   **91** | **74%** |           |


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