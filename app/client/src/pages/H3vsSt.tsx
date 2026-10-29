import { PageHeader, SectionTitle, Prose, Callout, CompareGrid } from '../components/content';
import { CodeBlock } from '../components/CodeBlock';
import { Card, CardContent } from '@databricks/appkit-ui/react';
import { HexGridDiagram, ResolutionDiagram, PointInPolygonDiagram, BufferDiagram } from '../components/Diagrams';
import { ExampleQuery } from '../components/ExampleQuery';
import { h3Hotspots, h3Ring, nearestVessels, vesselsInBbox } from '../data/exampleQueries';
import { Check, X } from 'lucide-react';

function YesNo({ ok, children }: { ok: boolean; children: React.ReactNode }) {
  return (
    <li className="flex items-start gap-2">
      {ok ? (
        <Check className="mt-0.5 h-4 w-4 shrink-0" style={{ color: 'var(--success)' }} />
      ) : (
        <X className="mt-0.5 h-4 w-4 shrink-0" style={{ color: 'var(--muted-foreground)' }} />
      )}
      <span>{children}</span>
    </li>
  );
}

export function H3vsStPage() {
  return (
    <div>
      <PageHeader
        eyebrow="The core decision"
        title="H3 grid indexing vs ST vector geometry"
        lead="Databricks SQL gives you two complementary ways to work with space. They are not competitors — they answer different questions. Understanding the trade-off is the key to fast, correct spatial analytics."
      />

      <CompareGrid>
        <Card>
          <CardContent className="pt-6">
            <HexGridDiagram className="mx-auto h-40" />
            <h3 className="mt-3 text-base font-semibold text-foreground">H3 — discrete hexagonal grid</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              Uber&apos;s hierarchical hex index. Every lon/lat snaps to a cell ID (a <code className="rounded bg-muted px-1 font-mono text-xs">BIGINT</code>).
              Space becomes a <strong>key you can join and group on</strong>.
            </p>
            <ul className="mt-3 space-y-1.5 text-sm text-muted-foreground">
              <YesNo ok>Blazing-fast joins &amp; aggregation (equi-join on cell ID)</YesNo>
              <YesNo ok>Natural binning / heatmaps at any zoom</YesNo>
              <YesNo ok>Works on any warehouse since DBR 11.2</YesNo>
              <YesNo ok={false}>Approximate — a cell is not an exact shape</YesNo>
            </ul>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <PointInPolygonDiagram className="mx-auto h-40" />
            <h3 className="mt-3 text-base font-semibold text-foreground">ST — exact vector geometry</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              OGC-standard functions on real <code className="rounded bg-muted px-1 font-mono text-xs">GEOMETRY</code>/<code className="rounded bg-muted px-1 font-mono text-xs">GEOGRAPHY</code> values.
              Points, lines and polygons with <strong>precise</strong> measurement and relationships.
            </p>
            <ul className="mt-3 space-y-1.5 text-sm text-muted-foreground">
              <YesNo ok>Exact distance, area, containment, intersection</YesNo>
              <YesNo ok>80+ standard functions (PostGIS-like)</YesNo>
              <YesNo ok>Spatial-join auto-optimization (up to 17× faster)</YesNo>
              <YesNo ok={false}>Needs DBR 17.1+ serverless for native types (Preview)</YesNo>
            </ul>
          </CardContent>
        </Card>
      </CompareGrid>

      <SectionTitle id="h3-model">How H3 thinks about the world</SectionTitle>
      <Prose>
        <p>
          H3 divides the globe into hexagons at <strong>16 resolutions</strong> (0 = continent-scale, 15 = a few square
          metres). Each cell has exactly one parent at the coarser level and 7 children at the finer level, so you can roll
          data up and down a hierarchy just by changing a number.
        </p>
      </Prose>
      <Card className="my-4">
        <CardContent className="pt-6">
          <ResolutionDiagram className="mx-auto h-28 w-full max-w-md" />
        </CardContent>
      </Card>
      <CodeBlock
        title="H3 — space as a join key"
        code={`-- Index each point to a resolution-9 hex cell
SELECT h3_longlatash3(-73.985, 40.748, 9) AS cell;        -- a BIGINT key

-- Count rides per cell: a plain GROUP BY, no spatial math
SELECT pickup_cell, count(*) AS rides
FROM trips_h3
GROUP BY pickup_cell;

-- Roll up to a coarser resolution for a zoomed-out heatmap
SELECT h3_toparent(pickup_cell, 7) AS coarse_cell, count(*) AS rides
FROM trips_h3
GROUP BY h3_toparent(pickup_cell, 7);

-- Proximity without geometry: all cells within 2 rings
SELECT explode(h3_kring(h3_longlatash3(-73.985, 40.748, 9), 2)) AS nearby;`}
      />
      <Prose>
        <p>
          Enough theory, here is a worked example. The query below indexes vessel positions into H3 cells and ranks the busiest.
          Drop the resolution to see space collapse into a few huge cells; raise it to zoom in.
        </p>
      </Prose>
      <ExampleQuery def={h3Hotspots} />
      <Prose>
        <p>
          And here is the proximity idea made concrete: every cell within <code>k</code> grid steps of a point, returned with a
          drawable GeoJSON boundary.
        </p>
      </Prose>
      <ExampleQuery def={h3Ring} />

      <SectionTitle id="st-model">How ST functions think about the world</SectionTitle>
      <Prose>
        <p>
          ST functions operate on the <em>actual shapes</em>. You ask precise questions — &ldquo;is this point inside that
          delivery zone?&rdquo;, &ldquo;how far apart are these two stores?&rdquo;, &ldquo;what&apos;s the overlap of these
          two regions?&rdquo; — and get exact answers.
        </p>
      </Prose>
      <div className="my-4 grid gap-4 sm:grid-cols-2">
        <Card>
          <CardContent className="pt-6">
            <BufferDiagram className="mx-auto h-28" />
            <p className="mt-2 text-center text-sm text-muted-foreground">Processing: grow a catchment area around a site.</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <PointInPolygonDiagram className="mx-auto h-28" />
            <p className="mt-2 text-center text-sm text-muted-foreground">Predicate: exactly which points fall inside a region.</p>
          </CardContent>
        </Card>
      </div>
      <CodeBlock
        title="ST — exact spatial questions"
        code={`-- Point-in-polygon: which stores are inside a delivery zone?
SELECT s.name, z.zone_name
FROM retail_stores s
JOIN delivery_zones z
  ON ST_Contains(z.boundary, s.location);

-- Exact distance between two stores (metres, on the sphere)
SELECT ST_DistanceSphere(a.location, b.location) AS metres
FROM retail_stores a, retail_stores b
WHERE a.store_id = 1 AND b.store_id = 2;

-- Everything within 1 km of a store (a buffer / catchment)
SELECT c.customer_id
FROM customers c, retail_stores s
WHERE s.store_id = 1
  AND ST_DWithin(ST_GeogFromText(ST_AsText(c.location)),
                 ST_GeogFromText(ST_AsText(s.location)), 1000);`}
      />
      <Prose>
        <p>
          Now the exact version. For any point, ST_DistanceSphere ranks the vessels nearest to it: precise metres, not
          approximate cells.
        </p>
      </Prose>
      <ExampleQuery def={nearestVessels} />
      <Prose>
        <p>
          And the predicate in action: a bounding-box polygon built from four coordinates, with <code>ST_Contains</code> counting
          exactly which positions fall inside it.
        </p>
      </Prose>
      <ExampleQuery def={vesselsInBbox} />

      <SectionTitle id="pick">Which should I reach for?</SectionTitle>
      <div className="my-4 overflow-hidden rounded-lg border">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b bg-muted/50 text-left">
              <th className="px-4 py-2.5 font-semibold text-foreground">If your question is…</th>
              <th className="px-4 py-2.5 font-semibold text-foreground">Reach for</th>
            </tr>
          </thead>
          <tbody className="text-muted-foreground">
            {[
              ['Count / aggregate events by area, build a heatmap', 'H3'],
              ['Join two huge datasets by approximate location', 'H3'],
              ['Roll data up and down zoom levels', 'H3'],
              ['Is this point exactly inside this polygon?', 'ST'],
              ['Exact distance, area, length or perimeter', 'ST'],
              ['Intersection, union or difference of shapes', 'ST'],
              ['Billions of rows that must also be precise', 'H3 to pre-filter, then ST'],
            ].map(([q, a]) => (
              <tr key={q} className="border-b last:border-0">
                <td className="px-4 py-2.5">{q}</td>
                <td className="px-4 py-2.5">
                  <span className="font-medium text-foreground">{a}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <SectionTitle id="combine">The power move: combine them</SectionTitle>
      <Prose>
        <p>
          The fastest precise spatial joins use H3 as a <strong>coarse pre-filter</strong> and ST for the{' '}
          <strong>exact finish</strong>. H3 cheaply eliminates far-apart pairs with an equi-join; ST then runs expensive
          geometry only on the handful of candidates that survive.
        </p>
      </Prose>
      <CodeBlock
        title="H3 pre-filter + ST precision"
        code={`-- Index both sides to the same resolution once
CREATE TABLE store_h3 AS
SELECT store_id, name, location,
  h3_longlatash3(ST_X(location), ST_Y(location), 9) AS h3_cell
FROM retail_stores;

CREATE TABLE customer_h3 AS
SELECT customer_id, name, location,
  h3_longlatash3(ST_X(location), ST_Y(location), 9) AS h3_cell
FROM customers;

-- Candidates share a nearby cell (cheap), survivors are exact (precise)
SELECT s.name AS store, c.name AS customer,
  ST_DistanceSphere(s.location, c.location) AS distance_m
FROM store_h3 s
JOIN customer_h3 c
  ON c.h3_cell IN (SELECT explode(h3_kring(s.h3_cell, 2)))   -- H3 pre-filter
WHERE ST_DistanceSphere(s.location, c.location) < 2000;      -- ST precision`}
      />

      <Callout tone="tip" title="Performance notes">
        Spatial predicates in a JOIN (<code>ST_Intersects</code>, <code>ST_Contains</code>, <code>ST_Within</code>) are
        auto-optimized with spatial indexing — up to 17× faster than classic clusters, no code change. Add a{' '}
        <code>/*+ BROADCAST(small_table) */</code> hint when one side is small, and prefer a projected SRID (e.g. 5070) over
        spheroid functions when you measure in metres.
      </Callout>
    </div>
  );
}
