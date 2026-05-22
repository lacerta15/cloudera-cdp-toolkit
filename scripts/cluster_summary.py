#!/usr/bin/env python3
"""Print a full summary of the Cloudera cluster via CM API."""
import json, urllib.request, urllib.parse, base64, os, sys, yaml

def load_cfg():
    p = os.path.join(os.path.dirname(__file__),'..','config','config.yml')
    if os.path.exists(p):
        import yaml; return yaml.safe_load(open(p)).get('cloudera',{})
    return {}

def cm_get(base, auth, path):
    req = urllib.request.Request(f"{base}{path}",
          headers={"Authorization": f"Basic {auth}", "Accept":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"[WARN] {path}: {e}"); return {}

def main():
    cfg  = load_cfg()
    host = cfg.get('cm_host', os.environ.get('CM_HOST','localhost'))
    port = cfg.get('cm_port', 7180)
    user = cfg.get('cm_user', 'admin')
    pw   = cfg.get('cm_pass', 'admin')
    clus = cfg.get('cluster_name','Cluster 1')
    base = f"http://{host}:{port}/api/v41"
    auth = base64.b64encode(f"{user}:{pw}".encode()).decode()

    print(f"\n{'='*60}")
    print(f"  Cloudera Cluster Summary")
    print(f"  CM: {host}:{port}  |  Cluster: {clus}")
    print(f"{'='*60}")

    ver = cm_get(base, auth, "/version")
    print(f"  CM Version : {ver.get('version','unknown')}")

    cenc = urllib.parse.quote(clus)
    info = cm_get(base, auth, f"/clusters/{cenc}")
    print(f"  CDP Version: {info.get('fullVersion','unknown')}")
    print(f"  Status     : {info.get('entityStatus','unknown')}")

    svcs = cm_get(base, auth, f"/clusters/{cenc}/services").get('items',[])
    print(f"\n  Services ({len(svcs)}):")
    for s in svcs:
        icon = '✅' if s.get('serviceState')=='STARTED' else '❌'
        print(f"    {icon}  {s.get('type',''):20} {s.get('serviceState',''):12} {s.get('healthSummary','')}")

    hosts = cm_get(base, auth, "/hosts").get('items',[])
    print(f"\n  Hosts ({len(hosts)}):")
    for h in hosts[:20]:
        print(f"    • {h.get('hostname',''):40} {h.get('healthSummary','')}")
    print()

if __name__ == '__main__':
    main()
