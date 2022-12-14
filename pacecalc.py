#! /bin/python3
import argparse
import re


arg_description = """
Pace calculator is a tool that takes two of `pace`, `time` and `distance` as input and gives the third one as output.

Some examples:
`./pacecalc.py 45:00 at 4:40` outputs `11:25km`
`./pacecalc.py marathon in 2:01:09` outputs `2:52min/km`
`./pacecalc.py 15km at 3:23` outputs `50:45min/km`
"""

arg_epilog = """
## Distance inputs
Distance takes a number [n], which can be an integer or a double. The following input formats are accepted:
- `[n]`, `[n]km` or `[n]k` for kilometers.
- `[n]mi` for miles

There are two pre-set distances that are not prepended by a number:
- `m` or `marathon`
- `hm` or `"half marathon"`. This last one needs to be surrounded by quotes.

## Time input
Pace Calculator accepts time input in two different formats: with or without letters.

### Without letters
`H:M:S`. Hours are optional, so `02:03` is 2 minutes and 3 seconds. The numbers can be zero padded, but don't have to be: `01:02:03`, `1:2:3` and `1:02:3` are equivalent.

In fact, you can add as many leading zeros as you like and minutes and seconds can be higher than 60. You can write the previous example as `000000062:03` if you like.

### With letters
To input time with letters, enter a number [n] followed by an h, m or s for hours minutes or seconds respectively. This is the format `[n]h[n]m[n]s`, where [n] is an integer and each of the number-letter combinations is optional.

If the only input is either hours or minutes, they can be entered as a double (e.g `1.5m`) or as time (e.g `1:30m`). This doesn't work for seconds, which only accepts integers.

### Time input examples
Some examples of valid inputs:
- `01h02m03s`
- `01:02:03`
- `1h2m`
- `1h3s`
- `01:02h`
- `2.5m`
- `2:30`
- `90s`
- `.5h`

These inputs are **invalid**:
- `0.5s` (seconds are always integers)
- `:30h` (time notation needs a number at both sides of the colon. `0:30h` and `.5h` *are* valid)
- `30m1h` (the order of the letters can't be changed)
- `1h30` (numbers are always followed by a letter. Add an `m` or `s` at the end, or remove all letters and enter `1:30:00`)
- `1:30h20s` (only integers are allowed if you use multiple letters. Valid alternatives are: `1:30:20` and `1h30m20s`)

## Pace input
Pace input is in minutes per kilometer. This can be whole minutes (`M`), minutes and seconds (`M:S` e.g. `1:30`), or minutes with seconds as a fraction (`M.S` e.g. `1.5`).
Just like the time input, leading zeros don't matter and you can add values higher than 60. Unlike the time input, you can't add hours or use letters.

# Output
The outputs are given in this format:
- `distance` in kilometers, with numbers after the decimal point added where needed. Examples: `12km`, `12.1km`, `0.12km`
- `time` in minutes and seconds. Hours are added if time >= 1 hour. Examples `5:00`, `1:05:00`
- `pace` in minutes per kilometer. Minutes and seconds Examples: `5:00min/km`, `65:00min/km`

Note: Outputs are always in kilometers. Even if the input distance is in miles, pace will be in min/km.

"""


class InputError(Exception):
    def __init__(self, unit, input):
        super().__init__(self)
        self.unit = unit
        self.input = input

    def __str__(self):
        return f"{self.unit} is not a valid input for {self.input}"


distance_units = [
    {"name": "mi", "dist_in_km": 1.609344},
    {"name": "km", "dist_in_km": 1},
    {"name": "k", "dist_in_km": 1},
]


def distance_str_to_km(distance: str) -> float:
    if distance == "hm" or distance == "half marathon":
        return 21.0975

    if distance == "m" or distance == "marathon":
        return 42.195

    for unit in distance_units:
        if distance.endswith(unit["name"]):
            distance = distance.removesuffix(unit["name"])
            return float(distance) * unit["dist_in_km"]

    try:
        return float(distance)
    except ValueError:
        raise InputError(distance, "distance")


def time_without_letters_to_minutes(time: str) -> float:
    split_time = time.split(":")
    if len(split_time) not in [2, 3]:
        raise InputError(time, "time")

    split_time.reverse()
    seconds_in_minutes = int(split_time[0]) / 60
    minutes = int(split_time[1])
    total_time = seconds_in_minutes + minutes
    if len(split_time) == 3:
        total_time += int(split_time[2]) * 60

    return total_time


def time_with_letters_to_minutes(time: str) -> float:
    allowed_letters = "hms"
    number_of_allowed_letters = 0
    for letter in allowed_letters:
        count = time.count(letter)
        if count == 1:
            number_of_allowed_letters += 1
        elif count > 1:
            raise InputError(time, "time")

    if number_of_allowed_letters == 1:
        for letter in "hm":
            pattern = re.compile(rf"^(?:\d|\.|:)+{letter}$")
            match = re.match(pattern, time)
            if not match:
                continue
            clean_match = match.group().removesuffix(letter)
            if ":" in clean_match:
                split_time = clean_match.split(":")
                decimals = float(split_time[0]) + float(split_time[1]) / 60
            else:
                decimals = float(clean_match)
            if letter == "h":
                return decimals * 60
            return decimals

        try:
            seconds = re.match(r"^\d+s$", time).group().removesuffix("s")
            return float(seconds) / 60
        except AttributeError:
            raise InputError(time, "time")

    if number_of_allowed_letters > 1:
        time_regex = re.compile(
            r"^(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?$"
        )
        match = re.match(time_regex, time)
        if not match:
            raise InputError(time, "time")

        return (
            float(match.group("hours") or 0) * 60
            + float(match.group("minutes") or 0)
            + float(match.group("seconds") or 0) / 60
        )


def time_str_to_minutes(time: str) -> float:
    if any(x in time for x in "hms"):
        return time_with_letters_to_minutes(time)
    return time_without_letters_to_minutes(time)


def pace_str_to_multiplier(pace: str) -> float:
    try:
        return float(pace)
    except ValueError:
        pass
    if ":" not in pace:
        raise InputError(pace, "pace")
    split_pace = pace.split(":")
    return float(split_pace[0]) + float(split_pace[1]) / 60


def minutes_to_time(decimal_minutes: float, show_hours: bool) -> str:
    formatted_hours = ""
    min_min_length = 0
    minutes, seconds = divmod(decimal_minutes, 1)
    formatted_seconds = str(round(seconds * 60)).rjust(2, "0")
    if decimal_minutes >= 60 and show_hours:
        whole_hours, minutes = divmod(decimal_minutes, 60)
        min_min_length = 2
        formatted_hours = f"{int(whole_hours)}:"

    formatted_minutes = str(int(minutes)).rjust(min_min_length, "0")
    return f"{formatted_hours}{formatted_minutes}:{formatted_seconds}"


def calculate_pace(distance: str, time: str) -> str:
    return minutes_to_time(
        time_str_to_minutes(time) / distance_str_to_km(distance), False
    )


def calculate_time(distance: str, pace: str) -> str:
    return minutes_to_time(
        distance_str_to_km(distance) * pace_str_to_multiplier(pace), True
    )


def calculate_distance(time: str, pace: str) -> float:
    distance = time_str_to_minutes(time) / pace_str_to_multiplier(pace)
    if distance.is_integer():
        return int(distance)
    return round(distance, 2)


# distinguishes time input from distance input. WILL fail when given pace as the argument!
def is_time(unit: str) -> bool:
    if unit.strip(" ").isalpha():
        return False
    if ":" in unit:
        return True
    if any(unit.endswith(x) for x in "hms"):
        return True
    return False


def create_message(first_unit: str, preposition: str, second_unit: str) -> str:
    first_unit = first_unit.lower()
    preposition = preposition.lower()
    second_unit = second_unit.lower()
    if preposition == "in":
        return f"{calculate_pace(distance=first_unit, time=second_unit)}min/km"

    if is_time(first_unit):
        return f"{calculate_distance(time=first_unit, pace=second_unit)}km"

    return calculate_time(distance=first_unit, pace=second_unit)


def parse_args():
    parser = argparse.ArgumentParser(
        description=arg_description,
        epilog=arg_epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("first_unit", help="pace, distance, or time")
    parser.add_argument("preposition", choices=["at", "in"])
    parser.add_argument("second_unit", help="pace, distance, or time")
    args = parser.parse_args()
    message = create_message(args.first_unit, args.preposition, args.second_unit)
    parser.exit(message=f"{message}\n")


if __name__ == "__main__":
    parse_args()
