# TODO

Future enhancements and feature ideas for bcrypt-speed-tests.

## High Priority

### Statistical Analysis

- [ ] Show median, min, max, stddev instead of just mean
- [ ] More robust against outliers, especially important for benchmarking
- [ ] Add `--show-all` flag to display individual timings

### Export Formats

- [ ] Add `--format json|csv|markdown|table` option
- [ ] JSON format for easier parsing/integration with other tools
- [ ] CSV for spreadsheet analysis
- [ ] Markdown for documentation
- [ ] Table is the current default format

## Medium Priority

### Recommendation Mode

- [ ] Add `--target-time <ms>` flag to suggest optimal cost factor
- [ ] Automatically benchmark and suggest cost to achieve target time
- [ ] Helps users pick the right cost factor for their security requirements

### Progress Indicator

- [ ] Show progress bar during benchmarks (consider using `rich`)
- [ ] Better UX for longer-running benchmarks
- [ ] Especially helpful when testing higher cost factors

### System Information

- [ ] Add `--include-system-info` flag
- [ ] Include CPU model, cores, platform details in output
- [ ] Useful for comparing benchmarks across different machines
- [ ] Could use `platform` and `psutil` modules

## Lower Priority

### Save/Compare Results

- [ ] `--save <file.json>` to persist results
- [ ] `--compare <file.json>` to compare against saved baseline
- [ ] Track performance over time or after system changes
- [ ] Show percentage differences

### Variable Password Lengths

- [ ] Test with different password sizes (short/medium/long)
- [ ] Some bcrypt implementations have different perf characteristics
- [ ] `--password-length <size>` or `--test-password-sizes`

## Nice to Have (Possibly Over-Engineering)

- [ ] Multi-threaded concurrent testing
- [ ] Memory profiling during benchmarks
- [ ] Chart generation (likely overkill for a CLI tool)
- [ ] Web-based result viewer

## Documentation Improvements

- [ ] Add examples section to README
- [ ] Document recommended cost factors for different use cases
- [ ] Add security best practices guide
- [ ] Create a comparison chart vs other password hashing algorithms

## Code Quality

- [x] Add comprehensive test suite
- [x] Set up CI/CD workflows
- [x] Add mypy type checking
- [x] Add ruff linting
- [ ] Add benchmarks for the benchmark tool itself (meta!)
- [ ] Performance profiling to ensure minimal overhead

---

**Note:** Items are ordered by perceived value and ease of implementation. Checkboxes can be marked as features are completed.
