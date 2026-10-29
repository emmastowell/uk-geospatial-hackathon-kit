import { useState, useMemo } from 'react';
import { PageHeader, SectionTitle, Prose, Callout } from '../components/content';
import { CodeBlock } from '../components/CodeBlock';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@databricks/appkit-ui/react';
import { Search } from 'lucide-react';

type Fn = { name: string; cat: string; desc: string };

const H3_FUNCTIONS: Fn[] = [
  { name: 'h3_longlatash3(lon, lat, res)', cat: 'Import', desc: 'Longitude/latitude → H3 cell ID (BIGINT).' },
  { name: 'h3_longlatash3string(lon, lat, res)', cat: 'Import', desc: 'Longitude/latitude → H3 cell ID as hex STRING.' },
  { name: 'h3_pointash3(geog, res)', cat: 'Import', desc: 'GEOGRAPHY point → H3 cell ID.' },
  { name: 'h3_polyfillash3(geog, res)', cat: 'Import', desc: 'Fill a polygon with the H3 cells it contains → ARRAY<BIGINT>.' },
  { name: 'h3_coverash3(geog, res)', cat: 'Import', desc: 'Cover a geography with a minimal set of H3 cells.' },
  { name: 'h3_try_polyfillash3(geog, res)', cat: 'Import', desc: 'Safe polyfill — returns NULL on error instead of failing.' },
  { name: 'h3_boundaryaswkt(cell)', cat: 'Export', desc: 'Cell boundary as a WKT polygon (for drawing hexes).' },
  { name: 'h3_boundaryasgeojson(cell)', cat: 'Export', desc: 'Cell boundary as GeoJSON — feed straight to a web map.' },
  { name: 'h3_centeraswkt(cell)', cat: 'Export', desc: 'Cell center as a WKT point.' },
  { name: 'h3_centerasgeojson(cell)', cat: 'Export', desc: 'Cell center as a GeoJSON point.' },
  { name: 'h3_h3tostring(cell)', cat: 'Convert', desc: 'BIGINT cell ID → hex STRING.' },
  { name: 'h3_stringtoh3(str)', cat: 'Convert', desc: 'Hex STRING → BIGINT cell ID.' },
  { name: 'h3_resolution(cell)', cat: 'Hierarchy', desc: 'Resolution (0–15) of a cell.' },
  { name: 'h3_toparent(cell, res)', cat: 'Hierarchy', desc: 'Parent cell at a coarser resolution (roll up).' },
  { name: 'h3_tochildren(cell, res)', cat: 'Hierarchy', desc: 'All child cells at a finer resolution (drill down).' },
  { name: 'h3_ischildof(a, b)', cat: 'Hierarchy', desc: 'True if cell a equals or is a child of cell b.' },
  { name: 'h3_distance(a, b)', cat: 'Neighbors', desc: 'Grid distance (number of cells) between two cells.' },
  { name: 'h3_kring(cell, k)', cat: 'Neighbors', desc: 'All cells within grid distance k (a filled disk).' },
  { name: 'h3_kringdistances(cell, k)', cat: 'Neighbors', desc: 'Cells within distance k, each with its distance.' },
  { name: 'h3_hexring(cell, k)', cat: 'Neighbors', desc: 'Hollow ring of cells at exactly distance k.' },
  { name: 'h3_compact(cells)', cat: 'Compaction', desc: 'Compact an array of cells to a minimal mixed-resolution set.' },
  { name: 'h3_uncompact(cells, res)', cat: 'Compaction', desc: 'Expand compacted cells back to a uniform resolution.' },
  { name: 'h3_isvalid(expr)', cat: 'Validation', desc: 'Is this BIGINT/STRING a valid H3 cell?' },
  { name: 'h3_ispentagon(cell)', cat: 'Validation', desc: 'Is this cell one of the 12 pentagons per resolution?' },
];

const ST_FUNCTIONS: Fn[] = [
  { name: 'ST_Point(x, y [, srid])', cat: 'Constructors', desc: 'Create a point geometry from coordinates.' },
  { name: 'ST_GeomFromText(wkt [, srid])', cat: 'Constructors', desc: 'Parse a GEOMETRY from WKT.' },
  { name: 'ST_GeogFromText(wkt)', cat: 'Constructors', desc: 'Parse a GEOGRAPHY (SRID 4326) from WKT.' },
  { name: 'ST_GeomFromGeoJSON(json)', cat: 'Constructors', desc: 'Parse a GEOMETRY from GeoJSON.' },
  { name: 'ST_MakeLine(points)', cat: 'Constructors', desc: 'Build a linestring from an array of points.' },
  { name: 'ST_MakePolygon(outer [, holes])', cat: 'Constructors', desc: 'Build a polygon from an outer ring and optional holes.' },
  { name: 'ST_AsText(geo)', cat: 'Export', desc: 'Serialize to WKT.' },
  { name: 'ST_AsGeoJSON(geo)', cat: 'Export', desc: 'Serialize to GeoJSON for web maps.' },
  { name: 'ST_AsBinary(geo)', cat: 'Export', desc: 'Serialize to WKB.' },
  { name: 'ST_X(geo) / ST_Y(geo)', cat: 'Accessors', desc: 'Extract the X (lon) / Y (lat) of a point.' },
  { name: 'ST_Envelope(geo)', cat: 'Accessors', desc: 'Minimum bounding rectangle of a geometry.' },
  { name: 'ST_GeometryType(geo)', cat: 'Accessors', desc: 'Type of the geometry as a string.' },
  { name: 'ST_NPoints(geo)', cat: 'Accessors', desc: 'Total number of vertices.' },
  { name: 'ST_Area(geo)', cat: 'Measurement', desc: 'Area of a polygon in CRS units.' },
  { name: 'ST_Length(geo)', cat: 'Measurement', desc: 'Length of a linestring in CRS units.' },
  { name: 'ST_Distance(a, b)', cat: 'Measurement', desc: 'Cartesian (planar) distance between geometries.' },
  { name: 'ST_DistanceSphere(a, b)', cat: 'Measurement', desc: 'Fast spherical distance in metres (approximate).' },
  { name: 'ST_DistanceSpheroid(a, b)', cat: 'Measurement', desc: 'Accurate geodesic distance on WGS84 in metres.' },
  { name: 'ST_Contains(a, b)', cat: 'Predicates', desc: 'True if a fully contains b.' },
  { name: 'ST_Within(a, b)', cat: 'Predicates', desc: 'True if a is fully within b (inverse of Contains).' },
  { name: 'ST_Intersects(a, b)', cat: 'Predicates', desc: 'True if the geometries share any space.' },
  { name: 'ST_DWithin(a, b, dist)', cat: 'Predicates', desc: 'True if the geometries are within a given distance.' },
  { name: 'ST_Touches(a, b)', cat: 'Predicates', desc: 'True if boundaries touch but interiors do not.' },
  { name: 'ST_Intersection(a, b)', cat: 'Overlay', desc: 'Geometry of the shared space.' },
  { name: 'ST_Union(a, b)', cat: 'Overlay', desc: 'Geometry combining both inputs.' },
  { name: 'ST_Union_Agg(geo)', cat: 'Overlay', desc: 'Aggregate: union of all geometries in a column.' },
  { name: 'ST_Difference(a, b)', cat: 'Overlay', desc: 'Geometry of a minus b.' },
  { name: 'ST_Buffer(geo, radius)', cat: 'Processing', desc: 'Grow a geometry by a radius (catchment areas).' },
  { name: 'ST_Centroid(geo)', cat: 'Processing', desc: 'Center of mass of a geometry.' },
  { name: 'ST_ConvexHull(geo)', cat: 'Processing', desc: 'Smallest convex polygon enclosing the geometry.' },
  { name: 'ST_Simplify(geo, tol)', cat: 'Processing', desc: 'Simplify vertices (Douglas–Peucker).' },
  { name: 'ST_Transform(geo, srid)', cat: 'Reference systems', desc: 'Reproject to a target coordinate system.' },
  { name: 'ST_SetSRID(geo, srid)', cat: 'Reference systems', desc: 'Set the SRID without reprojecting.' },
  { name: 'ST_IsValid(geo)', cat: 'Validation', desc: 'Is the geometry OGC-valid?' },
];

function groupByCat(fns: Fn[]) {
  const map = new Map<string, Fn[]>();
  for (const f of fns) {
    if (!map.has(f.cat)) map.set(f.cat, []);
    map.get(f.cat)!.push(f);
  }
  return Array.from(map.entries());
}

function FunctionList({ fns, query }: { fns: Fn[]; query: string }) {
  const q = query.trim().toLowerCase();
  const filtered = useMemo(
    () => (q ? fns.filter((f) => f.name.toLowerCase().includes(q) || f.desc.toLowerCase().includes(q) || f.cat.toLowerCase().includes(q)) : fns),
    [fns, q],
  );
  const groups = groupByCat(filtered);

  if (filtered.length === 0) {
    return <p className="rounded-lg border border-dashed p-6 text-center text-sm text-muted-foreground">No functions match &ldquo;{query}&rdquo;.</p>;
  }

  return (
    <div className="space-y-6">
      {groups.map(([cat, items]) => (
        <div key={cat}>
          <h3 className="mb-2 text-sm font-semibold text-foreground">{cat}</h3>
          <div className="overflow-hidden rounded-lg border">
            <table className="w-full text-sm">
              <tbody>
                {items.map((f) => (
                  <tr key={f.name} className="border-b last:border-0 align-top">
                    <td className="whitespace-nowrap px-4 py-2.5 font-mono text-[13px]" style={{ color: 'var(--chart-2)' }}>
                      {f.name}
                    </td>
                    <td className="px-4 py-2.5 text-muted-foreground">{f.desc}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
}

export function DbsqlReferencePage() {
  const [query, setQuery] = useState('');

  return (
    <div>
      <PageHeader
        eyebrow="Reference"
        title="DBSQL geospatial function reference"
        lead="Databricks SQL ships 39 H3 functions and 80+ ST functions. This is a working subset grouped by what you'd actually do with them. Use the search to filter across names and descriptions."
      />

      <div className="relative mb-6">
        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search functions… e.g. distance, polyfill, buffer"
          className="w-full rounded-lg border bg-background py-2.5 pl-10 pr-4 text-sm text-foreground outline-none transition-colors placeholder:text-muted-foreground focus:border-primary focus:ring-2 focus:ring-ring/40"
        />
      </div>

      <Tabs defaultValue="h3">
        <TabsList>
          <TabsTrigger value="h3">H3 functions</TabsTrigger>
          <TabsTrigger value="st">ST functions</TabsTrigger>
        </TabsList>
        <TabsContent value="h3" className="mt-5">
          <FunctionList fns={H3_FUNCTIONS} query={query} />
        </TabsContent>
        <TabsContent value="st" className="mt-5">
          <FunctionList fns={ST_FUNCTIONS} query={query} />
        </TabsContent>
      </Tabs>

      <SectionTitle id="worked">Worked example: taxi trips by zip code</SectionTitle>
      <Prose>
        <p>
          A classic pattern that uses import, hierarchy and join functions together — index trips and zip-code polygons to
          the same H3 resolution, then join on the cell ID instead of running point-in-polygon on every row.
        </p>
      </Prose>
      <CodeBlock
        title="H3 spatial join"
        code={`-- 1. Index every trip pickup to a fine resolution
CREATE TABLE trips_h3 AS
SELECT *, h3_longlatash3(pickup_longitude, pickup_latitude, 12) AS pickup_cell
FROM taxi_trips;

-- 2. Fill each zip-code polygon with the cells it covers
CREATE TABLE zipcode_h3 AS
SELECT zipcode, city, explode(h3_polyfillash3(geom, 12)) AS cell
FROM zipcodes;

-- 3. Join on the cell ID — a fast equi-join, no geometry at query time
SELECT z.zipcode, count(*) AS pickups
FROM trips_h3 t
JOIN zipcode_h3 z ON t.pickup_cell = z.cell
GROUP BY z.zipcode
ORDER BY pickups DESC;`}
      />

      <SectionTitle id="viz-prep">Preparing cells for a map</SectionTitle>
      <Prose>
        <p>
          Export functions turn cell IDs back into drawable geometry. Aggregate first, then emit GeoJSON so a client map can
          render a hexbin heatmap directly.
        </p>
      </Prose>
      <CodeBlock
        title="cells → GeoJSON for the client"
        code={`SELECT
  h3_h3tostring(pickup_cell)        AS cell_id,
  h3_boundaryasgeojson(pickup_cell) AS hex_geojson,  -- polygon to draw
  count(*)                          AS pickups        -- value to color by
FROM trips_h3
GROUP BY pickup_cell
HAVING count(*) > 10;`}
      />

      <Callout tone="tip" title="Test SQL before you wire it up">
        Validate any of these against your own tables from the terminal:{' '}
        <code>databricks experimental aitools tools query &quot;SELECT h3_longlatash3(-73.985, 40.748, 9)&quot;</code>. Always add a{' '}
        <code>LIMIT</code> while exploring.
      </Callout>
    </div>
  );
}
