# TODO

## Next up
- [ ] Implement `parse_fit()` in `parser.py`
- [ ] Wire parser output to `commands/import_run.py`
- [ ] Figure out full data schema for relationships between data-runs-runner

## Models
- [ ] how to handle heart rates
- [ ] `distance_miles()` on Run model
- [ ] `duration_formatted()` on Run model  
- [ ] `pace_formatted()` on Run model
- [ ] `as_dict()` and `dominant_zone()` on HRZone model

## Commands
- [ ] `runs` list view
- [ ] `run <id>` detail view with splits + HR zones
- [ ] `trends` weekly mileage table
- [ ] `pr` personal records
- [ ] `plan` AI training plan

## Stretch
- [ ] Pull `max_hr` from Runner model instead of hardcoded 190
- [ ] Add `--runner` flag to import command
- [ ] Parameter to import multiple `.fit` files at once
- [ ] Visualization / GPS map