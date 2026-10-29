import { PageHeader, SectionTitle, Prose, Callout, CompareGrid } from '../components/content';
import { CodeBlock } from '../components/CodeBlock';
import { Card, CardContent, CardHeader, CardTitle } from '@databricks/appkit-ui/react';

export function LakebasePage() {
  return (
    <div>
      <PageHeader
        eyebrow="Beyond the lakehouse"
        title="Operational geo in Lakebase & PostGIS"
        lead="The lakehouse is built for analytics over huge, mostly-static datasets. But many spatial workloads are operational: a map in an app that answers 'what's near me right now?' in milliseconds, for one user at a time. That's where Lakebase — Databricks' managed Postgres — and the PostGIS extension come in."
      />

      <SectionTitle id="why">Why a Postgres for geo at all?</SectionTitle>
      <Prose>
        <p>
          Lakebase is a fully-managed, Postgres-compatible OLTP database inside Databricks. Postgres has the most mature
          open-source spatial stack in existence — <strong>PostGIS</strong> — so once you enable the extension you get{' '}
          <code>GEOMETRY</code>/<code>GEOGRAPHY</code> columns, hundreds of <code>ST_</code> functions, and crucially{' '}
          <strong>GiST spatial indexes</strong> that make single-row proximity lookups return in single-digit milliseconds.
        </p>
      </Prose>

      <CompareGrid>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Lakehouse geo (DBSQL)</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm text-muted-foreground">
            <p>Scan and aggregate billions of rows. Seconds-scale.</p>
            <ul className="list-disc space-y-1 pl-5">
              <li>Heatmaps, cohort analysis, batch spatial joins</li>
              <li>H3 indexing + ST functions at scale</li>
              <li>Reads from Delta / Unity Catalog</li>
            </ul>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Lakebase geo (PostGIS)</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm text-muted-foreground">
            <p>Fetch a handful of rows by location. Millisecond-scale.</p>
            <ul className="list-disc space-y-1 pl-5">
              <li>&ldquo;Nearest 10 stores to the user&rdquo; lookups</li>
              <li>GiST / SP-GiST indexes, per-request queries</li>
              <li>Serves live app traffic for one user at a time</li>
            </ul>
          </CardContent>
        </Card>
      </CompareGrid>

      <SectionTitle id="postgis">Enabling PostGIS</SectionTitle>
      <Prose>
        <p>PostGIS is an extension. Enable it once, then model spatial columns and index them with GiST.</p>
      </Prose>
      <CodeBlock
        title="postgres (PostGIS)"
        lang="sql"
        code={`-- Enable the extension once per database
CREATE EXTENSION IF NOT EXISTS postgis;

-- A table with a geography column (lon/lat, SRID 4326)
CREATE TABLE stores (
  id        bigserial PRIMARY KEY,
  name      text NOT NULL,
  location  geography(Point, 4326)
);

-- The spatial index that makes proximity fast
CREATE INDEX stores_location_gix ON stores USING GIST (location);

INSERT INTO stores (name, location) VALUES
  ('Downtown', ST_SetSRID(ST_MakePoint(-73.9857, 40.7484), 4326)),
  ('Midtown',  ST_SetSRID(ST_MakePoint(-73.9787, 40.7614), 4326));`}
      />

      <SectionTitle id="knn">The query that defines operational geo</SectionTitle>
      <Prose>
        <p>
          A nearest-neighbour lookup. The <code>&lt;-&gt;</code> KNN operator uses the GiST index to answer in milliseconds,
          even with millions of rows — exactly the kind of query a user triggers by panning a map.
        </p>
      </Prose>
      <CodeBlock
        title="postgres — nearest N (index-accelerated)"
        lang="sql"
        code={`-- 10 nearest stores to a user's position, ordered by true distance
SELECT id, name,
       ST_Distance(location, ST_SetSRID(ST_MakePoint($1, $2), 4326)) AS metres
FROM stores
ORDER BY location <-> ST_SetSRID(ST_MakePoint($1, $2), 4326)   -- KNN via GiST
LIMIT 10;

-- Everything within a 1 km radius
SELECT id, name
FROM stores
WHERE ST_DWithin(location, ST_SetSRID(ST_MakePoint($1, $2), 4326), 1000);`}
      />

      <Callout tone="info" title="Note the function overlap">
        PostGIS also uses <code>ST_</code> names, but it is a <em>different</em> engine from DBSQL&apos;s ST functions — some
        signatures differ (<code>ST_MakePoint</code> vs <code>ST_Point</code>, parameter order, SRID handling). Treat them as
        two dialects of the same idea, not interchangeable code.
      </Callout>

      <SectionTitle id="pattern">The lakehouse + Lakebase pattern</SectionTitle>
      <Prose>
        <p>
          The two aren&apos;t rivals — they&apos;re layers. Do heavy spatial computation in the lakehouse, then publish the
          serving-ready result into Lakebase so your app reads it instantly. Databricks <strong>synced tables</strong> keep a
          Delta table continuously mirrored into Lakebase Postgres, so the operational copy stays fresh automatically.
        </p>
      </Prose>
      <Card className="my-4">
        <CardContent className="pt-6">
          <ol className="space-y-3 text-sm text-muted-foreground">
            <li className="flex gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">1</span>
              <span><strong className="text-foreground">Compute in the lakehouse:</strong> H3-index and enrich billions of rows with DBSQL on a warehouse.</span>
            </li>
            <li className="flex gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">2</span>
              <span><strong className="text-foreground">Sync to Lakebase:</strong> publish the serving table (e.g. store locations + attributes) via a synced table.</span>
            </li>
            <li className="flex gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">3</span>
              <span><strong className="text-foreground">Serve from the app:</strong> the AppKit app runs a GiST-indexed KNN query per request for instant maps.</span>
            </li>
          </ol>
        </CardContent>
      </Card>

      <Callout tone="warning" title="When NOT to add Lakebase">
        A read-only dashboard, heatmap, or report does <em>not</em> need Lakebase — query the warehouse directly with the
        analytics path. Reach for Lakebase only when you need sub-second per-user lookups, typeahead, or write-back of
        user-generated spatial data.
      </Callout>
    </div>
  );
}
