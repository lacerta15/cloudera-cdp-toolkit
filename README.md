# cloudera-cdp-toolkit
Scripts for managing Cloudera CDP Private Cloud Base and Public Cloud.

## Tools
| Script | Purpose |
|--------|---------|
| `scripts/cluster_summary.py` | Print cluster topology & version info |
| `scripts/parcel_manager.py` | Download, distribute, activate parcels |
| `scripts/cm_api_helper.sh` | cURL wrappers for CM REST API |
| `scripts/rotate_cm_logs.sh` | Rotate and compress Cloudera Manager logs |

## Quick Start
```bash
cp config/config.example.yml config/config.yml
# Edit CM host, user, pass
python3 scripts/cluster_summary.py
```
