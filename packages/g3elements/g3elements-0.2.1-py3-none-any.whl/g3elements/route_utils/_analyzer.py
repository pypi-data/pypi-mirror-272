import typing

from dataclasses import dataclass

from ._manager import RouteManager, TramNotSetError
from ._tram import Tram
from .._elements import (
    Crossing,
    Detector,
    ElementABC,
    Gate,
    PointMachine,
    Route,
    RouteLayoutDetector,
    RouteLayoutElement,
    _RouteLayoutElement,
)


@dataclass
class GateQueueItem:
    """
    Represents a route awaiting in the queue at a gate.

    Attributes:
        route (Route): A route that is awaiting for a passage.

        queue_number (int): the number of this route in the gate queue (i.e.,
        there are `queue_number-1` routes in the queue before this route).

        waiting_time (float): total (cumulative) time before the route may
        pass. It includes the time before the trigger detector, that allows
        this route to start the passage, is released, and the time before
        the trigger detectors of all active routes, that this route is awaiting
        before it starts the passage, has been released, too. Example:
        Route R1 is active immediately, so its waiting_time is 0. Route R2
        is active after DET01 is passed by R1, which takes 10 s, so R2's
        waiting time is 10 s. Finally, Route R3 is active after DET01
        is passed by R2, which takes another 10 s. R3's total waiting time is
        10 s + 10 s = 20 s.

        trigger_detector (RouteLayoutDetector | None): the detector that must
        be released before this route may be passed. Such a detector usually
        releases the last common layout element shared between this route and
        some route that has started being passed before it.

        last_detector_to_release (RouteLayoutDetector): the last detector that
        should be occupied and subsequently released during the passage.
        By default, this is the last detector in the route layout. However,
        this value may change to the furthest-from-the-startgate detector
        that triggers the passage of any other route,
        if the route is truncated in the passage scenario.
    """
    route: Route
    queue_number: int = 0
    waiting_time: float = 0.0
    trigger_detector: RouteLayoutDetector | None = None
    last_detector_to_release: RouteLayoutDetector | None = None

    def __post_init__(self):
        self.last_detector_to_release = self.route.layout[-1]

    @property
    def gate(self):
        """A gate, where the route is awaiting in a queue for a passage."""
        return self.route.layout.entry_gate

    def reset_estimations(self):
        self.trigger_detector = None
        self.waiting_time = 0.0


@dataclass
class DetectorEvent:
    """
    Represents an occupation event or a release event of a position detector
    as an element of a route layout.

    Args:
        detector (RouteLayoutDetector): The detector area which is occupied or
        released.
        action (bool): The type of the event (True means the detector area
        is occupied, False means it is released).
        time (float): The time (is seconds) when this event happens
        relative to the start of the tram movement.
    """
    detector: RouteLayoutDetector
    action: bool
    time: float


class RouteAnalyzer:
    def __init__(
        self, *routes: Route | typing.Iterable[Route | typing.Iterable]
    ) -> None:
        self._route_manager = RouteManager(routes)

    def _eval_predicate_for_route_layout(
        self,
        route: str | Route,
        compare_with: typing.Iterable[str | Route],
        predicate: typing.Callable[[set, set], bool],
        exit_on_value: bool,
    ) -> bool:
        """
        Implements base logic for evaluating predicates on route layouts.
        and is utilized for the following methods:
        - `intersects_at_least_one`;
        - `intersects_every`.

        This function evaluates the predicate function for the combination of
        the given route's layout and the layout of each route in
        the `compare_with` iterable.

        The `predicate` function could be used to perform various evaluations
        of a pair of route layouts, such as whether any of the layouts contains
        a specific element, or whether the layouts share common elements, or
        any other custom condition for the given combination.

        The `exit_on_value` parameter is used to determine the exit condition
        of the function. If the result of the predicate function matches the
        `exit_on_value`, the function returns this value immediately.

        Args:
            route (str | Route): The route, the layout of which is to be
            evaluated. Can be specified as a route name (string) or a Route
            object.
            compare_with (typing.Iterable[str | Route]): The list of other
            routes (specified either by name (strings) or as Route objects).
            The layouts of these routes will be compared with the layout of
            the given route.
            predicate (typing.Callable): A function that takes two sets
            (route layouts) as arguments and returns a boolean indicating
            whether a certain condition is met.
            exit_on_value (bool): The boolean value that causes the method
            to exit early if the predicate returns this value for any layout
            pair.

        Returns:
            bool: The final outcome based on the evaluations of the predicate.
            The function returns as soon as the predicate returns a value
            matching `exit_on_value` for any layout pair. If no such value
            is returned by  the predicate for any pair, the function returns
            the opposite of `exit_on_value`.
        """
        this_route_obj = self._route_manager._get_route(route)
        other_route_objs = self._route_manager._get_route_batch(compare_with)
        if not other_route_objs:
            return False
        this_layout = {element.core for element in this_route_obj.layout}
        for other_route_obj in other_route_objs:
            other_layout = {element.core for element in other_route_obj.layout}
            if predicate(this_layout, other_layout) is exit_on_value:
                return exit_on_value
        return not exit_on_value

    def intersects_at_least_one(
        self, route: str | Route, compare_with: typing.Iterable[str | Route]
    ) -> bool:
        """
        Determine if the given route has any common layout elements with any of
        the other routes that it is compared with.

        Example:
        assume there are three routes with the following layout elements:
        - Route1: A -> B -> C
        - Route2: D -> E -> F
        - Route3: G -> E -> K

        ```python
        intersects_at_least_one(Route1, [Route2, Route3])
        ```
        returns False, because Route1 does not share any elements with
        Route2 or Route3.

        ```python
        intersects_at_least_one(Route3, [Route1, Route2])
        ```
        returns True, because Route3 shares element E with Route2.

        Args:
            route (str | Route): The route to be checked for intersections.
            Can be specified as a route name (string) or a Route object.
            compare_with (typing.Iterable[str | Route]): The list of other
            routes (specified either by name (strings) or as Route objects)
            to check for common layout elements with the given route.

        Raises:
            UnknownRoute: If any of the routes is not registered.
            TypeError: If any of the routes is not of types `str` or `Route`.

        Returns:
            bool: True if the route has common layout elements with at least
            one of the routes it is compared with, False otherwise.
        """
        # How it works ↓  ↓  ↓
        """
        This method utilizes a negation logic in combination with
        using the base "_eval_predicate_for_route_layout" method.

        A step-by-step explanation:
        1. It is computed whether the layout of the given route ("lo1") and
           the layout of another route ("lo2") ARE NOT disjoint by negating
           the result of "lo1.isdisjoint(lo2)" through a lambda expression.
        2. If the condition desc. in (1) IS met for at least one
           combination of the given route and a route from "compare_with",
           the predicate (the lambda expression from (1)) returns True,
           that matches the "exit_on" value. The iteration is stoped, and
           "_eval_predicate_for_route" returns True as an early exit.
        3. The value, returned by "_eval_predicate_for_route", is retured
           right away, as it can be stated that if thje given route intersects
           at least one other route, "intersects_at_least_one" should be True.
        """
        return self._eval_predicate_for_route_layout(
            route,
            compare_with,
            predicate=lambda lo1, lo2: not lo1.isdisjoint(lo2),
            exit_on_value=True
            )  # lo == layout (type(layout) is set)

    def intersects_every(
        self, route: str | Route, compare_with: typing.Iterable[str | Route]
    ) -> bool:
        """
        Determine if the given route has any common layout elements with every
        the other route that it is compared with.

        Example:
        assume there are three routes with the following layout elements:
        - Route1: A -> B -> C
        - Route2: D -> E -> C
        - Route3: G -> E -> K

        ```python
        intersects_at_least_one(Route1, [Route2, Route3])
        ```
        returns False, because even though Route1 shares element C with
        Route02, it does not share any elements with Route3.

        ```python
        intersects_at_least_one(Route2, [Route1, Route3])
        ```
        returns True, because Route2 shares element C with Route01 and
        element E with Route03.

        Args:
            route (str | Route): The route to be checked for intersections.
            Can be specified as a route name (string) or a Route object.
            compare_with (typing.Iterable[str | Route]): The list of other
            routes (specified either by name (strings) or as Route objects)
            to check for common layout elements with the given route.

        Raises:
            UnknownRoute: If any of the routes is not registered.
            TypeError: If any of the routes is not of types `str` or `Route`.

        Returns:
            bool: True if the route has common layout elements with every route
            it is compared with, False otherwise.
        """
        # How it works ↓  ↓  ↓
        """
        This method utilizes a negation logic in combination with
        using the base "_eval_predicate_for_route_layout" method.

        A step-by-step explanation:
        1. It is computed whether the layout of the given route ("lo1") and
           the layout of another route ("lo2") ARE NOT disjoint by negating
           the result of "lo1.isdisjoint(lo2)" through a lambda expression.
        2. If the condition described in (1) IS NOT met for at least one
           combination of the given route and a route from "compare_with",
           the predicate (the lambda expression from (1)) returns False,
           that matches the "exit_on" value. The iteration is stoped, and
           "_eval_predicate_for_route" returns False as an early exit.
        3. The value, returned by "_eval_predicate_for_route", is retured
           right away, as it can be stated that if the given route does not
           intersect at least one other route, "intersects_at_least_one"
           should be False.
        """
        return self._eval_predicate_for_route_layout(
            route,
            compare_with,
            predicate=lambda lo1, lo2: not lo1.isdisjoint(lo2),
            exit_on_value=False
            )  # lo == layout (as a set)

    def _eval_predicate_for_route(
        self,
        *routes: str | Route,
        predicate: typing.Callable[[Route, typing.Iterable[Route]], bool],
        exit_on_value: bool
    ) -> bool:
        """
        This method implements base logic for the following methods:
        - `at_least_one_intersects_at_least_one`;
        - `every_intersects_at_least_one`;
        - `every_intersects_every`.

        It iterates through a given set of routes, and for each route, it
        evaluates a predicate function against the combination of this route
        and the rest of the routes in the set.

        The `predicate` function could be used to perform various evaluations
        of a combination of a route and an iterable of routes, such as whether
        routes intersect each other, have common detector areas, have specific
        length, or any other custom condition for the given combination.

        If the predicate returns the `exit_on_value` for any combination, the
        iteration is terminated, and the method returns the `exit_on_value`.
        If the predicate does not return the `exit_on_value` for any
        combination, the method returns the negation of the `exit_on_value`
        after completing the iteration.

        Args:
            predicate (typing.Callable): A function that takes a route and
            an iterable of routes as arguments and returns a boolean
            indicating whether a certain condition is met.

            exit_on_value (bool): The value of the predicate for which
            the iteration should be terminated early.

            *routes (str | Route): The set of routes to evaluate (to apply
            the predicate function to).

        Returns:
            bool: Returns `exit_on_value` if the condition specified by the
            `predicate` is equal to `exit_on_value` for any single route
            when compared against the rest of the routes in the set. Otherwise,
            it returns the negation of the `exit_on_value`.
        """
        route_objs = self._route_manager._get_route_batch(routes)
        if len(route_objs) < 2:
            return exit_on_value
        for i, route_obj in enumerate(route_objs):
            other_route_objs = route_objs[:i] + route_objs[i+1:]
            if predicate(route_obj, other_route_objs) is exit_on_value:
                return exit_on_value
        return not exit_on_value

    def at_least_one_intersects_at_least_one(
        self, *routes: str | Route
    ) -> bool:
        """
        Determine if at least one route in the given set has common layout
        elements with at least one other route.

        Example:
        assume there are three routes with the following layout elements:
        - Route1: A -> B -> C
        - Route2: D -> E -> F
        - Route3: G -> E -> K

        ```python
        at_least_one_intersects_at_least_one(Route1, Route2, Route3)
        ```
        returns True, because:
        - Route2 shares element E with Route3;

        Args:
            routes (str | Route): Routes to be checked for intersections.
            Can be specified as route names (strings) or Route objects.

        Returns:
            bool: True if at least one route intersects with at least one
            other route, False otherwise.
        """
        # How it works ↓  ↓  ↓
        """
        This method utilizes a double negation logic in combination with
        using the base "_eval_predicate_for_route" method.

        A step-by-step explanation:
        1. For each route ("r"), it is computed whether this route does NOT
           intersect with any of the other routes ("rs") by negating
           the result of "self.intersects_at_least_one(r, rs)"
           through a lambda expression.
        2. If the condition described in (1) is met for any route in
           the given set, it means that this particular route does NOT
           intersect with any other route, or, in other words, the route
           is independent of the others. In this case, the predicate
           (the lambda expression from (1)) returns True, that matches
           the "exit_on" value. The iteration is stoped, and
           "_eval_predicate_for_route" returns True as an early exit.
        3. The outer negation turns this into False, as it can be stated that
           if no route intersects at least one other route,
           "at_least_one_intersects_at_least_one" should be False.
        """
        return not self._eval_predicate_for_route(
            *routes,
            predicate=lambda r, rs: not self.intersects_at_least_one(r, rs),
            exit_on_value=True
            )  # r == route (Route obj), rs == routes (iterable of Route objs)

    def every_intersects_at_least_one(self, *routes: str | Route) -> bool:
        """
        Determine if every route in the given set has common layout
        elements with at least one other route.

        Example:
        assume there are three routes with the following layout elements:
        - Route1: A -> B -> C
        - Route2: D -> E -> C
        - Route3: G -> E -> K

        ```python
        every_intersects_at_least_one(Route1, Route2, Route3)
        ```
        returns True, because:
        - Route1 shares element C with Route2;
        - Route2 shares element E with Route3;

        Args:
            routes (str | Route): Routes to be checked for intersections.
            Can be specified as route names (strings) or Route objects.

        Returns:
            bool: True if every route intersects with at least one
            other route, False otherwise.
        """
        return self._eval_predicate_for_route(
            *routes,
            predicate=self.intersects_at_least_one,
            exit_on_value=False
            )

    def every_intersects_every(self, *routes: str | Route) -> bool:
        """
        Determine if every route in the given set has common layout
        elements with every other route.

        Example:
        assume there are three routes with the following layout elements:
        - Route1: A -> B -> C
        - Route2: D -> E -> C
        - Route3: A -> E -> K

        ```python
        every_intersects_every(Route1, Route2, Route3)
        ```
        returns True, because:
        - Route1 shares element C with Route2 and element A with Route3;
        - Route2 shares element C with Route1 and element E with Route3;
        - Route3 shares element A with Route1 and element E with Route2;

        Args:
            routes (str | Route): Routes to be checked for intersections.
            Can be specified as route names (strings) or Route objects.

        Returns:
            bool: True if every route intersects with every other route,
            False otherwise.
        """
        return self._eval_predicate_for_route(
            *routes,
            predicate=self.intersects_every,
            exit_on_value=False
            )

    def determine_common_layout_elements(
        self, *routes: str | Route
    ) -> set[Detector | PointMachine | Crossing]:
        """
        Determine all common layout elements that the given routes share.

        Args:
            routes (str | Route): A set of routes to be checked to contain
            the common elements. Can be specified as route names (strings)
            or Route objects.

        Example:
        assume there are three routes with the following layout elements:
        - Route1: A -> B -> C
        - Route2: C -> B -> A
        - Route3: D -> B -> C

        ```python
        determine_common_layout_elements(Route1, Route2, Route3)
        ```
        returns True, because:
        - Route1 shares section B -> C with Route3 and section A -> B -> C
        with Route2;
        - Route2 shares section C -> B with Route3;

        Returns:
            set: A set of common layout elements. Note that the set items
            are not the `RouteLayoutElement` objects directly stored in
            the layouts, but their core `ElementABC` objects. Also note that
            the order of the elements in the set is not guaranteed.
            If there are no common elements, an empty set is returned.
        """
        route_objs = self._route_manager._get_route_batch(routes)
        if len(route_objs) < 2:
            return set()
        route_obj = route_objs.pop()
        # init a set to hold the layout elements common for all the routes
        common_layout = {element.core for element in route_obj.layout}
        for route_obj in route_objs:
            another_layout = {element.core for element in route_obj.layout}
            common_layout.intersection_update(another_layout)
        return common_layout

    def share_common_layout_element(
        self,
        *routes: str | Route,
        element: str | ElementABC | RouteLayoutElement | None = None
    ) -> bool:
        """
        Determine if all the given routes share a common layout element.

        Example:
        assume there are three routes with the following layout elements:
        - Route1: A -> B -> C
        - Route2: C -> B -> A
        - Route3: D -> B -> C

        ```python
        share_common_layout_element(R1, R2, R3, element=None)
        ```
        returns True, because there is a common section (B, C) between
        all three routes.

        ```python
        share_common_layout_element(R1, R2, R3, element='A')
        ```
        returns False, because element A is not common for all the routes.

        ```python
        share_common_layout_element(R1, R2, R3, element='B')
        ```
        returns True, because element B is common for all three routes.

        Args:
            routes (str | Route): A set of routes to be checked to share
            a common element. Can be specified as route names (strings)
            or Route objects.
            element (str | ElementABC | RouteLayoutElement | None): The
            specific element to check for. If None, checks if any common
            element is shared by all the given routes.

        Returns:
            bool: True if all routes share a common element, False otherwise.
        """
        common_elements = self.determine_common_layout_elements(*routes)
        if element is None:               # if no specific element is provided,
            return bool(common_elements)  # check if common_layout is non-empty
        if isinstance(element, ElementABC):
            return element in common_elements
        if isinstance(element, _RouteLayoutElement):
            return element.core in common_elements
        if isinstance(element, str):
            return any((element == elem.name for elem in common_elements))
        raise TypeError(
            f'Invalid type of "element" argument: {type(element).__name__}.'
            )

    def determine_trigger_detector(
        self, route: str | Route, next_route: str | Route
    ) -> RouteLayoutDetector | None:
        """
        Determine the detector in an active route (`route`), that, upon
        release, allows an awaiting route (`next_route`) to be set. Typically,
        this detector releases the last shared element between the routes.

        Example: consider route R01 is currenty being passed, and route R02
        is waiting for a passage. These routes share several layout elements
        as depicted below:

        `G01 || === | DET01 | == | PME01 | == | DET02 | == | DET03 | == || G02`

        `G01 || === | DET01 | == | PME01 | == | DET04 | == | DET05 | == || G03`

        Here, the last common layout element shared between the routes is the
        point machine  PME01. Once PME01 is released, we can safely assume that
        all layout elements of R02 are unoccupied, and the route can be set for
        passage. The detector that releases PME01 during the passage of route
        R01, namely DET02, is hence the trigger detector for route R02.

        Args:
            route (str | Route): An active route or a route with a higher
            queue position (a "reference" route). Can be specified as
            a route name (string) or a Route object.
            next_route (str | Route): A route awaiting in queue that
            may be set next after the active route. Can be specified as
            a route name (string) or a Route object.

        Returns:
            RouteLayoutDetector | None: The detector in the active route layout
            that releases the last common element of the routes' layouts.
            If None is returned, it means that the routes share no elements
            and does not depend on each other.

        Raises:
            InvalidRouteLayout: If an element of the route layout is not a
            subtype of "RouteLayoutElement".
        """
        common = self.determine_common_layout_elements(route, next_route)
        if not common:
            return None
        route = self._route_manager._get_route(route)
        last_common_element = None
        last_common_element_index = None
        for element in reversed(route.layout):
            if element.core in common:
                last_common_element = element
                i = route.layout.index(element)
                last_common_element_index = i
                break
        if last_common_element_index is None:  # no common element was found
            return None
        # find the first detector in the layout after the last common element
        while not isinstance(last_common_element, RouteLayoutDetector):
            try:
                last_common_element_index += 1
                last_common_element = route.layout[last_common_element_index]
            except IndexError:
                last_common_element = route.layout[-1]  # last item is detector
                break
        assert isinstance(last_common_element, RouteLayoutDetector)
        return last_common_element

    def _choose_next_route(
        self,
        waiting_routes: list[GateQueueItem],
        active_routes: list[GateQueueItem]
    ) -> GateQueueItem:
        """
        Estimates the route that is likely to be selected next for passage,
        considering the routes already planned for passage.

        This method is utilized for the following methods:
        - `determine_route_order`.

        Example: consider the following passage scenario:
        - Route R01 is currently being passed at gate G01.
        - Route R02 is scheduled for a passage next at gate G02.
        - Routes R03 and R04 are waiting at G01, with R03 having a lower
        queue number than R04.
        - Route R05 is waiting at G02.

        The waiting_routes list would be:

        ```python
        [
            GateQueueItem(route=R03, queue_number=1),
            GateQueueItem(route=R04, queue_number=2),
            GateQueueItem(route=R05, queue_number=1)
        ]
        ```

        And the active_routes list would be:

        ```python
        [
            GateQueueItem(route=R01, delay=0.0),
            GateQueueItem(route=R02, delay=5.0)
        ]
        ```

        First, R04 is removed from the candidates for next route, because
        it physically cannot start before R03 (as reflected by its
        queue_number).

        Then, the waiting times are calculated for R03 and R05.

        Assume R03 could be set after 8.0 s of R01 passage or after 5.0 s of
        R02 passage. However, since R02 by itself starts its passage 5.0 s
        after R01, the total waiting time for R03 regarding to R02 is actually
        10.0 s. And since all the critical points should be passed in both
        R01 and R02, R03 has to wait the longest of those two time periods,
        which is 10.0 s.

        Now assume R05 only depends on R02 and can start its passage 2.0 s
        after its passage has started. The total waiting time for R05 is then
        2.0 + 5.0 = 7.0 s.

        Result: R03 has to wait 10.0 s before it may start the passage, and
        R05 has to wait 7.0 s. The latter is thus chosen as the best candidate
        for the next route to pass. Finally, the selected route is returned
        as the result.

        Args:
            waiting_routes (list[GateQueueItem]): A list of routes queued for
            passage at a gate.

            active_routes (list[GateQueueItem]): A list of routes that are
            are already scheduled for passage. Each `GateQueueItem` object
            if `active_routes` contains its delay (in seconds) relative to
            the first active route.

        Returns:
            GateQueueItem: The next route to be passed, chosen based on the
            following criteria:
            1) Gate queue index: The route with the smallest gate queue index
            is preferred.
            2) Waiting time: Among routes with the same gate queue index, the
            route with the shortest total waiting time is selected.

        Raises:
            TramNotSet: If the tram is not assigned to the active route.
            InvalidRouteLayout: If the trigger detector has an unexpected type.
        """
        # recreate the queue at every gate in waiting_routes items
        gate_queues = sorted(waiting_routes, key=lambda wr: wr.queue_number)
        # prefilter the waiting_routes by picking only the first route
        # in the queue for each gate
        next_routes: list[GateQueueItem] = []
        for wr in gate_queues:  # wr == waiting route
            if any(wr.gate == nr.gate for nr in next_routes):
                continue
            next_routes.append(wr)
        # find the route with the shortest total waiting time
        next_route = None
        for nr in next_routes:  # nr == next route
            for ar in active_routes:  # ar == active route
                trigger = self.determine_trigger_detector(ar.route, nr.route)
                if trigger is None:
                    # The waiting route and the active route do not share
                    # any layout elements and may be set at the same time
                    t = 0.0
                else:
                    # Estimate the time that it takes the tram to get to
                    # the trigger detector and pass though it
                    tram = self._route_manager.get_tram(
                        ar.route, raise_exc_if_not_found=True
                        )
                    assert tram is not None, "tram should not be None here"
                    t = (trigger.end_offset + tram.length) / tram.speed
                waiting_time = t + ar.waiting_time
                if waiting_time >= nr.waiting_time:
                    nr.waiting_time = waiting_time
                    nr.trigger_detector = trigger
            if next_route is None:
                next_route = nr
            elif nr.waiting_time < next_route.waiting_time:
                next_route.reset_estimations()
                next_route = nr
            else:
                nr.reset_estimations()
        assert next_route is not None, "Next route should not be None by now."
        return next_route

    def _determine_last_detector_to_release(
        self,
        route: GateQueueItem,
        triggers: list[RouteLayoutDetector],
        truncate: bool
    ) -> RouteLayoutDetector | None:
        """
        Get the furthest-from-the-startgate detector in the given route layout,
        which is also a trigger detector for some other route. This will be the
        last detector to release during the route passage. If the route is not
        to be truncated, the last detector is the last detetor its layout.

        This method is utilized for the following methods:
        - `determine_route_order`.

        Args:
            route (GateQueueItem): A route to estimate the last detector for.
            triggers (list[RouteLayoutDetector]): Detectors that trigger
            the passage of any route in a passage scenario.

        Returns:
            RouteLayoutDetector: The last detector to be occupied during
            the passage of the given route.
        """
        detectors = route.route.layout.detectors
        if truncate is False:
            return detectors[-1]

        def is_further(det1, det2) -> bool:
            nonlocal detectors
            det1_idx = detectors.index(det1)
            det2_idx = detectors.index(det2)
            return det1_idx > det2_idx

        last_detector = None
        for trigger in triggers:
            if trigger not in detectors:
                continue
            if (last_detector is None) or is_further(trigger, last_detector):
                last_detector = trigger
        return last_detector

    def determine_route_order(
        self,
        *routes: str | Route | typing.Iterable[str | Route],
        truncate: bool = True
    ) -> list[GateQueueItem]:
        """
        Determine the passage order for the given routes.

        The sorting algorithm assumes the routes are set in the optimal way,
        meaning that each requested route is allowed to pass as soon as
        it is possible. The algorithm takes into consideration the initial
        queues at the start gates, intersections of the routes, and
        the geometry of their layouts (specifically, the lengths of the spaces
        between the position detector areas). The routes are concidered to
        be intersecting if they share at least on common layout element.

        Example: consider five routes R01 to R05 are waiting for a passage
        at two start gates G01 and G02. Route R01 starts at gate G01,
        R02 — at G02, R03 — at G01, R04 — at G01, and R05 — at G02.

        The queue at each gate initially looks like this:

        `R04 (3) -- R03 (2) -- R01 (1) | G01 -> --`

        `--- (-) -- R05 (2) -- R02 (1) | G02 -> --`

        `determine_route_order` operates in the following manner:

        1) The routes are initially considered in a waiting list, and
        a list of active routes is empty.
        2) The first route that has been provided (in this case, R01)
        is always selected as the first to pass and is moved to the list
        of active routes.
        3) The next route to pass is determined based on its queue
        position and the waiting time, which is calculated considering
        the intersections of the routes and the geometry of their layouts.
        Since route R01 is already active, there are two routes that may
        pass next: R03 (from G01) and R02 (from G02). If the latter
        is determined to have the shortest waiting time between the two,
        it's selected next and moved to the list of active routes.
        4) The procedure outlined in step (3) is iteratively executed until
        all routes are ordered. With each iteration, the waiting time for each
        each route is recalculated, taking into account the state of
        the active routes during that iteration.
        5) Finally, the method returns the sorted list of active routes, which
        contains the routes in the order they are estimated to pass.

        The returned list may look like this:
        ```python
        [
            GateQueueItem(route=R01, queue_number=1, waiting_time=0.0),
            GateQueueItem(route=R02, queue_number=1, waiting_time=15.0),
            GateQueueItem(route=R05, queue_number=2, waiting_time=27.0),
            GateQueueItem(route=R03, queue_number=2, waiting_time=40.0),
            GateQueueItem(route=R04, queue_number=3, waiting_time=55.0)
        ]
        ```

        This list represents the optimal order in which the routes should
        be passed. In this case, the order is: R01, R02, R05, R03, R04.

        Note: The actual waiting times and the resulting order will depend
        on the specific details of the provided routes and trams.
        The values used in this example are purely illustrative.

        Args:
            routes (str | Route | typing.Iterable[str | Route]):
            The routes that are to be sorted to determine their passage order.

        Returns:
            list[GateQueueItem]: A list, in which the routes are ordered
            in the way that they are estimated to be passed.
        """
        waiting_routes: list[GateQueueItem] = []  # unsorted routes
        active_routes: list[GateQueueItem] = []  # sorted routes
        queue_len: dict[Gate, int] = {}  # number of routes at each gate
        route_objs = self._route_manager._get_route_batch(routes)
        for route in route_objs:
            # the number of the route in the queue at the startgate
            queue_number = queue_len.get(route.layout.entry_gate, -1) + 1
            waiting_routes.append(GateQueueItem(route, queue_number))
            queue_len[route.layout.entry_gate] = queue_number
        # the first route is always chosen as the first active route
        next_route = waiting_routes.pop(0)
        active_routes.append(next_route)
        while waiting_routes:
            next_route = self._choose_next_route(waiting_routes, active_routes)
            waiting_routes.remove(next_route)
            active_routes.append(next_route)
        triggers = [
            ar.trigger_detector for ar in active_routes if ar.trigger_detector
            ]  # every detector that triggers a passage of a route
        for active_route in active_routes:
            last_to_release = self._determine_last_detector_to_release(
                active_route, triggers, truncate
                )
            active_route.last_detector_to_release = last_to_release
        return active_routes

    def _get_event_generation_termination_value(
        self,
        route: Route,
        last_detector_to_release: RouteLayoutDetector | None,
    ) -> int:
        """
        Get the termination value for event generation loop based on the
        `last_detector_to_release` value and the route truncation. Basically,
        the termination value is the index of the detector, the occupation
        of which should be the last generated passage event. For example,
        termination value "1" means that the passage is finished after
        the occupation of the 2nd detector. (Note that indexation starts at 0.)

        If `last_detector_to_release` is None, it is set to the first detector
        in the route layout.

        Example: consider a route layout with two detector areas:
        DET01 and DET02.

        - If the last detector to release is None, 0 is returned, meaning
        the passage will end with the occupation of the 1st route detector;
        - If the last detector is DET01, 1 is returned, meaning the passage
        will end when the 2nd detector (which is DET02) is occupied;
        - If the last detector is DET02, 2 is returned, meaning the passage
        would end when the 3th detector is occupied. However, since there are
        only 2 detectors in the layout, the event generation loop is never
        terminated, and the passage will be finished with the release of DET02.

        This method is utilized for the following methods:
        - `_get_detector_events`.
        """
        if last_detector_to_release is None:
            return 0
        try:
            return route.layout.detectors.index(last_detector_to_release) + 1
        except ValueError:
            return len(route.layout.detectors)

    def _determine_detector_events(
        self,
        route: str | Route,
        last_detector_to_release: RouteLayoutDetector | None,
        tram: Tram | None = None
    ) -> list[DetectorEvent]:
        """
        Estimates the chronological order of occupation and release events of
        the position detectors in the layout of the given route.

        The events are generated up to the occupation of the first detector
        after the last detector to release. If this detector is the last
        detector is the layout, the last event is the release of this detector.
        If the `last_detector_to_release` parameter is None, it is set to
        the first detector in the route's layout, and the last event is
        the occupation of the first detector.

        Args:
            route (str | Route): A route to generate the events for.
            last_detector (RouteLayoutDetector | None): The last detector in
            the route layout to occupy and subsequently release.
            tram (Tram | None): A tram passing through the route.
            If None, a tram, assigned for this route, is used.

        Returns:
            events (list[DetectorEvent): a list, in which the detector
            occupation and release events are ordered in the chronological
            order of the tram passage.
        """
        route = self._route_manager._get_route(route)
        if tram is None:
            tram = self._route_manager.get_tram(route)
        if tram is None:
            raise TramNotSetError(
                f'Tram is not assigned to the route "{route.name}".'
                )
        assert isinstance(tram, Tram), "Tram should be a Tram object here."
        events: list[DetectorEvent] = []
        termination_idx = self._get_event_generation_termination_value(
            route, last_detector_to_release
            )
        for i, detector in enumerate(route.layout.detectors):
            # the front of the tram reaches the start of the detector area
            t_occupy = round(detector.start_offset / tram.speed, 3)
            events.append(DetectorEvent(detector, True, t_occupy))
            if i == termination_idx:
                break
            # the end of the tram leaves the end of the detector area
            total_length = detector.end_offset + tram.length
            t_release = round(total_length / tram.speed, 3)
            events.append(DetectorEvent(detector, False, t_release))
        # sort the event based on the time they happen
        return sorted(events, key=lambda event: event.time)

    def determine_detector_events(
        self,
        route: str | Route,
        tram: Tram | None = None
    ) -> list[DetectorEvent]:
        """
        Estimate the chronological order of occupation and release events of
        the position detectors in the layout of the given route.

        The occupation event happens when the front of a tram reaches
        the start of a detector area. The release event happens when the end
        of the tram leaves this area. It means that it is also necessary
        to take the length of the tham into account during the calculation of
        a release event.

        The events are generated for the full passage of the route, starting
        with the occupation of the first detector in the route layout, and
        finishing with the release of its last detector.

        Example: consider a route R01 that contains two detector areas:
        DET01 and DET02. Assume a tram TR01 with a speed of 5 m/s (18 kh/h)
        and a length of 30 m is passing through this route.

        `R01: == G01 ||=====|DET01|=====|DET02|=====|| G02 ==`

        `= TR01 -> == | 2 m | 8 m | 3 m | 9 m | 1 m | =======`

        In this scenario, the tram:
        - reaches the start of DET01 area at
        `t = ((2 m) / 5 m/s) = 0.4 s`;
        - leaves the end of DET01 area at
        `t = ((2 m + 8 m + 30 m) / 5 m/s) = 8.0 s`;
        - reaches the start of DET02 at
        `t = ((2 m + 8 m + 3 m) / 5 m/s) = 2.6 s`;
        - leaves the end of DET02 area at
        `t = ((2 m + 8 m + 3 m + 9m + 30m) / 5 m/s) = 10.4 s`;

        The resulting sorted list of events would look like this:
        ```python
        events = [
            DetectorEvent("DET01", True, 0.4),
            DetectorEvent("DET02", True, 2.6),
            DetectorEvent("DET01", False, 8.0),
            DetectorEvent("DET02", False, 10.4)
        ]
        ```

        Args:
            route (str | Route): A route to generate the events for.
            Can be specified as a route name (string) or a Route object.
            tram (Tram | None): A tram passing through the route.
            If None, the tram, assigned for this route, is used.

        Returns:
            events (list[DetectorEvent]): a list, in which the detector
            occupation and release events are ordered in the chronological
            order of the tram passage.
        """
        route = self._route_manager._get_route(route)
        return self._determine_detector_events(
            route=route,
            last_detector_to_release=route.layout.detectors[-1],
            tram=tram
            )

    def estimate_passage_duration(
        self, route: str | Route, tram: Tram | None = None
    ) -> float:
        """
        Calculate the time (in seconds) for a tram to fully pass through
        a given route.

        The passage duration is defined as the time from when the front of the
        tram enters the start of the route until the end of the tram leaves the
        end of the route. The tram's length is taken into account, too.

        Example: consider a route R01 with a total length of 23 meters.
        Assume a tram TR01 with a speed of 5 m/s (18 km/h) and
        a length of 30 m is passing through this route.

        `R01: == G01 ||=====|DET01|=====|DET02|=====|| G02 ==`

        `= TR01 -> == | 2 m | 8 m | 3 m | 9 m | 1 m | =======`

        In this scenario, the time it takes the tram to fully pass through
        the route is calculated as follows:

        `t = ((23 m (route length) + 30 m (tram length)) / 5 m/s) = 10.6 s`

        Args:
            route (Route): The route which the tram is passing through.
            tram (Tram | None): A tram passing through the route.
            If None, the tram assigned to this route is used.

        Returns:
            duration (float): The time duration (in seconds) for the tram
            to fully pass through the route. The duration is rounded to
            the nearest millisecond.
        """
        route_obj = self._route_manager._get_route(route)
        tram = self._route_manager.get_tram(
            route, raise_exc_if_not_found=True
            )
        assert tram is not None, "Tram should not be None here."
        return round((route_obj.layout.length + tram.length) / tram.speed, 3)
