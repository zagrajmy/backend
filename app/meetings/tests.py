from django.test import TestCase


class DummyTests(TestCase):
    def test_dummy(self) -> None:
        self.assertTrue(True)  # pylint: disable=redundant-unittest-assert
