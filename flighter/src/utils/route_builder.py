from datetime import timedelta

from src.schemas.flight import FlightSchema, RouteSchema


class RouteBuilder:
    MIN_FLIGHT_DURATION = timedelta(hours=1)
    MAX_FLIGHT_DURATION = timedelta(hours=6)

    MIN_CONNECTION_TIME = timedelta(hours=1)
    MAX_CONNECTION_TIME = timedelta(hours=6)

    MAX_TRANSFERS = 2
    MAX_FLIGHTS = MAX_TRANSFERS + 1
    MAX_ROUTES = 20

    def build(
        self,
        flights: list[FlightSchema],
        origin: str,
        destination: str,
    ) -> list[RouteSchema]:
        flights_by_origin = self._group_flights_by_origin(flights)

        routes = self._find_routes(
            flights_by_origin=flights_by_origin,
            origin=origin,
            destination=destination,
        )

        routes.sort(key=lambda route: route.total_price)

        return routes[:self.MAX_ROUTES]


    def _find_routes(
        self,
        flights_by_origin: dict[str, list[FlightSchema]],
        origin: str,
        destination: str,
    ) -> list[RouteSchema]:
        routes: list[RouteSchema] = []

        stack: list[tuple[list[FlightSchema], set[str]]] = [
            ([], {origin}),
        ]

        while stack:
            route_flights, visited_airports = stack.pop()

            current_airport = (
                route_flights[-1].destination
                if route_flights
                else origin
            )

            if current_airport == destination:
                routes.append(
                    RouteSchema(
                        flights=route_flights,
                        total_price=sum(flight.price for flight in route_flights),
                    )
                )
                continue

            if len(route_flights) >= self.MAX_FLIGHTS:
                continue

            for flight in flights_by_origin.get(current_airport, []):
                if flight.destination in visited_airports:
                    continue

                if route_flights:
                    previous_flight = route_flights[-1]
                    connection_time = (
                        flight.departure_time - previous_flight.arrival_time
                    )

                    if not (
                        self.MIN_CONNECTION_TIME
                        <= connection_time
                        <= self.MAX_CONNECTION_TIME
                    ):
                        continue

                stack.append(
                    (
                        [*route_flights, flight],
                        visited_airports | {flight.destination},
                    )
                )

        return routes

    def _group_flights_by_origin(
        self,
        flights: list[FlightSchema],
    ) -> dict[str, list[FlightSchema]]:
        flights_by_origin: dict[str, list[FlightSchema]] = {}

        for flight in flights:
            duration = flight.arrival_time - flight.departure_time

            if not self.MIN_FLIGHT_DURATION <= duration <= self.MAX_FLIGHT_DURATION:
                continue

            flights_by_origin.setdefault(flight.origin, []).append(flight)

        for airport_flights in flights_by_origin.values():
            airport_flights.sort(key=lambda flight: flight.departure_time)

        return flights_by_origin
