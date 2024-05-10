from typing import Dict, Optional


class KarteiEntry(object):
    entry_sep = "=="
    param_sep = "#"
    p_sep = "="

    def __init__(self, raw_text: str) -> None:
        self._raw_text: str = raw_text.strip()
        self._left_side: str
        self._right_side: str
        self._params: Optional[Dict[str, str]] = None
        self._load_entry()
        self._load_entry_params()

    def _load_entry(self) -> None:
        entry: str = self._raw_text.partition(self.param_sep)[0].strip()
        self._left_side = entry.partition(self.entry_sep)[0].strip()
        self._right_side = entry.partition(self.entry_sep)[2].strip()

    def _load_entry_params(self) -> None:
        entry_params: str = self._raw_text.partition(self.param_sep)[2]
        try:
            self._params = {
                param.split(self.p_sep)[0].strip(): param.split(self.p_sep)[1].strip()
                for param in entry_params.split()
            }
        except IndexError:
            pass

    @property
    def left(self) -> str:
        return self._left_side.strip()

    @property
    def right(self) -> str:
        return self._right_side.strip()

    @property
    def difficulty(self) -> int:
        if self._params is not None:
            result: Optional[str] = self._params.get("diff")
            if result is not None:
                try:
                    return int(result)
                except ValueError:
                    return 0
            else:
                return 0
        else:
            return 0

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"KarteiEntry(left=\"{self.left}\", right=\"{self.right}\", difficulty={self.difficulty})"
