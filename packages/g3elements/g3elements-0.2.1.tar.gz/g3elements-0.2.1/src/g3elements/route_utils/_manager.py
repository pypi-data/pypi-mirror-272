import itertools
import typing

from .._elements import Route
from ._tram import Tram


class UnknownRouteError(Exception):
    pass


class RouteAlreadyRegisteredError(Exception):
    pass


class TramNotSetError(Exception):
    pass


class RouteManager:
    def __init__(
        self, *routes: Route | typing.Iterable[Route | typing.Iterable]
    ) -> None:
        self._routes: set[Route] = set()
        self._route_tram_pairs: dict[str, Tram] = {}
        for route in self._flatten_routes(routes):
            self.add_route(route)

    @staticmethod
    def _flatten_routes(
        routes: Route | typing.Iterable[Route | typing.Iterable]
    ) -> set[Route]:
        """
        Flatten the given routes into a flat set of `Route` objects.

        Args:
            routes (Route | typing.Iterable[Route | typing.Iterable]):
            The routes to be flattened.

        Returns:
            set[Route]: A set of flattened Route objects.
        """
        flattened: set[Route] = set()

        def _flatten(current_item):
            if isinstance(current_item, Route):
                flattened.add(current_item)
            elif isinstance(current_item, typing.Iterable):
                for item in current_item:
                    _flatten(item)

        _flatten(routes)
        return flattened

    def get_routes(
        self,
        as_dict: bool = True,
        constraint: typing.Optional[typing.Callable[[Route], bool]] = None
    ) -> typing.Union[dict[str, Route], list[Route]]:
        """
        Retrieve the stored Route objects, optionally filtered by
        a constraint function.

        Args:
            as_dict (bool, optional): Determines the format of the returned
            data. If True (default), returns a dictionary with route names as
            keys and `Route` objects as values. If False, returns a list of
            `Route` objects.
            constraint (Callable[[Route], bool], optional): A function that
            takes a `Route` object and returns a boolean. If provided, this
            function is used to filter the routes. Defaults to None, in which
            case all routes are included.

        Returns:
            typing.Union[Dict[str, Route], List[Route]]: The stored `Route`
            objects that meet the specified constraint (if any).

        Example:
            ```python
            # assume a PassageGenerator instance is initialized
            # with a list of Route objects
            passage_generator = PassageGenerator(routes)

            # Define a constraint function that checks if a Route
            # has more than 3 position detectors in its layout
            def has_more_than_three_detectors(route: Route):
                return len(route.detectors) > 3

            # Get the routes with more than 3 detectors,
            # stored in a list. Note that the constraint is not called
            # by the user in the "get_routes" call!
            result = passage_generator.get_routes(
                as_dict=False,
                constraint=has_more_than_three_detectors
                )

            # Get the same result
            # with the same constraint defined as a lambda expression
            result_lambda = passage_generator.get_routes(
                as_dict=False,
                constraint=lambda route: len(route.detectors) > 3
                )

            # Check the results are as expected
            def assert_has_more_than_three_detectors(routes: list[Route]):
                for route in routes:
                    assert has_more_than_three_detectors(route) is True, (
                        f"Route {route.name} must have more than 3 position "
                        "detectors in its layout"
                    )
                return True

            assert assert_has_more_than_three_detectors(result) is True, (
                "Every route must have more than 3 position detectors "
                "in its layout"
            )
            assert result == result_lambda, (
                "Filtering with a classic function and a lambda function"
                "should produce the same result"
            )
            ```
        """
        routes = self._routes
        if constraint is not None:
            routes = set(filter(constraint, routes))
        if as_dict:
            return {route.name: route for route in routes}
        return list(routes)

    def _get_route(self, route: str | Route) -> Route:
        """
        This method's main purpose is to validate the `route` argument
        and retrieve the `Route` object corresponding to it. It may be
        used as a helper method in other methods.

        It ensures that:

        - if a `Route` object is provided, this object is present in
        this `PassageGenerator` instance `_routes` list.

        - if a string route name is provided, a `Route` object with this
        name is present in this `PassageGenerator` instance `_routes` list.

        - if the `route` argument is of any other type, an exception
        is raised.

        Args:
            route (str | Route): A route name or a `Route` object.

        Returns:
            Route: The `Route` object corresponding to the passed
            `route` parameter.

        Raises:
            UnknownRouteError: If the `route` argument does not correspond to
            any registered `Route` object.
            TypeError: If the `route` argument is not of type `str` or `Route`.
        """
        if isinstance(route, Route):
            if route in self._routes:
                return route
            else:
                raise UnknownRouteError(
                    f'Unknown Route object "{route.name}". '
                    f'Register the route with the "add_route" method.'
                    )
        if not isinstance(route, str):
            raise TypeError(
                f'Invalid "route" argument {route} of type "{type(route)}" '
                f'(expected type "str" or type "Route").'
                )
        routes = self.get_routes(as_dict=True)
        # routes is a dict if "get_route" is called with as_dict=True,
        # which it should be by default, so this is to make mypy happy
        assert isinstance(routes, dict), "routes must be a dict here"
        try:
            return routes[route]
        except KeyError as err:
            raise UnknownRouteError(
                f'Unknown route "{route}". '
                f'Register the route with the "add_route" method.'
                ) from err

    def _get_route_batch(
        self, routes: typing.Iterable[str | Route | typing.Iterable]
    ) -> list[Route]:
        """
        Retrieve a batch of `Route` objects from a given iterable object of
        route names, `Route` objects, or a mixture including iterables of
        the mentioned types. This method runs recursively and uses `_get_route`
        to validate each individual route.

        Args:
            routes (Iterable): An iterable (such as set, list, or tuple) that
            may contain route names, `Route` objects, or other iterables
            with a mix of both.

        Returns:
            list[Route]: A flat list of corresponding `Route` objects.

        Raises:
            UnknownRouteError: If the `route` argument does not correspond to
            any registered `Route` object.
            TypeError: If the `route` argument is not of type `str` or `Route`.
        """
        route_objs: list[Route] = []
        for route in routes:
            if isinstance(route, str) or isinstance(route, Route):
                route_objs.append(self._get_route(route))
            elif isinstance(route, typing.Iterable):
                route_objs.extend(self._get_route_batch(route))
            else:
                type_ = type(route).__name__
                raise TypeError(
                    f'Invalid "route" argument {route} of type "{type_}" '
                    f'(expected type "str", "Route", or an iterable).'
                    )
        return route_objs

    def get_route(
        self, route: str, raise_exc_if_not_found: bool = False
    ) -> Route | None:
        """
        Get the `Route` object corresponding to the given route name.

        Args:
            route (str): The name of the route.
            raise_exc_if_not_found (bool): raise `UnknownRouteError`
            if the route is not found. Default is False.

        Returns:
            Route | None: The `Route` object corresponding to the provided
            route name, or None, if the object has not been found and
            `raise_exc_if_not_found` is False.

        Raises:
            TypeError: If the `route` argument is not of type `str`.
            UnknownRouteError: If the route name does not correspond to any
            registered `Route` object, and `raise_exc_if_not_found` is `True`.
        """
        if not isinstance(route, str):
            raise TypeError(
                f'Invalid "route" argument {route} of type "{type(route)}"'
                f'(expected type "str").'
                )
        try:
            return self._get_route(route)
        except UnknownRouteError as err:
            if raise_exc_if_not_found:
                raise err
            else:
                return None

    def add_route(self, route: Route, allow_overwrite: bool = False):
        """
        Add a `Route` object to the registered routes and
        assign a `Tram` object to it.

        If a route with the same name is already registered, the method
        will either raise an exception or overwrite the existing
        route based on the value of the `allow_overwrite` parameter.

        Args:
            route (Route): The `Route` object to be registered.
            allow_overwrite (bool, optional): If set to `True`, allows
            overwriting an existing route with the same name.
            Defaults to `False`.

        Raises:
            TypeError: If the `route` argument is of invalid type.
            RouteAlreadyRegisteredError: If a route with the same name already
            exists and `allow_overwrite` is set to `False`.
        """
        if not isinstance(route, Route):
            raise TypeError(
                f'Invalid "route" argument {route} of type "{type(route)}" '
                f'(expected type "Route").'
                )
        if route.name in [r.name for r in self._routes]:
            if allow_overwrite:
                self.delete_route(route.name)
            else:
                raise RouteAlreadyRegisteredError(
                    f'A Route object with name "{route.name}" is already '
                    f'registered. Set "allow_overwrite=True" to overwrite it.'
                    )
        self._routes.add(route)
        tram = Tram()
        tram.route = route
        self._route_tram_pairs[route.name] = tram

    def delete_route(
        self, route: str | Route, raise_exc_if_not_found: bool = False
    ) -> None:
        """
        Ungerister a `Route` object and the `Tram` object assigned to it.

        Args:
            route (str | Route): The name of the route or the `Route` object
            itself.
            raise_exc_if_not_found (bool, optional): If set to `True`, raises
            an exception if the route is not found. Defaults to `False`.

        Raises:
            TypeError: If the provided `route` is neither a string nor
            a `Route` object.
            UnknownRouteError: If the route is not found and
            `raise_exc_if_not_found` is set to `True`.
        """
        try:
            route_obj = self._get_route(route)
            self._routes.remove(route_obj)  # raises ValueError if not found
            self._route_tram_pairs.pop(route_obj.name)  # raises KeyError
        except (KeyError, ValueError, UnknownRouteError):
            if raise_exc_if_not_found:
                raise UnknownRouteError(
                    f'Route "{route}" has not been found '
                    f'among the registered routes.'
                    )

    def set_tram(self, route: str | Route, tram: Tram):
        """
        Assing a custom tram to a route.

        Args:
            route (str | Route): A route to assing the tram to.
            tram (Tram): A custom tram.

        Raises:
            ValueError: if the `tram` argument type is invalid.
            UnknownRouteError: If the `route` argument does not correspond to
            any registered `Route` object.
            TypeError: If the `route` argument is not of type `str` or `Route`.
        """
        if not isinstance(tram, Tram):
            raise ValueError(
                f'Invalid "tram" parameter of type "{type(tram).__name__}". '
                f'Expected a "Tram" object or a "TramParams" object'
                )
        route = self._get_route(route)
        tram.route = route
        self._route_tram_pairs[route.name] = tram

    def get_tram(
        self, route: str | Route, raise_exc_if_not_found: bool = False
    ) -> Tram | None:
        """
        Get the tram assosiated with a route.

        Args:
            route (str | Route): A route to get the tram for.
            tram (Tram | None): the tram. If the route is not paired with
            any tram, returns None.

        Raises:
            UnknownRouteError: If the `route` argument does not correspond to
            any registered `Route` object.
            TypeError: If the `route` argument is not of type `str` or `Route`.
        """
        try:
            route = self._get_route(route)
        except UnknownRouteError as err:
            if raise_exc_if_not_found:
                raise err
            else:
                return None
        try:
            return self._route_tram_pairs[route.name]
        except KeyError as err:
            if raise_exc_if_not_found:
                raise TramNotSetError(
                    f'Route {route.name} does not have an assigned tram.'
                    ) from err
            else:
                return None

    def get_route_permutations(
        self,
        combo_size: int = 2,
        constraint: typing.Callable[[tuple[Route, ...]], bool] | None = None
    ) -> list[tuple[Route, ...]]:
        """
        Get all permutations of Route objects of a given size,
        filtered by a constraint function.

        This method returns all permutations of Route objects in the form of
        tuples. The length of each permutation tuple is equal to the
        `combo_size`.

        A constraint function can be provided to filter out permutations based
        on custom logic. The constraint function should take in a single
        argument, which is a tuple of Route objects, and return a boolean.
        Permutations, for which the constraint function returns True, are
        included in the result.

        Args:
            combo_size (int): The size of each Route permutation tuple.
            Defaults to 2.
            constraint (Callable[[tuple[Route, ...]], bool], optional):
            A function that takes a tuple of Route objects and returns
            a boolean. If provided, this function is used to filter
            the permutations. Defaults to None, in which case all permutations
            are included.

        Returns:
            list[tuple[Route, ...]]: A list of tuples, where each tuple is
            a permutation of Route objects that meet the specified constraint.

        Example:
            ```python
            # assume a PassageGenerator instance is initialized
            # with a list of Route objects
            routes: list[Route]
            passage_generator = PassageGenerator(routes)

            # Define a constraint function that checks if
            # at least one Route in the route permutation is Route R01
            def one_is_R01(route_combo: tuple[Route, ...]):
                for r in route_combo:
                    if r.name == "R01":
                        return True
                return False

            # Get the route pairs with one route in the pair being R01.
            # Note that the constraint is not called by the user in the
            # "get_route_permutations" call!
            result = passage_generator.get_route_permutations(
                combo_size=2,
                constraint=one_is_R01
                )

            # Get the same result
            # with the same constraint defined as a lambda expession
            result_lambda = passage_generator.get_route_permutations(
                combo_size=2,
                constraint=lambda perm: any(r.name == "R01" for r in perm)
                )

            # Check the results are as expected
            assert_one_is_R01(result: list[tuple[Route, ...]]):
                for perm in result:
                    assert one_is_R01(perm) is True, (
                        "One of the Routes in the permutation must be R01"
                    )
                return True

            assert length_greater_than_20(result) is True, (
                "Every route permutation must contain Route R01"
            )
            assert result == result_lambda, (
                "Filtering with a classic function and a lambda function"
                "should produce the same result"
                )
            ```
        """
        all_combinations = itertools.permutations(self._routes, combo_size)
        if constraint is not None:
            return list(filter(constraint, all_combinations))
        else:
            return list(all_combinations)
