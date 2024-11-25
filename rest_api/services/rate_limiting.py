from ..utils import SingletonMeta
from collections import defaultdict
from abc import ABC, abstractmethod
import time


class RateLimitTracker(ABC):

    @abstractmethod
    def attempt(self) -> bool:
        pass


class RateLimitTrackerFactory(ABC):

    @abstractmethod
    def create_tracker(self) -> RateLimitTracker:
        pass


class TimeRateLimitTracker(RateLimitTracker):
    """
    Track the abusive usage of a resource in time. The attempt function
    tells to the client, if his usage of the resource is abusive or not.
    """

    def __init__(self, max_limit_in_second, max_usage_per_second):
        self._time_scope_in_sec = max_limit_in_second
        self._max_usage_in_scope_per_sec = max_usage_per_second
        self._nbr_usage_in_scope = 0
        self._start_time_in_scope = time.time()

    def attempt(self) -> bool:
        # Check if the time scope has been reach to reset the
        # usage counter.
        if (time.time() - self._start_time_in_scope) > self._time_scope_in_sec:
            self._start_time_in_scope = time.time()
            self._nbr_usage_in_scope = 0

        self._nbr_usage_in_scope += 1
        return self._nbr_usage_in_scope <= (
            self._time_scope_in_sec * self._max_usage_in_scope_per_sec
        )


class TimeRateLimitTrackerFactory(RateLimitTrackerFactory):

    _max_limit_in_second: int
    _max_usage_per_second: int

    def __init__(self, max_limit_in_second, max_usage_per_second):
        self._max_limit_in_second = max_limit_in_second
        self._max_usage_per_second = max_usage_per_second

    def create_tracker(self) -> RateLimitTracker:
        return TimeRateLimitTracker(
            self._max_limit_in_second, self._max_usage_per_second
        )


class RateLimitService:
    """
    Manages rate limit's tracker for each user encountered
    """

    _tracked_users: defaultdict

    def __init__(self, factory: RateLimitTrackerFactory):
        self._tracked_users = defaultdict(factory.create_tracker)

    def get_tracked_user(self, id: str) -> RateLimitTracker:
        return self._tracked_users[id]
