#!/usr/bin/env bash
# Quick cURL wrappers for Cloudera Manager REST API
# Usage: source cm_api_helper.sh; cm_get /clusters
CM_HOST="${CM_HOST:-localhost}"; CM_PORT="${CM_PORT:-7180}"
CM_USER="${CM_USER:-admin}";     CM_PASS="${CM_PASS:-admin}"
CM_BASE="http://${CM_HOST}:${CM_PORT}/api/v41"

cm_get()  { curl -su "${CM_USER}:${CM_PASS}" "${CM_BASE}$1" | python3 -m json.tool; }
cm_post() { curl -su "${CM_USER}:${CM_PASS}" -X POST -H 'Content-Type:application/json' -d "${2:-{}}" "${CM_BASE}$1" | python3 -m json.tool; }

cm_cluster_status() { cm_get "/clusters"; }
cm_services()       { cm_get "/clusters/$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$1")/services"; }
cm_hosts()          { cm_get "/hosts"; }
cm_alerts()         { cm_get "/events?query=severity==CRITICAL&maxResults=10"; }

echo "CM API helpers loaded. CM: ${CM_HOST}:${CM_PORT}"
echo "Commands: cm_cluster_status | cm_services <cluster> | cm_hosts | cm_alerts"
