import { PageHeader, SectionTitle, Prose, Callout, FunctionTable, CompareGrid } from '../components/content';
import { CodeBlock } from '../components/CodeBlock';
import { ExampleQuery } from '../components/ExampleQuery';
import { longestVoyages } from '../data/exampleQueries';
import { Card, CardContent, CardHeader, CardTitle } from '@databricks/appkit-ui/react';

export function FoundationsPage() {
  return (
    <div>
      <PageHeader
        eyebrow="Foundations"
        title="Types, coordinate systems & formats"
        lead="Before functions, understand what a spatial value actually is. Databricks SQL has two native spatial data types and a handful of interchange formats. Getting these right prevents the most common geospatial bug: coordinates that silently mean the wrong thing."
      />

      <SectionTitle id="types">GEOMETRY vs GEOGRAPHY</SectionTitle>
      <Prose>
        <p>
          Databricks SQL ships two spatial types. They look similar but model the Earth differently — and that difference
          changes what your distance and area calculations mean.
        </p>
      </Prose>

      <CompareGrid>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <span style={{ color: 'var(--chart-1)' }}>■</span> GEOMETRY
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-muted-foreground">
            <p>Treats the Earth as a <strong>flat plane</strong> (Euclidean X/Y). Fast and exact in a projected coordinate system.</p>
            <ul className="list-disc space-y-1 pl-5">
              <li>Supports 11,000+ SRIDs (projected CRS)</li>
              <li>Distance / area in the CRS&apos;s own units (metres, feet…)</li>
              <li>Best for local or regional data already projected</li>
            </ul>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <span style={{ color: 'var(--chart-2)' }}>■</span> GEOGRAPHY
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-muted-foreground">
            <p>Models the Earth as a <strong>sphere/spheroid</strong> using longitude/latitude. Correct over long, global distances.</p>
            <ul className="list-disc space-y-1 pl-5">
              <li>WGS 84 only — <strong>SRID 4326</strong></li>
              <li>Distances in metres along the Earth&apos;s surface</li>
              <li>Best for global data in lon/lat</li>
            </ul>
          </CardContent>
        </Card>
      </CompareGrid>

      <Callout tone="warning" title="Longitude comes first">
        Databricks constructors take coordinates as <code>(longitude, latitude)</code> — i.e. <code>(x, y)</code> — not{' '}
        <code>(lat, lon)</code>. New York City is <code>ST_Point(-73.985, 40.748)</code>. Flipping them is the #1 geospatial
        mistake; <code>ST_FlipCoordinates()</code> exists precisely because it happens so often.
      </Callout>

      <Prose>
        <p>Both types support the full set of subtypes: <strong>Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon</strong> and <strong>GeometryCollection</strong>.</p>
      </Prose>

      <CodeBlock
        title="choosing a type"
        code={`-- GEOMETRY in a projected CRS (metres) — accurate local distances
SELECT ST_Distance(
  ST_Transform(ST_Point(-73.985, 40.748, 4326), 5070),  -- NAD83 / Albers
  ST_Transform(ST_Point(-73.968, 40.783, 4326), 5070)
) AS metres;

-- GEOGRAPHY — spherical distance straight from lon/lat, no projection
SELECT ST_DistanceSphere(
  ST_GeogFromText('POINT(-73.985 40.748)'),
  ST_GeogFromText('POINT(-73.968 40.783)')
) AS metres;`}
      />

      <SectionTitle id="srid">What is an SRID?</SectionTitle>
      <Prose>
        <p>
          A <strong>Spatial Reference Identifier</strong> tells the engine which coordinate system a geometry lives in.{' '}
          <code>4326</code> is plain lon/lat (WGS 84). Projected systems like <code>5070</code> (US Albers, metres) or a UTM
          zone flatten a region so that distances and areas are measured in real units.
        </p>
        <p>
          Rule of thumb: store in <code>4326</code>, then <code>ST_Transform()</code> to a projected SRID when you need to
          measure length or area in metres.
        </p>
      </Prose>

      <SectionTitle id="formats">Interchange formats</SectionTitle>
      <Prose>
        <p>Spatial values move between systems as text or binary. You&apos;ll meet these constantly:</p>
      </Prose>
      <FunctionTable
        rows={[
          { fn: 'WKT', desc: <>Well-Known Text — human readable, e.g. <code>POINT(-73.98 40.74)</code>. Import with <code>ST_GeomFromText</code>.</> },
          { fn: 'WKB', desc: <>Well-Known Binary — compact binary form. Import with <code>ST_GeomFromWKB</code>.</> },
          { fn: 'EWKT / EWKB', desc: <>Extended variants that also carry the SRID inline.</> },
          { fn: 'GeoJSON', desc: <>JSON format used by web maps and APIs. Import with <code>ST_GeomFromGeoJSON</code>, export with <code>ST_AsGeoJSON</code>.</> },
          { fn: 'Geohash', desc: <>Hierarchical string grid encoding. Convert with <code>ST_GeomFromGeoHash</code> / <code>ST_GeoHash</code>.</> },
        ]}
      />

      <CodeBlock
        title="formats in, formats out"
        code={`-- Parse from different sources
SELECT ST_GeomFromText('POINT(-73.985 40.748)', 4326)        AS from_wkt;
SELECT ST_GeomFromGeoJSON('{"type":"Point","coordinates":[-73.985,40.748]}') AS from_geojson;

-- Serialize the same geometry to whatever a downstream system expects
SELECT
  ST_AsText(location)    AS wkt,
  ST_AsGeoJSON(location) AS geojson,   -- feed this straight to a web map
  ST_GeoHash(location)   AS geohash
FROM retail_stores;`}
      />

      <Prose>
        <p>
          WKT isn&apos;t just for toy literals — real tables store geometry this way. Below, each vessel&apos;s voyage is a WKT
          <code>LINESTRING</code>; <code>ST_GeogFromText</code> parses it and <code>ST_Length</code> measures the true distance
          travelled. The example assumes a table of vessels with a WKT track column:
        </p>
      </Prose>
      <ExampleQuery def={longestVoyages} />

      <Callout tone="tip" title="Storing geometry where native types aren't available">
        Native <code>GEOMETRY</code>/<code>GEOGRAPHY</code> columns need serverless on DBR 17.1+. On older SQL warehouses, store
        geometry as a <code>STRING</code> WKT column and convert at query time with <code>ST_GeomFromText()</code>. H3 cell IDs,
        by contrast, are just <code>BIGINT</code>/<code>STRING</code> and work everywhere.
      </Callout>

      <Callout tone="info" title="Next">
        With types and formats in hand, the big decision is how to <em>index and query</em> space. That&apos;s the H3 vs ST
        distinction — the heart of this guide.
      </Callout>
    </div>
  );
}
