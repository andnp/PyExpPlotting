from typing import Any, Dict, Sequence

class ColorPalette:
    def __init__(self):
        self._mapper: Dict[str, str] = {}
        self._idx = 0

    def get(self, label: str | None):
        if label is None:
            label = ''

        if label not in self._mapper:
            self._mapper[label] = self.next()

        return self._mapper[label]

    def lock(self, colors: Dict[str, str]):
        self._mapper |= colors
        return self

    def next(self):
        self._idx += 1
        return None

class DivergentColors(ColorPalette):
    def __init__(self, classes: Sequence[Any]):
        super().__init__()

        n_classes = len(classes)
        if n_classes == 9:
            colors = self._9_class()
        elif n_classes == 4:
            colors = self._4_class()
        else:
            raise Exception('Cannot handle arbitrarily many classes')

        for cl, co in zip(sorted(classes), colors):
            self._mapper[cl] = co

    def _9_class(self):
        return [
            "#003f5c",
            "#446189",
            "#7f83b4",
            "#bea7dc",
            "#ffcbff",
            "#faa8dc",
            "#f383b2",
            "#e76083",
            "#d43d51",
        ]

    def _4_class(self):
        return [
            "#aa3344",
            "#c9646d",
            "#e59299",
            "#ffc1c6",
        ]
