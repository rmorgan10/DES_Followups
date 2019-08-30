# GW Simulation Analysis Pipeline

## Workflow Outline

1. A human must make an event diretory and `event_metadata.csv` file. See `events/GW190519/` for an example.

2. A human must provide an `exptable.txt` file in the event directory. See `events/GW190519/` for an example.

3. Run `generate_sims.py`. Use the event name as a command line argument. Example: `python generate_sims.py GW190510`.

The script `generate_sims.py` will do the following things:

- Trigger `makeSimlib_easyaccess.py` with the coordinates and exposure numbers corresponding to the event

- `makeSimlib_easyaccess.py` will then produce a `SIMLIB` file for the observations. This file will tell `SNANA` the observing conditions of the data.

- Clean the `SIMLIB` file of duplicate rows by running `clean_simlib.py`

- Create a `sims` directory inside the event directory with template `SNANA` input files for KNe, SNe, and AGN.

- Call `update_snana_inputs.py` to overwrite the templates with position, date, and name information of the current event.

- Run SNANA on the updated input files. Simulations will be tagged with the user's FNAL login name.

- Collect the simulations and move them to the `sims/` diretory for the current event.

