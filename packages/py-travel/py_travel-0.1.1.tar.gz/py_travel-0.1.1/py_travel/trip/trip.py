from datetime import datetime, date, timedelta
from typing import Tuple, List, Dict, Any

from py_travel.exceptions import ClientNotInitializedError, TravelWarnings, InvalidResponseError
from py_travel.location import Location, input_to_location
from py_travel.utils import meters_to_miles, get_distance, get_duration, get_steps, calculate_stage_steps
from .trip_config import TripConfig
from .stop import Stop


class Trip:
    """
    Trip class

    Attributes:
        client: Client object for the Google Maps API calls
        origin: Origin of the trip
        destination: Destination of the trip
        departure_date: Start date of the trip
        arrival_date: End date of the trip
        stops: List of stops associated with the trip
        updated: Boolean indicating if the object needs to call the Google Maps API to get the results
        api_response: Raw Google Maps API response
    """

    client: Any = None

    def __init__(
        self,
        origin: Tuple[float, float] | str | Location,
        destination: Tuple[float, float] | str | Location,
        stops: List[Tuple[Tuple[float, float] | str | Location, datetime]] = None,
        departure_date: datetime = None,
        arrival_date: datetime = None,
        config: TripConfig = None,
    ) -> None:
        """
        Initialize Trip object

        :param origin: Origin of the trip in pair (latitude, longitude) or address or Location object
        :param destination: Destination of the trip in pair (latitude, longitude) or address or Location object
        :param stops: A list of tuples containing the stop location (either a tuple containing the coordinates, the
            address or a Location object) and the departure date from the stop
        :param departure_date: Start date of the trip (optional)
        :param arrival_date: End date of the trip (optional)
        :param config: Trip configuration either as a dictionary or as a TripConfig object (optional)
        """

        self.__origin = input_to_location(origin)
        self.__destination = input_to_location(destination)

        self.__stops = (
            [Stop(input_to_location(loc), dep_date) for loc, dep_date in stops]
            if stops
            else []
        )
        self.__stops.sort(key=lambda stop: stop.departure_date)

        self.__departure_date = departure_date
        self.__arrival_date = arrival_date

        self.__config = config if config else {}

        self.__api_response: Dict = {}
        self.__updated = True

    @property
    def origin(self) -> Location:
        """
        :return: The origin location of the trip
        """
        return self.__origin

    @origin.setter
    def origin(self, new_origin: Tuple[float, float] | str | Location) -> None:
        """
        Sets the origin location of the trip

        Warning: This will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param new_origin: Origin of the trip in pair (latitude, longitude), string with address or Location object
        """
        self.__origin = input_to_location(new_origin)
        self.__updated = True

    @property
    def destination(self) -> Location:
        """
        :return: The destination location of the trip
        """
        return self.__destination

    @destination.setter
    def destination(
        self, new_destination: Tuple[float, float] | str | Location
    ) -> None:
        """
        Sets the destination location of the trip

        Warning: This will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param new_destination: Destination of the trip in pair (latitude, longitude), string with address or Location
            object
        """
        self.__destination = input_to_location(new_destination)
        self.__updated = True

    @property
    def stops(self) -> List[Stop]:
        """
        :return: The list of stops
        """
        return self.__stops

    @stops.setter
    def stops(
        self, stops: List[Tuple[Tuple[float, float] | str | Location, datetime]] | List[Stop]
    ) -> None:
        """
        Sets the stops for the trip

        Warning: This will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param stops: A list of tuples containing the stop location (either a tuple containing the coordinates, the
            address or a Location object) and the departure date from the stop, or a list of Stop objects
        """

        self.__stops = []
        for stop in stops:
            if isinstance(stop, Stop):
                self.__stops.append(stop)
            else:
                self.__stops.append(Stop(input_to_location(stop[0]), stop[1]))

        self.__stops.sort(key=lambda s: s.departure_date)
        self.__updated = True

    @property
    def departure_date(self) -> datetime:
        """
        :return: The departure date of the trip
        """
        return self.__departure_date

    @departure_date.setter
    def departure_date(self, new_departure_date: datetime) -> None:
        """
        Sets the departure date of the trip

        Warning: This will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param new_departure_date: The departure date of the trip
        """
        self.__departure_date = new_departure_date
        self.__updated = True

    @property
    def arrival_date(self) -> datetime:
        """
        :return: The arrival date of the trip
        """
        return self.__arrival_date

    @arrival_date.setter
    def arrival_date(self, new_arrival_date: datetime) -> None:
        """
        Sets the arrival date of the trip

        Warning: This will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param new_arrival_date: The arrival date of the trip
        """
        self.__arrival_date = new_arrival_date
        self.__updated = True

    @property
    def config(self) -> TripConfig:
        """
        :return: The configuration parameters of the trip
        """
        return self.__config

    @config.setter
    def config(self, new_config: TripConfig) -> None:
        """
        Set the configuration for the calculations

        Warning: This method will mark the trip as updated, possibly causing calls to the Google Maps API in the future.

        :param new_config: Trip configuration
        """

        self.__config = new_config
        self.__updated = True

    @property
    def api_response(self) -> Dict:
        """
        :return: The response from the Google Maps API
        """
        return self.__api_response

    @property
    def distance(self) -> float:
        """
        Warning: If the trip is marked as updated, it will first calculate the trip
        :return: The total distance of the trip in the unit given in the config ('metric' if not configured).
        """

        if self.__updated:
            self.calculate_trip()

        if self.__stops:
            meters = sum(get_distance(stage) for stage in self.__api_response.values())
        else:
            meters = get_distance(self.__api_response)

        return (
            meters / 1000
            if self.__config.get("units", "metric") == "metric"
            else meters_to_miles(meters)
        )

    @property
    def seconds(self) -> int:
        """
        Warning: If the trip is marked as updated, it will first calculate the trip
        :return: The amount of seconds travelled in the trip
        """

        if self.__updated:
            self.calculate_trip()

        if self.__stops:
            seconds = sum(get_duration(stage) for stage in self.__api_response.values())
        else:
            seconds = get_duration(self.__api_response)

        return seconds

    @property
    def days(self) -> int:
        """
        Warning: If the trip is marked as updated, it will first calculate the trip
        :return: Duration in days of the trip (rounded up)
        """

        if self.__updated:
            self.calculate_trip()  # This will call update_dates()

        return (self.__arrival_date.date() - self.__departure_date.date()).days + 1

    @property
    def stages_distances(self) -> List[float]:
        """
        Returns the distances between the locations of the trip in a list starting from origin - 1st stop and ending
        with last stop - destination. If the trip does not contain stops, the list will be of size 1.

        Warning: If the trip is marked as updated, it will first calculate the trip

        :return: A list of distances between the locations of the trip in order
        """

        if self.__updated:
            self.calculate_trip()

        distances: List[float] = []
        if self.__stops:
            for stage in self.__api_response.values():
                stage_meters = (
                    stage.get("legs", [{}])[0].get("distance", {}).get("value", None)
                )
                if not stage_meters:
                    raise InvalidResponseError("legs[0].distance.value")

                distances.append(stage_meters)
        else:
            meters = (
                self.__api_response.get("legs", [{}])[0]
                .get("distance", {})
                .get("value", None)
            )
            if not meters:
                raise InvalidResponseError("legs[0].distance.value")
            distances.append(meters)

        return [
            (
                distance / 1000
                if self.__config.get("units", "metric") == "metric"
                else meters_to_miles(distance)
            )
            for distance in distances
        ]

    @property
    def stages_seconds(self) -> List[int]:
        """
        Returns the seconds travelled between the locations of the trip in a list starting from origin - 1st stop and
        ending last stop - destination. If the trip does not contain stops, the list will be of size 1.

        Warning: If the trip is marked as updated, it will first calculate the trip

        :return: A list of seconds between the locations of the trip in order
        """

        if self.__updated:
            self.calculate_trip()

        seconds: List[int] = []
        if self.__stops:
            for stage in self.__api_response.values():
                stage_seconds = (
                    stage.get("legs", [{}])[0].get("duration", {}).get("value", None)
                )
                if not stage_seconds:
                    raise InvalidResponseError("legs[0].duration.value")

                seconds.append(stage_seconds)
        else:
            seconds_trip = (
                self.__api_response.get("legs", [{}])[0]
                .get("duration", {})
                .get("value", None)
            )
            if not seconds_trip:
                raise InvalidResponseError("legs[0].duration.value")
            seconds.append(seconds_trip)

        return seconds

    @property
    def trip_calendar(self) -> List[Tuple[date, float]]:
        """
        Creates a list of pairs day-distance travelled from the trip.

        Because the Google Maps API does not provide exact data for this calculation, the distances travelled will be
        an estimation.

        Warning: If the trip is marked as updated, it will first calculate the trip

        :return: A list of pairs day-distance travelled in the unit given in the config ('metric' if not configured).
        """

        if self.__updated:
            self.calculate_trip()

        # Create calendar
        calendar = {
            self.__departure_date.date() + timedelta(days=i): 0.0
            for i in range(self.days)
        }

        # Calculate kms travelled per day
        if self.__stops:
            current_date = self.__departure_date
            for index, stage in enumerate(self.__api_response.values()):
                steps = get_steps(stage)
                calendar = calculate_stage_steps(steps, current_date, calendar)
                current_date = self.__stops[index].departure_date if index < len(self.__stops) else None  # :)

        else:
            steps = get_steps(self.__api_response)
            calendar = calculate_stage_steps(steps, self.__departure_date, calendar)

        return [
            (
                day,
                meters / 1000 if self.__config.get("units", "metric") == "metric" else meters_to_miles(meters)
            )
            for day, meters in calendar.items() if meters > 0
        ]

    @classmethod
    def set_client(cls, client: Any) -> None:
        """
        Initializes the client for the directions request

        :param client: A client object. Must contain a method called 'directions' that returns the raw Google Maps
            Directions API response and takes the following parameters: origin, destination, mode, avoid, units,
            departure_time, arrival_time, transit_mode, transit_routing_preference and traffic_model
        """

        cls.client = client

    def calculate_trip(self, trip_config: TripConfig = None) -> Dict:
        """
        Calls the Google Maps API to calculate the trip, only if the trip needs to be updated.

        This method will make at least one call to the Google Maps API and at most 1 + the number of stops.

        :param trip_config: Trip configuration
        :return: The raw API response if no stops are provided, otherwise a dictionary with the raw API responses
        :raises ClientNotInitializedError: If the googlemaps client is not initialized
        :raises TripWarning: If a trip attribute is ignored based on the config given
        """

        if trip_config:
            self.config = trip_config

        if not self.__updated:
            return self.__api_response

        if not self.client:
            raise ClientNotInitializedError()

        if self.__arrival_date and self.__stops:
            TravelWarnings.ignore_field("arrival_date", "Ignored for trips with stops")
        elif (
            self.__arrival_date
            and not self.__config.get("mode", "not_configured") == "transit"
        ):
            TravelWarnings.ignore_field("arrival_date", "Only used for transit mode")

        # Make calls to the API
        if self.__stops:
            current_location = self.__origin.get_data()
            current_date = (
                self.__departure_date if self.__departure_date else datetime.now()
            )  # Fixes HTTP 400 error

            # Call for each stop
            for index, stop in enumerate(self.__stops):
                key = f"stage_{index}" if index > 0 else "departure"

                self.__api_response[key] = self.client.directions(
                    origin=current_location,
                    destination=stop.location.get_data(),
                    departure_time=current_date,
                    **self.__config,
                )[0]

                current_location = stop.location.get_data()
                current_date = stop.departure_date

            # Call for last stage of the trip
            self.__api_response["arrival"] = self.client.directions(
                origin=current_location,
                destination=self.__destination.get_data(),
                departure_time=current_date,
                **self.__config,
            )[0]

        else:
            # Date argument depending on the given fields and configuration
            if self.__departure_date:
                date_argument = {"departure_time": self.__departure_date}
            elif (
                self.__arrival_date
                and self.__config.get("mode", "not_configured") == "transit"
            ):
                date_argument = {"arrival_time": self.__arrival_date}
            else:
                date_argument = {
                    "departure_time": datetime.now()
                }  # Fixes HTTP 400 error

            self.__api_response = self.client.directions(
                origin=self.__origin.get_data(),
                destination=self.__destination.get_data(),
                **date_argument,
                **self.__config,
            )[0]

        self.__updated = False
        self.update_dates()  # Update dates
        return self.__api_response

    def update_dates(self) -> None:
        """
        Checks the given dates make sense and updates the ones that don't. If both departure and arrival dates are
        found, departure date has preference for conflict resolution.

        Warning: If the trip is marked as updated, it will first calculate the trip
        """

        if self.__updated:
            self.calculate_trip()

        travel_times = self.stages_seconds

        # Check departure date
        if not self.__departure_date and not self.__arrival_date:
            self.__departure_date = datetime.now()
            TravelWarnings.update_date("departure", "No departure date provided")
        elif not self.__departure_date:
            if not self.__stops:
                self.__departure_date = self.__arrival_date - timedelta(
                    seconds=travel_times[0]
                )
            else:
                self.__departure_date = self.__stops[0].departure_date - timedelta(
                    seconds=travel_times[0]
                )
            TravelWarnings.update_date("departure", "No departure date provided")

        # Check stop dates
        if self.__stops:
            current_date = self.__departure_date
            for index, stop in enumerate(self.__stops):
                stop_arrival = current_date + timedelta(seconds=travel_times[index])
                if stop.departure_date < stop_arrival:
                    TravelWarnings.update_date(
                        "stop", "Calculated arrival before departure date"
                    )
                    self.__stops[index] = Stop(stop.location, stop_arrival)
                    current_date = stop_arrival
                else:
                    current_date = stop.departure_date

        # Check arrival date
        if not self.__stops:
            new_arrival = self.__departure_date + timedelta(seconds=travel_times[0])
        else:
            new_arrival = self.__stops[-1].departure_date + timedelta(
                seconds=travel_times[-1]
            )

        if not self.__arrival_date:
            self.__arrival_date = new_arrival
            TravelWarnings.update_date("arrival", "No arrival date provided")
        elif self.__arrival_date != new_arrival:
            self.__arrival_date = new_arrival
            TravelWarnings.update_date("arrival", "Calculated arrival does not match")
