# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2023 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer flag dump without names."""

from baseline import Baseline

from plum.enum import EnumX
from sample_flag import Register, RegisterMixin

register = EnumX(Register, 1, "big", signed=False, strict=False)
register_mixin = EnumX(RegisterMixin, 1, "big", signed=False, strict=False)


class TestIntEnum:

    """Test FlagX default name with IntFlag."""

    expected_dump = Baseline(
        """
        +--------+-------------+-------+--------------------+
        | Offset | Value       | Bytes | Format             |
        +--------+-------------+-------+--------------------+
        | 0      | Register.SP | 01    | Register (IntFlag) |
        +--------+-------------+-------+--------------------+
        """
    )

    def test_pack_and_dump(self):
        _, dump = register.pack_and_dump(1)
        assert str(dump) == self.expected_dump


class TestIntMixinEnum:

    """Test FlagX default name with int, Flag mixin."""

    expected_dump = Baseline(
        """
        +--------+------------------+-------+---------------------------+
        | Offset | Value            | Bytes | Format                    |
        +--------+------------------+-------+---------------------------+
        | 0      | RegisterMixin.SP | 01    | RegisterMixin (int, Flag) |
        +--------+------------------+-------+---------------------------+
        """
    )

    def test_pack_and_dump(self):
        _, dump = register_mixin.pack_and_dump(1)
        assert str(dump) == self.expected_dump
