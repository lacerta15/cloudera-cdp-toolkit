#!/usr/bin/env python3
"""List, download and activate Cloudera parcels via CM API.
Usage:
  python3 parcel_manager.py --action list
  python3 parcel_manager.py --action download  --product CDH --version 7.1.9
  python3 parcel_manager.py --action activate  --product CDH --version 7.1.9
"""
import argparse, json, urllib.request, urllib.parse, base64, os, time, yaml

def load_cfg():
    p = os.path.join(os.path.dirname(__file__),'..','config','config.yml')
    if os.path.exists(p):
        return yaml.safe_load(open(p)).get('cloudera',{})
    return {}

def cm(base, auth, method, path, data=None):
    req = urllib.request.Request(f"{base}{path}", method=method,
          headers={"Authorization":f"Basic {auth}","Content-Type":"application/json"})
    if data:
        req.data = json.dumps(data).encode()
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def main():
    pa = argparse.ArgumentParser()
    pa.add_argument('--action', choices=['list','download','distribute','activate'], default='list')
    pa.add_argument('--product', default='CDH')
    pa.add_argument('--version', default='')
    args = pa.parse_args()

    cfg  = load_cfg()
    host = cfg.get('cm_host','localhost'); port = cfg.get('cm_port',7180)
    user = cfg.get('cm_user','admin');     pw   = cfg.get('cm_pass','admin')
    clus = cfg.get('cluster_name','Cluster 1')
    base = f"http://{host}:{port}/api/v41"
    auth = base64.b64encode(f"{user}:{pw}".encode()).decode()
    cenc = urllib.parse.quote(clus)

    parcels = cm(base, auth, 'GET', f"/clusters/{cenc}/parcels").get('items',[])

    if args.action == 'list':
        print(f"{'Product':<15} {'Version':<25} {'Stage'}")
        print("-"*60)
        for p in parcels:
            print(f"  {p.get('product',''):14} {p.get('version',''):24} {p.get('stage','')}")
        return

    penc = urllib.parse.quote(args.version)
    path = f"/clusters/{cenc}/parcels/products/{args.product}/versions/{penc}/commands"

    action_map = {
        'download':   f"{path}/startDownload",
        'distribute': f"{path}/startDistribution",
        'activate':   f"{path}/activate",
    }
    url = action_map.get(args.action)
    if url:
        r = cm(base, auth, 'POST', url)
        print(f"Command: {r.get('name','?')} | ID: {r.get('id','?')} | Active: {r.get('active','?')}")

if __name__ == '__main__':
    main()
