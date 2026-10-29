import { PageHeader, SectionTitle, Prose, Callout } from '../components/content';
import { CodeBlock } from '../components/CodeBlock';
import { Card, CardContent } from '@databricks/appkit-ui/react';
import { Layers, MousePointerClick, Palette, Gauge } from 'lucide-react';

const CAPABILITIES = [
  { icon: MousePointerClick, title: 'Custom interactivity', desc: 'Click a hex to drill in, draw a selection, link a map to a side panel — behaviour a managed dashboard can\u2019t express.' },
  { icon: Palette, title: 'Full styling control', desc: 'Your own layout, components and semantic colors via AppKit-ui tokens; the map is one element in a bespoke UI.' },
  { icon: Gauge, title: 'Live, per-user data', desc: 'Serve each user their own view — fetch from a warehouse, or do millisecond lookups from Lakebase.' },
  { icon: Layers, title: 'Multiple layers', desc: 'Overlay points, hex heatmaps, polygons and routes together with map libraries like deck.gl or MapLibre.' },
];

export function VisualizePage() {
  return (
    <div>
      <PageHeader
        eyebrow="See your data"
        title="Visualizing geo in Databricks Apps"
        lead="A custom Databricks App (like this one, built on AppKit) is the right surface when you need a bespoke, interactive map experience — not just a chart. You own the frontend, so you can render spatial data however your use case demands."
      />

      <SectionTitle id="when">When a custom app is the right call</SectionTitle>
      <Prose>
        <p>
          If you only need a few maps and charts for reporting, a managed <strong>AI/BI dashboard</strong> is simpler (see the
          next page). Reach for a custom app when you need any of these:
        </p>
      </Prose>
      <div className="my-5 grid gap-3 sm:grid-cols-2">
        {CAPABILITIES.map((c) => {
          const Icon = c.icon;
          return (
            <Card key={c.title}>
              <CardContent className="flex gap-3 pt-6">
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
                  <Icon className="h-4.5 w-4.5" />
                </span>
                <div>
                  <p className="text-sm font-semibold text-foreground">{c.title}</p>
                  <p className="mt-1 text-xs leading-relaxed text-muted-foreground">{c.desc}</p>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <SectionTitle id="flow">How the data gets to the map</SectionTitle>
      <Prose>
        <p>
          The pattern is always: compute geometry in SQL, emit it as <strong>GeoJSON</strong>, and hand it to a map
          component in the browser. In AppKit, read-only aggregates come from a <code>config/queries/*.obo.sql</code> file via
          the analytics query hook; the result rows carry GeoJSON strings you parse and feed to the renderer.
        </p>
      </Prose>
      <CodeBlock
        title="config/queries/hexbins.obo.sql"
        code={`-- Aggregate to H3 cells and emit drawable GeoJSON + a value to color by
SELECT
  h3_h3tostring(cell)          AS cell_id,
  h3_boundaryasgeojson(cell)   AS geometry,
  count(*)                     AS trips
FROM (
  SELECT h3_longlatash3(pickup_longitude, pickup_latitude, 8) AS cell
  FROM samples.nyctaxi.trips
)
GROUP BY cell
HAVING count(*) > 5;`}
      />
      <Prose>
        <p>On the client, the typed rows drive a map layer. The sketch below shows the shape of it (map library omitted):</p>
      </Prose>
      <CodeBlock
        title="client/src/MapView.tsx (sketch)"
        lang="tsx"
        code={`import { useAnalyticsQuery } from '@databricks/appkit/react';

function HexLayer() {
  const { data, loading, error } = useAnalyticsQuery('hexbins');
  if (loading) return <Skeleton className="h-96 w-full" />;
  if (error)   return <Alert variant="destructive">Couldn't load map data</Alert>;

  // Each row: { cell_id, geometry (GeoJSON string), trips }
  const features = data.rows.map((r) => ({
    type: 'Feature',
    geometry: JSON.parse(r.geometry),
    properties: { trips: r.trips },
  }));

  // Hand 'features' to deck.gl GeoJsonLayer / MapLibre, color by trips...
  return <DeckMap features={features} colorBy="trips" />;
}`}
      />

      <Callout tone="warning" title="Maps need tiles — plan for the network">
        Browser map libraries (MapLibre, deck.gl basemaps, Leaflet) fetch tile images from an external tile server. A deployed
        Databricks App must be able to reach that host, or you must self-host / embed tiles. Pure vector overlays (your GeoJSON
        hexes and polygons on a plain background) render with no external calls at all — the safest default.
      </Callout>

      <SectionTitle id="charts">Not everything needs a basemap</SectionTitle>
      <Prose>
        <p>
          Often the geography is a grouping, not the point. &ldquo;Trips by borough&rdquo; or &ldquo;revenue by region&rdquo;
          read perfectly well as a sorted <strong>bar chart</strong> — AppKit-ui ships ECharts-based <code>BarChart</code>,{' '}
          <code>LineChart</code> and <code>HeatmapChart</code> components you can bind directly to a <code>queryKey</code>. Use a
          map only when spatial position itself carries the meaning.
        </p>
      </Prose>

      <Callout tone="tip" title="Always handle the three states">
        Every data view in an app must cover <strong>loading</strong> (skeleton), <strong>empty</strong> (a helpful message),
        and <strong>error</strong> (an inline alert, never a blank map). A map that silently renders nothing looks identical to
        a map with no data — disambiguate it.
      </Callout>
    </div>
  );
}
