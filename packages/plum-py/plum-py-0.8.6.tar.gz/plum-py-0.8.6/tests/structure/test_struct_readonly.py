# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test Structure type read-only feature."""

import sys

import pytest
from baseline import Baseline

from plum.conformance import extract_method_code, wrap_message
from plum.exceptions import UnpackError
from plum.littleendian import uint8
from plum.structure import Structure, bitfield_member, member


class TestNormal:

    """Test readonly feature, normal members."""

    class Custom(Structure):
        """Sample structure type."""

        getable: int = member(fmt=uint8, readonly=True)
        setable: int = member(fmt=uint8, default=2)
        constant: int = member(fmt=uint8, default=3, readonly=True)

    def test_set_access_allowed(self):
        custom = self.Custom(getable=1, setable=2, constant=3)
        assert custom.setable == 2
        custom.setable = 0
        assert custom.setable == 0

    def test_set_access_blocked(self):
        if sys.version_info < (3, 11):
            expected_message = Baseline(
                """
                can't set attribute 'getable'
                """
            )
        else:
            expected_message = Baseline(
                """
                property 'getable' of '[CLASSNAME].Custom' object has no setter
                """
            )

        custom = self.Custom(getable=1, setable=2, constant=3)

        with pytest.raises(AttributeError) as trap:
            custom.getable = 0

        actual_message = str(trap.value)

        if sys.version_info < (3, 10):
            actual_message += " 'getable'"

        actual_message = actual_message.replace(type(self).__name__, "[CLASSNAME]")

        assert actual_message == expected_message

    expected_message = Baseline(
        """
        +--------+----------+-------+-------+--------------------+
        | Offset | Access   | Value | Bytes | Format             |
        +--------+----------+-------+-------+--------------------+
        |        |          |       |       | Custom (Structure) |
        | 0      | getable  | 0     | 00    | uint8              |
        | 1      | setable  | 0     | 00    | uint8              |
        | 2      | constant | 0     | 00    | uint8              |
        +--------+----------+-------+-------+--------------------+

        ValueError occurred during unpack operation:

        'constant' must be 3
        """
    )

    def test_unpack_constant_check(self):
        with pytest.raises(UnpackError) as trap:
            self.Custom.unpack(bytes(3))

        assert wrap_message(trap.value) == self.expected_message

    implementation_baseline = Baseline(
        """
        def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["Custom", int]:
            structure = list.__new__(cls)

            if dump is None:
                m_getable, offset = cls.getable.fmt.__unpack__(buffer, offset, dump)

                m_setable, offset = cls.setable.fmt.__unpack__(buffer, offset, dump)

                m_constant, offset = cls.constant.fmt.__unpack__(buffer, offset, dump)
                if m_constant != cls.constant.default:
                    raise ValueError(f"'constant' must be {cls.constant.default}")

            else:
                getable_dump = dump.add_record(access="getable", fmt=cls.getable.fmt)
                m_getable, offset = cls.getable.fmt.__unpack__(buffer, offset, getable_dump)

                setable_dump = dump.add_record(access="setable", fmt=cls.setable.fmt)
                m_setable, offset = cls.setable.fmt.__unpack__(buffer, offset, setable_dump)

                constant_dump = dump.add_record(access="constant", fmt=cls.constant.fmt)
                m_constant, offset = cls.constant.fmt.__unpack__(buffer, offset, constant_dump)
                if m_constant != cls.constant.default:
                    raise ValueError(f"'constant' must be {cls.constant.default}")

            structure[:] = (m_getable, m_setable, m_constant)

            return structure, offset

        """
    )

    def test_unpack_implementation(self):
        unpack_implementation = extract_method_code(
            self.Custom.implementation, "__unpack__"
        )
        assert unpack_implementation == self.implementation_baseline


class TestBitField(TestNormal):

    """Test readonly feature, normal members."""

    class Custom(Structure, fieldorder="least_to_most"):
        """Sample structure type."""

        getable: int = bitfield_member(size=4, readonly=True)
        setable: int = bitfield_member(size=4, default=2)
        constant: int = bitfield_member(size=4, default=3, readonly=True)

    expected_message = Baseline(
        """
        +---------+----------+-------+-------------------+--------------------+
        | Offset  | Access   | Value | Bytes             | Format             |
        +---------+----------+-------+-------------------+--------------------+
        |         |          |       |                   | Custom (Structure) |
        | 0       |          | 0     | 00 00             |                    |
        |  [0:4]  | getable  | 0     | ........ ....0000 | int                |
        |  [4:8]  | setable  | 0     | ........ 0000.... | int                |
        |  [8:12] | constant | 0     | ....0000 ........ | int                |
        +---------+----------+-------+-------------------+--------------------+

        ValueError occurred during unpack operation:

        'constant' must be 3
        """
    )

    implementation_baseline = Baseline(
        """
        def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["Custom", int]:
            structure = list.__new__(cls)

            if dump is None:
                bitfields_0, offset = cls.getable.__unpack__(buffer, offset, dump, "little", nbytes=2, signed=False)

                m_getable = (bitfields_0 >> 0) & 0xf

                m_setable = (bitfields_0 >> 4) & 0xf

                m_constant = (bitfields_0 >> 8) & 0xf
                if m_constant != cls.constant.default:
                    raise ValueError(f"'constant' must be {cls.constant.default}")

            else:
                bitfields_0_dump = dump.add_record()
                bitfields_0, offset = cls.getable.__unpack__(buffer, offset, bitfields_0_dump, "little", nbytes=2, signed=False)

                m_getable = (bitfields_0 >> 0) & 0xf
                dump.add_record(access="getable", bits=(0, 4), value=m_getable, fmt=int)

                m_setable = (bitfields_0 >> 4) & 0xf
                dump.add_record(access="setable", bits=(4, 4), value=m_setable, fmt=int)

                m_constant = (bitfields_0 >> 8) & 0xf
                dump.add_record(access="constant", bits=(8, 4), value=m_constant, fmt=int)
                if m_constant != cls.constant.default:
                    raise ValueError(f"'constant' must be {cls.constant.default}")

            structure[:] = (m_getable, m_setable, m_constant)

            return structure, offset

        """
    )
