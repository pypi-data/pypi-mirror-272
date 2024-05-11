# Test a Rung will be Rendered as ASCII

from pyld import Ladder, Rung
from pyld.elements import Coil, Contact, NegatedCoil, NegatedContact

SIMPLE_LADDER = """\
█
█               
█─────┤ ├────( )
█"""

def test_generate_simple_rung():
    """Validate Simple Ladder Generation with One Rung."""
    ladder = Ladder(
        Rung(
            Contact(),
            Coil(),
        )
    )
    assert SIMPLE_LADDER == ladder.render()

NEGATED_SIMPLE_LADDER = """\
█
█               
█─────┤/├────( )
█"""

def test_generate_simple_negated_rung():
    """Validate Simple Ladder Generation with One Rung."""
    ladder = Ladder(
        Rung(
            NegatedContact(),
            Coil(),
        )
    )
    assert NEGATED_SIMPLE_LADDER == ladder.render()

NEGATED_COIL_SIMPLE_LADDER = """\
█
█               
█─────┤ ├────(/)
█"""

def test_generate_simple_rung_neg_coil():
    """Validate Simple Ladder Generation with One Rung."""
    ladder = Ladder(
        Rung(
            Contact(),
            NegatedCoil(),
        )
    )
    assert NEGATED_COIL_SIMPLE_LADDER == ladder.render()

NEGATED_COIL_NEGATED_SIMPLE_LADDER = """\
█
█               
█─────┤/├────(/)
█"""

def test_generate_simple_negated_rung_negated_coil():
    """Validate Simple Ladder Generation with One Rung."""
    ladder = Ladder(
        Rung(
            NegatedContact(),
            NegatedCoil(),
        )
    )
    print(ladder.render())
    assert NEGATED_COIL_NEGATED_SIMPLE_LADDER == ladder.render()

SIMPLE_LADDER_LONG_NAMES = """\
█
█    SomePOU.LongName  AnotherPOU.EvenLongerName
█──────────┤ ├───────────────────────────────( )
█"""

def test_generate_simple_rung_long_name():
    """Validate Simple Ladder Generation with One Rung."""
    ladder = Ladder(
        Rung(
            Contact("SomePOU.LongName"),
            Coil("AnotherPOU.EvenLongerName"),
        )
    )
    assert SIMPLE_LADDER_LONG_NAMES == ladder.render()
