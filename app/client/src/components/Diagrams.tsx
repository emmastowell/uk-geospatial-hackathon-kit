// Lightweight SVG illustrations of geospatial concepts.
// All colors reference design tokens via CSS custom properties (no raw hex).

const SIZE = 26; // hex "radius" in px

function hexPoints(cx: number, cy: number, r: number): string {
  const pts: string[] = [];
  for (let i = 0; i < 6; i++) {
    const a = (Math.PI / 180) * (60 * i - 30); // pointy-top
    pts.push(`${cx + r * Math.cos(a)},${cy + r * Math.sin(a)}`);
  }
  return pts.join(' ');
}

// axial (q,r) -> pixel for pointy-top layout
function axialToPixel(q: number, r: number, size: number) {
  const x = size * (Math.sqrt(3) * q + (Math.sqrt(3) / 2) * r);
  const y = size * ((3 / 2) * r);
  return { x, y };
}

const NEIGHBORS: Array<[number, number]> = [
  [1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1], [0, 1],
];

/** H3 hexagonal grid with a highlighted center cell and its k-ring(1) neighbors. */
export function HexGridDiagram({ className }: { className?: string }) {
  const cells: Array<{ q: number; r: number }> = [];
  for (let q = -3; q <= 3; q++) {
    for (let r = -2; r <= 2; r++) {
      if (Math.abs(q + r) <= 3) cells.push({ q, r });
    }
  }
  const neighborSet = new Set(NEIGHBORS.map(([q, r]) => `${q},${r}`));

  return (
    <svg viewBox="-120 -90 240 180" className={className} role="img" aria-label="H3 hexagonal grid with center cell and ring of neighbors">
      {cells.map(({ q, r }) => {
        const { x, y } = axialToPixel(q, r, SIZE);
        const isCenter = q === 0 && r === 0;
        const isNeighbor = neighborSet.has(`${q},${r}`);
        const fill = isCenter
          ? 'var(--chart-2)'
          : isNeighbor
            ? 'color-mix(in oklab, var(--chart-2) 35%, transparent)'
            : 'var(--muted)';
        return (
          <polygon
            key={`${q},${r}`}
            points={hexPoints(x, y, SIZE - 1.5)}
            style={{ fill, stroke: 'var(--border)', strokeWidth: 1 }}
          />
        );
      })}
    </svg>
  );
}

/** Three nested hexagons illustrating H3 resolution hierarchy (coarse -> fine). */
export function ResolutionDiagram({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 300 120" className={className} role="img" aria-label="H3 resolution hierarchy from coarse to fine">
      {[
        { cx: 48, r: 40, label: 'res 5', fine: 1 },
        { cx: 150, r: 40, label: 'res 7', fine: 2 },
        { cx: 252, r: 40, label: 'res 9', fine: 3 },
      ].map(({ cx, r, label, fine }) => (
        <g key={label}>
          <polygon points={hexPoints(cx, 50, r)} style={{ fill: 'var(--muted)', stroke: 'var(--chart-2)', strokeWidth: 1.5 }} />
          {fine >= 2 &&
            [0, 60, 120, 180, 240, 300].map((a) => {
              const rad = (Math.PI / 180) * a;
              return (
                <polygon
                  key={a}
                  points={hexPoints(cx + r * 0.45 * Math.cos(rad), 50 + r * 0.45 * Math.sin(rad), r * 0.28)}
                  style={{ fill: 'none', stroke: 'color-mix(in oklab, var(--chart-2) 60%, transparent)', strokeWidth: 1 }}
                />
              );
            })}
          <text x={cx} y={108} textAnchor="middle" style={{ fill: 'var(--muted-foreground)', fontSize: 11, fontFamily: 'monospace' }}>
            {label}
          </text>
        </g>
      ))}
      <text x={150} y={14} textAnchor="middle" style={{ fill: 'var(--muted-foreground)', fontSize: 11 }}>
        coarse → fine (each cell has 7 children)
      </text>
    </svg>
  );
}

/** Point, LineString and Polygon vector primitives. */
export function GeometryShapesDiagram({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 300 120" className={className} role="img" aria-label="Point, line and polygon geometry primitives">
      {/* Point */}
      <g>
        <circle cx={50} cy={55} r={7} style={{ fill: 'var(--chart-2)' }} />
        <text x={50} y={95} textAnchor="middle" style={{ fill: 'var(--muted-foreground)', fontSize: 11, fontFamily: 'monospace' }}>POINT</text>
      </g>
      {/* LineString */}
      <g>
        <polyline
          points="120,70 140,40 160,62 180,35"
          style={{ fill: 'none', stroke: 'var(--chart-1)', strokeWidth: 2.5, strokeLinejoin: 'round', strokeLinecap: 'round' }}
        />
        {[[120, 70], [140, 40], [160, 62], [180, 35]].map(([x, y], i) => (
          <circle key={i} cx={x} cy={y} r={3} style={{ fill: 'var(--chart-1)' }} />
        ))}
        <text x={150} y={95} textAnchor="middle" style={{ fill: 'var(--muted-foreground)', fontSize: 11, fontFamily: 'monospace' }}>LINESTRING</text>
      </g>
      {/* Polygon */}
      <g>
        <polygon
          points="230,38 268,48 262,78 238,82 222,60"
          style={{ fill: 'color-mix(in oklab, var(--chart-4) 35%, transparent)', stroke: 'var(--chart-4)', strokeWidth: 2, strokeLinejoin: 'round' }}
        />
        <text x={248} y={95} textAnchor="middle" style={{ fill: 'var(--muted-foreground)', fontSize: 11, fontFamily: 'monospace' }}>POLYGON</text>
      </g>
    </svg>
  );
}

/** Point-in-polygon predicate: points inside vs outside a boundary. */
export function PointInPolygonDiagram({ className }: { className?: string }) {
  const inside: Array<[number, number]> = [[110, 70], [150, 55], [135, 90]];
  const outside: Array<[number, number]> = [[40, 40], [240, 95], [250, 35]];
  return (
    <svg viewBox="0 0 300 130" className={className} role="img" aria-label="Point in polygon spatial predicate">
      <polygon
        points="85,35 200,45 215,105 95,110 70,70"
        style={{ fill: 'color-mix(in oklab, var(--chart-2) 15%, transparent)', stroke: 'var(--chart-2)', strokeWidth: 2, strokeLinejoin: 'round' }}
      />
      {inside.map(([x, y], i) => (
        <circle key={`i${i}`} cx={x} cy={y} r={5} style={{ fill: 'var(--success)' }} />
      ))}
      {outside.map(([x, y], i) => (
        <circle key={`o${i}`} cx={x} cy={y} r={5} style={{ fill: 'var(--muted-foreground)' }} />
      ))}
      <text x={150} y={124} textAnchor="middle" style={{ fill: 'var(--muted-foreground)', fontSize: 11 }}>
        ST_Contains(zone, point)
      </text>
    </svg>
  );
}

/** Buffer: a radius expanded around a point. */
export function BufferDiagram({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 200 120" className={className} role="img" aria-label="Buffer around a point">
      <circle cx={100} cy={55} r={42} style={{ fill: 'color-mix(in oklab, var(--chart-1) 18%, transparent)', stroke: 'var(--chart-1)', strokeWidth: 1.5, strokeDasharray: '4 3' }} />
      <circle cx={100} cy={55} r={6} style={{ fill: 'var(--chart-1)' }} />
      <line x1={100} y1={55} x2={142} y2={55} style={{ stroke: 'var(--chart-1)', strokeWidth: 1.5 }} />
      <text x={121} y={48} textAnchor="middle" style={{ fill: 'var(--muted-foreground)', fontSize: 10, fontFamily: 'monospace' }}>r</text>
      <text x={100} y={112} textAnchor="middle" style={{ fill: 'var(--muted-foreground)', fontSize: 11 }}>
        ST_Buffer(geom, radius)
      </text>
    </svg>
  );
}
