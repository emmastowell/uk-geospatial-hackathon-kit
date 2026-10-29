export type ParamSpec = {
  name: string;
  label: string;
  default: number;
  help?: string;
};

export type ExampleDef = {
  concept: 'h3' | 'st';
  title: string;
  description: string;
  /** Table the query reads, with the columns it expects. */
  table: string;
  columns: string;
  params: ParamSpec[];
  /** SQL with `:name` placeholders; the page shows it with the default values filled in. */
  sqlText: string;
};

const POSITIONS = 'your_catalog.your_schema.vessel_positions';
const POSITION_COLUMNS = 'latitude, longitude, speed_knots, vessel_category (one row per position report)';
const VESSELS = 'your_catalog.your_schema.vessel_current_locations';

export const h3Hotspots: ExampleDef = {
  concept: 'h3',
  title: 'Bin positions into hexagons',
  description:
    'Snap vessel positions to H3 cells and count the busiest ones. Lower the resolution for bigger cells (zoomed out), raise it for smaller cells (zoomed in).',
  table: POSITIONS,
  columns: POSITION_COLUMNS,
  params: [
    { name: 'res', label: 'H3 resolution', default: 5, help: '0 = continent · 15 = metres' },
    { name: 'row_limit', label: 'Max rows', default: 25 },
  ],
  sqlText: `SELECT
  h3_h3tostring(cell)        AS h3_cell,
  count(*)                   AS positions,
  round(avg(speed_knots), 1) AS avg_speed_knots
FROM (
  SELECT h3_longlatash3(longitude, latitude, :res) AS cell, speed_knots
  FROM ${POSITIONS}
)
GROUP BY cell
ORDER BY positions DESC
LIMIT :row_limit`,
};

export const h3Ring: ExampleDef = {
  concept: 'h3',
  title: 'Neighbouring cells as GeoJSON',
  description:
    'Every H3 cell within k grid steps of a point (a filled hexagonal disk), each with its grid distance and a drawable GeoJSON boundary: exactly what you’d feed a map.',
  table: 'none (built from the point you choose)',
  columns: 'no table needed',
  params: [
    { name: 'lon', label: 'Longitude', default: -74 },
    { name: 'lat', label: 'Latitude', default: 40.7 },
    { name: 'res', label: 'H3 resolution', default: 6 },
    { name: 'k', label: 'Ring size (k)', default: 2, help: 'Steps out from the centre' },
  ],
  sqlText: `SELECT
  h3_h3tostring(cell)                                 AS h3_cell,
  h3_distance(cell, h3_longlatash3(:lon, :lat, :res)) AS ring_distance,
  h3_boundaryasgeojson(cell)                          AS boundary_geojson
FROM (
  SELECT explode(h3_kring(h3_longlatash3(:lon, :lat, :res), :k)) AS cell
)
ORDER BY ring_distance, h3_cell`,
};

export const nearestVessels: ExampleDef = {
  concept: 'st',
  title: 'Nearest vessels to a point',
  description:
    'Rank vessels by how close their last known position is to a point you choose. ST_DistanceSphere returns metres on the Earth’s surface; the query shows kilometres.',
  table: VESSELS,
  columns: 'vessel_name, vessel_category, current_lon, current_lat, speed_knots, last_seen (one row per vessel)',
  params: [
    { name: 'lon', label: 'Longitude', default: -74, help: 'West is negative' },
    { name: 'lat', label: 'Latitude', default: 40.7, help: 'South is negative' },
    { name: 'row_limit', label: 'Max rows', default: 25 },
  ],
  sqlText: `SELECT
  vessel_name,
  vessel_category,
  round(ST_DistanceSphere(
    ST_Point(current_lon, current_lat),
    ST_Point(:lon, :lat)) / 1000, 2) AS distance_km,
  round(speed_knots, 1) AS speed_knots,
  last_seen
FROM ${VESSELS}
ORDER BY distance_km ASC
LIMIT :row_limit`,
};

export const longestVoyages: ExampleDef = {
  concept: 'st',
  title: 'Measure track length from WKT',
  description:
    'Each vessel’s recorded path is stored as a WKT LINESTRING. ST_GeogFromText parses that text into geometry and ST_Length measures its true length along the Earth’s surface.',
  table: VESSELS,
  columns: 'vessel_name, vessel_category, num_waypoints, trajectory_wkt (a LINESTRING as text)',
  params: [
    { name: 'min_waypoints', label: 'Min waypoints', default: 500, help: 'Longer, denser tracks only' },
    { name: 'row_limit', label: 'Max rows', default: 25 },
  ],
  sqlText: `SELECT
  vessel_name,
  vessel_category,
  num_waypoints,
  round(ST_Length(ST_GeogFromText(trajectory_wkt)) / 1000, 1) AS track_length_km
FROM ${VESSELS}
WHERE trajectory_wkt IS NOT NULL AND num_waypoints >= :min_waypoints
ORDER BY track_length_km DESC
LIMIT :row_limit`,
};

export const vesselsInBbox: ExampleDef = {
  concept: 'st',
  title: 'Count positions inside a polygon',
  description:
    'Build a bounding-box polygon from four coordinates (as WKT) and count the positions that fall inside it with ST_Contains, broken down by vessel category.',
  table: POSITIONS,
  columns: POSITION_COLUMNS,
  params: [
    { name: 'min_lon', label: 'Min longitude', default: -80.5 },
    { name: 'min_lat', label: 'Min latitude', default: 25 },
    { name: 'max_lon', label: 'Max longitude', default: -79.5 },
    { name: 'max_lat', label: 'Max latitude', default: 26.5 },
    { name: 'row_limit', label: 'Max rows', default: 25 },
  ],
  sqlText: `SELECT vessel_category, count(*) AS positions
FROM ${POSITIONS}
WHERE ST_Contains(
  ST_GeomFromText(
    'POLYGON((' ||
    CAST(:min_lon AS STRING)||' '||CAST(:min_lat AS STRING)||','||
    CAST(:max_lon AS STRING)||' '||CAST(:min_lat AS STRING)||','||
    CAST(:max_lon AS STRING)||' '||CAST(:max_lat AS STRING)||','||
    CAST(:min_lon AS STRING)||' '||CAST(:max_lat AS STRING)||','||
    CAST(:min_lon AS STRING)||' '||CAST(:min_lat AS STRING)||'))'),
  ST_Point(longitude, latitude))
GROUP BY vessel_category
ORDER BY positions DESC
LIMIT :row_limit`,
};
