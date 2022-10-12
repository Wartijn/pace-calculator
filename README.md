Pace calculator is a tool that takes two of `pace`, `time` and `distance` as input and gives the third one as output.

# Requirements
Python 3.6 or higher 

# Usage

Download `pacecalc.py` and execute it by supplying it with a three-word sentence that's constructed like this: `[first_unit] [preposition] [second_unit]`

Some examples:
- `./pacecalc.py 45:00 at 4:40` outputs `11:25km`
- `./pacecalc.py marathon in 2:01:09` outputs `2:52min/km`
- `./pacecalc.py 15km at 3:23` outputs `50:45min/km`

## Supported sentence formats
- `[distance] in [time]` which outputs `pace`
- `[distance] at [pace]` which outputs `time`
- `[time] at [pace]` which outputs `distance`

## Distance inputs
Distance takes a number [n], which can be an integer or a double. The following input formats are accepted: 
- `[n]`, `[n]km` or `[n]k` for kilometers. 
- `[n]m` for meters
- `[n]mi` for miles

There are two pre-set distances that are not prepended by a number:
- `m` or `marathon` 
- `hm` or `"half marathon"`. This last one needs to be surrounded by quotes.  

## Time input
`H:M:S`. Hours are optional, so `02:03` is 2 minutes and 3 seconds. The numbers can be zero padded, but don't have to: `01:02:03`, `1:2:3` and `1:02:3` are equivalent. 
In fact, you can add as many leading zeros as you like and minutes and seconds can be higher than 60. You can write the previous example as `000000062:03` if you like.

## Pace input
`M:S` as minutes per kilometer. Both minutes and seconds are required. Just like the time input, leading zeros don't matter and you can add values higher than 60. Unlike the time input, you can't add hours. 

# Output
The outputs are given in this format:
- `distance` in kilometers, with numbers after the decimal point added where needed. Examples: `12km`, `12.1km`, `0.12km`
- `time` in minutes and seconds. Hours are added if time >= 1 hour. Examples `5:00`, `1:05:00`
- `pace` in minutes per kilometer. Minutes and seconds Examples: `5:00min/km`, `65:00min/km`

Note: Outputs are always in kilometers. Even if the input distance is in miles or meters, pace will be in min/km.

# Development
The dependencies can be installed by running `poetry install`. 
If you'd like to contribute, please add tests and run `black`.

# Some notes
### Negative numbers
It's possible to add negative numbers to the inputs, but this isn't covered in any tests and I might add checks to prevent these inputs.

### Supported sentences
The following sentences are supported:
- `[distance] in [time]` (output: `pace`)
- `[distance] at [pace]` (output: `time`)
- `[time] at [pace]` (output: `distance`)

This leaves the following sentences that you could make, but are currently **not supported**:
- `[pace] [preposition] [time]` (output: `distance`)
- `[pace] [preposition] [distance]` (output: `time`)
- `[time] [preposition] [distance]` (output: `pace`)

The reason they are not supported is that the supported sentences already provide every combination of units, and I don't know what prepositions I should add to the unsupported sentences to turn them into something that make sense.
I haven't run into a situation where I felt that I should use anything else than the supported sentences, although that might be because I'm familiar with the limits of this script. 
