import re
import typing as t


class KxMatch:
    start: int
    end: int

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end


class KxPattern:
    def contains_match(self, string: str) -> bool:
        if self.search(string) is not None:
            return True
        return False

    def full_match(self, string: str) -> bool:
        return False

    def search(self, string: str) -> t.Union[KxMatch, None]:
        return None

    def search_all(self, string: str) -> t.List:
        result = []
        i = 0
        while i <= len(string):
            kx_match = self.search(string[i:])
            if kx_match is None:
                break
            result.append(kx_match)
            i += kx_match.start + 1
        return result


class KxPatternWildcard(KxPattern):
    def __str__(self) -> str:
        return "*"

    def full_match(self, string: str) -> bool:
        return True

    def search(self, string: str) -> t.Union[KxMatch, None]:
        return KxMatch(start=0, end=0)


class KxPatternChars(KxPattern):

    _pattern: str
    _re_pattern: re.Pattern

    def __init__(self, pattern: str):
        super().__init__()
        self._pattern = pattern
        self._re_pattern = re.compile(re.escape(pattern))

    def __str__(self) -> str:
        return f"chars({self._pattern})"

    def full_match(self, string: str) -> bool:
        kx_match = self.search(string)
        if kx_match is not None and kx_match.start == 0 and kx_match.end == len(string):
            return True
        return False

    def search(self, string: str) -> t.Union[KxMatch, None]:
        re_match = self._re_pattern.search(string)
        if re_match is not None:
            return KxMatch(start=re_match.start(), end=re_match.end())
        return None


class KxPatternEmpty(KxPatternChars):
    def __init__(self):
        super().__init__("")


class KxPatternParentheses(KxPattern):

    _sub_pattern: KxPattern

    def __init__(self, sub_pattern: KxPattern):
        super().__init__()
        self._sub_pattern = sub_pattern

    def contains_match(self, string: str) -> bool:
        return self._sub_pattern.contains_match(string)

    def full_match(self, string: str) -> bool:
        return self._sub_pattern.full_match(string)

    def search(self, string: str) -> t.Union[KxMatch, None]:
        return self._sub_pattern.search(str)


class KxPatternExcludes(KxPattern):

    _sub_pattern: KxPattern

    def __init__(self, sub_pattern: KxPattern):
        super().__init__()
        self._sub_pattern = sub_pattern

    def __str__(self) -> str:
        return f"~({self._sub_pattern})"

    def contains_match(self, string: str) -> bool:
        kx_match = self._sub_pattern.search(str)

        return super().contains_match(string)

    def full_match(self, string: str) -> bool:
        kx_match = self._sub_pattern.search(string)
        if kx_match is None:
            return True
        return False

    def search(self, string: str) -> t.Union[KxMatch, None]:
        kx_match = self._sub_pattern.search(string)
        if kx_match is None or kx_match.end > 0:
            return KxMatch(start=0, end=0)
        return None


class KxPatternOr(KxPattern):

    _sub_patterns: t.List[KxPattern]

    def __init__(self, sub_patterns: t.List[KxPattern]):
        super().__init__()
        self._sub_patterns = sub_patterns

    def __str__(self) -> str:
        if len(self._sub_patterns) == 0:
            return "or()"
        r = f"( {self._sub_patterns[0]}"
        for sub_pattern in self._sub_patterns[1:]:
            r += f"| {sub_pattern}"
        r += " )"
        return r

    def full_match(self, string: str) -> bool:
        for sub_pattern in self._sub_patterns:
            if sub_pattern.full_match(string):
                return True
        return False

    def search(self, string: str) -> t.Union[KxMatch, None]:
        for sub_pattern in self._sub_patterns:
            kx_match = sub_pattern.search(string)
            if kx_match is not None:
                return kx_match
        return None


class KxPatternAnd(KxPattern):

    _sub_patterns: t.List[KxPattern]

    def __init__(self, sub_patterns: t.List[KxPattern]):
        super().__init__()
        self._sub_patterns = sub_patterns

    def full_match(self, string: str) -> bool:
        kx_match = self.search(string)
        if kx_match is not None and kx_match.start == 0:
            return True
        return False

    def search(self, string: str) -> t.Union[KxMatch, None]:
        start = len(string) + 1
        end = -1
        print(f"len: {len(self._sub_patterns)}")
        for sub_pattern in self._sub_patterns:
            kx_match = sub_pattern.search(string)
            if kx_match is None:
                return None
            if kx_match.start < start:
                start = kx_match.start
            if kx_match.end > end:
                end = kx_match.end
        return KxMatch(start, end)


class KxPatternConcat(KxPattern):
    _sub_patterns: t.List[KxPattern]

    def __init__(self, sub_patterns: t.List[KxPattern]):
        super().__init__()
        self._sub_patterns = sub_patterns

    def __str__(self) -> str:
        if len(self._sub_patterns) == 0:
            return "concat()"
        r = f"concat( {self._sub_patterns[0]}"
        for sub_pattern in self._sub_patterns[1:]:
            r += f". {sub_pattern}"
        r += " )"
        return r

    def search(self, string: str) -> t.Union[KxMatch, None]:
        n = len(self._sub_patterns)
        m = len(string)
        c = [[None for j in range(m + 1)] for i in range(n + 1)]
        for j in range(m + 1):
            c[0][j] = j
        for i in range(1, n):
            for j in range(m + 1):
                for k in range(j + 1):
                    if c[i - 1][k] is not None and self._sub_patterns[i - 1].full_match(
                        string[k:j]
                    ):
                        c[i][j] = c[i - 1][k]
                        break
        for j in range(0, m):
            if c[n][j] is not None:
                return KxMatch(start=c[n][j], end=j)
        return None

    def full_match(self, string: str) -> bool:
        n = len(self._sub_patterns)
        m = len(string)
        c = [[None for j in range(m + 1)] for i in range(n + 1)]
        c[0][0] = 0
        for i in range(1, n + 1):
            for j in range(m + 1):
                for k in range(j + 1):
                    if c[i - 1][k] is not None and self._sub_patterns[i - 1].full_match(
                        string[k:j]
                    ):
                        c[i][j] = c[i - 1][k]
                        break
        if c[n][m] is not None:
            return True
        return False
