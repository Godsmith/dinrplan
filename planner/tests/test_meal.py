from planner.models import Meal


def test_default_persons_is_4():
    m = Meal()
    assert m.persons == 4
