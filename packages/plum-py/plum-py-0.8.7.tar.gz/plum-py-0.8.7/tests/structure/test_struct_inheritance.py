# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test Structure type inheritance behaviors."""

from baseline import Baseline

from plum.littleendian import uint8, uint16
from plum.structure import Structure, member


class Base(Structure):

    m0 = member(fmt=uint8)
    m1 = member(fmt=uint8)


class TestAddMethod:

    """Inherit members, but just add a method."""

    class Struct(Base):
        @property
        def product(self):
            return self.m0 * self.m1

    def test_init_and_property(self):
        assert self.Struct(m0=2, m1=3).product == 6

    def test_round_trip(self):
        expected_dump = Baseline(
            """
            +--------+--------+-------+-------+--------------------+
            | Offset | Access | Value | Bytes | Format             |
            +--------+--------+-------+-------+--------------------+
            |        |        |       |       | Struct (Structure) |
            | 0      | m0     | 1     | 01    | uint8              |
            | 1      | m1     | 2     | 02    | uint8              |
            +--------+--------+-------+-------+--------------------+
            """
        )
        original = self.Struct(m0=1, m1=2)
        buffer, pack_dump = original.ipack_and_dump()
        copy, unpack_dump = self.Struct.unpack_and_dump(buffer)
        assert str(pack_dump) == expected_dump
        assert str(unpack_dump) == expected_dump
        assert original == copy


class TestAddMembers:

    """Inherit members, but just add a method."""

    class Struct(Base):

        m2 = member(fmt=uint8)
        m3 = member(fmt=uint8)

    def test_round_trip(self):
        expected_dump = Baseline(
            """
            +--------+--------+-------+-------+--------------------+
            | Offset | Access | Value | Bytes | Format             |
            +--------+--------+-------+-------+--------------------+
            |        |        |       |       | Struct (Structure) |
            | 0      | m0     | 1     | 01    | uint8              |
            | 1      | m1     | 2     | 02    | uint8              |
            | 2      | m2     | 3     | 03    | uint8              |
            | 3      | m3     | 4     | 04    | uint8              |
            +--------+--------+-------+-------+--------------------+
            """
        )
        original = self.Struct(m0=1, m1=2, m2=3, m3=4)
        buffer, pack_dump = original.ipack_and_dump()
        copy, unpack_dump = self.Struct.unpack_and_dump(buffer)
        assert str(pack_dump) == expected_dump
        assert str(unpack_dump) == expected_dump
        assert original == copy


class TestOverrideDefaults:

    """Inherit, overriding the format and default values for some members."""

    class Base(Structure):
        base_default_val = member(fmt=uint8, default=0)
        base_default_factory = member(fmt=uint8, default=lambda self: 1)

        to_override_base_default_val = member(fmt=uint8, default=2)
        to_override_base_default_factory = member(fmt=uint8, default=lambda self: 3)

        order_outer_0 = member(fmt=uint8, default=4)
        order_inner = member(fmt=uint8, default=5)
        order_outer_1 = member(fmt=uint8, default=6)

    class Inheriting(Base):
        # Make sure untouched fields (base_default_val, base_default_factory) inherit properly

        # Override format and defaults
        to_override_base_default_val = member(fmt=uint16, default=20)
        to_override_base_default_factory = member(fmt=uint16, default=lambda self: 30)

        # Ensure order is preserved when overriding a single member
        order_inner = member(fmt=uint16, default=lambda self: 50)

        # Add new fields with both types of defaults
        new_0 = member(fmt=uint16, default=70)
        new_1 = member(fmt=uint16, default=lambda self: 80)

    def test_inheriting(self):
        """Test structure with inherited and overriding members."""
        expected_dump = Baseline(
            """
            +--------+----------------------------------+-------+-------+------------------------+
            | Offset | Access                           | Value | Bytes | Format                 |
            +--------+----------------------------------+-------+-------+------------------------+
            |        |                                  |       |       | Inheriting (Structure) |
            |  0     | base_default_val                 | 0     | 00    | uint8                  |
            |  1     | base_default_factory             | 1     | 01    | uint8                  |
            |  2     | to_override_base_default_val     | 20    | 14 00 | uint16                 |
            |  4     | to_override_base_default_factory | 30    | 1e 00 | uint16                 |
            |  6     | order_outer_0                    | 4     | 04    | uint8                  |
            |  7     | order_inner                      | 50    | 32 00 | uint16                 |
            |  9     | order_outer_1                    | 6     | 06    | uint8                  |
            | 10     | new_0                            | 70    | 46 00 | uint16                 |
            | 12     | new_1                            | 80    | 50 00 | uint16                 |
            +--------+----------------------------------+-------+-------+------------------------+
            """
        )
        inheriting = self.Inheriting()
        _, dump = inheriting.ipack_and_dump()
        assert str(dump) == expected_dump

    def test_specify_arg_vals(self):
        """Test structure with specified (non-default) values for some inherited and new members."""
        expected_dump = Baseline(
            """
            +--------+----------------------------------+-------+-------+------------------------+
            | Offset | Access                           | Value | Bytes | Format                 |
            +--------+----------------------------------+-------+-------+------------------------+
            |        |                                  |       |       | Inheriting (Structure) |
            |  0     | base_default_val                 | 255   | ff    | uint8                  |
            |  1     | base_default_factory             | 100   | 64    | uint8                  |
            |  2     | to_override_base_default_val     | 200   | c8 00 | uint16                 |
            |  4     | to_override_base_default_factory | 300   | 2c 01 | uint16                 |
            |  6     | order_outer_0                    | 4     | 04    | uint8                  |
            |  7     | order_inner                      | 500   | f4 01 | uint16                 |
            |  9     | order_outer_1                    | 6     | 06    | uint8                  |
            | 10     | new_0                            | 700   | bc 02 | uint16                 |
            | 12     | new_1                            | 800   | 20 03 | uint16                 |
            +--------+----------------------------------+-------+-------+------------------------+
            """
        )
        inheriting = self.Inheriting(
            base_default_val=255,
            base_default_factory=100,
            to_override_base_default_val=200,
            to_override_base_default_factory=300,
            order_inner=500,
            new_0=700,
            new_1=800,
        )
        _, dump = inheriting.ipack_and_dump()
        assert str(dump) == expected_dump
