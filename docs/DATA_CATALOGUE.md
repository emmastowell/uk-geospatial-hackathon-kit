# Data catalogue

Generated from `notebooks/table_docs.py` (the same text applied as Unity Catalog comments by notebook 06). Do not edit by hand: change `table_docs.py` and rerun `python3 scripts/build_catalogue.py`.

57 tables, 872 documented columns.

| Table | Columns | Summary |
|---|---|---|
| [`bgs_geocoast_geocoast_v1_authority_area_inundation`](#bgs_geocoast_geocoast_v1_authority_area_inundation) | 35 | BGS GeoCoast: per local authority, the area, population, urban area, built area, roads and railways exposed to coastal inundation by 2050, 2080 and 2100, alongside the authority baseline |
| [`bgs_geocoast_geocoast_v1_authority_coastline_cliff_erosion_mean`](#bgs_geocoast_geocoast_v1_authority_coastline_cliff_erosion_mean) | 7 | BGS GeoCoast: cliff erosion susceptibility of the coastline per local authority, mean scenario |
| [`bgs_geocoast_geocoast_v1_authority_coastline_cliff_erosion_worst`](#bgs_geocoast_geocoast_v1_authority_coastline_cliff_erosion_worst) | 7 | BGS GeoCoast: cliff erosion susceptibility of the coastline per local authority, worst-case scenario |
| [`bgs_geocoast_geocoast_v1_authority_coastline_inundation`](#bgs_geocoast_geocoast_v1_authority_coastline_inundation) | 11 | BGS GeoCoast: coastline length and share susceptible to inundation by 2050, 2080 and 2100 per local authority |
| [`bgs_geocoast_geocoast_v1_authority_coastline_multi_formations`](#bgs_geocoast_geocoast_v1_authority_coastline_multi_formations) | 6 | BGS GeoCoast: coastline per local authority backed by more than one geological formation |
| [`bgs_geocoast_geocoast_v1_erosion_profile_domains`](#bgs_geocoast_geocoast_v1_erosion_profile_domains) | 9 | BGS GeoCoast: coastal erosion and profile domains (polygons or lines classifying the coast by erosion susceptibility and profile) |
| [`bgs_geocoast_geocoast_v1_smp_coastline_cliff_erosion_mean`](#bgs_geocoast_geocoast_v1_smp_coastline_cliff_erosion_mean) | 7 | BGS GeoCoast: cliff erosion susceptibility per Shoreline Management Plan unit, mean scenario |
| [`bgs_geocoast_geocoast_v1_smp_coastline_cliff_erosion_worst`](#bgs_geocoast_geocoast_v1_smp_coastline_cliff_erosion_worst) | 7 | BGS GeoCoast: cliff erosion susceptibility per Shoreline Management Plan unit, worst-case scenario |
| [`bgs_geocoast_geocoast_v1_smp_coastline_inundation`](#bgs_geocoast_geocoast_v1_smp_coastline_inundation) | 11 | BGS GeoCoast: coastline susceptible to inundation by 2050, 2080 and 2100 per Shoreline Management Plan unit |
| [`bgs_geocoast_geocoast_v1_smp_coastline_length`](#bgs_geocoast_geocoast_v1_smp_coastline_length) | 5 | BGS GeoCoast: total coastline length per Shoreline Management Plan unit |
| [`bgs_geocoast_geocoast_v1_smp_coastline_multi_formations`](#bgs_geocoast_geocoast_v1_smp_coastline_multi_formations) | 6 | BGS GeoCoast: coastline per Shoreline Management Plan unit backed by more than one geological formation |
| [`desnz_repd`](#desnz_repd) | 55 | DESNZ Renewable Energy Planning Database (REPD): renewable electricity projects in the UK pipeline, from application through operation, with technology, capacity, planning status and location |
| [`dft_aadf`](#dft_aadf) | 34 | DfT road traffic counts: Average Annual Daily Flow (AADF) by count point, year and vehicle class, for major and minor roads in Great Britain |
| [`dft_evci_constituency`](#dft_evci_constituency) | 6 | DfT public electric vehicle charger counts by Westminster parliamentary constituency (UK), long format, by quarter |
| [`dft_evci_local_authority`](#dft_evci_local_authority) | 6 | DfT public electric vehicle charger counts by local authority district (UK), long format: counts and rates per 100,000 population for all public chargers and for 50kW+ chargers, by quarter |
| [`ea_flood_areas`](#ea_flood_areas) | 6 | Environment Agency flood areas: the geographic areas used for flood alerts and warnings in England, from the real-time flood-monitoring API, with a centroid |
| [`ea_flood_defences`](#ea_flood_defences) | 37 | Environment Agency Asset Information Management System (AIMS) spatial flood defences: about 141,000 flood and coastal defence assets in England (walls, embankments, high ground, culverts, barriers) as lines, with owner, maintainer, standard of protection, crest levels and inspection dates |
| [`ea_flood_warnings`](#ea_flood_warnings) | 7 | Environment Agency current flood alerts and warnings at the time the loader ran (a point-in-time snapshot, often empty or small in dry weather) |
| [`ea_rofrs_postcodes`](#ea_rofrs_postcodes) | 25 | Environment Agency Risk of Flooding from Rivers and Sea (RoFRS), postcodes in areas at risk: counts of residential, non-residential and unclassified properties per postcode in each flood risk band (very low, low, medium, high) |
| [`ea_stations`](#ea_stations) | 7 | Environment Agency monitoring stations (river level, flow, rainfall and tidal gauges) from the real-time flood-monitoring API. Grain: one row per station |
| [`emodnet_bathymetry`](#emodnet_bathymetry) | 3 | EMODnet Bathymetry digital terrain model (2022 release) for UK and Irish waters and coasts, block-averaged from its native 1/16 arc-minute grid (about 115 m) to cells of about 0.0104 degrees (about 1.2 km north-south, narrower east-west) |
| [`emodnet_vessel_density`](#emodnet_vessel_density) | 6 | Vessel traffic density from EMODnet Human Activities (derived by EMSA from terrestrial and satellite AIS positions): annual averages of monthly density for 2022 to 2024, for all vessel types and for 13 vessel type groups, around UK and Irish waters |
| [`gtfs_agency`](#gtfs_agency) | 7 | BODS GTFS agency.txt: the bus operators (agencies) in the Bus Open Data Service national timetable feed |
| [`gtfs_calendar`](#gtfs_calendar) | 10 | BODS GTFS calendar.txt: the weekly pattern and date range during which each timetable service runs |
| [`gtfs_routes`](#gtfs_routes) | 5 | BODS GTFS routes.txt: bus routes (line numbers) in the national timetable feed |
| [`gtfs_stop_times`](#gtfs_stop_times) | 10 | BODS GTFS stop_times.txt: the scheduled arrival and departure at every stop for every bus trip in the national feed |
| [`gtfs_stops`](#gtfs_stops) | 9 | BODS GTFS stops.txt: bus stops used by the national timetable feed, with coordinates |
| [`gtfs_trips`](#gtfs_trips) | 9 | BODS GTFS trips.txt: each scheduled bus journey in the national timetable feed |
| [`lsoa_2021_boundaries`](#lsoa_2021_boundaries) | 2 | 2021 Census Lower layer Super Output Area (LSOA) boundaries for England and Wales, generalised and clipped to the coastline (BGC, V5) |
| [`naptan_stops`](#naptan_stops) | 43 | National Public Transport Access Nodes (NaPTAN): every bus stop, rail station, tram and metro stop, ferry terminal, airport and coach bay in Great Britain, with name, locality and type |
| [`nged_connection_queue`](#nged_connection_queue) | 17 | NGED connection queue: pending and accepted connection applications for generation and storage by supply point, in queue order |
| [`nged_embedded_capacity_register`](#nged_embedded_capacity_register) | 58 | NGED Embedded Capacity Register: generators and storage connected to, or accepted to connect to, the NGED distribution network (Midlands, South West, Wales), with technology, registered capacity, connection status and dates |
| [`nged_ltds_capacity_heatmap`](#nged_ltds_capacity_heatmap) | 37 | NGED Long Term Development Statement capacity heatmap: for each substation (primary, bulk supply point, grid supply point) the firm capacity, available demand and generation headroom, constraint status and the pipeline of connection offers |
| [`northern_powergrid_capacity_heatmap`](#northern_powergrid_capacity_heatmap) | 33 | Northern Powergrid network capacity heatmap: 670 primary substations and grid/bulk supply points with firm capacity, observed demand, generation and demand headroom, fault level and constraint colour codes |
| [`northern_powergrid_connection_queue`](#northern_powergrid_connection_queue) | 10 | Northern Powergrid connection queue: generation and storage connection requests waiting behind each grid supply point, with technology, export capacity and queue position |
| [`northern_powergrid_gsp_connection_info`](#northern_powergrid_gsp_connection_info) | 12 | Northern Powergrid grid supply point (GSP) connection information: connected capacity to date, developer capacity still available, technical import/export limits and expected reinforcement dates, 50 GSPs |
| [`northern_powergrid_historical_peak_demand`](#northern_powergrid_historical_peak_demand) | 19 | Northern Powergrid historical peak demand by substation for 2019/20 to 2023/24, with year-on-year growth |
| [`northern_powergrid_lct_postal_districts`](#northern_powergrid_lct_postal_districts) | 13 | Northern Powergrid low-carbon technology (LCT) connections by postal district: customers and counts of solar PV, heat pumps, energy storage and EV chargers, as numbers and as shares of connections |
| [`nspl`](#nspl) | 35 | ONS National Statistics Postcode Lookup (NSPL), latest release |
| [`os_boundary_line_district_borough_unitary`](#os_boundary_line_district_borough_unitary) | 15 | Ordnance Survey Boundary-Line: district, borough and unitary authority polygons for Great Britain (about 350 areas) |
| [`os_boundary_line_english_region`](#os_boundary_line_english_region) | 15 | Ordnance Survey Boundary-Line: the nine English regions as polygons |
| [`os_boundary_line_westminster_const`](#os_boundary_line_westminster_const) | 15 | Ordnance Survey Boundary-Line: Westminster parliamentary constituency polygons for Great Britain |
| [`os_code_point_open`](#os_code_point_open) | 10 | Ordnance Survey Code-Point Open: one point per postcode unit in Great Britain, located at the mean position of the delivery points |
| [`os_open_rivers`](#os_open_rivers) | 9 | Ordnance Survey Open Rivers: the river and watercourse network for Great Britain as flow-directed centreline links, including canals and lakes' through-routes |
| [`os_open_roads_links`](#os_open_roads_links) | 20 | Ordnance Survey Open Roads: the national road network for Great Britain as centreline links (about 4 million links), with classification, function, form of way and structure |
| [`os_open_roads_nodes`](#os_open_roads_nodes) | 2 | Ordnance Survey Open Roads nodes: the junctions, road ends and other connection points of the national road network (about 3.3 million points) |
| [`os_open_uprn`](#os_open_uprn) | 5 | Ordnance Survey Open UPRN: every addressable location in Great Britain (about 41 million Unique Property Reference Numbers) with a coordinate |
| [`osm_sar_facilities`](#osm_sar_facilities) | 4 | Search-and-rescue related facilities in Great Britain from OpenStreetMap (lifeboat stations, coastguard stations and rescue stations), via the Overpass API. Not an official register: completeness and tagging are volunteer-dependent, so treat as indicative |
| [`overture_buildings`](#overture_buildings) | 6 | Overture Maps building footprints for the configured bounding box only (default: Greater Manchester, not national, because national coverage is about 30 million polygons) |
| [`overture_connectors`](#overture_connectors) | 1 | Overture Maps transportation connectors for Great Britain and Northern Ireland: the junction points where segments meet, forming the routable network graph |
| [`overture_division_areas`](#overture_division_areas) | 6 | Overture Maps administrative division areas (country, region, county, locality polygons) for Great Britain and Ireland |
| [`overture_places`](#overture_places) | 8 | Overture Maps places (points of interest) for Great Britain and Northern Ireland with confidence 0.5 or higher: shops, services, healthcare, education, transport and so on |
| [`overture_segments`](#overture_segments) | 10 | Overture Maps transportation segments for Great Britain and Northern Ireland: every road, path, rail and water centreline as a line, with class, surface, speed limits and flags |
| [`rnli_lifeboat_stations`](#rnli_lifeboat_stations) | 14 | RNLI lifeboat station locations across the UK, Ireland, Channel Islands and Isle of Man (238 stations), from the RNLI Geospatial Team |
| [`stats19_casualty`](#stats19_casualty) | 24 | DfT STATS19 road safety data, casualties: each person injured or killed in a police-reported collision, last five years |
| [`stats19_collision`](#stats19_collision) | 44 | DfT STATS19 road safety data, collisions: every police-reported injury collision in Great Britain for the last five years, with location, conditions and severity |
| [`stats19_vehicle`](#stats19_vehicle) | 32 | DfT STATS19 road safety data, vehicles: each vehicle involved in a police-reported injury collision, last five years, with manoeuvre, point of impact and driver attributes |

## bgs_geocoast_geocoast_v1_authority_area_inundation

BGS GeoCoast: per local authority, the area, population, urban area, built area, roads and railways exposed to coastal inundation by 2050, 2080 and 2100, alongside the authority baseline. Grain: one row per authority polygon. Strong input for the Resilience & risk track exposure model. Source: British Geological Survey GeoCoast Open, distributed via the OS Data Hub Downloads API (shapefile, loaded to WGS84). It is a national screening dataset of coastal susceptibility to inundation (sea level rise) and cliff erosion for 2050, 2080 and 2100, not site-level hazard mapping. See the BGS GeoCoast documentation for methods and class definitions. Licence: Open Government Licence v3.0; contains British Geological Survey materials (c) UKRI.

| Column | Description |
|---|---|
| `dau` | Code or short name of the district / unitary authority. |
| `adm_unit` | Name of the local authority (administrative unit) the record summarises. |
| `area_kmsq` | Baseline: total area of the authority in square kilometres. |
| `population` | Baseline: population of the authority. |
| `urban_kmsq` | Baseline: urban area of the authority, square kilometres. |
| `build_kmsq` | Baseline: built-up area of the authority, square kilometres. |
| `road_km` | Baseline: length of road in the authority, kilometres. |
| `railway_km` | Baseline: length of railway in the authority, kilometres. |
| `railway_st` | Baseline: number of railway stations in the authority. |
| `area_2050` | Area (km2) of the authority susceptible to coastal inundation by 2050. |
| `urban_2050` | Urban area (km2) susceptible to coastal inundation by 2050. |
| `build_2050` | Built-up area (km2) susceptible to coastal inundation by 2050. |
| `road_2050` | Road length (km) susceptible to coastal inundation by 2050. |
| `rw_2050` | Railway length (km) susceptible to coastal inundation by 2050. |
| `rws_2050` | Number of railway stations susceptible to coastal inundation by 2050. |
| `area_2080` | Area (km2) of the authority susceptible to coastal inundation by 2080. |
| `urban_2080` | Urban area (km2) susceptible to coastal inundation by 2080. |
| `build_2080` | Built-up area (km2) susceptible to coastal inundation by 2080. |
| `road_2080` | Road length (km) susceptible to coastal inundation by 2080. |
| `rw_2080` | Railway length (km) susceptible to coastal inundation by 2080. |
| `rws_2080` | Number of railway stations susceptible to coastal inundation by 2080. |
| `area_2100` | Area (km2) of the authority susceptible to coastal inundation by 2100. |
| `urban_2100` | Urban area (km2) susceptible to coastal inundation by 2100. |
| `build_2100` | Built-up area (km2) susceptible to coastal inundation by 2100. |
| `road_2100` | Road length (km) susceptible to coastal inundation by 2100. |
| `rw_2100` | Railway length (km) susceptible to coastal inundation by 2100. |
| `rws_2100` | Number of railway stations susceptible to coastal inundation by 2100. |
| `inund_2050` | Percentage of the authority susceptible to inundation by 2050. |
| `class_2050` | Susceptibility class of the authority for 2050 (higher = more exposed; see BGS documentation). |
| `inund_2080` | Percentage of the authority susceptible to inundation by 2080. |
| `class_2080` | Susceptibility class of the authority for 2080. |
| `inund_2100` | Percentage of the authority susceptible to inundation by 2100. |
| `class_2100` | Susceptibility class of the authority for 2100. |
| `product` | Name of the BGS product the record belongs to (GeoCoast). |
| `dataset` | Name of the BGS dataset (layer) the record belongs to. |

## bgs_geocoast_geocoast_v1_authority_coastline_cliff_erosion_mean

BGS GeoCoast: cliff erosion susceptibility of the coastline per local authority, mean scenario. Grain: one row per authority coastline. Source: British Geological Survey GeoCoast Open, distributed via the OS Data Hub Downloads API (shapefile, loaded to WGS84). It is a national screening dataset of coastal susceptibility to inundation (sea level rise) and cliff erosion for 2050, 2080 and 2100, not site-level hazard mapping. See the BGS GeoCoast documentation for methods and class definitions. Licence: Open Government Licence v3.0; contains British Geological Survey materials (c) UKRI.

| Column | Description |
|---|---|
| `adm_unit` | Name of the local authority (administrative unit) the record summarises. |
| `coast_km` | Length of coastline in the unit, kilometres. |
| `sections` | Number of coastal sections the unit has been divided into for the analysis. |
| `mean_km` | Length in kilometres of coastline susceptible to cliff erosion under the mean scenario. |
| `per_mean` | Percentage of the coastline susceptible to cliff erosion under the mean scenario. |
| `product` | Name of the BGS product the record belongs to (GeoCoast). |
| `dataset` | Name of the BGS dataset (layer) the record belongs to. |

## bgs_geocoast_geocoast_v1_authority_coastline_cliff_erosion_worst

BGS GeoCoast: cliff erosion susceptibility of the coastline per local authority, worst-case scenario. Grain: one row per authority coastline. Source: British Geological Survey GeoCoast Open, distributed via the OS Data Hub Downloads API (shapefile, loaded to WGS84). It is a national screening dataset of coastal susceptibility to inundation (sea level rise) and cliff erosion for 2050, 2080 and 2100, not site-level hazard mapping. See the BGS GeoCoast documentation for methods and class definitions. Licence: Open Government Licence v3.0; contains British Geological Survey materials (c) UKRI.

| Column | Description |
|---|---|
| `adm_unit` | Name of the local authority (administrative unit) the record summarises. |
| `coast_km` | Length of coastline in the unit, kilometres. |
| `sections` | Number of coastal sections the unit has been divided into for the analysis. |
| `high_km` | Length in kilometres of coastline in the highest cliff erosion class under the worst-case scenario. |
| `per_high` | Percentage of the coastline in the highest cliff erosion class under the worst-case scenario. |
| `product` | Name of the BGS product the record belongs to (GeoCoast). |
| `dataset` | Name of the BGS dataset (layer) the record belongs to. |

## bgs_geocoast_geocoast_v1_authority_coastline_inundation

BGS GeoCoast: coastline length and share susceptible to inundation by 2050, 2080 and 2100 per local authority. Grain: one row per authority coastline. Source: British Geological Survey GeoCoast Open, distributed via the OS Data Hub Downloads API (shapefile, loaded to WGS84). It is a national screening dataset of coastal susceptibility to inundation (sea level rise) and cliff erosion for 2050, 2080 and 2100, not site-level hazard mapping. See the BGS GeoCoast documentation for methods and class definitions. Licence: Open Government Licence v3.0; contains British Geological Survey materials (c) UKRI.

| Column | Description |
|---|---|
| `adm_unit` | Name of the local authority (administrative unit) the record summarises. |
| `coast_km` | Length of coastline in the unit, kilometres. |
| `sections` | Number of coastal sections the unit has been divided into for the analysis. |
| `inund2050` | Length in kilometres of coastline susceptible to inundation by 2050. |
| `per_2050` | Percentage of the coastline susceptible to inundation by 2050. |
| `inund2080` | Length in kilometres of coastline susceptible to inundation by 2080. |
| `per_2080` | Percentage of the coastline susceptible to inundation by 2080. |
| `inund2100` | Length in kilometres of coastline susceptible to inundation by 2100. |
| `per_2100` | Percentage of the coastline susceptible to inundation by 2100. |
| `product` | Name of the BGS product the record belongs to (GeoCoast). |
| `dataset` | Name of the BGS dataset (layer) the record belongs to. |

## bgs_geocoast_geocoast_v1_authority_coastline_multi_formations

BGS GeoCoast: coastline per local authority backed by more than one geological formation. Grain: one row per authority coastline. Source: British Geological Survey GeoCoast Open, distributed via the OS Data Hub Downloads API (shapefile, loaded to WGS84). It is a national screening dataset of coastal susceptibility to inundation (sea level rise) and cliff erosion for 2050, 2080 and 2100, not site-level hazard mapping. See the BGS GeoCoast documentation for methods and class definitions. Licence: Open Government Licence v3.0; contains British Geological Survey materials (c) UKRI.

| Column | Description |
|---|---|
| `adm_unit` | Name of the local authority (administrative unit) the record summarises. |
| `coast_km` | Length of coastline in the unit, kilometres. |
| `multi_km` | Length in kilometres of coastline with multiple geological formations. |
| `per_multi` | Percentage of the coastline with multiple geological formations. |
| `product` | Name of the BGS product the record belongs to (GeoCoast). |
| `dataset` | Name of the BGS dataset (layer) the record belongs to. |

## bgs_geocoast_geocoast_v1_erosion_profile_domains

BGS GeoCoast: coastal erosion and profile domains (polygons or lines classifying the coast by erosion susceptibility and profile). Grain: one row per domain segment. Source: British Geological Survey GeoCoast Open, distributed via the OS Data Hub Downloads API (shapefile, loaded to WGS84). It is a national screening dataset of coastal susceptibility to inundation (sea level rise) and cliff erosion for 2050, 2080 and 2100, not site-level hazard mapping. See the BGS GeoCoast documentation for methods and class definitions. Licence: Open Government Licence v3.0; contains British Geological Survey materials (c) UKRI.

| Column | Description |
|---|---|
| `product` | Name of the BGS product the record belongs to (GeoCoast). |
| `dataset` | Name of the BGS dataset (layer) the record belongs to. |
| `erosiondom` | Dominant erosion class of the coastal domain. |
| `erosionsus` | Erosion susceptibility class of the domain. |
| `erosionbac` | Erosion class of the backshore (land behind the cliff or beach). |
| `profiledom` | Dominant coastal profile type of the domain. |
| `profileh` | Profile height of the coastal domain (cliff or backshore height class). |
| `profiler` | Profile relief or ratio of the coastal domain. |
| `smp` | Shoreline Management Plan unit the domain belongs to. |

## bgs_geocoast_geocoast_v1_smp_coastline_cliff_erosion_mean

BGS GeoCoast: cliff erosion susceptibility per Shoreline Management Plan unit, mean scenario. Grain: one row per SMP unit. Source: British Geological Survey GeoCoast Open, distributed via the OS Data Hub Downloads API (shapefile, loaded to WGS84). It is a national screening dataset of coastal susceptibility to inundation (sea level rise) and cliff erosion for 2050, 2080 and 2100, not site-level hazard mapping. See the BGS GeoCoast documentation for methods and class definitions. Licence: Open Government Licence v3.0; contains British Geological Survey materials (c) UKRI.

| Column | Description |
|---|---|
| `lpd_smp` | Shoreline Management Plan (SMP) coastal sub-cell identifier or name that the record summarises. |
| `sections` | Number of coastal sections the unit has been divided into for the analysis. |
| `coast_km` | Length of coastline in the unit, kilometres. |
| `mean_km` | Length in kilometres of coastline susceptible to cliff erosion under the mean scenario. |
| `per_mean` | Percentage of the coastline susceptible to cliff erosion under the mean scenario. |
| `product` | Name of the BGS product the record belongs to (GeoCoast). |
| `dataset` | Name of the BGS dataset (layer) the record belongs to. |

## bgs_geocoast_geocoast_v1_smp_coastline_cliff_erosion_worst

BGS GeoCoast: cliff erosion susceptibility per Shoreline Management Plan unit, worst-case scenario. Grain: one row per SMP unit. Source: British Geological Survey GeoCoast Open, distributed via the OS Data Hub Downloads API (shapefile, loaded to WGS84). It is a national screening dataset of coastal susceptibility to inundation (sea level rise) and cliff erosion for 2050, 2080 and 2100, not site-level hazard mapping. See the BGS GeoCoast documentation for methods and class definitions. Licence: Open Government Licence v3.0; contains British Geological Survey materials (c) UKRI.

| Column | Description |
|---|---|
| `lpd_smp` | Shoreline Management Plan (SMP) coastal sub-cell identifier or name that the record summarises. |
| `sections` | Number of coastal sections the unit has been divided into for the analysis. |
| `coast_km` | Length of coastline in the unit, kilometres. |
| `high_km` | Length in kilometres of coastline in the highest cliff erosion class under the worst-case scenario. |
| `per_high` | Percentage of the coastline in the highest cliff erosion class under the worst-case scenario. |
| `product` | Name of the BGS product the record belongs to (GeoCoast). |
| `dataset` | Name of the BGS dataset (layer) the record belongs to. |

## bgs_geocoast_geocoast_v1_smp_coastline_inundation

BGS GeoCoast: coastline susceptible to inundation by 2050, 2080 and 2100 per Shoreline Management Plan unit. Grain: one row per SMP unit. Source: British Geological Survey GeoCoast Open, distributed via the OS Data Hub Downloads API (shapefile, loaded to WGS84). It is a national screening dataset of coastal susceptibility to inundation (sea level rise) and cliff erosion for 2050, 2080 and 2100, not site-level hazard mapping. See the BGS GeoCoast documentation for methods and class definitions. Licence: Open Government Licence v3.0; contains British Geological Survey materials (c) UKRI.

| Column | Description |
|---|---|
| `lpd_smp` | Shoreline Management Plan (SMP) coastal sub-cell identifier or name that the record summarises. |
| `sections` | Number of coastal sections the unit has been divided into for the analysis. |
| `coast_km` | Length of coastline in the unit, kilometres. |
| `inund2050` | Length in kilometres of coastline susceptible to inundation by 2050. |
| `per_2050` | Percentage of the coastline susceptible to inundation by 2050. |
| `inund2080` | Length in kilometres of coastline susceptible to inundation by 2080. |
| `per_2080` | Percentage of the coastline susceptible to inundation by 2080. |
| `inund2100` | Length in kilometres of coastline susceptible to inundation by 2100. |
| `per_2100` | Percentage of the coastline susceptible to inundation by 2100. |
| `product` | Name of the BGS product the record belongs to (GeoCoast). |
| `dataset` | Name of the BGS dataset (layer) the record belongs to. |

## bgs_geocoast_geocoast_v1_smp_coastline_length

BGS GeoCoast: total coastline length per Shoreline Management Plan unit. Grain: one row per SMP unit. Source: British Geological Survey GeoCoast Open, distributed via the OS Data Hub Downloads API (shapefile, loaded to WGS84). It is a national screening dataset of coastal susceptibility to inundation (sea level rise) and cliff erosion for 2050, 2080 and 2100, not site-level hazard mapping. See the BGS GeoCoast documentation for methods and class definitions. Licence: Open Government Licence v3.0; contains British Geological Survey materials (c) UKRI.

| Column | Description |
|---|---|
| `lpd_smp` | Shoreline Management Plan (SMP) coastal sub-cell identifier or name that the record summarises. |
| `sections` | Number of coastal sections the unit has been divided into for the analysis. |
| `coast_km` | Length of coastline in the unit, kilometres. |
| `product` | Name of the BGS product the record belongs to (GeoCoast). |
| `dataset` | Name of the BGS dataset (layer) the record belongs to. |

## bgs_geocoast_geocoast_v1_smp_coastline_multi_formations

BGS GeoCoast: coastline per Shoreline Management Plan unit backed by more than one geological formation. Grain: one row per SMP unit. Source: British Geological Survey GeoCoast Open, distributed via the OS Data Hub Downloads API (shapefile, loaded to WGS84). It is a national screening dataset of coastal susceptibility to inundation (sea level rise) and cliff erosion for 2050, 2080 and 2100, not site-level hazard mapping. See the BGS GeoCoast documentation for methods and class definitions. Licence: Open Government Licence v3.0; contains British Geological Survey materials (c) UKRI.

| Column | Description |
|---|---|
| `lpd_smp` | Shoreline Management Plan (SMP) coastal sub-cell identifier or name that the record summarises. |
| `coast_km` | Length of coastline in the unit, kilometres. |
| `multi_km` | Length in kilometres of coastline with multiple geological formations. |
| `per_multi` | Percentage of the coastline with multiple geological formations. |
| `product` | Name of the BGS product the record belongs to (GeoCoast). |
| `dataset` | Name of the BGS dataset (layer) the record belongs to. |

## desnz_repd

DESNZ Renewable Energy Planning Database (REPD): renewable electricity projects in the UK pipeline, from application through operation, with technology, capacity, planning status and location. Grain: one row per project (ref_id). Use as the energy asset location layer for the Resilience and Investment tracks. Coordinates were converted from OS National Grid (easting/northing) to WGS84. Source: DESNZ (gov.uk). Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `old_ref_id` | Previous REPD reference, where the project was re-registered. |
| `ref_id` | REPD reference number. Primary key. |
| `record_last_updated_dd_mm_yyyy` | Date the record was last updated (DD/MM/YYYY). |
| `operator_or_applicant` | Company operating or applying to build the site. |
| `site_name` | Name of the site. |
| `technology_type` | Technology, for example Solar Photovoltaics, Wind Onshore, Wind Offshore, Battery, Biomass. |
| `storage_type` | Storage technology for storage projects, for example Battery. |
| `storage_co_location_repd_ref_id` | REPD reference of a co-located generation project, if any. |
| `installed_capacity_mwelec` | Installed electrical capacity in megawatts (MWe). |
| `share_community_scheme` | Whether a share of the project is offered to the local community. |
| `chp_enabled` | Whether the site is a combined heat and power installation. |
| `cfd_allocation_round` | Contracts for Difference allocation round, if awarded. |
| `ro_banding_roc_mwh` | Renewables Obligation banding (ROCs per MWh). |
| `fit_tariff_p_kwh` | Feed-in Tariff rate in pence per kWh. |
| `cfd_capacity_mw` | Capacity awarded under a Contract for Difference, MW. |
| `turbine_capacity_mw` | Capacity of each wind turbine, MW. |
| `no_of_turbines` | Number of wind turbines. |
| `height_of_turbines_m` | Turbine tip height in metres. |
| `mounting_type_for_solar` | Solar mounting type, for example Ground or Roof. |
| `development_status` | Full development status, for example Operational, Awaiting Construction, Under Construction, Application Submitted, Planning Permission Expired. |
| `development_status_short` | Short development status: Operational, Under Construction, Awaiting Construction, Application Submitted, etc. |
| `are_they_re_applying_new_repd_ref` | New REPD reference if the applicant re-applied. |
| `are_they_re_applying_old_repd_ref` | Old REPD reference if the applicant re-applied. |
| `address` | Site address. |
| `county` | County. |
| `region` | Region (England) or nation. |
| `country` | Country. |
| `post_code` | Site postcode. |
| `x_coordinate` | OS National Grid easting as supplied (text with formatting). |
| `y_coordinate` | OS National Grid northing as supplied (text with formatting). |
| `planning_authority` | Local planning authority that handled the application. |
| `planning_application_reference` | Planning application reference. |
| `appeal_reference` | Planning appeal reference. |
| `secretary_of_state_reference` | Secretary of State case reference. |
| `type_of_secretary_of_state_intervention` | Type of Secretary of State intervention (call-in, recovery of appeal, etc.). |
| `judicial_review` | Judicial review status. |
| `offshore_wind_round` | Offshore wind leasing round. |
| `planning_application_submitted` | Date the planning application was submitted. |
| `planning_application_withdrawn` | Date the planning application was withdrawn. |
| `planning_permission_refused` | Date planning permission was refused. |
| `appeal_lodged` | Date an appeal was lodged. |
| `appeal_withdrawn` | Date the appeal was withdrawn. |
| `appeal_refused` | Date the appeal was refused. |
| `appeal_granted` | Date the appeal was granted. |
| `planning_permission_granted` | Date planning permission was granted. |
| `secretary_of_state_intervened` | Date the Secretary of State intervened. |
| `secretary_of_state_refusal` | Date the Secretary of State refused. |
| `secretary_of_state_granted` | Date the Secretary of State granted. |
| `planning_permission_expired` | Date planning permission expired. |
| `under_construction` | Date construction started. |
| `operational` | Date the site became operational. |
| `heat_network_ref` | Heat network reference, for heat projects. |
| `solar_site_area_sqm` | Area of a solar site in square metres. |
| `easting` | Parsed OS National Grid easting (metres, EPSG:27700) used to derive geom. |
| `northing` | Parsed OS National Grid northing (metres, EPSG:27700) used to derive geom. |

## dft_aadf

DfT road traffic counts: Average Annual Daily Flow (AADF) by count point, year and vehicle class, for major and minor roads in Great Britain. Grain: one row per count point per year. Use for traffic demand on the road network; join to os_open_roads_links by H3 or ST_ distance. Source: DfT road traffic statistics. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `count_point_id` | Unique id of the traffic count point. |
| `year` | Calendar year of the AADF estimate. |
| `region_id` | DfT region id. |
| `region_name` | Region name. |
| `region_ons_code` | ONS code of the region. |
| `local_authority_id` | DfT local authority id. |
| `local_authority_name` | Local authority name. |
| `local_authority_code` | ONS code of the local authority. |
| `road_name` | Road number or name, for example 'A1' or 'M25'. |
| `road_category` | Road category: PA = principal A road, TA = trunk A road, PM = principal (non-trunk) motorway, TM = trunk motorway, M = minor road, etc. |
| `road_type` | Major or Minor road. |
| `start_junction_road_name` | Road name at the start junction of the link. |
| `end_junction_road_name` | Road name at the end junction of the link. |
| `easting` | Easting of the count point, OS National Grid (EPSG:27700), metres. |
| `northing` | Northing of the count point, OS National Grid (EPSG:27700), metres. |
| `latitude` | Latitude of the count point, WGS84, as supplied by DfT. |
| `longitude` | Longitude of the count point, WGS84, as supplied by DfT. |
| `link_length_km` | Length of the road link represented by the count point, kilometres. |
| `link_length_miles` | Length of the road link represented by the count point, miles. |
| `estimation_method` | How the AADF was derived: Counted (manual count that year) or Estimated. |
| `estimation_method_detailed` | Detailed estimation method, for example 'Counted', 'Estimated using previous year's AADF on this link'. |
| `pedal_cycles` | Average annual daily flow (vehicles per day, both directions) of pedal cycles. |
| `two_wheeled_motor_vehicles` | Average annual daily flow (vehicles per day, both directions) of two-wheeled motor vehicles (motorcycles, mopeds, scooters). |
| `cars_and_taxis` | Average annual daily flow (vehicles per day, both directions) of cars and taxis. |
| `buses_and_coaches` | Average annual daily flow (vehicles per day, both directions) of buses and coaches. |
| `lgvs` | Average annual daily flow (vehicles per day, both directions) of light goods vehicles (vans up to 3.5 tonnes). |
| `hgvs_2_rigid_axle` | Average annual daily flow (vehicles per day, both directions) of heavy goods vehicles, 2-axle rigid. |
| `hgvs_3_rigid_axle` | Average annual daily flow (vehicles per day, both directions) of heavy goods vehicles, 3-axle rigid. |
| `hgvs_4_or_more_rigid_axle` | Average annual daily flow (vehicles per day, both directions) of heavy goods vehicles, 4 or more axle rigid. |
| `hgvs_3_or_4_articulated_axle` | Average annual daily flow (vehicles per day, both directions) of heavy goods vehicles, 3 or 4 axle articulated. |
| `hgvs_5_articulated_axle` | Average annual daily flow (vehicles per day, both directions) of heavy goods vehicles, 5 axle articulated. |
| `hgvs_6_articulated_axle` | Average annual daily flow (vehicles per day, both directions) of heavy goods vehicles, 6 or more axle articulated. |
| `all_hgvs` | Average annual daily flow (vehicles per day, both directions) of all heavy goods vehicles (sum of the HGV classes). |
| `all_motor_vehicles` | Average annual daily flow (vehicles per day, both directions) of all motor vehicles (excludes pedal cycles). |

## dft_evci_constituency

DfT public electric vehicle charger counts by Westminster parliamentary constituency (UK), long format, by quarter. Join to nspl.pcon24cd or os_boundary_line_westminster_const on area_code. Source: DfT electric vehicle charging infrastructure statistics, data tables (EVCI, July 2026 release), from the National Chargepoint Registry. Licence: Open Government Licence v3.0. Area counts only; device locations are not openly published.

| Column | Description |
|---|---|
| `area_code` | ONS code of the area (local authority district, or Westminster parliamentary constituency). |
| `area_name` | Name of the area. |
| `table_ref` | DfT worksheet the value came from (for example EVCI0102a). |
| `measure` | What is measured: public chargers, public 50kW+ (rapid) chargers, or either per 100,000 population, with the geography. |
| `quarter_start` | First day of the quarter the value is for (the DfT snapshot date, for example 2026-07-01). |
| `value` | Number of public chargers, or chargers per 100,000 population, depending on measure. |

## dft_evci_local_authority

DfT public electric vehicle charger counts by local authority district (UK), long format: counts and rates per 100,000 population for all public chargers and for 50kW+ chargers, by quarter. Use as the area baseline for EV charging gaps (Access & equity). Join to nspl.lad26cd or os_boundary_line_* census_code on area_code. Point locations: see overture_places with category 'ev_charging_station'. Source: DfT electric vehicle charging infrastructure statistics, data tables (EVCI, July 2026 release), from the National Chargepoint Registry. Licence: Open Government Licence v3.0. Area counts only; device locations are not openly published.

| Column | Description |
|---|---|
| `area_code` | ONS code of the area (local authority district, or Westminster parliamentary constituency). |
| `area_name` | Name of the area. |
| `table_ref` | DfT worksheet the value came from (for example EVCI0102a). |
| `measure` | What is measured: public chargers, public 50kW+ (rapid) chargers, or either per 100,000 population, with the geography. |
| `quarter_start` | First day of the quarter the value is for (the DfT snapshot date, for example 2026-07-01). |
| `value` | Number of public chargers, or chargers per 100,000 population, depending on measure. |

## ea_flood_areas

Environment Agency flood areas: the geographic areas used for flood alerts and warnings in England, from the real-time flood-monitoring API, with a centroid. Grain: one row per flood area. Join to ea_flood_warnings on area_id. The polygon itself is behind polygon_url (GeoJSON). Snapshot taken when the loader ran. Hackathon track: Resilience & risk. Source: EA flood-monitoring API. Licence: Open Government Licence v3.0; contains Environment Agency information (c) Environment Agency copyright and database right.

| Column | Description |
|---|---|
| `area_id` | Flood area code (notation). Primary key. |
| `label` | Short label for the flood area. |
| `description` | Human-readable description of the area covered. |
| `river_or_sea` | River or sea the flood area relates to. |
| `county` | County or counties the area falls in. |
| `polygon_url` | URL of the GeoJSON polygon for the flood area on the EA API. |

## ea_flood_defences

Environment Agency Asset Information Management System (AIMS) spatial flood defences: about 141,000 flood and coastal defence assets in England (walls, embankments, high ground, culverts, barriers) as lines, with owner, maintainer, standard of protection, crest levels and inspection dates. The only open national asset inventory with condition data. IMPORTANT: current_condition is empty for about three quarters of assets, so condition analysis covers only the assessed subset; do not read a missing grade as 'good'. Grain: one row per asset (asset_id; an asset can appear on both banks). Hackathon tracks: Investment & prioritisation (core), Resilience. Source: Environment Agency, Spatial Flood Defences including standardised attributes (AIMS), OGC API Features. Licence: Open Government Licence v3.0; contains Environment Agency information (c) Environment Agency copyright and database right.

| Column | Description |
|---|---|
| `asset_id` | Environment Agency asset identifier. |
| `asset_name` | Asset name. 'Not Available' where unnamed. |
| `asset_sub_type` | Asset type, for example Wall, Embankment, Natural High Ground, Culvert, Barrier, Sluice. |
| `primary_purpose` | Main purpose of the asset, for example Flood Risk Management or Coastal Defence. |
| `alternative_purpose_1` | Secondary purpose, if any. |
| `alternative_purpose_2` | Third purpose, if any. |
| `asset_length` | Length of the asset in metres. |
| `toe_level` | Level of the asset toe, metres above Ordnance Datum. |
| `protection_type` | Type of flooding the asset protects against, for example Fluvial (river), Tidal or Coastal. |
| `asset_maintainer` | Organisation or party responsible for maintaining the asset. |
| `asset_operator` | Organisation that operates the asset. |
| `asset_owner` | Owner of the asset ('Unknown' where not recorded). |
| `current_condition` | Condition grade from the latest inspection, 1 (very good) to 5 (very poor); 0 or missing means not assessed or not applicable. Empty for most assets. |
| `target_condition` | Condition grade the asset is intended to be maintained at, same 1 to 5 scale. |
| `current_sop` | Current standard of protection the asset provides (AIMS convention, see the product description). |
| `current_sop_date` | Date the current standard of protection was assessed. |
| `design_sop` | Standard of protection the asset was designed to provide (AIMS convention, see the product description). |
| `design_sop_dqf` | Data quality flag for design_sop. |
| `design_ucl` | Design upstream crest level, metres above Ordnance Datum. |
| `year_last_refurbished` | Year the asset was last refurbished. |
| `last_inspection_date` | Date of the last inspection. |
| `next_inspection_date` | Date the next inspection is due. |
| `asset_start_date` | Date the asset was built or came into service. |
| `actual_dcl` | Actual downstream crest level, metres above Ordnance Datum. |
| `actual_dcl_dqf` | Data quality flag for actual_dcl (for example a crest level data quality class). |
| `actual_ucl` | Actual upstream crest level, metres above Ordnance Datum. |
| `actual_ucl_dqf` | Data quality flag for actual_ucl. |
| `design_dcl` | Design downstream crest level, metres above Ordnance Datum. |
| `bank` | Which bank the asset is on: Left, Right or Both (looking downstream). |
| `effective_cl` | Effective crest level, the lowest point that controls the protection level, metres above Ordnance Datum. |
| `effective_cl_dqf` | Data quality flag for effective_cl. |
| `include_in_flood_map` | Whether the asset is used in the national flood map modelling (Yes or No). |
| `water_management_area` | EA water management area the asset is in. |
| `local_authority` | Local authority the asset is in. |
| `frms_code` | Flood and Coastal Risk Management scheme code the asset belongs to, if any. |
| `water_course_name` | Name of the watercourse the asset sits on. |
| `gdb_geomattr_data` | Internal geodatabase geometry attribute carried over from the source; not meaningful for analysis. |

## ea_flood_warnings

Environment Agency current flood alerts and warnings at the time the loader ran (a point-in-time snapshot, often empty or small in dry weather). Grain: one row per active warning. Join to ea_flood_areas on area_id. Source: EA flood-monitoring API. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `area_id` | Flood area code. Joins to ea_flood_areas.area_id. |
| `severity` | Severity label: Flood alert, Flood warning, Severe flood warning or Warning no longer in force. |
| `severity_level` | Numeric severity: 1 = severe flood warning, 2 = flood warning, 3 = flood alert, 4 = no longer in force. |
| `message` | Free-text message issued by the Environment Agency. |
| `time_raised` | When the warning was raised (ISO 8601 text). |
| `ea_area` | Environment Agency area that issued the warning. |
| `snapshot_ts` | When this snapshot was loaded. |

## ea_rofrs_postcodes

Environment Agency Risk of Flooding from Rivers and Sea (RoFRS), postcodes in areas at risk: counts of residential, non-residential and unclassified properties per postcode in each flood risk band (very low, low, medium, high). Grain: one row per postcode unit. Join to nspl on postcode (nspl.pcds with the space removed as needed). Only postcodes with properties at some risk are present. Hackathon track: Resilience & risk. Risk bands are annual chance of flooding ignoring defences' failure. Source: Environment Agency via data.gov.uk. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `pc` | Postcode (unit level) with properties in an area at risk of flooding from rivers and sea. |
| `cntpc` | Total number of properties (residential, non-residential and unclassified) in the postcode. |
| `res_cntpc` | Number of residential properties in the postcode. |
| `nrp_cntpc` | Number of non-residential properties in the postcode. |
| `unc_cntpc` | Number of unclassified properties in the postcode. |
| `sortoff` | Sort key for the postcode (postcode without spaces). |
| `district` | Postcode district (outward code), for example 'CB4'. |
| `sector` | Postcode sector, for example 'CB4 1'. |
| `unit` | Full postcode unit, for example 'CB4 1AB'. |
| `res_cnt_verylow` | Residential properties in the postcode at very low (less than 0.1% chance in any year) risk of flooding from rivers and sea. |
| `nrp_cnt_verylow` | Non-residential properties in the postcode at very low (less than 0.1% chance in any year) risk of flooding from rivers and sea. |
| `unc_cnt_verylow` | Unclassified properties in the postcode at very low (less than 0.1% chance in any year) risk of flooding from rivers and sea. |
| `tot_cnt_verylow` | All properties in the postcode at very low (less than 0.1% chance in any year) risk of flooding from rivers and sea. |
| `res_cnt_low` | Residential properties in the postcode at low (0.1% to 1% chance in any year) risk of flooding from rivers and sea. |
| `nrp_cnt_low` | Non-residential properties in the postcode at low (0.1% to 1% chance in any year) risk of flooding from rivers and sea. |
| `unc_cnt_low` | Unclassified properties in the postcode at low (0.1% to 1% chance in any year) risk of flooding from rivers and sea. |
| `tot_cnt_low` | All properties in the postcode at low (0.1% to 1% chance in any year) risk of flooding from rivers and sea. |
| `res_cnt_medium` | Residential properties in the postcode at medium (1% to 3.3% chance in any year) risk of flooding from rivers and sea. |
| `nrp_cnt_medium` | Non-residential properties in the postcode at medium (1% to 3.3% chance in any year) risk of flooding from rivers and sea. |
| `unc_cnt_medium` | Unclassified properties in the postcode at medium (1% to 3.3% chance in any year) risk of flooding from rivers and sea. |
| `tot_cnt_medium` | All properties in the postcode at medium (1% to 3.3% chance in any year) risk of flooding from rivers and sea. |
| `res_cnt_high` | Residential properties in the postcode at high (3.3% or greater chance in any year) risk of flooding from rivers and sea. |
| `nrp_cnt_high` | Non-residential properties in the postcode at high (3.3% or greater chance in any year) risk of flooding from rivers and sea. |
| `unc_cnt_high` | Unclassified properties in the postcode at high (3.3% or greater chance in any year) risk of flooding from rivers and sea. |
| `tot_cnt_high` | All properties in the postcode at high (3.3% or greater chance in any year) risk of flooding from rivers and sea. |

## ea_stations

Environment Agency monitoring stations (river level, flow, rainfall and tidal gauges) from the real-time flood-monitoring API. Grain: one row per station. Tidal stations help with the coastal surge part of the Resilience track. Hackathon track: Resilience & risk. Source: EA flood-monitoring API. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `station_id` | Station reference (notation). Primary key. |
| `label` | Station name. |
| `river_name` | River the station is on, if any. |
| `town` | Nearest town. |
| `catchment` | Name of the river catchment. |
| `station_type` | Station type as reported by the API. |
| `measures` | List (as text) of parameters measured at the station, for example level, flow, rainfall. |

## emodnet_bathymetry

EMODnet Bathymetry digital terrain model (2022 release) for UK and Irish waters and coasts, block-averaged from its native 1/16 arc-minute grid (about 115 m) to cells of about 0.0104 degrees (about 1.2 km north-south, narrower east-west). depth_m is negative below sea level and positive for land elevation; values outside -400 m to +60 m are removed to keep the continental shelf and coast. This is a European compilation; it is suitable for regional analysis, not navigation or engineering. One row per cell centre. Hackathon track: Resilience & risk (coastal exposure). Source: EMODnet (European Marine Observation and Data Network), served by OGC WCS and clipped to the UK and Ireland (-12 to 4 degrees longitude, 48 to 62 degrees latitude). Licence: EMODnet data are open with attribution required (CC BY 4.0); cite EMODnet and the original data provider (EMSA for vessel density).

| Column | Description |
|---|---|
| `lon` | Longitude of the cell centre, WGS84. |
| `lat` | Latitude of the cell centre, WGS84. |
| `depth_m` | Mean depth or elevation of the cell in metres relative to Lowest Astronomical Tide (negative = below sea level, positive = land), rounded to 0.1 m. |

## emodnet_vessel_density

Vessel traffic density from EMODnet Human Activities (derived by EMSA from terrestrial and satellite AIS positions): annual averages of monthly density for 2022 to 2024, for all vessel types and for 13 vessel type groups, around UK and Irish waters. A measure of vessel traffic around the UK. This is a gridded density product (cells about 1.4 to 1.8 km across), NOT vessel tracks, so it cannot show routes, speeds or individual vessels. Only cells with traffic are present (zero cells omitted). Each row is a grid cell centre: several cells can fall in one H3 res 8 hexagon, so aggregate (sum or mean) by h3_8 before joining. Years before 2022 are listed by the service but not served. Grain: one row per year, vessel type and cell. Hackathon tracks: Investment & prioritisation (vessel traffic demand), Resilience. Source: EMODnet (European Marine Observation and Data Network), served by OGC WCS and clipped to the UK and Ireland (-12 to 4 degrees longitude, 48 to 62 degrees latitude). Licence: EMODnet data are open with attribution required (CC BY 4.0); cite EMODnet and the original data provider (EMSA for vessel density).

| Column | Description |
|---|---|
| `year` | Year of the annual average (2022, 2023 or 2024). |
| `vessel_type_code` | EMSA vessel type group code: 00 Other, 01 Fishing, 02 Service, 03 Dredging or underwater ops, 04 Sailing, 05 Pleasure Craft, 06 High speed craft, 07 Tug and towing, 08 Passenger, 09 Cargo, 10 Tanker, 11 Military and Law Enforcement, 12 Unknown, all = every type combined. |
| `vessel_type` | Name of the vessel type group. 'All types' is the sum of the others; do not add it to them. |
| `density` | Vessel density at the cell, as defined by the EMODnet product (vessel presence in hours per square kilometre per month, annual average). Larger = busier. Check the EMODnet metadata for the exact unit. |
| `lon` | Longitude of the grid cell centre, WGS84. |
| `lat` | Latitude of the grid cell centre, WGS84. |

## gtfs_agency

BODS GTFS agency.txt: the bus operators (agencies) in the Bus Open Data Service national timetable feed. Grain: one row per operator. Join to gtfs_routes on agency_id. Source: DfT Bus Open Data Service (BODS). Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `agency_id` | Operator identifier within the feed. Primary key. |
| `agency_name` | Operator name. |
| `agency_url` | Operator website. |
| `agency_timezone` | Timezone of the operator, normally Europe/London. |
| `agency_lang` | Primary language of the operator. |
| `agency_phone` | Operator customer contact number. |
| `agency_noc` | National Operator Code (NOC), the unique DfT code for the operator. |

## gtfs_calendar

BODS GTFS calendar.txt: the weekly pattern and date range during which each timetable service runs. Grain: one row per service_id. Join to gtfs_trips on service_id. Bank-holiday exceptions (calendar_dates.txt) are not loaded. Source: DfT Bus Open Data Service. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `service_id` | Service pattern identifier. Primary key; referenced by gtfs_trips.service_id. |
| `monday` | 1 if the service runs on Mondays within the date range, else 0. |
| `tuesday` | 1 if the service runs on Tuesdays within the date range, else 0. |
| `wednesday` | 1 if the service runs on Wednesdays within the date range, else 0. |
| `thursday` | 1 if the service runs on Thursdays within the date range, else 0. |
| `friday` | 1 if the service runs on Fridays within the date range, else 0. |
| `saturday` | 1 if the service runs on Saturdays within the date range, else 0. |
| `sunday` | 1 if the service runs on Sundays within the date range, else 0. |
| `start_date` | First date the service pattern is valid (YYYYMMDD). |
| `end_date` | Last date the service pattern is valid (YYYYMMDD). |

## gtfs_routes

BODS GTFS routes.txt: bus routes (line numbers) in the national timetable feed. Grain: one row per route. Join to gtfs_agency on agency_id and to gtfs_trips on route_id. Source: DfT Bus Open Data Service. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `route_id` | Route identifier. Primary key; referenced by gtfs_trips.route_id. |
| `agency_id` | Operator that runs the route. Joins to gtfs_agency.agency_id. |
| `route_short_name` | Public line number or name, for example '42' or 'X5'. |
| `route_long_name` | Full route description, often origin and destination. May be empty. |
| `route_type` | GTFS route type code; buses are 3. |

## gtfs_stop_times

BODS GTFS stop_times.txt: the scheduled arrival and departure at every stop for every bus trip in the national feed. Very large (hundreds of millions of rows). Grain: one row per trip and stop sequence. Join to gtfs_trips on trip_id and gtfs_stops on stop_id. Use to compute service frequency and journey times per stop or H3 cell. Source: DfT Bus Open Data Service. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `trip_id` | Trip the stop time belongs to. Joins to gtfs_trips.trip_id. |
| `arrival_time` | Scheduled arrival time (HH:MM:SS). Can exceed 24:00:00 for trips running past midnight. |
| `departure_time` | Scheduled departure time (HH:MM:SS). Can exceed 24:00:00. |
| `stop_id` | Stop served. Joins to gtfs_stops.stop_id (ATCO code). |
| `stop_sequence` | Order of the stop within the trip, ascending. |
| `stop_headsign` | Destination text shown on the vehicle at this stop, if it differs from the trip headsign. |
| `pickup_type` | Pick-up rule: 0 = regular, 1 = none, 2 = phone agency, 3 = coordinate with driver. |
| `drop_off_type` | Drop-off rule: 0 = regular, 1 = none, 2 = phone agency, 3 = coordinate with driver. |
| `shape_dist_traveled` | Distance along the route shape to this stop, in the feed's units. Often empty. |
| `timepoint` | 1 if the times are exact (timing point), 0 if approximate. |

## gtfs_stops

BODS GTFS stops.txt: bus stops used by the national timetable feed, with coordinates. Grain: one row per stop_id (ATCO code). Join to naptan_stops on atcocode = stop_id for richer attributes and to gtfs_stop_times on stop_id. Source: DfT Bus Open Data Service. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `stop_id` | Stop identifier, equal to the NaPTAN ATCO code. Primary key. |
| `stop_code` | Public stop code shown to passengers (NaPTAN code). |
| `stop_name` | Stop name as shown in timetables. |
| `stop_lat` | Latitude as supplied in the feed, WGS84 (string-typed copy of lat). |
| `stop_lon` | Longitude as supplied in the feed, WGS84 (string-typed copy of lon). |
| `wheelchair_boarding` | Wheelchair boarding: 0 = unknown, 1 = some vehicles can board, 2 = not possible. |
| `location_type` | GTFS location type: 0 = stop, 1 = station, 2 = entrance, 3 = generic node, 4 = boarding area. |
| `parent_station` | Parent station stop_id, if the stop is part of a larger station. |
| `platform_code` | Platform or bay identifier at a station. |

## gtfs_trips

BODS GTFS trips.txt: each scheduled bus journey in the national timetable feed. Grain: one row per trip. Join to gtfs_routes on route_id, gtfs_calendar on service_id and gtfs_stop_times on trip_id. Source: DfT Bus Open Data Service. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `route_id` | Route the trip runs on. Joins to gtfs_routes.route_id. |
| `service_id` | Service calendar the trip follows. Joins to gtfs_calendar.service_id. |
| `trip_id` | Trip identifier. Primary key; referenced by gtfs_stop_times.trip_id. |
| `trip_headsign` | Destination text shown on the vehicle. |
| `direction_id` | Direction of travel: 0 = outbound, 1 = inbound. |
| `block_id` | Vehicle block the trip belongs to (trips run by the same vehicle in sequence). |
| `shape_id` | Route shape identifier (shapes are not loaded). |
| `wheelchair_accessible` | Wheelchair access: 0 = unknown, 1 = accessible, 2 = not accessible. |
| `vehicle_journey_code` | Operator's journey code from the source TransXChange timetable. |

## lsoa_2021_boundaries

2021 Census Lower layer Super Output Area (LSOA) boundaries for England and Wales, generalised and clipped to the coastline (BGC, V5). About 35,700 polygons of roughly 1,500 residents each. Use to aggregate postcode, census and point data into neighbourhood-scale areas. Grain: one row per LSOA. Join to nspl on lsoa21cd. Hackathon tracks: Access & equity, Resilience. Source: ONS Open Geography Portal. Licence: Open Government Licence v3.0; contains OS data (c) Crown copyright.

| Column | Description |
|---|---|
| `lsoa21cd` | LSOA 2021 code, for example 'E01000001'. Primary key. |
| `lsoa21nm` | LSOA 2021 name, usually local authority plus a letter suffix, for example 'City of London 001A'. |

## naptan_stops

National Public Transport Access Nodes (NaPTAN): every bus stop, rail station, tram and metro stop, ferry terminal, airport and coach bay in Great Britain, with name, locality and type. Grain: one row per access node (atcocode). Use for stop-density and distance-to-stop access scoring. Join to gtfs_stops on atcocode = stop_id (BODS uses ATCO codes as stop ids). Hackathon tracks: Access & equity (core), Investment. Source: DfT NaPTAN API. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `atcocode` | ATCO code, the national unique identifier for the stop. Primary key. Matches gtfs_stops.stop_id for bus stops. |
| `naptancode` | Short public code shown on bus stop flags and used for SMS/web lookup. |
| `platecode` | Code printed on the stop plate (often the same as naptancode). |
| `cleardowncode` | Legacy clear-down code used by some operators for stop identification. |
| `commonname` | Common name of the stop as used in timetables, for example 'High Street'. |
| `commonnamelang` | Language code of commonname (for example 'en', 'cy'). |
| `shortcommonname` | Abbreviated stop name for space-constrained displays. |
| `shortcommonnamelang` | Language code of shortcommonname. |
| `landmark` | Nearby landmark used to disambiguate the stop. |
| `landmarklang` | Language code of landmark. |
| `street` | Name of the street the stop is on. |
| `streetlang` | Language code of street. |
| `crossing` | Nearby crossing, where recorded. |
| `crossinglang` | Language code of crossing. |
| `indicator` | Short text identifying the stop on the street, for example 'opp', 'adj', 'o/s' or 'Stop A'. |
| `indicatorlang` | Language code of indicator. |
| `bearing` | Compass direction the vehicles at the stop are heading: N, NE, E, SE, S, SW, W or NW. |
| `nptglocalitycode` | National Public Transport Gazetteer (NPTG) locality code the stop belongs to. |
| `localityname` | Name of the locality. |
| `parentlocalityname` | Name of the parent locality (often the town). |
| `grandparentlocalityname` | Name of the grandparent locality (often the district). |
| `town` | Town name as recorded on the stop. |
| `townlang` | Language code of town. |
| `suburb` | Suburb name as recorded on the stop. |
| `suburblang` | Language code of suburb. |
| `localitycentre` | 1 if the stop coordinate is the centre of the locality, else 0. |
| `gridtype` | Grid used for easting/northing: U = UK OS National Grid, I = Irish Grid. |
| `easting` | Easting of the stop, in the grid named by gridtype, metres. |
| `northing` | Northing of the stop, in the grid named by gridtype, metres. |
| `longitude` | Longitude of the stop, WGS84, as supplied by NaPTAN. |
| `latitude` | Latitude of the stop, WGS84, as supplied by NaPTAN. |
| `stoptype` | NaPTAN stop type code, for example BCT = on-street bus/coach/tram stop, BCS = bus/coach station bay, RSE = rail station entrance, PLT = rail platform, FER = ferry entrance, AIR = airport entrance, MET = metro/tram entrance. |
| `busstoptype` | Bus stop type: MKD = marked (pole/flag), HAR = hail and ride, CUS = custom, FLX = flexible zone. Only for bus stop types. |
| `timingstatus` | Timing point status: PTP = principal timing point, TIP = timing point, OTH = other, OTH = not a timing point. |
| `defaultwaittime` | Default wait time at the stop, in minutes. |
| `notes` | Free-text notes on the stop. |
| `noteslang` | Language code of notes. |
| `administrativeareacode` | NPTG administrative area code responsible for the stop. |
| `creationdatetime` | When the stop record was created. |
| `modificationdatetime` | When the stop record was last modified. |
| `revisionnumber` | Revision count of the record. |
| `modification` | Type of last modification: new, revise or delete. |
| `status` | Record status: active, inactive or pending. |

## nged_connection_queue

NGED connection queue: pending and accepted connection applications for generation and storage by supply point, in queue order. Shows where new energy assets are waiting to connect. 45 per-area files combined; source_file records which. Grain: one row per machine in an application. Hackathon track: Investment & prioritisation. Source: National Grid Electricity Distribution (NGED) Connected Data portal (East Midlands, West Midlands, South West and South Wales licence areas only). Licence: NGED open data licence (CC BY 4.0 style; check the portal terms).

| Column | Description |
|---|---|
| `licence_area` | NGED licence area the application is in. |
| `gsp` | Grid supply point the application connects behind. |
| `tanm` | Transmission-area network model identifier for the supply point. |
| `danm` | Distribution-area network model identifier for the supply point. |
| `status` | Application status, for example Connected, Accepted or Offered. |
| `bus_number` | Network model bus number. |
| `bus_name` | Network model bus (substation) name. |
| `site_id` | Identifier of the site. |
| `application_id` | Identifier of the connection application. |
| `site_export_capacity_mw` | Site export capacity in MW. |
| `site_import_capacity_mw` | Site import capacity in MW. |
| `machine_export_capacity_mw` | Export capacity of the individual machine (generator or storage unit) in MW. |
| `machine_import_capacity_mw` | Import capacity of the individual machine in MW. |
| `fuel_type` | Fuel or technology of the machine, for example Solar, Wind, Battery, Gas. |
| `machine_id` | Identifier of the machine within the site. |
| `position` | Position in the connection queue. |
| `source_file` | Name of the NGED per-area file the row came from. |

## nged_embedded_capacity_register

NGED Embedded Capacity Register: generators and storage connected to, or accepted to connect to, the NGED distribution network (Midlands, South West, Wales), with technology, registered capacity, connection status and dates. Energy asset locations for the Resilience and Investment tracks. DATA PROTECTION: the source publishes customer names, addresses, postcodes and meter point identifiers, which can identify individuals for domestic installations. Use technology, capacity, status and location; do not join or publish the identity columns. Some coordinates are masked by NGED and give a null geom. Grain: one row per registered connection. Source: National Grid Electricity Distribution (NGED) Connected Data portal (East Midlands, West Midlands, South West and South Wales licence areas only). Licence: NGED open data licence (CC BY 4.0 style; check the portal terms).

| Column | Description |
|---|---|
| `export_mpan_msid` | Meter point (MPAN or MSID) identifier for the export connection. Supply-point identifier; treat with care. |
| `import_mpan_msid` | Meter point (MPAN or MSID) identifier for the import connection. Supply-point identifier; treat with care. |
| `customer_name` | Name of the connected customer as published by NGED. May identify a person or small business. |
| `customer_site` | Name of the customer's site. |
| `address_line_1` | Site address, line 1. Personal data risk for domestic sites. |
| `address_line_2` | Site address, line 2. |
| `town_city` | Town or city. |
| `county` | County. |
| `postcode` | Site postcode. |
| `country` | Country. |
| `location_x_coordinate_eastings_where_data_is_held` | Easting, OS National Grid (EPSG:27700), where held. 'REDACTED' where NGED withheld it. |
| `location_y_coordinate_northings_where_data_is_held` | Northing, OS National Grid (EPSG:27700), where held. 'REDACTED' where NGED withheld it. |
| `grid_supply_point` | Grid supply point the site is connected behind. |
| `bulk_supply_point` | Bulk supply point the site is connected behind. |
| `primary` | Primary substation the site is connected behind. |
| `point_of_connection_poc_voltage_kv` | Voltage at the point of connection, kV. |
| `licence_area` | NGED licence area. |
| `flexible_connection_yes_no` | Whether the connection is a flexible (curtailable) connection. |
| `connection_status` | Connection status: Connected, Accepted to Connect, etc. |
| `already_connected_registered_capacity_mw` | Registered capacity already connected, MW. |
| `connected_maximum_export_capacity_mw` | Connected maximum export capacity, MW. |
| `connected_maximum_export_capacity_mva` | Connected maximum export capacity, MVA. |
| `connected_maximum_import_capacity_mw` | Connected maximum import capacity, MW. |
| `connected_maximum_import_capacity_mva` | Connected maximum import capacity, MVA. |
| `date_connected` | Date the connection was made. |
| `accepted_to_connect_registered_capacity_mw` | Registered capacity accepted but not yet connected, MW. |
| `accepted_change_to_maximum_export_capacity_mw` | Accepted change to maximum export capacity, MW. |
| `accepted_change_to_maximum_export_capacity_mva` | Accepted change to maximum export capacity, MVA. |
| `accepted_change_to_maximum_import_capacity_mw` | Accepted change to maximum import capacity, MW. |
| `accepted_change_to_maximum_import_capacity_mva` | Accepted change to maximum import capacity, MVA. |
| `date_accepted` | Date the offer was accepted. |
| `target_energisation_date` | Target date to energise the connection. |
| `distribution_service_provider_y_n` | Whether the customer provides distribution services. |
| `transmission_service_provider_y_n` | Whether the customer provides transmission services. |
| `reference` | NGED reference for the record. |
| `in_a_connection_queue_y_n` | Whether the project is also in the connection queue. |
| `distribution_reinforcement_reference` | Reference of distribution network reinforcement the connection depends on. |
| `transmission_reinforcement_reference` | Reference of transmission reinforcement the connection depends on. |
| `last_updated` | Date the record was last updated. |
| `local_authority` | Local authority area derived by the loader from location, if present. |
| `energy_source_1` | Energy source 1 of the site (for example Solar, Wind, Battery, Gas). |
| `energy_conversion_technology_1` | Conversion technology for energy source 1 (for example Photovoltaic, Onshore Wind, Battery). |
| `chp_cogeneration_yes_no` | Whether energy source 1 is combined heat and power. |
| `storage_capacity_1_mwh` | Storage energy capacity for source 1, MWh. |
| `storage_duration_1_hours` | Storage duration for source 1, hours. |
| `energy_source_conversion_tech_1_reg_capacity_mw` | Registered capacity for source 1, MW. |
| `energy_source_2` | Energy source 2 of the site (for example Solar, Wind, Battery, Gas). |
| `energy_conversion_technology_2` | Conversion technology for energy source 2 (for example Photovoltaic, Onshore Wind, Battery). |
| `chp_cogeneration2_yes_no` | Whether energy source 2 is combined heat and power. |
| `storage_capacity_2_mwh` | Storage energy capacity for source 2, MWh. |
| `storage_duration_2_hours` | Storage duration for source 2, hours. |
| `energy_source_conversion_tech_2_reg_capacity_mw` | Registered capacity for source 2, MW. |
| `energy_source_3` | Energy source 3 of the site (for example Solar, Wind, Battery, Gas). |
| `energy_conversion_technology_3` | Conversion technology for energy source 3 (for example Photovoltaic, Onshore Wind, Battery). |
| `chp_cogeneration3_yes_no` | Whether energy source 3 is combined heat and power. |
| `storage_capacity_3_mwh` | Storage energy capacity for source 3, MWh. |
| `storage_duration_3_hours` | Storage duration for source 3, hours. |
| `energy_source_conversion_tech_3_reg_capacity_mw` | Registered capacity for source 3, MW. |

## nged_ltds_capacity_heatmap

NGED Long Term Development Statement capacity heatmap: for each substation (primary, bulk supply point, grid supply point) the firm capacity, available demand and generation headroom, constraint status and the pipeline of connection offers. Covers the Midlands, South West and Wales licence areas only. Use demandavailablecapacity and generationavailablecapacity to find where new load (EV charging, heat pumps) or generation can connect. Capacities are as published, in MW or MVA per NGED's heatmap definitions. Grain: one row per substation. Hackathon tracks: Access & equity, Investment & prioritisation. Source: National Grid Electricity Distribution (NGED) Connected Data portal (East Midlands, West Midlands, South West and South Wales licence areas only). Licence: NGED open data licence (CC BY 4.0 style; check the portal terms).

| Column | Description |
|---|---|
| `json_featuretype` | Feature type marker from the source JSON file. |
| `mrid` | NGED master resource identifier for the substation. Primary key. |
| `name` | Substation name. |
| `type` | Substation level: PRIMARY, BSP (bulk supply point) or GSP (grid supply point). |
| `area` | NGED area or region the substation is in. |
| `voltages` | Voltage transformation at the site, for example '132-33' (kV). |
| `gsp` | Grid supply point the substation is fed from. |
| `bsp` | Bulk supply point the substation is fed from. |
| `primary` | Primary substation name, where the record is at primary level. |
| `demandfirmcapacity` | Firm (N-1) capacity for demand customers. |
| `demandavailablecapacity` | Headroom still available for new demand after existing load and accepted offers. |
| `demandmaximum` | Maximum observed demand. |
| `demandminimum` | Minimum observed demand. |
| `demandconstraint` | RAG (red/amber/green) constraint status for new demand connections. |
| `demandconstraintlimitingfactor` | What limits new demand at the site: for example Thermal, Fault Level or Voltage. |
| `generationfirmcapacity` | Firm capacity for generation connections. |
| `generationavailablecapacity` | Headroom still available for new generation after existing and accepted connections. |
| `generationconstraint` | RAG constraint status for new generation connections. |
| `generationconstraintlimitingfactor` | What limits new generation: Thermal, Fault Level, Voltage or Reverse Power Flow. |
| `reversepowerflowtotalcapacity` | Total capacity for reverse power flow (export back up the network). |
| `reversepowerflowavailablecapacity` | Reverse power flow capacity still available. |
| `voltage` | Operating voltage in kV. |
| `loadbudgetestimatesprovidedcount` | Number of demand budget estimates NGED has provided. |
| `loadbudgetestimatesprovidedcapacity` | Capacity of demand budget estimates provided. |
| `generationbudgetestimatesprovidedcount` | Number of generation budget estimates provided. |
| `generationbudgetestimatesprovidedcapacity` | Capacity of generation budget estimates provided. |
| `loadconnectionoffersacceptedcount` | Number of accepted demand connection offers. |
| `loadconnectionoffersacceptedcapacity` | Capacity of accepted demand connection offers. |
| `generationconnectionoffersacceptedcount` | Number of accepted generation connection offers. |
| `generationconnectionoffersacceptedcapacity` | Capacity of accepted generation connection offers. |
| `loadconnectionoffersmadecount` | Number of demand connection offers made (not yet accepted). |
| `loadconnectionoffersmadecapacity` | Capacity of demand connection offers made. |
| `generationconnectionoffersmadecount` | Number of generation connection offers made (not yet accepted). |
| `generationconnectionoffersmadecapacity` | Capacity of generation connection offers made. |
| `longitude` | Longitude as supplied by NGED (WGS84). |
| `latitude` | Latitude as supplied by NGED (WGS84). |
| `licence_area` | NGED licence area the record came from: east-midlands, west-midlands, south-west or south-wales. |

## northern_powergrid_capacity_heatmap

Northern Powergrid network capacity heatmap: 670 primary substations and grid/bulk supply points with firm capacity, observed demand, generation and demand headroom, fault level and constraint colour codes. Shows where new load (EV charging, heat pumps) or generation can connect in the North East and Yorkshire. Covers NPG only; see nged_ltds_capacity_heatmap for the Midlands, South West and Wales. Grain: one row per substation. Hackathon tracks: Access & equity, Investment & prioritisation. Source: Northern Powergrid open data portal (North East, Yorkshire and northern Lincolnshire licence areas only). Licence: Northern Powergrid open data licence (CC BY 4.0 style; check the portal terms).

| Column | Description |
|---|---|
| `psp_name` | Primary substation name. |
| `grid_easting` | Easting of the substation, OS National Grid (EPSG:27700), metres. |
| `grid_northing` | Northing of the substation, OS National Grid (EPSG:27700), metres. |
| `typetable` | Substation level, for example Primary. |
| `pvoltage` | Primary voltage in kV. |
| `firm_cap` | Firm capacity of the substation in MVA. |
| `mindemand` | Minimum observed demand in MW. |
| `maxdemand` | Maximum observed demand in MW. |
| `rpf` | Reverse power flow, MW (generation exporting back up the network). |
| `gentot` | Total connected and accepted generation, MW. |
| `demtot` | Total connected and accepted demand, MW. |
| `genhr` | Generation headroom, MW. |
| `demhr` | Demand headroom, MW. |
| `fl_break_d` | Fault level (breaking), kA, with existing demand. |
| `fl_break_r` | Fault level rating (breaking), kA. |
| `fl_make_d` | Fault level (making), kA, with existing demand. |
| `fl_make_r` | Fault level rating (making), kA. |
| `fl` | Fault level utilisation as a fraction of rating. |
| `worst_tap` | Worst-case transformer tap position used in the voltage assessment. |
| `gen_voltage_constraint` | Voltage constraint status for new generation. |
| `upgenconst` | Constraint on generation originating upstream of the substation. |
| `dem_voltage_constraint` | Voltage constraint status for new demand. |
| `gsp_hm_constraint_manual` | Manual constraint flag at the grid supply point heatmap level. |
| `odp_primary_name` | Name of the primary substation in the operational data point system. |
| `updemconst` | Constraint on demand from upstream of the substation (Yes or No). |
| `upstreamname` | Name of the upstream substation. |
| `gsp_name` | Grid supply point the substation is fed from. |
| `genconstraint` | Generation constraint RAG status (Green, Amber, Red). |
| `demconstraint` | Demand constraint RAG status (Green, Amber, Red). |
| `worst_case_constraint_gen_colour` | Worst-case generation constraint colour across all factors. |
| `worst_case_constraint_dem_colour` | Worst-case demand constraint colour across all factors. |
| `substation_location` | Latitude and longitude of the substation as text 'lat; lon' (WGS84). |
| `fault_level` | Fault level utilisation as a percentage of rating. |

## northern_powergrid_connection_queue

Northern Powergrid connection queue: generation and storage connection requests waiting behind each grid supply point, with technology, export capacity and queue position. Grain: one row per queue entry. Hackathon track: Investment & prioritisation. Source: Northern Powergrid open data portal (North East, Yorkshire and northern Lincolnshire licence areas only). Licence: Northern Powergrid open data licence (CC BY 4.0 style; check the portal terms).

| Column | Description |
|---|---|
| `row_number` | Row number in the source file. |
| `gsp` | Grid supply point the request connects behind. |
| `licence_area` | Northern Powergrid licence area (Northeast or Yorkshire). |
| `technology` | Technology of the request, for example Solar, Battery, Wind. |
| `export_capacity` | Requested export capacity in MW. |
| `queue_position` | Position in the NPG queue for the grid supply point. |
| `transmission_gate` | Transmission connection reform gate the project is in (for example Gate 1 or 2). |
| `dno_acceptance_date` | Date NPG accepted the application. |
| `final_queue_rank` | Final rank after connections reform queue reordering. |
| `phase` | Project phase or stage in the connection process. |

## northern_powergrid_gsp_connection_info

Northern Powergrid grid supply point (GSP) connection information: connected capacity to date, developer capacity still available, technical import/export limits and expected reinforcement dates, 50 GSPs. Grain: one row per GSP. Hackathon track: Investment & prioritisation. Source: Northern Powergrid open data portal (North East, Yorkshire and northern Lincolnshire licence areas only). Licence: Northern Powergrid open data licence (CC BY 4.0 style; check the portal terms).

| Column | Description |
|---|---|
| `gsp_id` | Grid supply point identifier. |
| `licence_area` | Northern Powergrid licence area. |
| `title` | Grid supply point name. |
| `connected_capacity_to_date_mw` | Generation capacity already connected behind the GSP, MW. |
| `developer_capacity_available_mw` | Capacity still available to new developers behind the GSP, MW. |
| `transmission_reinforcement_expected_completion_date` | Expected completion of transmission reinforcement that would release more capacity. |
| `connection_asset_reverse_power_limits_mva` | Reverse power flow limit of the connection assets, MVA. |
| `technical_limits_enabled` | Whether technical limits (export constraints agreed with the transmission operator) are in force. |
| `gsp_technical_export_limit` | Technical export limit at the GSP, MW. |
| `gsp_technical_import_limit_winter` | Technical import limit in winter, MW. |
| `gsp_technical_import_limit_summer` | Technical import limit in summer, MW. |
| `gsp_technical_import_limit_access_period` | Technical import limit during the access period (planned outage window), MW. |

## northern_powergrid_historical_peak_demand

Northern Powergrid historical peak demand by substation for 2019/20 to 2023/24, with year-on-year growth. Use to spot substations with fast-growing load. Grain: one row per substation. Source: Northern Powergrid open data portal (North East, Yorkshire and northern Lincolnshire licence areas only). Licence: Northern Powergrid open data licence (CC BY 4.0 style; check the portal terms).

| Column | Description |
|---|---|
| `grid_supply_point` | Grid supply point the substation is fed from. |
| `bulk_supply_point` | Bulk supply point the substation is fed from. |
| `primary` | Primary substation name. |
| `voltage_kv` | Voltage of the substation in kV. |
| `licence_area` | Northern Powergrid licence area. |
| `max_load_2019_20_mva` | Maximum load recorded in 2019/20, MVA. |
| `max_load_2019_20_pf` | Power factor at maximum load in 2019/20. |
| `max_load_2020_21_mva` | Maximum load recorded in 2020/21, MVA. |
| `max_load_2020_21_pf` | Power factor at maximum load in 2020/21. |
| `max_load_2021_22_mva` | Maximum load recorded in 2021/22, MVA. |
| `max_load_2021_22_pf` | Power factor at maximum load in 2021/22. |
| `max_load_2022_23_mva` | Maximum load recorded in 2022/23, MVA. |
| `max_load_2022_23_pf` | Power factor at maximum load in 2022/23. |
| `max_load_2023_24_mva` | Maximum load recorded in 2023/24, MVA. |
| `max_load_2023_24_pf` | Power factor at maximum load in 2023/24. |
| `percentage_growth` | Percentage change in maximum load, 2019/20 to 2020/21. |
| `percentage_growth0` | Percentage change in maximum load, 2020/21 to 2021/22. |
| `percentage_growth1` | Percentage change in maximum load, 2021/22 to 2022/23. |
| `percentage_growth2` | Percentage change in maximum load, 2022/23 to 2023/24. |

## northern_powergrid_lct_postal_districts

Northern Powergrid low-carbon technology (LCT) connections by postal district: customers and counts of solar PV, heat pumps, energy storage and EV chargers, as numbers and as shares of connections. A direct source of home EV charger uptake for the North East and Yorkshire (areas outside NPG have no rows). Grain: one row per postal district polygon (24 rows lack a polygon). Hackathon track: Access & equity. Source: Northern Powergrid open data portal (North East, Yorkshire and northern Lincolnshire licence areas only). Licence: Northern Powergrid open data licence (CC BY 4.0 style; check the portal terms).

| Column | Description |
|---|---|
| `unique_postal_districts` | Postal district code (outward code), for example 'LS6'. |
| `customer_numbers` | Number of NPG customers in the district. |
| `number_of_pvs` | Number of connections with solar PV. |
| `number_of_heat_pumps` | Number of connections with heat pumps. |
| `number_of_energy_storage` | Number of connections with energy storage. |
| `number_of_ev_chargers` | Number of connections with home EV chargers. |
| `total_number_of_lcts` | Total low-carbon technologies across all types in the district. |
| `of_connections_with_lct` | Share of connections in the district with any LCT. |
| `of_connections_with_pv` | Share of connections with solar PV. |
| `of_connections_with_heatpumps` | Share of connections with heat pumps. |
| `of_connections_with_energy_storage` | Share of connections with energy storage. |
| `of_connections_with_ev_chargers` | Share of connections with EV chargers. |
| `geo_point_2d` | District centroid as text 'lat; lon' (WGS84), as supplied. |

## nspl

ONS National Statistics Postcode Lookup (NSPL), latest release. One row per live or terminated UK postcode with the statistical, administrative and electoral geographies it falls in, plus a grid reference and WGS84 centroid. Postcodes with no grid reference (lat 99.999999) are removed. Grain: one row per postcode (pcds). Join to lsoa_2021_boundaries on lsoa21cd, to os_code_point_open on postcode, and to point tables on h3_8. Column name suffixes are the year of the geography edition (for example lad26cd = local authority district, 2026). Hackathon tracks: Access & equity (core), Resilience. Source: ONS Open Geography Portal. Licence: Open Government Licence v3.0; contains OS data, Royal Mail data and National Statistics data (c) Crown copyright.

| Column | Description |
|---|---|
| `pcd7` | Postcode in 7-character format (no gap for 5- and 6-character postcodes). |
| `pcd8` | Postcode in 8-character format (outward code padded to 4 characters, no gap). |
| `pcds` | Postcode with a single space between outward and inward codes, for example 'CB4 1AB'. Primary key for this table. |
| `dointr` | Date of introduction of the postcode (YYYYMM). |
| `doterm` | Date of termination of the postcode (YYYYMM). Null if the postcode is live. |
| `usrtypind` | User type indicator: 0 = small user (fewer than 25 items a day), 1 = large user. |
| `east1m` | Easting of the postcode centroid, OS National Grid (EPSG:27700), 1 metre resolution. |
| `north1m` | Northing of the postcode centroid, OS National Grid (EPSG:27700), 1 metre resolution. |
| `gridind` | Grid reference positional quality indicator (1 = within the building of the matched address closest to the postcode mean, down to 9 = no grid reference). |
| `oa21cd` | 2021 Census Output Area code. |
| `cty26cd` | County code (2026 edition). |
| `ced25cd` | County Electoral Division code (2025 edition). |
| `lad26cd` | Local Authority District code (2026 edition). |
| `wd26cd` | Electoral ward code (2026 edition). |
| `nhser24cd` | NHS England region code (2024 edition). |
| `ctry26cd` | Country code (2026 edition): E92 England, N92 Northern Ireland, S92 Scotland, W92 Wales, L93 Channel Islands, M83 Isle of Man. |
| `rgn26cd` | Region (England) code (2026 edition). |
| `pcon24cd` | Westminster parliamentary constituency code (2024 boundaries). |
| `ttwa15cd` | Travel to Work Area code (2015 edition). |
| `itl25cd` | International Territorial Level (ITL) code (2025 edition), successor to NUTS. |
| `npark16cd` | National Park code (2016 edition). Null if outside a National Park. |
| `lsoa21cd` | 2021 Census Lower layer Super Output Area code. Joins to lsoa_2021_boundaries (England and Wales only). |
| `msoa21cd` | 2021 Census Middle layer Super Output Area code. |
| `wz11cd` | 2011 Census Workplace Zone code. |
| `sicbl26cd` | Sub Integrated Care Board location code (2026 edition). |
| `bua24cd` | Built-up area code (2024 edition). Null if outside a built-up area. |
| `ruc21ind` | 2021 Rural Urban Classification indicator (England and Wales). |
| `oac21ind` | 2021 Output Area Classification indicator (England and Wales). |
| `lat` | Latitude of the postcode centroid, WGS84 (EPSG:4326). |
| `long` | Longitude of the postcode centroid, WGS84 (EPSG:4326). Same value as lon. |
| `lep21cd1` | First Local Enterprise Partnership code (2021 edition). |
| `lep21cd2` | Second Local Enterprise Partnership code (2021 edition), where the postcode spans two LEPs. |
| `pfa23cd` | Police Force Area code (2023 edition). |
| `imd25ind` | Index of Multiple Deprivation (2025 edition) rank or indicator for the postcode's small area. Country-specific scales are not comparable across England, Wales, Scotland and Northern Ireland. |
| `icb26cd` | Integrated Care Board code (2026 edition). |

## os_boundary_line_district_borough_unitary

Ordnance Survey Boundary-Line: district, borough and unitary authority polygons for Great Britain (about 350 areas). The authoritative local authority boundary. Grain: one row per polygon (multi-part areas may have several rows sharing admin_unit_id). Source: OS Data Hub Downloads API, Boundary-Line (GeoPackage, converted from OS National Grid EPSG:27700 to WGS84). Licence: OS OpenData Licence (Open Government Licence compatible).

| Column | Description |
|---|---|
| `name` | Name of the administrative area, for example 'Manchester District (B)'. |
| `area_code` | OS area code for the type of area (for example DIS = district, UTA = unitary authority, EUR = European region, WMC = Westminster constituency). |
| `area_description` | Text description of the area type matching area_code. |
| `file_name` | Name of the source file within Boundary-Line that the polygon came from (for example a county or region file). |
| `feature_serial_number` | Serial number of the polygon within its source file. |
| `collection_serial_number` | Serial number of the collection of polygons the feature belongs to. |
| `global_polygon_id` | Identifier of the polygon unique across the whole Boundary-Line release. |
| `admin_unit_id` | Identifier of the administrative unit, shared by all polygons of a multi-part area. |
| `census_code` | ONS/GSS census code of the area, for example 'E08000003'. Joins to nspl.lad26cd for districts (editions may differ). |
| `hectares` | Area of the unit in hectares, including inland water. |
| `non_inland_area` | Area in hectares of tidal water (non-inland) within the unit. |
| `area_type_code` | Code for the type of area (duplicate of area_code in most releases). |
| `area_type_description` | Description of the type of area. |
| `non_area_type_code` | Reserved; empty in current releases. |
| `non_area_type_description` | Reserved; empty in current releases. |

## os_boundary_line_english_region

Ordnance Survey Boundary-Line: the nine English regions as polygons. Grain: one row per polygon. Use for regional roll-ups of track scores. Source: OS Data Hub Downloads API, Boundary-Line (GeoPackage, converted from OS National Grid EPSG:27700 to WGS84). Licence: OS OpenData Licence (Open Government Licence compatible).

| Column | Description |
|---|---|
| `name` | Name of the administrative area, for example 'Manchester District (B)'. |
| `area_code` | OS area code for the type of area (for example DIS = district, UTA = unitary authority, EUR = European region, WMC = Westminster constituency). |
| `area_description` | Text description of the area type matching area_code. |
| `file_name` | Name of the source file within Boundary-Line that the polygon came from (for example a county or region file). |
| `feature_serial_number` | Serial number of the polygon within its source file. |
| `collection_serial_number` | Serial number of the collection of polygons the feature belongs to. |
| `global_polygon_id` | Identifier of the polygon unique across the whole Boundary-Line release. |
| `admin_unit_id` | Identifier of the administrative unit, shared by all polygons of a multi-part area. |
| `census_code` | ONS/GSS census code of the area, for example 'E08000003'. Joins to nspl.lad26cd for districts (editions may differ). |
| `hectares` | Area of the unit in hectares, including inland water. |
| `non_inland_area` | Area in hectares of tidal water (non-inland) within the unit. |
| `area_type_code` | Code for the type of area (duplicate of area_code in most releases). |
| `area_type_description` | Description of the type of area. |
| `non_area_type_code` | Reserved; empty in current releases. |
| `non_area_type_description` | Reserved; empty in current releases. |

## os_boundary_line_westminster_const

Ordnance Survey Boundary-Line: Westminster parliamentary constituency polygons for Great Britain. Grain: one row per polygon. Useful for political and constituency-level impact framing of infrastructure gaps. Source: OS Data Hub Downloads API, Boundary-Line (GeoPackage, converted from OS National Grid EPSG:27700 to WGS84). Licence: OS OpenData Licence (Open Government Licence compatible).

| Column | Description |
|---|---|
| `name` | Name of the administrative area, for example 'Manchester District (B)'. |
| `area_code` | OS area code for the type of area (for example DIS = district, UTA = unitary authority, EUR = European region, WMC = Westminster constituency). |
| `area_description` | Text description of the area type matching area_code. |
| `file_name` | Name of the source file within Boundary-Line that the polygon came from (for example a county or region file). |
| `feature_serial_number` | Serial number of the polygon within its source file. |
| `collection_serial_number` | Serial number of the collection of polygons the feature belongs to. |
| `global_polygon_id` | Identifier of the polygon unique across the whole Boundary-Line release. |
| `admin_unit_id` | Identifier of the administrative unit, shared by all polygons of a multi-part area. |
| `census_code` | ONS/GSS census code of the area, for example 'E08000003'. Joins to nspl.lad26cd for districts (editions may differ). |
| `hectares` | Area of the unit in hectares, including inland water. |
| `non_inland_area` | Area in hectares of tidal water (non-inland) within the unit. |
| `area_type_code` | Code for the type of area (duplicate of area_code in most releases). |
| `area_type_description` | Description of the type of area. |
| `non_area_type_code` | Reserved; empty in current releases. |
| `non_area_type_description` | Reserved; empty in current releases. |

## os_code_point_open

Ordnance Survey Code-Point Open: one point per postcode unit in Great Britain, located at the mean position of the delivery points. Alternative to nspl for postcode locations; carries NHS and admin area codes. Grain: one row per postcode. Join to nspl on postcode (nspl.pcd7/pcd8/pcds, matching the spacing). Source: OS Data Hub Downloads API. Licence: OS OpenData Licence (Open Government Licence compatible).

| Column | Description |
|---|---|
| `postcode` | Postcode unit, 7 characters without a gap for shorter forms, for example 'CB41AB' or 'B11AA'. |
| `positional_quality_indicator` | Positional quality: 10 = within the building of the matched address closest to the mean, 20 = as 10 but by a different method, 30 = approximate, 40 = postcode unit mean (PAF), 50 = estimated from surrounding unit postcodes, 60 = postcode sector mean, 90 = no coordinates available. |
| `eastings` | Easting of the postcode point, OS National Grid (EPSG:27700), metres. |
| `northings` | Northing of the postcode point, OS National Grid (EPSG:27700), metres. |
| `country_code` | ONS country code of the postcode (E92 England, S92 Scotland, W92 Wales, L93 Channel Islands, M83 Isle of Man). |
| `nhs_regional_ha_code` | NHS region health authority code (legacy). |
| `nhs_ha_code` | NHS health authority code (legacy). |
| `admin_county_code` | Administrative county code (legacy ONS code). |
| `admin_district_code` | Administrative district code (legacy ONS code). |
| `admin_ward_code` | Administrative ward code (legacy ONS code). |

## os_open_rivers

Ordnance Survey Open Rivers: the river and watercourse network for Great Britain as flow-directed centreline links, including canals and lakes' through-routes. Grain: one row per watercourse link. Combine with os_open_roads_links and the EA flood layers to find roads crossing watercourses (Resilience track). Source: OS Data Hub Downloads API (GeoPackage, converted from OS National Grid EPSG:27700 to WGS84). Licence: OS OpenData Licence (Open Government Licence compatible).

| Column | Description |
|---|---|
| `id` | Identifier of the watercourse link. Primary key. |
| `flow_direction` | Direction of flow relative to the digitised line: in direction, against direction or both. |
| `length` | Length of the link in metres. |
| `fictitious` | Whether the link is fictitious (a connection through a lake or tidal section rather than a surveyed channel). |
| `form` | Form of the watercourse: inlandRiver, tidalRiver, canal, lake, etc. |
| `watercourse_name` | Name of the watercourse, if any. |
| `watercourse_name_alternative` | Alternative or second-language name of the watercourse. |
| `start_node` | Node at the start of the link. |
| `end_node` | Node at the end of the link. |

## os_open_roads_links

Ordnance Survey Open Roads: the national road network for Great Britain as centreline links (about 4 million links), with classification, function, form of way and structure. Grain: one row per road link. The core network layer for all three tracks. road_structure marks bridges and tunnels, which makes it a better bridge/tunnel flag than overture_segments but it still carries no asset condition data. Join start_node / end_node to os_open_roads_nodes.id. Source: OS Data Hub Downloads API (GeoPackage, converted from OS National Grid EPSG:27700 to WGS84). Licence: OS OpenData Licence (Open Government Licence compatible).

| Column | Description |
|---|---|
| `id` | OS TOID-style identifier of the road link. Primary key. |
| `fictitious` | True if the link is a fictitious connection (for example a ferry or a link across a gap) rather than a real road. |
| `road_classification` | Road classification: Motorway, A Road, B Road, Classified Unnumbered, Unclassified, Not Classified or Unknown. |
| `road_function` | Road function: Motorway, A Road, B Road, Minor Road, Local Road, Local Access Road, Restricted Local Access Road, Secondary Access Road. |
| `form_of_way` | Form of way: Single Carriageway, Dual Carriageway, Roundabout, Slip Road, Collapsed Dual Carriageway, Shared Use Carriageway, Guided Busway, Track, Enclosed Traffic Area. |
| `road_classification_number` | Road number, for example 'A38' or 'M1'. Empty for unnumbered roads. |
| `name_1` | Primary road name. |
| `name_1_lang` | Language of name_1 (for example 'eng' or 'cym'). |
| `name_2` | Secondary road name (for example the Welsh name). |
| `name_2_lang` | Language of name_2. |
| `road_structure` | Structure the link is on: Bridge, Tunnel, Enclosed Traffic Area, Road Over Road or none. Useful as a national bridge/tunnel flag. |
| `length` | Link length. |
| `length_uom` | Unit of measure for length, normally 'm'. |
| `loop` | True if the link starts and ends at the same node. |
| `primary_route` | True if the link is part of the Primary Route Network. |
| `trunk_road` | True if the link is part of the trunk road network managed by National Highways or the devolved equivalent. |
| `start_node` | Identifier of the node at the start of the link. Joins to os_open_roads_nodes.id. |
| `end_node` | Identifier of the node at the end of the link. Joins to os_open_roads_nodes.id. |
| `road_number_toid` | TOID of the road number feature in the OS Open TOID dataset. |
| `road_name_toid` | TOID of the road name feature in the OS Open TOID dataset. |

## os_open_roads_nodes

Ordnance Survey Open Roads nodes: the junctions, road ends and other connection points of the national road network (about 3.3 million points). Grain: one row per node. os_open_roads_links.start_node and end_node join to id here. Count nodes per H3 cell for junction density; filter form_of_road_node for roundabouts or dead ends. Source: OS Data Hub Downloads API (GeoPackage, converted from OS National Grid EPSG:27700 to WGS84). Licence: OS OpenData Licence (Open Government Licence compatible).

| Column | Description |
|---|---|
| `id` | Identifier of the road node. Primary key; referenced by os_open_roads_links.start_node and end_node. |
| `form_of_road_node` | Node form: junction, road end, roundabout, pseudo node (a split in a link with no junction), or motorway junction. |

## os_open_uprn

Ordnance Survey Open UPRN: every addressable location in Great Britain (about 41 million Unique Property Reference Numbers) with a coordinate. Contains no address text. Use for property-level exposure counts (flood, EV charging access, distance to a bus stop) by joining on h3_8 or using ST_ functions. Grain: one row per UPRN. Source: OS Data Hub Downloads API. Licence: OS OpenData Licence (Open Government Licence compatible).

| Column | Description |
|---|---|
| `uprn` | Unique Property Reference Number, a persistent identifier for an addressable location. Primary key. |
| `x_coordinate` | Easting, OS National Grid (EPSG:27700), metres. |
| `y_coordinate` | Northing, OS National Grid (EPSG:27700), metres. |
| `latitude` | Latitude, WGS84, as supplied by OS. |
| `longitude` | Longitude, WGS84, as supplied by OS. |

## osm_sar_facilities

Search-and-rescue related facilities in Great Britain from OpenStreetMap (lifeboat stations, coastguard stations and rescue stations), via the Overpass API. Not an official register: completeness and tagging are volunteer-dependent, so treat as indicative. Grain: one row per OSM object (node, way or relation centre). Hackathon tracks: Access & equity (emergency response coverage), Resilience. Source: OpenStreetMap contributors. Licence: Open Database Licence (ODbL) 1.0; attribution 'OpenStreetMap contributors' required.

| Column | Description |
|---|---|
| `osm_id` | OpenStreetMap object type and id, for example 'node123456'. Primary key. |
| `name` | Facility name, if tagged. |
| `facility_type` | OSM tag value identifying the facility: lifeboat_station, coast_guard or rescue_station. |
| `operator` | Operator tag, for example RNLI or HM Coastguard, if tagged. |

## overture_buildings

Overture Maps building footprints for the configured bounding box only (default: Greater Manchester, not national, because national coverage is about 30 million polygons). Check the loader widget buildings_bbox before assuming coverage. Grain: one row per building. Use for exposure counts and built-form analysis. Source: Overture Maps Foundation (release recorded in the loader log). Overture segments and connectors derive from OpenStreetMap and other sources. Licence: ODbL 1.0 for transportation and buildings themes derived from OSM; CDLA Permissive 2.0 / CC0 for other themes (check the Overture attribution page). Attribution: (c) OpenStreetMap contributors and Overture Maps Foundation.

| Column | Description |
|---|---|
| `id` | Overture GERS id of the building. Primary key. |
| `subtype` | Building subtype, for example residential, commercial, industrial, education, medical, transportation. |
| `class` | Building class, for example house, apartments, garage, retail, office, hospital, school. |
| `height` | Building height in metres, where known. |
| `num_floors` | Number of floors above ground, where known. |
| `name` | Primary name of the building, if any. |

## overture_connectors

Overture Maps transportation connectors for Great Britain and Northern Ireland: the junction points where segments meet, forming the routable network graph. Grain: one row per connector. Count connectors per H3 cell as a measure of network density and connectivity. Source: Overture Maps Foundation (release recorded in the loader log). Overture segments and connectors derive from OpenStreetMap and other sources. Licence: ODbL 1.0 for transportation and buildings themes derived from OSM; CDLA Permissive 2.0 / CC0 for other themes (check the Overture attribution page). Attribution: (c) OpenStreetMap contributors and Overture Maps Foundation.

| Column | Description |
|---|---|
| `id` | Overture GERS id of the connector. Primary key; referenced by segments' connectors list. |

## overture_division_areas

Overture Maps administrative division areas (country, region, county, locality polygons) for Great Britain and Ireland. Grain: one row per division area; land and maritime areas can both appear. Use as a boundary layer alongside os_boundary_line_* and lsoa_2021_boundaries. Source: Overture Maps Foundation (release recorded in the loader log). Overture segments and connectors derive from OpenStreetMap and other sources. Licence: ODbL 1.0 for transportation and buildings themes derived from OSM; CDLA Permissive 2.0 / CC0 for other themes (check the Overture attribution page). Attribution: (c) OpenStreetMap contributors and Overture Maps Foundation.

| Column | Description |
|---|---|
| `id` | Overture GERS id of the division area. Primary key. |
| `subtype` | Division level: country, dependency, region, county, localadmin, locality, borough, macrohood, neighborhood, etc. |
| `class` | Area class: land or maritime. |
| `name` | Primary name of the division. |
| `country` | ISO 3166-1 alpha-2 country code, for example GB or IE. |
| `region` | ISO 3166-2 region code, for example GB-ENG or GB-SCT. |

## overture_places

Overture Maps places (points of interest) for Great Britain and Northern Ireland with confidence 0.5 or higher: shops, services, healthcare, education, transport and so on. Grain: one row per place. Use category = 'ev_charging_station' for approximate EV charge point locations; this layer has no connector count, power rating or operator detail. Also useful for emergency services and ports. Hackathon tracks: Access & equity, Resilience. Source: Overture Maps Foundation (release recorded in the loader log). Overture segments and connectors derive from OpenStreetMap and other sources. Licence: ODbL 1.0 for transportation and buildings themes derived from OSM; CDLA Permissive 2.0 / CC0 for other themes (check the Overture attribution page). Attribution: (c) OpenStreetMap contributors and Overture Maps Foundation.

| Column | Description |
|---|---|
| `id` | Overture GERS id of the place. Primary key. |
| `name` | Primary name of the place. |
| `category` | Primary category from the Overture taxonomy, for example ev_charging_station, hospital, fire_station, airport. |
| `basic_category` | Broad grouping of the category (a coarser level of the Overture taxonomy). |
| `category_hierarchy` | Array of taxonomy levels from broadest to the primary category. |
| `confidence` | Overture confidence score between 0 and 1 that the place exists and is correctly described. Loader keeps 0.5 and above. |
| `postcode` | Postcode from the first listed address, when present. Not validated against nspl. |
| `locality` | Locality or town from the first listed address, when present. |

## overture_segments

Overture Maps transportation segments for Great Britain and Northern Ireland: every road, path, rail and water centreline as a line, with class, surface, speed limits and flags. Grain: one row per segment. is_bridge and is_tunnel flag structures, but carry no condition or ownership information (there is no open national bridge inventory). Join segments to overture_connectors through the connectors list (not loaded here) or spatially. Hackathon tracks: Resilience, Investment & prioritisation. Source: Overture Maps Foundation (release recorded in the loader log). Overture segments and connectors derive from OpenStreetMap and other sources. Licence: ODbL 1.0 for transportation and buildings themes derived from OSM; CDLA Permissive 2.0 / CC0 for other themes (check the Overture attribution page). Attribution: (c) OpenStreetMap contributors and Overture Maps Foundation.

| Column | Description |
|---|---|
| `id` | Overture GERS id of the segment. Stable across releases where the feature is unchanged. Primary key. |
| `subtype` | Segment subtype: road, rail or water. |
| `class` | Road class: motorway, trunk, primary, secondary, tertiary, residential, service, pedestrian, footway, cycleway, path, track, etc. |
| `subclass` | Finer class, for example link, sidewalk, crosswalk, parking_aisle, driveway, alley. |
| `name` | Primary name of the segment, if any. |
| `road_surface` | Array of surface values (paved, unpaved, gravel, etc.), each possibly limited to a part of the segment (between = fractions along the line). |
| `speed_limits` | Array of speed limit structs (max_speed value and unit, min_speed, direction, applicability window along the segment). |
| `road_flags` | Array of structs { values: array of flags, between: fractions along the segment }. Flags include is_bridge, is_tunnel, is_link, is_under_construction and is_abandoned. |
| `is_bridge` | True if any part of the segment carries the is_bridge flag. Derived by the loader. |
| `is_tunnel` | True if any part of the segment carries the is_tunnel flag. Derived by the loader. |

## rnli_lifeboat_stations

RNLI lifeboat station locations across the UK, Ireland, Channel Islands and Isle of Man (238 stations), from the RNLI Geospatial Team. Official locations for search-and-rescue coverage analysis. Covers RNLI only; HM Coastguard rescue teams and SAR helicopters are not included. Grain: one row per station. Hackathon tracks: Access & equity (emergency response), Resilience. Source: RNLI Geospatial Team ArcGIS service. Licence: check the RNLI ArcGIS item terms before redistribution.

| Column | Description |
|---|---|
| `objectid` | ArcGIS object id. |
| `stationtype` | Station type: for example All-weather lifeboat, Inshore lifeboat, or both. |
| `county` | County the station is in. |
| `division` | RNLI operational division. |
| `region` | RNLI region. |
| `country` | Country the station is in. |
| `lifesavingarea` | RNLI lifesaving area. |
| `lifesavingregion` | RNLI lifesaving region. |
| `url` | RNLI web page for the station. |
| `station` | Station name. |
| `lat` | Latitude of the station, WGS84. |
| `long` | Longitude of the station, WGS84 (same as lon). |
| `funclocid` | RNLI functional location identifier. |
| `what3words` | what3words address of the station. |

## stats19_casualty

DfT STATS19 road safety data, casualties: each person injured or killed in a police-reported collision, last five years. Grain: one row per casualty. Join to stats19_collision on collision_index and to stats19_vehicle on collision_index plus vehicle_reference. Attribute columns are numeric codes; see the DfT data guide. Source: DfT road safety data. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `collision_index` | Collision reference. Joins to stats19_collision.collision_index. |
| `collision_year` | Year of the collision. |
| `collision_ref_no` | Police collision reference number. |
| `vehicle_reference` | Vehicle the casualty was in or struck by. Joins to stats19_vehicle.vehicle_reference. |
| `casualty_reference` | Casualty number within the collision. |
| `casualty_class` | 1 = driver or rider, 2 = passenger, 3 = pedestrian. |
| `sex_of_casualty` | 1 = male, 2 = female, 9 = unknown. |
| `age_of_casualty` | Casualty age in years (-1 if unknown). |
| `age_band_of_casualty` | Casualty age band code. |
| `casualty_severity` | 1 = fatal, 2 = serious, 3 = slight. |
| `pedestrian_location` | Where the pedestrian was (crossing, carriageway, footway) when hit (code). |
| `pedestrian_movement` | What the pedestrian was doing (crossing, walking along, etc.) (code). |
| `car_passenger` | Front or rear seat passenger (code). |
| `bus_or_coach_passenger` | Bus passenger status: boarding, alighting, standing, seated (code). |
| `pedestrian_road_maintenance_worker` | Whether the pedestrian was a road maintenance worker (code). |
| `casualty_type` | Casualty type code (pedestrian, cyclist, motorcycle rider, car occupant, bus occupant, horse rider, etc.). |
| `casualty_imd_decile` | Index of Multiple Deprivation decile of the casualty's home area (1 = most deprived). |
| `lsoa_of_casualty` | LSOA 2011 code of the casualty's home address. |
| `enhanced_casualty_severity` | Enhanced (injury-based) severity code for the casualty. |
| `casualty_injury_based` | Casualty severity based on reported injuries only. |
| `casualty_adjusted_severity_serious` | Probability-adjusted weighting that the casualty is serious. |
| `casualty_adjusted_severity_slight` | Probability-adjusted weighting that the casualty is slight. |
| `casualty_distance_banding` | Distance band between the casualty's home and the collision location (code). |
| `escooter_flag` | Flag identifying e-scooter casualties. |

## stats19_collision

DfT STATS19 road safety data, collisions: every police-reported injury collision in Great Britain for the last five years, with location, conditions and severity. Grain: one row per collision (collision_index). Join to stats19_vehicle and stats19_casualty on collision_index. Most attribute columns are numeric codes; the lookup is the DfT 'Road Safety Open Dataset Data Guide'. Hackathon tracks: Investment & prioritisation, Resilience. Source: DfT road safety data. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `collision_index` | Unique collision reference (year plus reference number). Primary key; joins vehicle and casualty tables. |
| `collision_year` | Year of the collision. |
| `collision_ref_no` | Police collision reference number, unique within the year and force. |
| `location_easting_osgr` | Collision location easting, OS National Grid (EPSG:27700), metres. |
| `location_northing_osgr` | Collision location northing, OS National Grid (EPSG:27700), metres. |
| `longitude` | Collision longitude, WGS84, as supplied by DfT (string). |
| `latitude` | Collision latitude, WGS84, as supplied by DfT (string). |
| `police_force` | Code of the reporting police force (see data guide). |
| `collision_severity` | Severity of the collision: 1 = fatal, 2 = serious, 3 = slight (worst casualty injury). |
| `number_of_vehicles` | Number of vehicles involved. |
| `number_of_casualties` | Number of casualties. |
| `date` | Date of the collision (DD/MM/YYYY). |
| `day_of_week` | Day of week: 1 = Sunday, 2 = Monday ... 7 = Saturday. |
| `time` | Time of the collision (HH:MM). |
| `local_authority_district` | Legacy local authority district code of the location. |
| `local_authority_ons_district` | ONS code of the local authority district where the collision occurred. |
| `local_authority_highway` | Highway authority code responsible for the road at the time. |
| `local_authority_highway_current` | Current ONS code of the highway authority (reflects boundary changes). |
| `first_road_class` | Class of the first road: 1 = motorway, 2 = A(M), 3 = A, 4 = B, 5 = C, 6 = unclassified. |
| `first_road_number` | Road number of the first road (0 if unclassified). |
| `road_type` | Road type code: roundabout, one way street, dual carriageway, single carriageway, slip road. |
| `speed_limit` | Speed limit in mph at the collision location. |
| `junction_detail_historic` | Junction detail code using the pre-2020 scheme. |
| `junction_detail` | Junction detail code: type of junction (roundabout, T junction, crossroads, slip road, private drive, etc.). |
| `junction_control` | Junction control code: authorised person, auto traffic signal, stop sign, give way or uncontrolled. |
| `second_road_class` | Class of the second road at a junction (same scheme as first_road_class). |
| `second_road_number` | Road number of the second road. |
| `pedestrian_crossing_human_control_historic` | Human control of a nearby pedestrian crossing (historic scheme). |
| `pedestrian_crossing_physical_facilities_historic` | Physical facilities of a nearby pedestrian crossing (historic scheme). |
| `pedestrian_crossing` | Pedestrian crossing type within 50 m (current scheme). |
| `light_conditions` | Light conditions: 1 = daylight, 4 = darkness with lights lit, 5 = darkness with lights unlit, 6 = darkness with no lighting, 7 = darkness with unknown lighting. |
| `weather_conditions` | Weather code: fine, raining, snowing, fog or mist, with or without high winds. |
| `road_surface_conditions` | Road surface code: dry, wet or damp, snow, frost or ice, flood over 3 cm deep. |
| `special_conditions_at_site` | Special conditions code such as roadworks, defective signals or oil/diesel on road. |
| `carriageway_hazards_historic` | Carriageway hazards code (historic scheme). |
| `carriageway_hazards` | Carriageway hazards code: previous collision, object in carriageway, animal, etc. |
| `urban_or_rural_area` | 1 = urban, 2 = rural, 3 = unallocated. |
| `did_police_officer_attend_scene_of_accident` | 1 = police officer attended, 2 = no officer attended, 3 = self-reported by the public. |
| `trunk_road_flag` | 1 = trunk road (including motorways) managed by National Highways or devolved equivalent, 2 = non-trunk. |
| `lsoa_of_accident_location` | LSOA 2011 code of the collision location (England and Wales). Not the 2021 LSOA in lsoa_2021_boundaries. |
| `enhanced_severity_collision` | Code of the enhanced (injury-based) severity adjustment flag for the collision. |
| `collision_injury_based` | Collision severity based on reported injuries only (no police judgement adjustment). |
| `collision_adjusted_severity_serious` | Probability-adjusted weighting that the collision is serious, to correct for severity misclassification between police forces. |
| `collision_adjusted_severity_slight` | Probability-adjusted weighting that the collision is slight, to correct for severity misclassification between police forces. |

## stats19_vehicle

DfT STATS19 road safety data, vehicles: each vehicle involved in a police-reported injury collision, last five years, with manoeuvre, point of impact and driver attributes. Grain: one row per vehicle per collision. Join to stats19_collision on collision_index and to stats19_casualty on collision_index plus vehicle_reference. Attribute columns are numeric codes; see the DfT data guide. Source: DfT road safety data. Licence: Open Government Licence v3.0.

| Column | Description |
|---|---|
| `collision_index` | Collision reference. Joins to stats19_collision.collision_index. |
| `collision_year` | Year of the collision. |
| `collision_ref_no` | Police collision reference number. |
| `vehicle_reference` | Vehicle number within the collision (1, 2, 3 ...). Casualties link to vehicles through this. |
| `vehicle_type` | Vehicle type code: pedal cycle, motorcycle classes, car, taxi, bus or coach, goods vehicle classes, etc. |
| `towing_and_articulation` | Towing or articulation code (no tow, caravan, trailer, articulated vehicle). |
| `vehicle_manoeuvre_historic` | Manoeuvre code at the time of the collision (historic scheme). |
| `vehicle_manoeuvre` | Manoeuvre code: going ahead, turning left or right, overtaking, reversing, waiting to turn, etc. |
| `vehicle_direction_from` | Compass direction the vehicle was travelling from (code). |
| `vehicle_direction_to` | Compass direction the vehicle was travelling to (code). |
| `vehicle_location_restricted_lane_historic` | Restricted lane the vehicle was in (historic scheme). |
| `vehicle_location_restricted_lane` | Restricted lane code: bus lane, cycle lane, on footway, etc. |
| `junction_location` | Position of the vehicle relative to a junction (code). |
| `skidding_and_overturning` | Skidding or overturning code. |
| `hit_object_in_carriageway` | Code for an object in the carriageway that was hit (for example animal, bollard, parked vehicle). |
| `vehicle_leaving_carriageway` | Code describing how the vehicle left the carriageway, if it did. |
| `hit_object_off_carriageway` | Code for an object off the carriageway that was hit (for example lamp post, tree, barrier). |
| `first_point_of_impact` | First point of impact code: front, back, offside, nearside, did not impact. |
| `vehicle_left_hand_drive` | Code for whether the vehicle was left-hand drive. |
| `journey_purpose_of_driver_historic` | Journey purpose code (historic scheme). |
| `journey_purpose_of_driver` | Journey purpose code: commuting, work, school run, taking pupil to school, other. |
| `sex_of_driver` | Driver sex: 1 = male, 2 = female, 3 = not known. |
| `age_of_driver` | Driver age in years (-1 if unknown). |
| `age_band_of_driver` | Driver age band code (for example 6 = 11 to 15, 7 = 16 to 20). |
| `engine_capacity_cc` | Engine capacity in cubic centimetres (-1 if unknown or not applicable). |
| `propulsion_code` | Propulsion code: petrol, heavy oil, electric, hybrid, gas, etc. |
| `age_of_vehicle` | Age of the vehicle in years (-1 if unknown). |
| `generic_make_model` | Generic make and model text (only where the vehicle could be matched). |
| `driver_imd_decile` | Index of Multiple Deprivation decile of the driver's home area (1 = most deprived). |
| `lsoa_of_driver` | LSOA 2011 code of the driver's home address. |
| `escooter_flag` | Flag identifying e-scooters among vehicle types. |
| `driver_distance_banding` | Distance band between the driver's home and the collision location (code). |
