import itertools
import typing

from .._elements import Route


class Tram:
    _counter = itertools.count(0)
    MAX_LENGTH: float | None = 50  # 50 m
    """Maximum allowed length of the tram in [m]."""
    MAX_SPEED: float | None = 20   # 20 m/s == 72 km/h
    """Maximum allowed speed of the tram in [m/s]."""

    def __init__(
        self,
        length: int | float = 25.0,
        speed: int | float = 10.0,
        name: typing.Optional[str] = None,
        route: typing.Optional[Route] = None
    ) -> None:
        self._speed = self._check_speed(speed)
        self._length = self._check_length(length)
        if name is None:
            name = f'Tram_{next(self._counter)}'
        else:
            name = self._check_name(name)
        self._name = name
        self._route = self._check_route(route)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(length={self.length}, '
            f'speed={self.speed}, name={self.name}, route={self.route})'
            )

    def __str__(self) -> str:
        if self.route is None:
            return self.name
        return f'{self.name} ({self.route.name})'

    @staticmethod
    def _check_if_positive(value: int | float) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError(f'"{value}" is not a numeric value.')
        if value <= 0:
            raise ValueError(f'{value} is not a positive value.')

    def _check_length(self, length: int | float) -> float:
        self._check_if_positive(length)
        if self.MAX_LENGTH is not None and length > self.MAX_LENGTH:
            raise ValueError(
                f'The length of the tram cannot exceed {self.MAX_LENGTH} m.'
                )
        return float(length)

    def _check_speed(self, speed: int | float) -> float:
        self._check_if_positive(speed)
        if self.MAX_SPEED is not None and speed > self.MAX_SPEED:
            raise ValueError(
                f'The speed of the tram cannot exceed {self.MAX_SPEED} km/h.'
                )
        return float(speed)

    def _check_name(self, name: str) -> str:
        if not isinstance(name, str):
            raise ValueError('Tram name must be a string.')
        if not name:
            raise ValueError('Tram name cannot be empty.')
        return name.strip()

    def _check_route(self, route: Route | None) -> Route | None:
        if route is not None and not isinstance(route, Route):
            raise ValueError(
                f'Invalid route argument "{route}" of type '
                f'"{type(route).__name__}". Expected type "Route".'
                )
        return route

    @property
    def length(self) -> float:
        return self._length

    @length.setter
    def length(self, length: float):
        self._length = self._check_length(length)

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, speed: float) -> None:
        self._speed = self._check_speed(speed)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = self._check_name(name)

    @property
    def route(self) -> Route | None:
        return self._route

    @route.setter
    def route(self, route: Route | None) -> None:
        self._route = self._check_route(route)
