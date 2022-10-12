import pytest

from pacecalc import (
    distance_str_to_km,
    time_str_to_minutes,
    pace_str_to_multiplier,
    create_message,
    minutes_to_time,
)


class TestUnits:
    def test_distance_str_to_km(self):
        # the different units
        assert distance_str_to_km("0mi") == 0.0
        assert distance_str_to_km("1mi") == 1.609344
        assert distance_str_to_km("1000m") == 1
        assert distance_str_to_km("1km") == 1
        assert distance_str_to_km("123k") == 123
        assert distance_str_to_km("123") == 123

        # inputs with decimal point
        assert distance_str_to_km("1.0mi") == 1.609344
        assert distance_str_to_km("99.99mi") == 160.91830656
        assert distance_str_to_km(".5mi") == 0.804672

        # set distances
        assert distance_str_to_km("m") == 42.195
        assert distance_str_to_km("hm") == 21.0975

        with pytest.raises(ValueError):
            distance_str_to_km("mi")

    def test_time_str_to_minutes(self):
        assert time_str_to_minutes("00:00") == 0
        assert time_str_to_minutes("00:30") == 0.5
        assert time_str_to_minutes("01:00") == 1
        assert time_str_to_minutes("01:00:00") == 60
        assert time_str_to_minutes("1:1:6") == 61.1
        assert time_str_to_minutes("24:01:00") == 1441

    def test_pace_str_to_multiplier(self):
        assert pace_str_to_multiplier("00:00") == 0
        assert pace_str_to_multiplier("00:30") == 0.5
        assert pace_str_to_multiplier("04:30") == 4.5
        assert pace_str_to_multiplier("4:30") == 4.5

    def test_minutes_to_time(self):
        assert minutes_to_time(0.0, False) == "0:00"
        assert minutes_to_time(0.33, False) == "0:20"

        assert minutes_to_time(6.00, False) == "6:00"
        assert minutes_to_time(6.00, True) == "6:00"

        assert minutes_to_time(6.25, False) == "6:15"
        assert minutes_to_time(6.25, True) == "6:15"

        assert minutes_to_time(60.0, False) == "60:00"
        assert minutes_to_time(60.0, True) == "1:00:00"


def pace_message(pace):
    return f"{pace}min/km"


def distance_message(distance):
    return f"{distance}km"


def time_message(time):
    return time


class TestMessagesFromInput:
    def test_calculate_pace(self):
        assert create_message("10k", "in", "1:00:00") == pace_message("6:00")
        assert create_message("10Km", "in", "1:00:00") == pace_message("6:00")
        assert create_message("10KM", "in", "1:00:00") == pace_message("6:00")

    def test_calculate_distance(self):
        assert create_message("1:00:00", "at", "6:00") == distance_message("10")
        assert create_message("57:00", "at", "6:00") == distance_message("9.5")

    def test_calculate_time(self):
        assert create_message("10k", "at", "6:00") == time_message("1:00:00")
        assert create_message("1.6k", "at", "6:00") == time_message("9:36")
