import typing as t
import unittest

from keylix.core import (
    KxMatch,
    KxPattern,
    KxPatternAnd,
    KxPatternChars,
    KxPatternConcat,
    KxPatternExcludes,
    KxPatternOr,
    KxPatternWildcard,
)


class TestKxPattern(unittest.TestCase):
    def run_full_match_tests(
        self,
        kx_pattern: KxPattern,
        matching: t.List[str] = [],
        not_matching: t.List[str] = [],
    ) -> None:
        """Runs kx_pattern.full_match() tests"""

        for string in not_matching:
            self.assertEqual(
                kx_pattern.full_match(string),
                False,
                f'Incorrectly full-matched {kx_pattern} with "{string}".',
            )

        for string in matching:
            self.assertEqual(
                kx_pattern.full_match(string),
                True,
                f'Failed to full-match {kx_pattern} with "{string}".',
            )

    def run_search_tests(
        self, kx_pattern: KxPattern, test_strings: t.Dict[str, t.Union[KxMatch, None]]
    ):
        """Runs kx_pattern.search() tests"""

        for string, expectation in test_strings.items():
            result = kx_pattern.search(string)
            if expectation is None:
                self.assertIsNone(result)
            else:
                self.assertIsNotNone(result)
                self.assertEqual(result.start, expectation.start)
                self.assertEqual(result.end, expectation.end)


class TestKxPatternChars(TestKxPattern):
    def test_search_01(self):
        # pattern: empty
        kx_pat = KxPatternChars("")

        self.run_search_tests(
            kx_pat,
            {
                "": KxMatch(0, 0),
                "abc": KxMatch(0, 0),
                "defg": KxMatch(0, 0),
                "0123456789": KxMatch(0, 0),
            },
        )

    def test_search_02(self):
        # pattern: "ab"
        kx_pattern = KxPatternChars("ab")

        self.run_search_tests(
            kx_pattern,
            {
                "": None,
                "a": None,
                "b": None,
                "ab": KxMatch(0, 2),
                "ba": None,
                "prefix ab": KxMatch(7, 9),
                "ab suffix": KxMatch(0, 2),
                "prefix ab suffix": KxMatch(7, 9),
                "aab": KxMatch(1, 3),
                "abb": KxMatch(0, 2),
                "a infix b": None,
                "prefix ab random words ab suffix": KxMatch(7, 9),
                "random words": None,
            },
        )

    def test_full_match_01(self):
        # pattern: empty
        kx_pattern = KxPatternChars("")

        self.run_full_match_tests(
            kx_pattern,
            matching=[""],
            not_matching=[
                "a",
                "ab",
                " ",
                "random words",
                "more random words",
                "0123456789",
            ],
        )

    def test_full_match_02(self):
        # pattern: "ab"
        kx_pattern = KxPatternChars("ab")

        self.run_full_match_tests(
            kx_pattern,
            matching=["ab"],
            not_matching=[
                "",
                "a",
                "b",
                "ba",
                "prefix ab",
                "ab suffix",
                "prefix ab suffix",
                "aab",
                "abb",
                "a infix b",
                "prefix ab random words ab suffix",
                "random words",
            ],
        )


class TestKxPatternWildcard(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.kx_pattern = KxPatternWildcard()

    def test_search_01(self):
        self.assertIsNotNone(
            self.kx_pattern.search(""), "Failed to find in an empty string."
        )
        self.assertIsNotNone(
            self.kx_pattern.search("a non empty string"),
            "Failed to find in a single-character string.",
        )

    def test_full_match_01(self):
        self.assertEqual(
            self.kx_pattern.full_match(""),
            True,
            "Failed to full match an empty string.",
        )
        self.assertEqual(
            self.kx_pattern.full_match("a non empty string"),
            True,
            "Failed to full match a non-empty string.",
        )


class TestKxPatternExcludes(TestKxPattern):
    def test_search_01(self):
        # pattern: empty
        kx_subpat0 = KxPatternChars("")
        kx_pattern = KxPatternExcludes(kx_subpat0)

        self.run_search_tests(
            kx_pattern,
            {
                "": None,
                "abc": None,
                "defg": None,
                "0123456789": None,
            },
        )

    def test_search_02(self):
        # pattern: "ab"
        kx_subpat0 = KxPatternChars("ab")
        kx_pattern = KxPatternExcludes(kx_subpat0)

        self.run_search_tests(
            kx_pattern,
            {
                "": KxMatch(0, 0),
                "a": KxMatch(0, 0),
                "b": KxMatch(0, 0),
                "ab": KxMatch(0, 0),
                "ba": KxMatch(0, 0),
                "prefix ab": KxMatch(0, 0),
                "ab suffix": KxMatch(0, 0),
                "prefix ab suffix": KxMatch(0, 0),
                "aab": KxMatch(0, 0),
                "abb": KxMatch(0, 0),
                "a infix b": KxMatch(0, 0),
                "prefix ab random words ab suffix": KxMatch(0, 0),
                "random words": KxMatch(0, 0),
            },
        )

    def test_search_03(self):
        # pattern: empty
        kx_subpat0 = KxPatternWildcard()
        kx_pattern = KxPatternExcludes(kx_subpat0)

        self.run_search_tests(
            kx_pattern,
            {
                "": None,
                "abc": None,
                "defg": None,
                "0123456789": None,
            },
        )

    def test_full_match_01(self):
        # pattern: empty
        kx_subpat0 = KxPatternChars("")
        kx_pattern = KxPatternExcludes(kx_subpat0)

        self.run_full_match_tests(
            kx_pattern,
            matching=[],
            not_matching=[
                "",
                "a",
                "ab",
                " ",
                "random words",
                "more random words",
                "0123456789",
            ],
        )

    def test_full_match_02(self):
        # pattern: "ab"
        kx_subpat0 = KxPatternChars("ab")
        kx_pattern = KxPatternExcludes(kx_subpat0)

        self.run_full_match_tests(
            kx_pattern,
            matching=[
                "",
                "a",
                "b",
                "ba",
                "a infix b",
                "random words",
            ],
            not_matching=[
                "ab",
                "prefix ab",
                "ab suffix",
                "prefix ab suffix",
                "aab",
                "abb",
                "prefix ab random words ab suffix",
            ],
        )

    def test_full_match_03(self):
        # pattern: empty
        kx_subpat0 = KxPatternWildcard()
        kx_pattern = KxPatternExcludes(kx_subpat0)

        self.run_full_match_tests(
            kx_pattern,
            matching=[],
            not_matching=[
                "",
                "a",
                "ab",
                " ",
                "random words",
                "more random words",
                "0123456789",
            ],
        )


class TestKxPatternOr(TestKxPattern):
    # Any 0- or 1-element OR-pattern expressions cannot be constructed with
    # the current keylix notation. However, we can still test these cases.

    def test_search_01(self):
        # pattern: empty set
        kx_pattern = KxPatternOr([])

        self.run_search_tests(
            kx_pattern,
            test_strings={
                "": None,
                "random string": None,
                "another random string": None,
                "0123456789": None,
            },
        )

    def test_search_02(self):
        # pattern: or( "" ) - a single empty chars sub-pattern. A match should
        # exist for any input.
        kx_subpat0 = KxPatternChars("")
        kx_pattern = KxPatternOr([kx_subpat0])

        self.run_search_tests(
            kx_pattern,
            test_strings={
                "": KxMatch(0, 0),
                "random string": KxMatch(0, 0),
                "another random string": KxMatch(0, 0),
            },
        )

    def test_search_03(self):
        # pattern: or( "ab" ) - a single chars sub-pattern. Searches for
        # or( "ab" ) and "ab" patterns should give identical results.
        kx_subpat0 = KxPatternChars("ab")
        kx_pattern = KxPatternOr([kx_subpat0])

        self.run_search_tests(
            kx_pattern,
            {
                "": kx_subpat0.search(""),
                "a": kx_subpat0.search("a"),
                "b": kx_subpat0.search("b"),
                "ab": kx_subpat0.search("ab"),
                "ba": kx_subpat0.search("ba"),
                "prefix ab": kx_subpat0.search("prefix ab"),
                "ab suffix": kx_subpat0.search("ab suffix"),
                "prefix ab suffix": kx_subpat0.search("prefix ab suffix"),
                "aab": kx_subpat0.search("aab"),
                "abb": kx_subpat0.search("abb"),
                "a infix b": kx_subpat0.search("a infix b"),
                "prefix ab random words ab suffix": kx_subpat0.search(
                    "prefix ab random words ab suffix"
                ),
                "random words": kx_subpat0.search("random words"),
            },
        )

    def test_search_04(self):
        # pattern: or( * ) - a single wildcard sub-pattern.
        kx_pat0 = KxPatternWildcard()
        kx_pattern = KxPatternOr([kx_pat0])

        self.run_search_tests(
            kx_pattern,
            test_strings={
                "": KxMatch(0, 0),
                "random string": KxMatch(0, 0),
                "another random string": KxMatch(0, 0),
            },
        )

    def test_search_05(self):
        # pattern: or( "" | "" )
        kx_subpat0 = KxPatternChars("")
        kx_subpat1 = KxPatternChars("")
        kx_pattern = KxPatternOr([kx_subpat0, kx_subpat1])

        self.run_search_tests(
            kx_pattern,
            test_strings={
                "": KxMatch(0, 0),
                "random string": KxMatch(0, 0),
                "another random string": KxMatch(0, 0),
            },
        )

    def test_search_06(self):
        # pattern: or( | ab )
        kx_subpat0 = KxPatternChars("")
        kx_subpat1 = KxPatternChars("ab")
        kx_pattern = KxPatternOr([kx_subpat0, kx_subpat1])

        self.run_search_tests(
            kx_pattern,
            {
                "": KxMatch(0, 0),
                "a": KxMatch(0, 0),
                "b": KxMatch(0, 0),
                "ab": KxMatch(0, 0),
                "ba": KxMatch(0, 0),
                "prefix ab": KxMatch(0, 0),
                "ab suffix": KxMatch(0, 0),
                "prefix ab suffix": KxMatch(0, 0),
                "aab": KxMatch(0, 0),
                "abb": KxMatch(0, 0),
                "a infix b": KxMatch(0, 0),
                "prefix ab random words ab suffix": KxMatch(0, 0),
                "random words": KxMatch(0, 0),
            },
        )

    def test_search_07(self):
        # pattern: or( ab | )
        kx_subpat0 = KxPatternChars("ab")
        kx_subpat1 = KxPatternChars("")
        kx_pattern = KxPatternOr([kx_subpat0, kx_subpat1])

        self.run_search_tests(
            kx_pattern,
            {
                "": KxMatch(0, 0),
                "a": KxMatch(0, 0),
                "b": KxMatch(0, 0),
                "ab": KxMatch(0, 2),
                "ba": KxMatch(0, 0),
                "prefix ab": KxMatch(7, 9),
                "ab suffix": KxMatch(0, 2),
                "prefix ab suffix": KxMatch(7, 9),
                "aab": KxMatch(1, 3),
                "abb": KxMatch(0, 2),
                "a infix b": KxMatch(0, 0),
                "prefix ab random words ab suffix": KxMatch(7, 9),
                "random words": KxMatch(0, 0),
            },
        )

    def test_search_08(self):
        # pattern: or( ab | cd )
        kx_subpat0 = KxPatternChars("ab")
        kx_subpat1 = KxPatternChars("cd")
        kx_pattern = KxPatternOr([kx_subpat0, kx_subpat1])

        self.run_search_tests(
            kx_pattern,
            {
                "": None,
                "a": None,
                "b": None,
                "ab": KxMatch(0, 2),
                "ba": None,
                "prefix ab": KxMatch(7, 9),
                "ab suffix": KxMatch(0, 2),
                "prefix ab suffix": KxMatch(7, 9),
                "aab": KxMatch(1, 3),
                "abb": KxMatch(0, 2),
                "a infix b": None,
                "prefix ab random words ab suffix": KxMatch(7, 9),
                "random words": None,
                "acd suffix": KxMatch(1, 3),
                "a infix cd infix2 b suffix": KxMatch(8, 10),
                "cd": KxMatch(0, 2),
                "acbd": None,
                "abcd": KxMatch(0, 2),
                "cdab": KxMatch(2, 4),
            },
        )

    def test_search_09(self):
        # pattern or( * | cd )
        kx_subpat0 = KxPatternWildcard()
        kx_subpat1 = KxPatternChars("cd")
        kx_pattern = KxPatternOr([kx_subpat0, kx_subpat1])

        self.run_search_tests(
            kx_pattern,
            test_strings={
                "": KxMatch(0, 0),
                "random string": KxMatch(0, 0),
                "another random string": KxMatch(0, 0),
            },
        )

    def test_full_match_01(self):
        # pattern: empty set
        kx_pattern = KxPatternOr([])

        self.run_full_match_tests(
            kx_pattern,
            not_matching=[
                "",
                "random string",
                "another random string",
                "0123456789",
            ],
        )

    def test_full_match_02(self):
        # pattern: or( "" ) - a single empty chars sub-pattern. A match should
        # exist for any input.
        kx_subpat0 = KxPatternChars("")
        kx_pattern = KxPatternOr([kx_subpat0])

        self.run_full_match_tests(
            kx_pattern,
            matching=[""],
            not_matching=[
                "random string",
                "another random string",
                "0123456789",
            ],
        )

    def test_full_match_03(self):
        # pattern: or( "ab" ) - a single chars sub-pattern. Searches for
        # or( "ab" ) and "ab" patterns should give identical results.
        kx_subpat0 = KxPatternChars("ab")
        kx_pattern = KxPatternOr([kx_subpat0])

        self.run_full_match_tests(
            kx_pattern,
            matching=["ab"],
            not_matching=[
                "",
                "a",
                "b",
                "ba",
                "prefix ab",
                "ab suffix",
                "prefix ab suffix",
                "aab",
                "abb",
                "a infix b",
                "prefix ab random words ab suffix",
                "random words",
            ],
        )

    def test_full_match_04(self):
        # pattern: or( * ) - a single wildcard sub-pattern.
        kx_pat0 = KxPatternWildcard()
        kx_pattern = KxPatternOr([kx_pat0])

        self.run_full_match_tests(
            kx_pattern,
            matching=[
                "",
                "random string",
                "another random string",
            ],
        )

    def test_full_match_05(self):
        # pattern: or( "" | "" )
        kx_subpat0 = KxPatternChars("")
        kx_subpat1 = KxPatternChars("")
        kx_pattern = KxPatternOr([kx_subpat0, kx_subpat1])

        self.run_full_match_tests(
            kx_pattern,
            matching=[""],
            not_matching=[
                "random string",
                "another random string",
                "0123456789",
            ],
        )

    def test_full_match_06(self):
        # pattern: or( | ab )
        kx_subpat0 = KxPatternChars("")
        kx_subpat1 = KxPatternChars("ab")
        kx_pattern = KxPatternOr([kx_subpat0, kx_subpat1])

        self.run_full_match_tests(
            kx_pattern,
            matching=["", "ab"],
            not_matching=[
                "a",
                "b",
                "ba",
                "prefix ab",
                "ab suffix",
                "prefix ab suffix",
                "aab",
                "abb",
                "a infix b",
                "prefix ab random words ab suffix",
                "random words",
            ],
        )

    def test_full_match_07(self):
        # pattern: or( ab | )
        kx_subpat0 = KxPatternChars("ab")
        kx_subpat1 = KxPatternChars("")
        kx_pattern = KxPatternOr([kx_subpat0, kx_subpat1])

        self.run_full_match_tests(
            kx_pattern,
            matching=["", "ab"],
            not_matching=[
                "a",
                "b",
                "ba",
                "prefix ab",
                "ab suffix",
                "prefix ab suffix",
                "aab",
                "abb",
                "a infix b",
                "prefix ab random words ab suffix",
                "random words",
            ],
        )

    def test_full_match_08(self):
        # pattern: or( ab | cd )
        kx_subpat0 = KxPatternChars("ab")
        kx_subpat1 = KxPatternChars("cd")
        kx_pattern = KxPatternOr([kx_subpat0, kx_subpat1])

        self.run_full_match_tests(
            kx_pattern,
            matching=["ab", "cd"],
            not_matching=[
                "",
                "a",
                "b",
                "c",
                "d",
                "ba",
                "prefix ab",
                "ab suffix",
                "prefix ab suffix",
                "aab",
                "abb",
                "a infix b",
                "prefix ab random words ab suffix",
                "random words",
                "acd suffix",
                "a infix cd infix2 b suffix",
                "acbd",
                "abcd",
                "cdab",
            ],
        )

    def test_full_match_09(self):
        # pattern or( * | cd )
        kx_subpat0 = KxPatternWildcard()
        kx_subpat1 = KxPatternChars("cd")
        kx_pattern = KxPatternOr([kx_subpat0, kx_subpat1])

        self.run_full_match_tests(
            kx_pattern,
            matching=[
                "",
                "random string",
                "another random string",
            ],
        )


class TestKxPatternAnd(unittest.TestCase):
    def _test_search_01(self):
        pass

    def _test_full_match_01(self):
        pass


class TestKxPatternConcat(TestKxPattern):
    def test_search_01(self):
        kx_pattern = KxPatternConcat([])
        self.assertIsNotNone(kx_pattern.search("fdaf"))
        is_full_match = kx_pattern.full_match("asdf")
        self.assertEqual(is_full_match, False, "found full match for an empty pattern")

    def test_search_02(self):
        kx_subpat0 = KxPatternChars("asd")
        kx_subpat1 = KxPatternWildcard()
        kx_pattern = KxPatternConcat([kx_subpat0, kx_subpat1])
        self.assertEqual(kx_pattern.full_match("asd"), True)

    def test_full_match_01(self):
        # pattern concat()
        kx_pattern = KxPatternConcat([])

        self.run_full_match_tests(
            kx_pattern,
            matching=[""],
            not_matching=[
                "random string",
            ],
        )

    def test_full_match_02(self):
        # pattern: concat( "ab" )
        kx_subpat0 = KxPatternChars("ab")
        kx_pattern = KxPatternConcat([kx_subpat0])

        self.run_full_match_tests(
            kx_pattern,
            matching=["ab"],
            not_matching=[
                "",
                "random string",
                "ff",  # same length
                "ab but with a suffix",
                "prefix and ab",
                "prefix, ab, and suffix",
            ],
        )

    def test_full_match_03(self):
        # pattern: concat( * )
        kx_subpat0 = KxPatternWildcard()
        kx_pattern = KxPatternConcat([kx_subpat0])

        self.run_full_match_tests(
            kx_pattern,
            matching=["", "ab", "anything and more"],
            not_matching=[],
        )

    def test_full_match_04(self):
        # pattern: concat( "ab" . * )
        kx_subpat0 = KxPatternChars("ab")
        kx_subpat1 = KxPatternWildcard()
        kx_pattern = KxPatternConcat([kx_subpat0, kx_subpat1])

        self.run_full_match_tests(
            kx_pattern,
            matching=["ab", "ab but with a suffix"],
            not_matching=[
                "",
                "random string",
                "ff",  # same length
                "prefix and ab",
                "prefix, ab, and suffix",
            ],
        )

    def test_full_match_05(self):
        # pattern: concat( * . "ab" )
        kx_subpat0 = KxPatternWildcard()
        kx_subpat1 = KxPatternChars("ab")
        kx_pattern = KxPatternConcat([kx_subpat0, kx_subpat1])

        self.run_full_match_tests(
            kx_pattern,
            matching=["ab", "prefix and ab"],
            not_matching=[
                "",
                "random string",
                "ff",  # same length
                "ab but with a suffix",
                "prefix, ab, and suffix",
            ],
        )

    def test_full_match_06(self):
        # pattern: concat( * . "ab" . * )
        kx_subpat0 = KxPatternWildcard()
        kx_subpat1 = KxPatternChars("ab")
        kx_subpat2 = KxPatternWildcard()
        kx_pattern = KxPatternConcat([kx_subpat0, kx_subpat1, kx_subpat2])

        self.run_full_match_tests(
            kx_pattern,
            matching=[
                "ab",
                "prefix and ab",
                "ab but with a suffix",
                "prefix, ab, and suffix",
            ],
            not_matching=[
                "",
                "random string",
                "ff",  # same length
            ],
        )


if __name__ == "__main__":
    unittest.main()
