"""Verify every source the notebooks depend on is reachable, from your laptop. No Databricks needed.

    uv run --with requests python -I scripts/check_sources.py
"""
import re
import sys
import requests

UA = {"User-Agent": "Mozilla/5.0 (two-postcodes-hackathon check)"}
results = []


def check(name, fn):
    try:
        results.append((name, "OK", str(fn())[:150]))
    except Exception as e:  # noqa: BLE001
        results.append((name, "FAIL", f"{type(e).__name__}: {str(e)[:130]}"))


def get(url, **kw):
    r = requests.get(url, headers=UA, timeout=60, allow_redirects=True, **kw)
    r.raise_for_status()
    return r


def ranged(url):
    r = requests.get(url, headers={**UA, "Range": "bytes=0-2047"}, timeout=60, allow_redirects=True, stream=True)
    r.raise_for_status()
    return f"{r.status_code} {r.headers.get('content-type')}"


def nspl():
    h = get("https://www.arcgis.com/sharing/rest/search", params={
        "q": 'title:"National Statistics Postcode Lookup" owner:ONSGeography_data type:"CSV Collection"',
        "sortField": "modified", "sortOrder": "desc", "num": 5, "f": "json"}).json()["results"]
    h = [x for x in h if "User Guide" not in x["title"] and x["name"].lower().endswith(".zip")]
    return h[0]["title"], ranged(f"https://www.arcgis.com/sharing/rest/content/items/{h[0]['id']}/data")


def lsoa():
    b = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Lower_layer_Super_Output_Areas_December_2021_Boundaries_EW_BGC_V5/FeatureServer/0"
    n = get(f"{b}/query", params={"where": "1=1", "returnCountOnly": "true", "f": "json"}).json()["count"]
    g = get(f"{b}/query", params={"where": "1=1", "outFields": "LSOA21CD,LSOA21NM", "outSR": 4326, "f": "geojson",
                                   "resultOffset": 0, "resultRecordCount": 2, "orderByFields": "LSOA21CD"}).json()
    return n, list(g["features"][0]["properties"])


def overture():
    xml = get("https://overturemaps-us-west-2.s3.amazonaws.com/?list-type=2&prefix=release/&delimiter=/").text
    rel = sorted(re.findall(r"release/([0-9-]+\.[0-9]+)/", xml))[-1]
    x = get(f"https://overturemaps-us-west-2.s3.amazonaws.com/?list-type=2&prefix=release/{rel}/theme=transportation/&delimiter=/").text
    return rel, re.findall(r"type=(\w+)/", x)


def os_products():
    out = []
    for p in ("OpenRoads", "OpenRivers", "OpenUPRN", "CodePointOpen", "BoundaryLine", "GeoCoast_Open"):
        o = get(f"https://api.os.uk/downloads/v1/products/{p}/downloads").json()
        out.append(f"{p}:{[x['format'][:8] for x in o if x['area'] == 'GB']}")
    return out


def repd():
    page = "https://www.gov.uk/government/publications/renewable-energy-planning-database-monthly-extract"
    return sorted(set(re.findall(r"https://assets\.publishing\.service\.gov\.uk/[^\"']+\.(?:csv|xlsx)", get(page).text)))


def rofrs():
    r = get("https://ckan.publishing.service.gov.uk/api/3/action/package_show",
            params={"id": "risk-of-flooding-from-rivers-and-sea-postcodes-in-areas-at-risk2"}).json()["result"]["resources"]
    return [(x["format"], x["url"]) for x in r][:4]


def overpass():
    q = '[out:json][timeout:60];area["ISO3166-1"="GB"][admin_level=2]->.gb;nwr["emergency"="lifeboat_station"](area.gb);out center tags 5;'
    for _ in range(3):
        r = requests.post("https://overpass-api.de/api/interpreter", data={"data": q}, timeout=90,
                          headers={"User-Agent": "two-postcodes-hackathon/1.0", "Accept": "*/*"})
        if r.status_code == 200:
            break
    r.raise_for_status()
    return len(r.json()["elements"]), "lifeboat stations (limit 5)"


check("NSPL", nspl)
check("LSOA boundaries", lsoa)
check("Overture release", overture)
check("OS downloads", os_products)
check("NaPTAN", lambda: ranged("https://naptan.api.dft.gov.uk/v1/access-nodes?dataFormat=csv"))
check("BODS GTFS", lambda: ranged("https://data.bus-data.dft.gov.uk/timetable/download/gtfs-file/all/"))
for k in ("collision", "vehicle", "casualty"):
    check(f"STATS19 {k}", lambda k=k: ranged(f"https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-{k}-last-5-years.csv"))
check("DfT AADF", lambda: ranged("https://storage.googleapis.com/dft-statistics/road-traffic/downloads/data-gov-uk/dft_traffic_counts_aadf.zip"))
check("DfT MRDB 2024", lambda: ranged("https://storage.googleapis.com/dft-statistics/road-traffic/mrdb-2024.zip"))
check("EA flood areas", lambda: len(get("https://environment.data.gov.uk/flood-monitoring/id/floodAreas", params={"_limit": 5}).json()["items"]))
check("EA warnings", lambda: len(get("https://environment.data.gov.uk/flood-monitoring/id/floods").json()["items"]))
check("EA stations", lambda: len(get("https://environment.data.gov.uk/flood-monitoring/id/stations", params={"_limit": 5}).json()["items"]))
check("EA RoFRS postcodes", rofrs)
check("DESNZ REPD links", repd)
check("Overpass SAR", overpass)

w = max(len(r[0]) for r in results)
for n, s, d in results:
    print(f"{s:4}  {n:<{w}}  {d}")
sys.exit(1 if any(s == "FAIL" for _, s, _ in results) else 0)
