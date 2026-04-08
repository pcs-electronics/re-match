---
name: re-match
description: 'Control RigExpert Match Antenna Analyzer and plot Touchstone data. Use for reading R and X values, checking connection status, and generating plots.'
argument-hint: 'Describe your task: read data from analyzer, check status, plot Smith chart, etc.'
---

# RigExpert Match Skill

## Overview

This skill provides functionality for controlling the RigExpert Match Antenna Analyzer and plotting Touchstone data. It includes two main scripts:

1. **match-cli.py**: A command-line interface for controlling the RigExpert Match Antenna Analyzer.
2. **tt-plot.py**: A script for plotting Touchstone data from stdin or a file.

## Workflow

1. **Check Status**: Before taking the first measurement, check the status of the analyzer by running `python3 match-cli.py status`.
2. **Default Parameters**: The default center frequency is 345 MHz, sweep range is 690 MHz, and the number of points is 100.
3. **Frequency Range**: The minimum operating frequency is 0 MHz, and the maximum is 690 MHz.
4. **Data File Location**: The `data.s1p` file should be located at the AI agent's workspace, so the agent can read and write there. Always use a full path when referring to `data.s1p` (for example, `/home/dn/WORK/RigExpertMatch/re-match/data.s1p`).
5. **Take Measurements**: Always run `python3 match-cli.py` in a way that saves the Touchstone output to `data.s1p` by using the output option (for example, `--output /home/dn/WORK/RigExpertMatch/re-match/data.s1p`). Never emit the S1P data to stdout. Always run `python3 tt-plot.py` to read S1P data from `data.s1p`, never from stdin. When the user asks to do the measurements, use the script with appropriate parameters to save the measurement to the `data.s1p` file. Then, run the `python3 tt-plot.py` script on this file to generate `data.png`, which should be inserted into the message channel to the user. Additionally, output a text showing the minimum frequency, center frequency, and maximum frequency. Do not report anything about `data.s1p` or `data.png` to the user. Eliminate "technical" data such as file names, script names, or command-line options from the output.
6. **Default Chart Type**: The default chart type is SWR chart, but you may offer other options to the user in a "for dummies" format. Never refer to Python files when offering options.
7. **Plot Another Chart**: When the user asks to plot another type of chart, use the `data.s1p` file as the source of data. Do not perform actual measurements unless the center frequency, sweep range, or number of points are changed. Choosing another band affects the center frequency and the frequency range, so the actual measurement should be performed.
8. **Default SWR Range**: The default SWR range is 10, but you may offer 2 to the user in a "for dummies" format.
9. **Default R,X Range**: The default R,X range is 1000, but you may offer 100 to the user in a "for dummies" format.

## Features

### match-cli.py

- **Read Data**: Read R and X values from the analyzer and output in Touchstone format.
- **Status Check**: Check the connection status of the analyzer.
- **Trace Mode**: Enable trace mode to output raw data from the analyzer for debugging.
- **Frequency Input**: Support for frequency input in kHz or MHz with appropriate suffixes.
- **Timestamp**: Include timestamp in the Touchstone file header.

### tt-plot.py

- **Input Handling**: Parse Touchstone data from stdin or a file with `.s1p` extension.
- **Format Detection**: Automatically detect the Touchstone format (S,RI, S,MA, S,DB, or Z,RI).
- **Plot Generation**: Generate plots based on the specified type (SWR to 10, SWR to 2, S11, RX to 1000, RX to 100, Smith chart).
- **Output**: Save the resulting plot to a file specified by the user.
- **Help Display**: Display help when run without parameters or with `-h` or `--help`.

## Usage

### match-cli.py

#### Display Help

```bash
python3 match-cli.py -h
```

#### Check Status

```bash
python3 match-cli.py status
```

#### Read Data

```bash
python3 match-cli.py read --center 100MHz --range 200MHz --points 100
```

#### Read Data with Trace

```bash
python3 match-cli.py read --center 100MHz --range 200MHz --points 100 --trace
```

### tt-plot.py

#### Display Help

```bash
python3 tt-plot.py -h
```

#### Plot SWR to 10

```bash
python3 tt-plot.py --type swr10 --output plot.png < data.s1p
```

#### Plot Smith Chart

```bash
python3 tt-plot.py --type smith --output smith_chart.png data.s1p
```

#### Plot RX to 100

```bash
python3 tt-plot.py --type rx100 --output rx_plot.png data.s1p
```

## Supported Formats

### match-cli.py

- **Frequency Input**: Support for frequency input in kHz or MHz with appropriate suffixes.
- **Output Format**: Touchstone format with timestamp and header.

### tt-plot.py

- **S,RI**: Real and imaginary parts of the S-parameter.
- **S,MA**: Magnitude and angle of the S-parameter.
- **S,DB**: Magnitude in decibels (dB) of the S-parameter.
- **Z,RI**: Real and imaginary parts of the impedance (Z).

## Examples

### match-cli.py

#### Example Output

```
! Touchstone file generated by match-cli.py on 2023-11-15 14:30:45
# MHz Z RI R 50
100.0 49.99 0.04
100.0 50.03 0.07
100.0 50.03 0.03
...
```

#### Trace Mode Output

```
Command sent: FQ100000000
Command sent: SW200000000
Command sent: FRX10
! Touchstone file generated by match-cli.py on 2023-11-15 14:30:45
# MHz Z RI R 50
Raw data: OK
Raw data: OK
Raw data: 0.000000,49.99, 0.04
100.0 49.99 0.04
Raw data: 20.000000,50.03, 0.07
100.0 50.03 0.07
...
```

### tt-plot.py

#### Example Output

```
Plot saved to plot.png
```

#### Important Note

Do not offer similar "technical style" help. Avoid referring to Python files or command-line options when offering assistance. Instead, provide user-friendly guidance in a "for dummies" format.

## Radio Amateur Bands

| Band | Nickname | Min Frequency (MHz) | Max Frequency (MHz) |
|------|----------|---------------------|---------------------|
| 160m | Top Band | 1.8 | 2.0 |
| 80m | | 3.5 | 4.0 |
| 40m | | 7.0 | 7.3 |
| 30m | | 10.1 | 10.15 |
| 20m | | 14.0 | 14.35 |
| 17m | | 18.068 | 18.168 |
| 15m | | 21.0 | 21.45 |
| 12m | | 24.89 | 24.99 |
| 10m | | 28.0 | 29.7 |
| 6m | Magic Band | 50.0 | 54.0 |
| 4m | | 70.0 | 70.5 |
| 2m | | 144.0 | 148.0 |
| 1.25m | | 222.0 | 225.0 |
| 70cm | | 420.0 | 450.0 |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This code was generated with the help of an AI model, Mistral Vibe.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Support

For support, please contact the project maintainers or open an issue on the project repository.
