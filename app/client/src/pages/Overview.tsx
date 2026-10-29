import { Link } from 'react-router';
import { Card, CardContent } from '@databricks/appkit-ui/react';
import { Hexagon, Shapes, Database, LayoutDashboard, GitCompare, BookOpen, ArrowRight, FlaskConical } from 'lucide-react';
import { PageHeader, Callout, Prose, SectionTitle } from '../components/content';
import { HexGridDiagram, GeometryShapesDiagram } from '../components/Diagrams';

const PATH = [
  { to: '/foundations', icon: BookOpen, title: 'Foundations: types & formats', desc: 'GEOMETRY vs GEOGRAPHY, SRIDs, and the WKT / WKB / GeoJSON formats everything is built on.' },
  { to: '/h3-vs-st', icon: Hexagon, title: 'H3 vs ST functions', desc: 'The single most important choice: hexagonal grid indexing vs exact vector geometry — and when to combine them.' },
  { to: '/dbsql', icon: Shapes, title: 'DBSQL function reference', desc: 'A categorized tour of the 39 H3 and 80+ ST functions in Databricks SQL, with runnable examples.' },
  { to: '/lakebase', icon: Database, title: 'Lakebase & PostGIS', desc: 'Operational, low-latency geo in Lakebase Postgres with PostGIS — and how it complements lakehouse geo.' },
  { to: '/visualize', icon: LayoutDashboard, title: 'Visualize in Databricks Apps', desc: 'Render points, hexes and polygons on a map inside a custom AppKit app.' },
  { to: '/aibi-genie', icon: GitCompare, title: 'AI/BI dashboards vs Genie', desc: 'Governed map dashboards vs natural-language exploration — which to reach for.' },
];

export function OverviewPage() {
  return (
    <div>
      <PageHeader
        eyebrow="Start here"
        title="Geospatial analytics on Databricks"
        lead="Databricks turns the lakehouse into a spatial engine: index billions of points with H3, run exact vector operations with ST functions, serve operational lookups from Lakebase, and visualize it all in apps, dashboards, and Genie. This guide walks the whole stack, from a single SELECT to a production map."
      />

      <div className="grid gap-4 sm:grid-cols-2">
        <Card>
          <CardContent className="flex flex-col gap-3 pt-6">
            <div className="flex items-center gap-2">
              <Hexagon className="h-4 w-4" style={{ color: 'var(--chart-2)' }} />
              <span className="text-sm font-semibold text-foreground">H3 — grid indexing</span>
            </div>
            <HexGridDiagram className="h-36 w-full" />
            <p className="text-sm text-muted-foreground">
              Snap the world to a hierarchy of hexagons. Fast joins, aggregation and binning at any zoom level.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="flex flex-col gap-3 pt-6">
            <div className="flex items-center gap-2">
              <Shapes className="h-4 w-4" style={{ color: 'var(--chart-1)' }} />
              <span className="text-sm font-semibold text-foreground">ST — vector geometry</span>
            </div>
            <GeometryShapesDiagram className="h-36 w-full" />
            <p className="text-sm text-muted-foreground">
              Represent exact points, lines and polygons. Measure distances, test containment, and run set operations.
            </p>
          </CardContent>
        </Card>
      </div>

      <Callout tone="key" title="The one-sentence mental model">
        Use <strong>H3</strong> when you need speed and scale over approximate cells; use <strong>ST functions</strong> when
        you need exact spatial geometry; use <strong>both</strong> when you want H3 to pre-filter and ST to finish the job precisely.
      </Callout>

      <Link
        to="/h3-vs-st"
        className="group mt-6 flex items-center gap-4 rounded-xl border bg-card p-5 transition-colors hover:border-primary/40 hover:bg-muted/40"
      >
        <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <FlaskConical className="h-5 w-5" />
        </span>
        <div className="min-w-0 flex-1">
          <p className="flex items-center gap-1.5 text-sm font-semibold text-foreground">
            Worked examples are built into the lessons
            <ArrowRight className="h-4 w-4 -translate-x-1 opacity-0 transition-all group-hover:translate-x-0 group-hover:opacity-100" />
          </p>
          <p className="mt-0.5 text-xs leading-relaxed text-muted-foreground">
            Throughout the guide, &ldquo;Example&rdquo; blocks give copy-ready H3 &amp; ST queries with the table shape they expect and
            the values to change. Start on the H3 vs ST page.
          </p>
        </div>
      </Link>

      <SectionTitle>Your learning path</SectionTitle>
      <Prose>
        <p>Work through the sections in order, or jump straight to what you need. Every page is self-contained with copy-pasteable SQL.</p>
      </Prose>
      <div className="mt-5 grid gap-3 sm:grid-cols-2">
        {PATH.map((p, i) => {
          const Icon = p.icon;
          return (
            <Link
              key={p.to}
              to={p.to}
              className="group flex gap-3 rounded-lg border bg-card p-4 transition-colors hover:border-primary/40 hover:bg-muted/40"
            >
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
                <Icon className="h-4.5 w-4.5" />
              </span>
              <div className="min-w-0">
                <p className="flex items-center gap-1 text-sm font-semibold text-foreground">
                  <span className="text-muted-foreground">{i + 1}.</span> {p.title}
                  <ArrowRight className="h-3.5 w-3.5 -translate-x-1 opacity-0 transition-all group-hover:translate-x-0 group-hover:opacity-100" />
                </p>
                <p className="mt-1 text-xs leading-relaxed text-muted-foreground">{p.desc}</p>
              </div>
            </Link>
          );
        })}
      </div>

      <Callout tone="info" title="What you need to follow along">
        H3 functions have been available since Databricks Runtime 11.2 and work on any SQL warehouse. The native{' '}
        <code>GEOMETRY</code> / <code>GEOGRAPHY</code> types and ST functions require DBR 17.1+ (Public Preview) and are
        best on serverless. Where a feature needs newer compute, this guide calls it out.
      </Callout>
    </div>
  );
}
