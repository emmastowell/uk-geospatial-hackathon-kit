import { PageHeader, SectionTitle, Prose, Callout, CompareGrid } from '../components/content';
import { CodeBlock } from '../components/CodeBlock';
import { Card, CardContent, CardHeader, CardTitle } from '@databricks/appkit-ui/react';
import { Check, X } from 'lucide-react';

function Row({ label, aibi, genie }: { label: string; aibi: boolean | string; genie: boolean | string }) {
  const cell = (v: boolean | string) =>
    typeof v === 'string' ? (
      <span className="text-xs text-muted-foreground">{v}</span>
    ) : v ? (
      <Check className="h-4 w-4" style={{ color: 'var(--success)' }} />
    ) : (
      <X className="h-4 w-4" style={{ color: 'var(--muted-foreground)' }} />
    );
  return (
    <tr className="border-b last:border-0">
      <td className="px-4 py-2.5 text-sm text-muted-foreground">{label}</td>
      <td className="px-4 py-2.5">{cell(aibi)}</td>
      <td className="px-4 py-2.5">{cell(genie)}</td>
    </tr>
  );
}

export function AibiGeniePage() {
  return (
    <div>
      <PageHeader
        eyebrow="See your data"
        title="AI/BI dashboards vs Genie"
        lead="Databricks offers two no-/low-code ways to let people explore spatial data without building an app. AI/BI dashboards are governed, curated views; Genie is conversational, open-ended exploration. They solve different problems and often ship together."
      />

      <CompareGrid>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">AI/BI dashboards</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm text-muted-foreground">
            <p>A curated set of visualizations an author builds and publishes — including a native <strong>map (marker &amp; choropleth)</strong> visualization.</p>
            <ul className="list-disc space-y-1 pl-5">
              <li>Predictable, repeatable, pixel-stable</li>
              <li>Cross-filters, parameters, scheduled refresh</li>
              <li>Best for KPIs and recurring reporting</li>
            </ul>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Genie</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2 text-sm text-muted-foreground">
            <p>A natural-language interface over a curated set of tables. Ask a question, get generated SQL and a result.</p>
            <ul className="list-disc space-y-1 pl-5">
              <li>Open-ended, ad-hoc, follow-up questions</li>
              <li>Generates SQL you can inspect and verify</li>
              <li>Best for exploration the author didn&apos;t anticipate</li>
            </ul>
          </CardContent>
        </Card>
      </CompareGrid>

      <SectionTitle id="matrix">Side by side</SectionTitle>
      <div className="my-4 overflow-hidden rounded-lg border">
        <table className="w-full">
          <thead>
            <tr className="border-b bg-muted/50 text-left">
              <th className="px-4 py-2.5 text-sm font-semibold text-foreground">Dimension</th>
              <th className="px-4 py-2.5 text-sm font-semibold text-foreground">AI/BI dashboard</th>
              <th className="px-4 py-2.5 text-sm font-semibold text-foreground">Genie</th>
            </tr>
          </thead>
          <tbody>
            <Row label="Answers questions you planned for" aibi genie={false} />
            <Row label="Answers questions you didn't plan for" aibi={false} genie />
            <Row label="Native map visualization" aibi genie="chart/table output" />
            <Row label="Natural-language input" aibi={false} genie />
            <Row label="Shows the SQL behind the answer" aibi="authored" genie="generated, inspectable" />
            <Row label="Consistent layout every time" aibi genie={false} />
            <Row label="Audience" aibi="broad, recurring" genie="analysts & power users" />
          </tbody>
        </table>
      </div>

      <SectionTitle id="geo">What this means for spatial data</SectionTitle>
      <Prose>
        <p>
          For a <strong>map that people look at every week</strong> — &ldquo;deliveries per region&rdquo;, &ldquo;store
          coverage&rdquo; — an AI/BI dashboard with the map visualization is the lowest-effort, most governable choice. Point it
          at a query that aggregates to H3 cells or regions and it renders a choropleth or marker layer directly.
        </p>
        <p>
          For <strong>&ldquo;let me poke at the data&rdquo;</strong> — &ldquo;which zip codes had the biggest week-over-week
          jump in pickups near the airport?&rdquo; — Genie lets a user ask in English and returns generated SQL (often using
          the very <code>h3_</code> and <code>ST_</code> functions from this guide) that they can read and trust.
        </p>
      </Prose>

      <CodeBlock
        title="a question Genie might turn into SQL"
        code={`-- User asks: "pickups per neighborhood within 2km of JFK, last week"
SELECT z.zone_name, count(*) AS pickups
FROM trips t
JOIN zones z
  ON ST_Contains(z.boundary, ST_Point(t.pickup_lon, t.pickup_lat))
WHERE t.pickup_ts >= current_date() - INTERVAL 7 DAYS
  AND ST_DWithin(
        ST_GeogFromText(ST_AsText(ST_Point(t.pickup_lon, t.pickup_lat))),
        ST_GeogFromText('POINT(-73.7781 40.6413)'), 2000)
GROUP BY z.zone_name
ORDER BY pickups DESC;`}
      />

      <Callout tone="key" title="They're better together">
        A common production shape: an <strong>AI/BI dashboard</strong> for the standard spatial KPIs, with a <strong>Genie</strong>{' '}
        space attached for follow-up questions. And when you need bespoke interactivity beyond either — custom map tooling,
        write-back, per-user millisecond lookups — that&apos;s when you graduate to a custom <strong>Databricks App</strong>{' '}
        (the previous page).
      </Callout>

      <Callout tone="info" title="Embedding Genie in a custom app">
        If you build an app, AppKit can host a Genie chat surface. The non-negotiable there is <strong>trust</strong>: show the
        signed-in user, render the generated SQL for every answer, reflect streaming status, and add an &ldquo;AI-generated —
        verify&rdquo; disclaimer. Never hide how a spatial answer was computed.
      </Callout>
    </div>
  );
}
