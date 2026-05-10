# PWM RC-Circuit Based DAC

This contains the supplemental code used to numerically compute
the minimum RC time constant values to fulfill a given error
bound of settled analog voltage.

## Usage

1. Install the [uv package manager](https://docs.astral.sh/uv/) for python.
2. Run:

```sh
uv sync
uv run main.py
```

3. It should output the graph `plot.png` and the value of `tau`
   for 95% duty cycle in seconds.

