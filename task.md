# 🎯 Deep Troubleshooting: BME Telemetry & Pipeline Stabilization

- `[x]` Run System Discovery Scan.
- `[x]` Execute L-1 Self-Healing Initialization (Truth Markers).
- `[x]` Analyze `validate_bme_logic.py` and `warden.py` to identify timing / I2C vulnerabilities.
- `[x]` Review `pulse.sh` for unresponsive subprocess drops or acoustic capture lockouts.
- `[x]` Apply "Hardware Hardening" constants (3.0s settle delay, defensive garbage detection).
- `[x]` Validate telemetry flow end-to-end.
- `[x]` Implement Resilient DTR Hardware Reset logic for >3 consecutive drops in `warden.py`.
- `[x]` Validate Resilience execution sequence.
- `[/]` Strip hardcoded assumptions from `vision.py` prompt.
- `[ ]` Sever Warden recommendations from Vision context to prevent narrative fallacy.
- `[ ]` Restructure JSON schema for `compositional_truth_check`.
