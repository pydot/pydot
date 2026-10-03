#!/bin/env python3
# SPDX-FileCopyrightText: 2026 pydot contributors
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import sys
import textwrap
from collections.abc import Generator, Set
from pathlib import Path
from typing import Any, Callable

# Make the constants importable without pulling in the rest of pydot,
# since we may be overwriting one of its source files.
srcdir = Path("src") / "pydot"
if srcdir.exists():
    sys.path.insert(0, str(srcdir))


class MixinGenerator:
    """Generate the Python code for a mixin class."""

    def __init__(
        self,
        rootname: str,
        attr_names: Set[str],
    ) -> None:
        """Set up the code generator with the necessary inputs."""
        self.name: str = rootname
        self.attrs: set[str] = set(attr_names)
        self.generators: list[Callable[...]] = []

    def add_generator(self, generator: Callable[...]) -> None:
        """Register an output generator."""
        self.generators.append(generator)

    def _generate_for_attr(self, attr: str) -> str:
        return "\n".join(generator(attr) for generator in self.generators)

    def generate(self) -> Generator[str, Any, None]:
        """Generate code for the given mixing class, as configured."""
        yield from [
            "\n" + textwrap.indent(self._generate_for_attr(attr), " " * 4)
            for attr in sorted(self.attrs)
        ]


class GetSetGenerator(MixinGenerator):
    """Generate get_foo and set_foo method mixins."""

    def __init__(self, rootname: str, attr_names: Set[str]) -> None:
        """Set up the generator."""
        super().__init__(rootname, attr_names)
        self.add_generator(self.get_generator)
        self.add_generator(self.set_generator)

    def get_generator(self, attr: str) -> str:
        """Generate ``get_foo`` methods."""
        return textwrap.dedent(f'''\
            def get_{attr}(self) -> Any:
                """Get the ``{attr}`` attribute for the graph element."""
                return self.get("{attr}")
            ''')

    def set_generator(self, attr: str) -> str:
        """Generate ``set_foo`` methods."""
        return textwrap.dedent(f'''\
            def set_{attr}(self, value: Any) -> None:
                """Set the ``{attr}`` attribute for the graph element."""
                return self.set("{attr}", value)
            ''')


if __name__ == "__main__":
    from constants import (
        CLUSTER_ATTRIBUTES,
        COMMON_ATTRIBUTES,
        EDGE_ATTRIBUTES,
        GRAPH_ATTRIBUTES,
        NODE_ATTRIBUTES,
        # OUTPUT_FORMATS,
    )

    getset_classes = {
        "Common": COMMON_ATTRIBUTES,
        "Node": NODE_ATTRIBUTES,
        "Edge": EDGE_ATTRIBUTES,
        "Graph": GRAPH_ATTRIBUTES,
        "Cluster": CLUSTER_ATTRIBUTES,
    }

    out = sys.stdout

    out.write(
        textwrap.dedent('''\
        # SPDX-FileCopyrightText: 2026 pydot contributors
        #
        # SPDX-License-Identifier: MIT

        """Mixin classes to define convenience methods."""

        from __future__ import annotations

        from typing import Any
        ''')
    )

    for klass, attrs in getset_classes.items():
        out.write(
            textwrap.dedent(f'''\


            class {klass}Mixin:
                """Attribute convenience methods for {klass}."""

                def get(self, name: str) -> Any:
                    """Generic get method (must be reimplemented)."""
                    raise NotImplementedError

                def set(self, name: str, value: Any) -> None:
                    """Generic set method (must be reimplemented)."""
                    raise NotImplementedError
            ''')
        )

        gen = GetSetGenerator(klass, attrs)
        for method in gen.generate():
            out.write(method)
