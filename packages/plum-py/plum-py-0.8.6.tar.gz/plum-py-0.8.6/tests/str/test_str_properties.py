# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test StrX transform properties."""

import pytest

from plum.exceptions import SizeError
from plum.str import StrX


class TestDefault:

    """Test with as many left to default as possible."""

    strx = StrX("ascii")

    def test_hint(self):
        assert self.strx.__hint__ == "str"

    def test_name(self):
        assert self.strx.name == "str (ascii)"

    def test_encoding(self):
        assert self.strx.encoding == "ascii"

    def test_errors(self):
        assert self.strx.errors == "strict"

    def test_nbytes(self):
        with pytest.raises(SizeError):
            return self.strx.nbytes

    def test_pad(self):
        assert self.strx.pad == b""

    def test_zero_termination(self):
        assert self.strx.zero_termination is False


class TestPositional:

    """Test explicitly defined with positional argument."""

    strx = StrX("ascii", "ignore", 10, b"\x00", True, "name")

    def test_name(self):
        assert self.strx.name == "name"

    def test_hint(self):
        assert self.strx.__hint__ == "str"

    def test_encoding(self):
        assert self.strx.encoding == "ascii"

    def test_errors(self):
        assert self.strx.errors == "ignore"

    def test_nbytes(self):
        assert self.strx.nbytes == 10

    def test_pad(self):
        assert self.strx.pad == b"\x00"

    def test_zero_termination(self):
        assert self.strx.zero_termination is True


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    strx = StrX(
        encoding="ascii",
        errors="ignore",
        nbytes=10,
        pad=b"\x00",
        zero_termination=True,
        name="name",
    )
