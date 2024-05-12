# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test Structure nesting ability."""

from baseline import Baseline

from plum.conformance import Case, CaseData
from plum.littleendian import uint8
from plum.structure import Structure, member


class Nested(Structure):

    """Sample structure (for nesting inside another structure)."""

    inner: int = member(fmt=uint8)


class Outer(Structure):
    """Sample structure containing a nested structure."""

    outer: Nested = member(fmt=Nested)


class TestNested(Case):

    data = CaseData(
        fmt=Outer,
        bindata=b"\x00",
        nbytes=1,
        values=(
            Outer(outer=Nested(inner=0)),
            [[0]],
        ),
        dump=Baseline(
            """
            +--------+---------+-------+-------+--------------------+
            | Offset | Access  | Value | Bytes | Format             |
            +--------+---------+-------+-------+--------------------+
            |        |         |       |       | Outer (Structure)  |
            |        | outer   |       |       | Nested (Structure) |
            | 0      |   inner | 0     | 00    | uint8              |
            +--------+---------+-------+-------+--------------------+
            """
        ),
        excess=Baseline(
            """
            +--------+---------+----------------+-------+--------------------+
            | Offset | Access  | Value          | Bytes | Format             |
            +--------+---------+----------------+-------+--------------------+
            |        |         |                |       | Outer (Structure)  |
            |        | outer   |                |       | Nested (Structure) |
            | 0      |   inner | 0              | 00    | uint8              |
            +--------+---------+----------------+-------+--------------------+
            | 1      |         | <excess bytes> | 99    |                    |
            +--------+---------+----------------+-------+--------------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+---------+----------------------+-------+--------------------+
            | Offset | Access  | Value                | Bytes | Format             |
            +--------+---------+----------------------+-------+--------------------+
            |        |         |                      |       | Outer (Structure)  |
            |        | outer   |                      |       | Nested (Structure) |
            |        |   inner | <insufficient bytes> |       | uint8              |
            +--------+---------+----------------------+-------+--------------------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack uint8, 1 needed, only 0 available
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, outer: 'Nested') -> None:
                self[:] = (outer, )

            @outer.getter
            def outer(self) -> 'Nested':
                return self[0]

            @outer.setter
            def outer(self, value: 'Nested') -> None:
                self[0] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                if isinstance(value, dict):
                    value = cls._make_structure_from_dict(value)

                (m_outer, ) = value

                if dump is None:
                    cls.outer.fmt.__pack__(m_outer, pieces, dump)

                else:
                    outer_dump = dump.add_record(access="outer", fmt=cls.outer.fmt)
                    cls.outer.fmt.__pack__(m_outer, pieces, outer_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["Outer", int]:
                structure = list.__new__(cls)

                if dump is None:
                    m_outer, offset = cls.outer.fmt.__unpack__(buffer, offset, dump)

                else:
                    outer_dump = dump.add_record(access="outer", fmt=cls.outer.fmt)
                    m_outer, offset = cls.outer.fmt.__unpack__(buffer, offset, outer_dump)

                structure[:] = (m_outer, )

                return structure, offset

            def __eq__(self, other: Any) -> bool:
                if isinstance(other, dict):
                    other = self._make_structure_from_dict(other)
                return list.__eq__(self, other)

            def __ne__(self, other: Any) -> bool:
                if isinstance(other, dict):
                    other = self._make_structure_from_dict(other)
                return list.__ne__(self, other)

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(outer={self.outer!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )
