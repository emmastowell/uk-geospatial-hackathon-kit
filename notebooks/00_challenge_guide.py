# Databricks notebook source

# MAGIC %md
# MAGIC # Hackathon Challenge Guide
# MAGIC
# MAGIC Welcome to the hackathon! This notebook outlines **three challenges** built on geospatial and infrastructure datasets in `hackathon.two_postcodes`. Each section provides:
# MAGIC
# MAGIC 1. **The Brief** -- what you're solving and why it matters
# MAGIC 2. **Key Tables** -- the datasets you'll use (all live in `hackathon.two_postcodes`)
# MAGIC 3. **Starter SQL** -- working queries you can run right now to explore the data and build from
# MAGIC 4. **Geospatial Techniques** -- the spatial functions and H3 patterns to reach for
# MAGIC 5. **Stretch Goals** -- extra-credit ideas to push your solution further
# MAGIC
# MAGIC **Universal join key:** H3 resolution 8 (`h3_8`) is pre-computed on every point table. Start joins there before reaching for `ST_` functions on raw geometry.
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC # Challenge 1: "Coastal Countdown"
# MAGIC
# MAGIC ## The Brief
# MAGIC The sea is coming. By 2100, entire stretches of road, rail and built-up land will sit below projected inundation lines. **Your job:** build a single authority-level **exposure scorecard** that answers *"Where in England and Wales is the most infrastructure at stake, and how fast is the threat growing?"*
# MAGIC
# MAGIC ## What You'll Build
# MAGIC A **ranked league table** of local authorities scored by a composite coastal exposure index -- combining road-km, railway-km, population, built-up area, and renewable energy capacity sitting inside inundation zones across **three time horizons (2050 / 2080 / 2100)**. Present it as an interactive map or dashboard showing the top-20 most exposed authorities with a "ticking clock" view of how their score worsens from 2050 to 2100.
# MAGIC
# MAGIC ## Key Tables
# MAGIC
# MAGIC | Table | Role |
# MAGIC |---|---|
# MAGIC | `bgs_geocoast_geocoast_v1_authority_area_inundation` | **Centrepiece:** pre-computed road/rail/population/urban exposure per authority per epoch |
# MAGIC | `bgs_geocoast_*_coastline_*` (6 tables) | Coastline-level inundation and cliff erosion (mean + worst case) by authority and SMP |
# MAGIC | `ea_rofrs_postcodes` | Postcode-level river/sea flood risk bands |
# MAGIC | `ea_flood_areas` + `ea_flood_defences` | Flood alert zones and existing defence lines |
# MAGIC | `os_open_roads_links` | Road network geometry for direct spatial overlay |
# MAGIC | `overture_segments` (filter `subtype = 'rail'`) | Rail centrelines with `is_bridge` / `is_tunnel` flags |
# MAGIC | `desnz_repd` | Renewable energy sites (MW, technology, status) to overlay onto hazard zones |
# MAGIC | `nspl` | Postcode-to-LSOA/authority lookup with IMD rank and H3 |
# MAGIC | `os_boundary_line_district_borough_unitary` | Authority polygons for choropleth mapping |
# MAGIC
# MAGIC ## Geospatial Techniques in Play
# MAGIC * `ST_Intersects` between BGS inundation polygons and OS Open Roads / Overture rail segments
# MAGIC * `ST_Area` / `ST_Length` to measure exposed geometry directly
# MAGIC * **H3 hexagonal aggregation** -- roll postcode-level EA flood risk into the same hex grid as DESNZ renewable energy sites
# MAGIC * `ST_Buffer` around railway stations from the BGS authority table to estimate population catchments at risk
# MAGIC
# MAGIC ## Stretch Goals
# MAGIC * Add EA flood defence lines and score which authorities have the widest gap between exposure and existing defences
# MAGIC * Overlay STATS19 collision data to show where flood-exposed roads already have high accident rates -- a compound-risk view
# MAGIC * Animate the 2050 / 2080 / 2100 progression on a hex map
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 1A: Composite Coastal Exposure Index
# MAGIC -- Ranks authorities by a weighted score combining road, rail, population,
# MAGIC -- urban area, and built-up area exposure across the three time horizons.
# MAGIC -- Adjust the weights to suit your narrative.
# MAGIC
# MAGIC SELECT
# MAGIC   adm_unit                        AS authority,
# MAGIC   population,
# MAGIC   road_km                         AS total_road_km,
# MAGIC   railway_km                      AS total_railway_km,
# MAGIC
# MAGIC   -- 2050 exposure
# MAGIC   road_2050,
# MAGIC   rw_2050                         AS rail_2050,
# MAGIC   inund_2050                      AS pct_inundation_2050,
# MAGIC
# MAGIC   -- 2080 exposure
# MAGIC   road_2080,
# MAGIC   rw_2080                         AS rail_2080,
# MAGIC   inund_2080                      AS pct_inundation_2080,
# MAGIC
# MAGIC   -- 2100 exposure
# MAGIC   road_2100,
# MAGIC   rw_2100                         AS rail_2100,
# MAGIC   inund_2100                      AS pct_inundation_2100,
# MAGIC
# MAGIC   -- Composite score (normalised by baseline, then weighted sum)
# MAGIC   ROUND(
# MAGIC     0.30 * (road_2100  / NULLIF(road_km, 0))    +  -- road exposure weight
# MAGIC     0.25 * (rw_2100    / NULLIF(railway_km, 0))  +  -- rail exposure weight
# MAGIC     0.20 * (inund_2100 / 100.0)                  +  -- % area inundated
# MAGIC     0.15 * (build_2100 / NULLIF(build_kmsq, 0))  +  -- built-up area
# MAGIC     0.10 * (urban_2100 / NULLIF(urban_kmsq, 0)),    -- urban area
# MAGIC     4
# MAGIC   ) AS exposure_index_2100
# MAGIC
# MAGIC FROM hackathon.two_postcodes.bgs_geocoast_geocoast_v1_authority_area_inundation
# MAGIC WHERE road_km > 0          -- exclude authorities with no roads (data quality)
# MAGIC   AND railway_km > 0       -- exclude authorities with no rail
# MAGIC ORDER BY exposure_index_2100 DESC
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 1B: "Ticking Clock" view
# MAGIC -- Unpivots the three epochs into rows so you can chart the progression
# MAGIC -- for each authority as a time series.
# MAGIC
# MAGIC WITH top_authorities AS (
# MAGIC   SELECT adm_unit, road_km, railway_km,
# MAGIC          road_2050, road_2080, road_2100,
# MAGIC          rw_2050,   rw_2080,   rw_2100,
# MAGIC          build_2050, build_2080, build_2100,
# MAGIC          inund_2050, inund_2080, inund_2100
# MAGIC   FROM hackathon.two_postcodes.bgs_geocoast_geocoast_v1_authority_area_inundation
# MAGIC   WHERE road_km > 0 AND railway_km > 0
# MAGIC   ORDER BY inund_2100 DESC
# MAGIC   LIMIT 10
# MAGIC )
# MAGIC SELECT
# MAGIC   adm_unit                          AS authority,
# MAGIC   epoch,
# MAGIC   road_exposed_km,
# MAGIC   rail_exposed_km,
# MAGIC   pct_area_inundated
# MAGIC FROM top_authorities
# MAGIC LATERAL VIEW INLINE(ARRAY(
# MAGIC   NAMED_STRUCT('epoch', 2050, 'road_exposed_km', road_2050, 'rail_exposed_km', rw_2050, 'pct_area_inundated', inund_2050),
# MAGIC   NAMED_STRUCT('epoch', 2080, 'road_exposed_km', road_2080, 'rail_exposed_km', rw_2080, 'pct_area_inundated', inund_2080),
# MAGIC   NAMED_STRUCT('epoch', 2100, 'road_exposed_km', road_2100, 'rail_exposed_km', rw_2100, 'pct_area_inundated', inund_2100)
# MAGIC )) t AS epoch, road_exposed_km, rail_exposed_km, pct_area_inundated
# MAGIC ORDER BY authority, epoch

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 1C: H3 join -- EA postcode flood risk × DESNZ renewable sites
# MAGIC -- Counts flood-risk properties and renewable MW per H3 res-8 hex.
# MAGIC -- Hexes with high flood risk AND significant renewable capacity are priority concern zones.
# MAGIC
# MAGIC WITH flood_hex AS (
# MAGIC   SELECT
# MAGIC     n.h3_8,
# MAGIC     COUNT(*)                                        AS postcodes_at_risk,
# MAGIC     SUM(e.tot_cnt_medium + e.tot_cnt_high)          AS properties_medium_high_risk
# MAGIC   FROM hackathon.two_postcodes.ea_rofrs_postcodes   e
# MAGIC   JOIN hackathon.two_postcodes.nspl                 n  ON REPLACE(e.pc, ' ', '') = REPLACE(n.pcds, ' ', '')
# MAGIC   GROUP BY n.h3_8
# MAGIC ),
# MAGIC renewable_hex AS (
# MAGIC   SELECT
# MAGIC     h3_8,
# MAGIC     COUNT(*)                                        AS renewable_sites,
# MAGIC     ROUND(SUM(installed_capacity_mwelec), 1)        AS total_mw
# MAGIC   FROM hackathon.two_postcodes.desnz_repd
# MAGIC   WHERE h3_8 IS NOT NULL
# MAGIC   GROUP BY h3_8
# MAGIC )
# MAGIC SELECT
# MAGIC   h3_h3tostring(f.h3_8)                             AS hex_id,
# MAGIC   f.postcodes_at_risk,
# MAGIC   f.properties_medium_high_risk,
# MAGIC   COALESCE(r.renewable_sites, 0)                    AS renewable_sites,
# MAGIC   COALESCE(r.total_mw, 0)                           AS renewable_mw_at_risk
# MAGIC FROM flood_hex       f
# MAGIC LEFT JOIN renewable_hex r ON f.h3_8 = r.h3_8
# MAGIC WHERE r.h3_8 IS NOT NULL   -- keep only hexes where renewables and flood risk overlap
# MAGIC ORDER BY renewable_mw_at_risk DESC
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 1D: Coastline-level inundation overview
# MAGIC -- Shows which authorities have the most coastline projected to be inundated,
# MAGIC -- and how the percentage grows from 2050 to 2100.
# MAGIC
# MAGIC SELECT
# MAGIC   adm_unit                         AS authority,
# MAGIC   ROUND(coast_km, 1)               AS coastline_km,
# MAGIC   ROUND(inund2050, 1)              AS inundated_km_2050,
# MAGIC   ROUND(per_2050, 1)               AS pct_2050,
# MAGIC   ROUND(inund2080, 1)              AS inundated_km_2080,
# MAGIC   ROUND(per_2080, 1)               AS pct_2080,
# MAGIC   ROUND(inund2100, 1)              AS inundated_km_2100,
# MAGIC   ROUND(per_2100, 1)               AS pct_2100,
# MAGIC   ROUND(per_2100 - per_2050, 1)    AS pct_increase_2050_to_2100
# MAGIC FROM hackathon.two_postcodes.bgs_geocoast_geocoast_v1_authority_coastline_inundation
# MAGIC ORDER BY per_2100 DESC
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %md
# MAGIC # Challenge 2: "The Last Mile"
# MAGIC
# MAGIC ## The Brief
# MAGIC Some neighbourhoods are 30 seconds from a bus stop, an EV charger, and a lifeboat station. Others are 30 minutes from all three. **Your job:** build a postcode-level access score that exposes **transit deserts, charging gaps, and emergency-response blind spots** in one pass -- and show which communities fall through every net at once.
# MAGIC
# MAGIC ## What You'll Build
# MAGIC A composite **"Last Mile Index"** for every LSOA in England and Wales, combining three sub-scores:
# MAGIC * **(a)** Public transport frequency within walking distance
# MAGIC * **(b)** Proximity to the nearest EV charger
# MAGIC * **(c)** Distance to the nearest emergency response facility
# MAGIC
# MAGIC Present it as a **hex map** where the coldest hexes are the most underserved -- the places where all three scores are poor simultaneously.
# MAGIC
# MAGIC ## Key Tables
# MAGIC
# MAGIC | Table | Role |
# MAGIC |---|---|
# MAGIC | `gtfs_stops` + `gtfs_stop_times` + `gtfs_trips` + `gtfs_calendar` | Compute weekday departure count per stop |
# MAGIC | `naptan_stops` | All public transport nodes (bus, rail, tram, ferry, airport) with type and H3 |
# MAGIC | `overture_places` (filter `category = 'ev_charging_station'`) | Individual charger locations |
# MAGIC | `dft_evci_local_authority` | Quarterly device-count trends per authority (temporal context) |
# MAGIC | `osm_sar_facilities` + `rnli_lifeboat_stations` | Emergency response facility locations |
# MAGIC | `nspl` | Postcode centroids with LSOA, IMD rank, rural/urban classification, H3 |
# MAGIC | `lsoa_2021_boundaries` | LSOA polygons for aggregation and centroid derivation |
# MAGIC | `os_open_uprn` | Every addressable location in GB -- weight the score by address density |
# MAGIC | `os_boundary_line_district_borough_unitary` | Authority boundaries for labelling and filtering |
# MAGIC
# MAGIC ## Geospatial Techniques in Play
# MAGIC * `h3_kring(h3_8, k)` to define walk-distance bands (k=1 \~460 m, k=2 \~920 m) around every postcode and count GTFS departures inside that ring
# MAGIC * `ST_Distance` from each LSOA centroid to the nearest EV charger and nearest SAR/lifeboat facility
# MAGIC * `h3_toparent` for multi-resolution hex maps -- zoom out for regional patterns, zoom in for neighbourhood detail
# MAGIC * `ST_Contains` with OS boundary polygons to clip and label results by local authority and constituency
# MAGIC
# MAGIC ## Stretch Goals
# MAGIC * Cross-reference the worst "Last Mile" LSOAs against IMD deprivation rank from NSPL
# MAGIC * Add wheelchair-accessible transit as a separate sub-score using `gtfs_trips.wheelchair_accessible`
# MAGIC * Compute the number of UPRNs (addresses) per hex that are beyond 800 m of any NaPTAN stop -- the true "transit desert" population count
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 2A: Weekday departure count per GTFS stop
# MAGIC -- This is the core transit frequency signal.
# MAGIC -- Join through trips -> calendar to keep only weekday services,
# MAGIC -- then count departures per stop.
# MAGIC
# MAGIC SELECT
# MAGIC   st.stop_id,
# MAGIC   gs.stop_name,
# MAGIC   gs.h3_8,
# MAGIC   COUNT(*)   AS weekday_departures
# MAGIC FROM hackathon.two_postcodes.gtfs_stop_times   st
# MAGIC JOIN hackathon.two_postcodes.gtfs_trips        t   ON st.trip_id    = t.trip_id
# MAGIC JOIN hackathon.two_postcodes.gtfs_calendar     c   ON t.service_id  = c.service_id
# MAGIC JOIN hackathon.two_postcodes.gtfs_stops        gs  ON st.stop_id    = gs.stop_id
# MAGIC WHERE c.monday = 1           -- weekday service
# MAGIC   AND gs.h3_8 IS NOT NULL
# MAGIC GROUP BY st.stop_id, gs.stop_name, gs.h3_8
# MAGIC ORDER BY weekday_departures DESC
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 2B: Transit frequency within walking distance of each postcode
# MAGIC -- Uses h3_kring to find all H3 hexes within ~460m (k=1) of each postcode,
# MAGIC -- then sums the weekday departures from stops in those hexes.
# MAGIC -- Low values = transit desert.
# MAGIC
# MAGIC WITH stop_departures AS (
# MAGIC   SELECT
# MAGIC     gs.h3_8,
# MAGIC     COUNT(*)   AS weekday_deps
# MAGIC   FROM hackathon.two_postcodes.gtfs_stop_times   st
# MAGIC   JOIN hackathon.two_postcodes.gtfs_trips        t   ON st.trip_id    = t.trip_id
# MAGIC   JOIN hackathon.two_postcodes.gtfs_calendar     c   ON t.service_id  = c.service_id
# MAGIC   JOIN hackathon.two_postcodes.gtfs_stops        gs  ON st.stop_id    = gs.stop_id
# MAGIC   WHERE c.monday = 1
# MAGIC     AND gs.h3_8 IS NOT NULL
# MAGIC   GROUP BY gs.h3_8
# MAGIC ),
# MAGIC postcode_rings AS (
# MAGIC   SELECT
# MAGIC     pcds,
# MAGIC     lsoa21cd,
# MAGIC     h3_8     AS pc_h3,
# MAGIC     EXPLODE(h3_kring(h3_8, 1)) AS neighbour_h3   -- k=1 ~ 460m walk
# MAGIC   FROM hackathon.two_postcodes.nspl
# MAGIC   WHERE h3_8 IS NOT NULL
# MAGIC     AND lsoa21cd IS NOT NULL
# MAGIC )
# MAGIC SELECT
# MAGIC   pr.lsoa21cd,
# MAGIC   COUNT(DISTINCT pr.pcds)                          AS postcodes,
# MAGIC   COALESCE(SUM(sd.weekday_deps), 0)                AS total_nearby_departures,
# MAGIC   ROUND(COALESCE(SUM(sd.weekday_deps), 0)
# MAGIC         / COUNT(DISTINCT pr.pcds), 1)              AS avg_departures_per_postcode
# MAGIC FROM postcode_rings     pr
# MAGIC LEFT JOIN stop_departures sd ON pr.neighbour_h3 = sd.h3_8
# MAGIC GROUP BY pr.lsoa21cd
# MAGIC ORDER BY avg_departures_per_postcode ASC
# MAGIC LIMIT 20   -- the most transit-deprived LSOAs

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 2C: EV charger locations from Overture Places
# MAGIC -- Quick look at the EV charging station data you'll use for proximity scoring.
# MAGIC
# MAGIC SELECT
# MAGIC   id,
# MAGIC   name,
# MAGIC   category,
# MAGIC   postcode,
# MAGIC   locality,
# MAGIC   ST_X(geom)  AS lon,
# MAGIC   ST_Y(geom)  AS lat
# MAGIC FROM hackathon.two_postcodes.overture_places
# MAGIC WHERE category = 'ev_charging_station'
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 2D: Emergency response facility overview
# MAGIC -- Combine OSM SAR facilities and RNLI lifeboat stations into a single view
# MAGIC -- to assess emergency coverage.
# MAGIC
# MAGIC SELECT
# MAGIC   'OSM_SAR'          AS source,
# MAGIC   name,
# MAGIC   facility_type      AS type,
# MAGIC   operator,
# MAGIC   lat,
# MAGIC   lon,
# MAGIC   h3_8
# MAGIC FROM hackathon.two_postcodes.osm_sar_facilities
# MAGIC
# MAGIC UNION ALL
# MAGIC
# MAGIC SELECT
# MAGIC   'RNLI'             AS source,
# MAGIC   station            AS name,
# MAGIC   stationtype        AS type,
# MAGIC   'RNLI'             AS operator,
# MAGIC   lat,
# MAGIC   lon,
# MAGIC   h3_8
# MAGIC FROM hackathon.two_postcodes.rnli_lifeboat_stations
# MAGIC ORDER BY source, name
# MAGIC LIMIT 30

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 2E: EV charger infrastructure rollout over time
# MAGIC -- Shows the quarterly trajectory of charging devices per local authority.
# MAGIC -- Use this for temporal context: which authorities are catching up?
# MAGIC
# MAGIC SELECT
# MAGIC   area_name,
# MAGIC   quarter_start,
# MAGIC   measure,
# MAGIC   value
# MAGIC FROM hackathon.two_postcodes.dft_evci_local_authority
# MAGIC WHERE measure LIKE '%device%'
# MAGIC ORDER BY area_name, quarter_start
# MAGIC LIMIT 30

# COMMAND ----------

# MAGIC %md
# MAGIC # Challenge 3: "Grid Lock"
# MAGIC
# MAGIC ## The Brief
# MAGIC There's a fixed pot of money. You can upgrade substations, reinforce bridges, or add EV chargers -- but not all three everywhere. **Your job:** build a spatially-weighted **priority model** that ranks where the next pound of infrastructure investment should go based on grid capacity headroom, transport demand, renewable energy pipeline, vessel traffic, and structural exposure.
# MAGIC
# MAGIC ## What You'll Build
# MAGIC A **hex-level investment priority score** across NGED and NPG licence areas, blending:
# MAGIC * Grid constraint severity
# MAGIC * Road traffic demand
# MAGIC * Planned renewable MW awaiting connection
# MAGIC * Vessel traffic density around ports
# MAGIC * Bridge/tunnel counts under load
# MAGIC
# MAGIC Present it as a **dashboard** where a decision-maker can toggle budget weighting sliders and watch the priority map re-rank in real time.
# MAGIC
# MAGIC ## Key Tables
# MAGIC
# MAGIC | Table | Role |
# MAGIC |---|---|
# MAGIC | `nged_ltds_capacity_heatmap` | Substation-level demand/generation firm and available capacity, constraints, with geometry |
# MAGIC | `northern_powergrid_capacity_heatmap` + `northern_powergrid_connection_queue` | Northern Powergrid equivalent |
# MAGIC | `nged_connection_queue` + `nged_embedded_capacity_register` | Queued connections and embedded generation |
# MAGIC | `desnz_repd` | Renewable pipeline: planned MW, technology, connection status |
# MAGIC | `dft_aadf` | Traffic volume per road count point per year |
# MAGIC | `overture_segments` | Road/rail/water centrelines with `is_bridge`, `is_tunnel`, speed limits |
# MAGIC | `overture_buildings` | Building footprints for built-environment density |
# MAGIC | `emodnet_vessel_density` | Annual vessel density by type (cargo, tanker, passenger, fishing) with H3 |
# MAGIC | `dft_evci_local_authority` | EV charger rollout trajectory per authority |
# MAGIC | `nspl` | Geographic lookup for authority/region/constituency labelling |
# MAGIC
# MAGIC ## Geospatial Techniques in Play
# MAGIC * `ST_Distance` + H3 join to snap substation locations onto the nearest road segments and renewable sites
# MAGIC * `h3_kring` to spread substation capacity headroom into surrounding hexes (heatmap)
# MAGIC * `ST_Intersects` with `overture_segments` where `is_bridge = true` to count structures per hex, weighted by DfT AADF traffic volume
# MAGIC * H3-based join of `emodnet_vessel_density` to coastal hexes, overlaid with `rnli_lifeboat_stations`
# MAGIC * `ST_Within` to clip the entire model to a single authority or constituency
# MAGIC
# MAGIC ## Stretch Goals
# MAGIC * Overlay the NPG/NGED connection queue onto the renewable pipeline to show where generation is stalled behind grid constraints -- the "curtailment heat map"
# MAGIC * Join `northern_powergrid_historical_peak_demand` with the capacity heatmap to flag substations where peak demand is approaching firm capacity -- the "red line" substations
# MAGIC * **Combine all three challenge outputs:** take the most flood-exposed authorities from Challenge 1, the most underserved LSOAs from Challenge 2, and run them through the prioritisation model to produce a single "invest here first" shortlist
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 3A: NGED substation capacity & constraints
# MAGIC -- Shows demand and generation headroom at each substation.
# MAGIC -- Negative available capacity = the grid is already constrained there.
# MAGIC
# MAGIC SELECT
# MAGIC   name                                       AS substation,
# MAGIC   type,
# MAGIC   licence_area,
# MAGIC   demandfirmcapacity                         AS demand_firm_mva,
# MAGIC   demandavailablecapacity                    AS demand_available_mva,
# MAGIC   demandconstraint,
# MAGIC   generationfirmcapacity                     AS gen_firm_mva,
# MAGIC   generationavailablecapacity                AS gen_available_mva,
# MAGIC   generationconstraint,
# MAGIC   h3_h3tostring(h3_8)                        AS hex_id,
# MAGIC   ROUND(lat, 4)                              AS lat,
# MAGIC   ROUND(lon, 4)                              AS lon
# MAGIC FROM hackathon.two_postcodes.nged_ltds_capacity_heatmap
# MAGIC WHERE demandavailablecapacity IS NOT NULL
# MAGIC ORDER BY demandavailablecapacity ASC    -- most constrained first
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 3B: Renewable pipeline vs grid connection status
# MAGIC -- Summarises planned renewable MW by technology and development status.
# MAGIC -- "Awaiting Construction" or "Application Submitted" projects with high MW
# MAGIC -- indicate where grid connection is the bottleneck.
# MAGIC
# MAGIC SELECT
# MAGIC   technology_type,
# MAGIC   development_status_short                      AS status,
# MAGIC   COUNT(*)                                      AS sites,
# MAGIC   ROUND(SUM(installed_capacity_mwelec), 1)      AS total_mw,
# MAGIC   ROUND(AVG(installed_capacity_mwelec), 2)      AS avg_mw_per_site
# MAGIC FROM hackathon.two_postcodes.desnz_repd
# MAGIC WHERE country = 'England' OR country = 'Wales'
# MAGIC GROUP BY technology_type, development_status_short
# MAGIC ORDER BY total_mw DESC
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 3C: Bridges/tunnels per hex, weighted by traffic volume
# MAGIC -- Counts bridge and tunnel segments per H3 hex from Overture,
# MAGIC -- then joins to DfT AADF traffic counts in the same hex.
# MAGIC -- High bridge count + high traffic = structural priority zone.
# MAGIC
# MAGIC WITH bridge_hex AS (
# MAGIC   SELECT
# MAGIC     h3_pointash3(ST_Centroid(geom), 8)      AS h3_8,
# MAGIC     SUM(CASE WHEN is_bridge THEN 1 ELSE 0 END) AS bridge_count,
# MAGIC     SUM(CASE WHEN is_tunnel THEN 1 ELSE 0 END) AS tunnel_count
# MAGIC   FROM hackathon.two_postcodes.overture_segments
# MAGIC   WHERE subtype = 'road'
# MAGIC     AND (is_bridge = true OR is_tunnel = true)
# MAGIC   GROUP BY 1
# MAGIC ),
# MAGIC traffic_hex AS (
# MAGIC   SELECT
# MAGIC     h3_8,
# MAGIC     ROUND(AVG(all_motor_vehicles), 0)       AS avg_daily_vehicles,
# MAGIC     MAX(year)                               AS latest_year
# MAGIC   FROM hackathon.two_postcodes.dft_aadf
# MAGIC   WHERE h3_8 IS NOT NULL
# MAGIC   GROUP BY h3_8
# MAGIC )
# MAGIC SELECT
# MAGIC   h3_h3tostring(b.h3_8)                     AS hex_id,
# MAGIC   b.bridge_count,
# MAGIC   b.tunnel_count,
# MAGIC   t.avg_daily_vehicles,
# MAGIC   t.latest_year,
# MAGIC   -- Priority score: more bridges under heavier traffic
# MAGIC   ROUND(b.bridge_count * COALESCE(t.avg_daily_vehicles, 0) / 1000.0, 1)
# MAGIC                                             AS bridge_traffic_score
# MAGIC FROM bridge_hex   b
# MAGIC LEFT JOIN traffic_hex t ON b.h3_8 = t.h3_8
# MAGIC ORDER BY bridge_traffic_score DESC
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 3D: EMODnet vessel density by type
# MAGIC -- Shows the busiest coastal hexes by vessel traffic.
# MAGIC -- Join this to rnli_lifeboat_stations to find high-traffic areas
# MAGIC -- with thin emergency cover.
# MAGIC
# MAGIC SELECT
# MAGIC   h3_h3tostring(v.h3_8)                     AS hex_id,
# MAGIC   v.vessel_type,
# MAGIC   ROUND(SUM(v.density), 2)                  AS total_density,
# MAGIC   v.year,
# MAGIC   -- Flag if an RNLI station is in the same hex
# MAGIC   MAX(CASE WHEN r.h3_8 IS NOT NULL THEN 1 ELSE 0 END) AS has_rnli_station
# MAGIC FROM hackathon.two_postcodes.emodnet_vessel_density   v
# MAGIC LEFT JOIN hackathon.two_postcodes.rnli_lifeboat_stations r
# MAGIC   ON v.h3_8 = r.h3_8
# MAGIC WHERE v.h3_8 IS NOT NULL
# MAGIC GROUP BY v.h3_8, v.vessel_type, v.year
# MAGIC ORDER BY total_density DESC
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Challenge 3E: "Red line" substations -- where peak demand is approaching firm capacity
# MAGIC -- Compares NPG historical peak demand to the capacity heatmap
# MAGIC -- to flag substations that may be running out of headroom.
# MAGIC
# MAGIC SELECT
# MAGIC   hp.primary                                              AS substation,
# MAGIC   hp.licence_area,
# MAGIC   hp.max_load_2023_24_mva                                 AS peak_demand_mva,
# MAGIC   ch.firm_cap                                             AS firm_capacity_mva,
# MAGIC   ROUND(hp.max_load_2023_24_mva / NULLIF(ch.firm_cap, 0) * 100, 1)
# MAGIC                                                           AS pct_capacity_used,
# MAGIC   hp.percentage_growth2                                   AS pct_growth_latest
# MAGIC FROM hackathon.two_postcodes.northern_powergrid_historical_peak_demand   hp
# MAGIC JOIN hackathon.two_postcodes.northern_powergrid_capacity_heatmap         ch
# MAGIC   ON hp.primary = ch.psp_name
# MAGIC WHERE ch.firm_cap > 0
# MAGIC   AND hp.max_load_2023_24_mva IS NOT NULL
# MAGIC ORDER BY pct_capacity_used DESC
# MAGIC LIMIT 20

# COMMAND ----------

# MAGIC %md
# MAGIC # Tips for All Teams
# MAGIC
# MAGIC ## H3 is your universal join key
# MAGIC `h3_8` (resolution 8, \~0.74 km² per hex, \~460 m edge) is pre-computed on **every point table**. Start joins there before reaching for `ST_` functions on raw geometry. For display, use `h3_h3tostring(h3_8)`. For a coarser regional view, use `h3_toparent(h3_8, 5)`.
# MAGIC
# MAGIC ## Quick wins
# MAGIC * The **BGS authority inundation table** is the fastest path to a working Challenge 1 prototype -- it already has the exposure numbers pre-computed. Verify one authority with a raw `ST_Intersects` on road geometry, then present both the quick score and the verified score side by side.
# MAGIC * For demo impact, **a single hex map with a clear colour ramp beats ten tables of numbers**.
# MAGIC * Use `LATERAL VIEW INLINE(ARRAY(...))` to unpivot the 2050/2080/2100 columns into rows for time-series charts.
# MAGIC
# MAGIC ## Key spatial functions
# MAGIC
# MAGIC | Function | Use for |
# MAGIC |---|---|
# MAGIC | `h3_kring(h3_8, k)` | Walk-distance bands (k=1 \~460 m, k=2 \~920 m) |
# MAGIC | `h3_toparent(h3_8, resolution)` | Multi-resolution roll-up |
# MAGIC | `h3_pointash3(geom, 8)` | Convert a point geometry to H3 |
# MAGIC | `ST_Intersects(a, b)` | Spatial overlay (e.g. roads inside inundation zones) |
# MAGIC | `ST_Distance(a, b)` | Nearest-facility proximity |
# MAGIC | `ST_Buffer(geom, metres)` | Catchment areas |
# MAGIC | `ST_Area(geom)` / `ST_Length(geom)` | Direct measurement of exposed geometry |
# MAGIC | `ST_Centroid(geom)` | Derive LSOA centroids from polygons |
# MAGIC | `ST_Contains(boundary, point)` | Clip to authority / constituency |
# MAGIC
# MAGIC ## Combining challenges (the ultimate stretch goal)
# MAGIC Take the most **flood-exposed authorities** from Challenge 1, the most **underserved LSOAs** from Challenge 2, and run them through the **investment priority model** from Challenge 3 to produce a single **"invest here first"** shortlist. This cross-challenge synthesis is the most compelling story you can tell.
# MAGIC
# MAGIC ---
# MAGIC *Good luck! All tables are in `hackathon.two_postcodes`. Run any cell above to start exploring.*
