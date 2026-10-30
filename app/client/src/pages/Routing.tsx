import { PageHeader, SectionTitle, Prose, Callout, CompareGrid, FunctionTable } from '../components/content';
import { CodeBlock } from '../components/CodeBlock';
import { Card, CardContent, CardHeader, CardTitle } from '@databricks/appkit-ui/react';

const SOLUTION_URL = 'https://github.com/emmastowell/uk-geospatial-hackathon-kit/tree/main/routing';

const ENGINES = [
  {
    name: 'Valhalla',
    stack: 'C++, MIT licence',
    strengths: 'Travel mode and preferences set per request; routes, matrices, isochrones and map matching in one engine; Python bindings (pyvalhalla).',
    watch: 'Slower than OSRM for very large matrices.',
  },
  {
    name: 'OSRM',
    stack: 'C++, BSD licence',
    strengths: 'Very fast routes and matrices from a preprocessed graph; well suited to large batch matrices.',
    watch: 'Travel modes are fixed when the graph is built, so a change means a rebuild; no isochrones.',
  },
  {
    name: 'GraphHopper',
    stack: 'Java, Apache 2.0 licence',
    strengths: 'Fast routing with flexible custom models; isochrones and map matching.',
    watch: 'The matrix API is part of the commercial edition, not the open-source engine.',
  },
  {
    name: 'pgRouting',
    stack: 'Postgres extension, GPL licence',
    strengths: 'Shortest paths as SQL functions over any network you store in tables, such as pipes, rail or footpaths.',
    watch: 'Not built for country-scale road routing; check your Postgres service supports the extension.',
  },
];

export function RoutingPage() {
  return (
    <div>
      <PageHeader
        eyebrow="Beyond the lakehouse"
        title="Routing engines"
        lead="Spatial SQL tells you how far apart two places are as the crow flies. Most real questions are about the network: how long it takes to drive, walk or cycle, and what lies within a 15-minute trip. A routing engine answers those questions over a road graph built from OpenStreetMap."
      />

      <SectionTitle id="why">Why straight-line distance is not enough</SectionTitle>
      <Prose>
        <p>
          <code>ST_DistanceSphere</code> and <code>h3_distance</code> measure separation, not travel. Two postcodes either side
          of an estuary can be 2 km apart and a 40-minute drive. A hospital can be the nearest in a straight line and the third
          nearest by road. When the answer depends on roads, one-way streets, speed limits or footpaths, you need a routing
          engine.
        </p>
      </Prose>

      <CompareGrid>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Crow-flies distance (DBSQL)</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm text-muted-foreground">
            <p>Geometry only. Runs over billions of rows.</p>
            <ul className="list-disc space-y-1 pl-5">
              <li>Radius searches and nearest-neighbour shortlists</li>
              <li>Pre-filtering candidates with H3 cells</li>
              <li>No knowledge of roads or travel modes</li>
            </ul>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Network distance (routing engine)</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm text-muted-foreground">
            <p>Travel time and distance along the road graph.</p>
            <ul className="list-disc space-y-1 pl-5">
              <li>Car, walking, cycling and lorry routes</li>
              <li>Reachable areas within a time (isochrones)</li>
              <li>Many-to-many travel-time matrices</li>
            </ul>
          </CardContent>
        </Card>
      </CompareGrid>

      <SectionTitle id="what">What a routing engine does</SectionTitle>
      <Prose>
        <p>
          A routing engine turns OpenStreetMap roads and paths into a graph: junctions become nodes and road segments become
          edges that carry speeds, access rules and turn restrictions. Building that graph is a one-off batch step that takes
          minutes for a county and longer for a country. Answering a question is then a graph search that takes milliseconds.
          Most engines offer the same family of requests:
        </p>
      </Prose>
      <FunctionTable
        rows={[
          { fn: 'route', desc: 'Turn-by-turn directions through two or more points, with time, distance and the path shape.' },
          { fn: 'matrix', desc: 'Travel time and distance from every source to every target in one request.' },
          { fn: 'isochrone', desc: 'The area reachable within a time or distance, returned as GeoJSON polygons.' },
          { fn: 'map matching', desc: 'The roads a noisy GPS trace most likely followed.' },
          { fn: 'locate', desc: 'Snap a point to the nearest road a travel mode can use.' },
          { fn: 'optimised route', desc: 'The best order to visit a set of stops (the travelling salesperson problem).' },
        ]}
      />

      <SectionTitle id="engines">Choosing an engine</SectionTitle>
      <Prose>
        <p>The main open-source options differ in speed, flexibility and what they can answer.</p>
      </Prose>
      <div className="my-4 overflow-x-auto rounded-lg border">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b bg-muted/50 text-left">
              <th className="px-4 py-2.5 font-semibold text-foreground">Engine</th>
              <th className="px-4 py-2.5 font-semibold text-foreground">Strengths</th>
              <th className="px-4 py-2.5 font-semibold text-foreground">Watch out for</th>
            </tr>
          </thead>
          <tbody>
            {ENGINES.map((engine) => (
              <tr key={engine.name} className="border-b align-top last:border-0">
                <td className="whitespace-nowrap px-4 py-2.5">
                  <p className="font-semibold text-foreground">{engine.name}</p>
                  <p className="text-xs text-muted-foreground">{engine.stack}</p>
                </td>
                <td className="px-4 py-2.5 text-muted-foreground">{engine.strengths}</td>
                <td className="px-4 py-2.5 text-muted-foreground">{engine.watch}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <Callout tone="tip" title="A sensible default">
        Start with <strong>Valhalla</strong> if you need isochrones or want to change travel modes per request. Reach for{' '}
        <strong>OSRM</strong> when you need very large car matrices and the travel mode is fixed.
      </Callout>

      <SectionTitle id="pattern">The pattern on Databricks</SectionTitle>
      <Prose>
        <p>
          A routing engine is a native program that holds its graph in memory and answers one request at a time per worker, so
          it does not run well as a Spark function. Instead, build the graph once in a job, keep it in Unity Catalog, and serve
          it from a Databricks App that notebooks, dashboards and services can call.
        </p>
      </Prose>
      <Card className="my-4">
        <CardContent className="pt-6">
          <ol className="space-y-3 text-sm text-muted-foreground">
            <li className="flex gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">1</span>
              <span><strong className="text-foreground">Build in a job:</strong> download an OpenStreetMap extract and build routing tiles on a single node with plenty of memory and local disk.</span>
            </li>
            <li className="flex gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">2</span>
              <span><strong className="text-foreground">Store in a volume:</strong> publish the tiles to a Unity Catalog volume, so they are governed and can be rebuilt without touching the App.</span>
            </li>
            <li className="flex gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">3</span>
              <span><strong className="text-foreground">Serve from an App:</strong> the App loads the tiles at start-up and exposes the engine&apos;s HTTP API, with sign-in and permissions handled by Databricks Apps.</span>
            </li>
            <li className="flex gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">4</span>
              <span><strong className="text-foreground">Join back in SQL:</strong> bring routes, matrices and isochrones back to the lakehouse and join them to your tables with H3 and ST functions.</span>
            </li>
          </ol>
        </CardContent>
      </Card>

      <SectionTitle id="join">Joining routing results to your data</SectionTitle>
      <Prose>
        <p>
          Isochrones come back as GeoJSON, which <code>ST_GeomFromGeoJSON</code> reads directly. Use the H3 then ST pattern from
          the H3 vs ST lesson: <code>h3_coverash3</code> narrows the search to the cells the area touches, and{' '}
          <code>ST_Contains</code> keeps only the points inside it.
        </p>
      </Prose>
      <CodeBlock
        title="python: ask the routing App for a 10-minute walk"
        lang="python"
        code={`isochrone = routing.call("isochrone", {
    "locations": [{"lat": 50.1186, "lon": -5.5373}],   # Penzance
    "costing": "pedestrian",
    "contours": [{"time": 10}],
    "polygons": True,
})
walk_area = json.dumps(isochrone["features"][0]["geometry"])`}
      />
      <CodeBlock
        title="sql: bus stops within that walk"
        code={`SELECT count(*) AS bus_stops_within_10_min_walk
FROM your_catalog.your_schema.bus_stops
WHERE h3_8 IN (SELECT explode(h3_coverash3(:area, 8)))                 -- H3 narrows
  AND ST_Contains(ST_GeomFromGeoJSON(:area), ST_Point(lon, lat, 4326));  -- ST confirms`}
      />
      <Callout tone="info" title="Send one matrix, not many routes">
        A matrix request returns every source-to-target time at once and is far quicker than a loop of single routes. Keep
        each request within the engine&apos;s pair limit and split bigger jobs into batches.
      </Callout>

      <SectionTitle id="routing-in-a-box">Routing in a box</SectionTitle>
      <Prose>
        <p>
          This kit includes a ready-made Valhalla deployment in the{' '}
          <a href={SOLUTION_URL} target="_blank" rel="noopener noreferrer" className="font-medium text-primary underline underline-offset-2">
            <code>routing/</code> folder
          </a>
          . One bundle creates a Unity Catalog schema and volume, a job that builds tiles from any OpenStreetMap extract, and
          the routing App: a map for routes and isochrones, a guide to the API, and Valhalla&apos;s own API at{' '}
          <code>/api</code>. A quickstart notebook calls the App and joins the results to the hackathon tables.
        </p>
      </Prose>
      <CodeBlock
        title="bash: deploy and run end to end"
        lang="bash"
        code={`cd routing

# Schema, volume, job and App
databricks bundle deploy -t aws -p <profile>

# Build the Great Britain tiles (about 20 minutes)
databricks bundle run build_valhalla_tiles -t aws -p <profile>

# Start the App
databricks bundle run valhalla_routing -t aws -p <profile>`}
      />
      <Prose>
        <p>
          For a quick trial, build a small area such as the Isle of Wight by passing <code>--var extent=isle-of-wight</code>{' '}
          and the matching Geofabrik <code>osm_url</code>. The folder&apos;s README covers the variables, the Azure target,
          refreshing the data and calling the App from a notebook.
        </p>
      </Prose>

      <Callout tone="warning" title="Know the limits">
        Travel times assume free-flowing traffic: there is no live or typical traffic and no public transport timetable, so
        use car times to compare places rather than to predict a journey. The tile build needs classic compute, so it does not
        run on Databricks Free Edition. Credit OpenStreetMap contributors (Open Database Licence) when you publish results.
      </Callout>
    </div>
  );
}
