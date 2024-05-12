# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test items transform with fmt=None and with list of values."""

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.exceptions import PackError
from plum.items import items
from plum.littleendian import uint8, uint16


class Test:

    expected_dump = Baseline(
        """
        +--------+--------+-------+-------+------------+
        | Offset | Access | Value | Bytes | Format     |
        +--------+--------+-------+-------+------------+
        |        |        |       |       | items:list |
        | 0      | [0]    | 1     | 01    | uint8      |
        | 1      | [1]    | 2     | 02 00 | uint16     |
        +--------+--------+-------+-------+------------+
        """
    )

    expected_bytes = bytes.fromhex("010200")

    sample = [(1, uint8), (2, uint16)]

    def test_pack(self):
        assert items.pack(self.sample) == self.expected_bytes

    def test_pack_and_dump(self):
        memory, dump = items.pack_and_dump(self.sample)

        assert memory == self.expected_bytes
        assert str(dump) == self.expected_dump

    def test_bad_item(self):
        sample = [(1, uint8), 2]

        with pytest.raises(PackError) as trap:
            items.pack(sample)

        expected = Baseline(
            """
            +--------+--------+-------+-------+---------------+
            | Offset | Access | Value | Bytes | Format        |
            +--------+--------+-------+-------+---------------+
            |        |        |       |       | items:list    |
            | 0      | [0]    | 1     | 01    | uint8         |
            |        | [1]    | 2     |       | int (invalid) |
            +--------+--------+-------+-------+---------------+

            TypeError occurred during pack operation:

            no format specified, value must be a packable data type or (value,
            fmt) pairing (or dict/list of them)
            """
        )

        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)
