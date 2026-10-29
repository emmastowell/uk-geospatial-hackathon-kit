import type { ReactNode } from 'react';
import { Badge } from '@databricks/appkit-ui/react';

/** Page title block with eyebrow + lead paragraph. */
export function PageHeader({ eyebrow, title, lead }: { eyebrow: string; title: string; lead: ReactNode }) {
  return (
    <header className="mb-8 border-b pb-6">
      <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-primary">{eyebrow}</p>
      <h1 className="text-3xl font-bold tracking-tight text-foreground md:text-4xl">{title}</h1>
      <p className="mt-3 max-w-3xl text-base leading-relaxed text-muted-foreground">{lead}</p>
    </header>
  );
}

/** Section heading used within pages. */
export function SectionTitle({ children, id }: { children: ReactNode; id?: string }) {
  return (
    <h2 id={id} className="mt-12 mb-4 scroll-mt-20 text-xl font-semibold tracking-tight text-foreground first:mt-0">
      {children}
    </h2>
  );
}

export function Prose({ children }: { children: ReactNode }) {
  return <div className="space-y-4 text-sm leading-relaxed text-muted-foreground [&_strong]:font-semibold [&_strong]:text-foreground [&_code]:rounded [&_code]:bg-muted [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:font-mono [&_code]:text-[0.85em] [&_code]:text-foreground">{children}</div>;
}

type Tone = 'info' | 'tip' | 'warning' | 'key';
const toneConfig: Record<Tone, { label: string; color: string }> = {
  info: { label: 'Note', color: 'var(--chart-3)' },
  tip: { label: 'Tip', color: 'var(--success)' },
  warning: { label: 'Watch out', color: 'var(--warning)' },
  key: { label: 'Key idea', color: 'var(--primary)' },
};

export function Callout({ tone = 'info', title, children }: { tone?: Tone; title?: string; children: ReactNode }) {
  const cfg = toneConfig[tone];
  return (
    <div
      className="my-5 rounded-lg border bg-card p-4"
      style={{ borderLeftWidth: 4, borderLeftColor: cfg.color }}
    >
      <p className="mb-1 text-xs font-semibold uppercase tracking-wide" style={{ color: cfg.color }}>
        {title ?? cfg.label}
      </p>
      <div className="text-sm leading-relaxed text-muted-foreground [&_strong]:font-semibold [&_strong]:text-foreground [&_code]:rounded [&_code]:bg-muted [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:font-mono [&_code]:text-[0.85em] [&_code]:text-foreground">
        {children}
      </div>
    </div>
  );
}

/** Reference table of SQL functions. */
export function FunctionTable({ rows }: { rows: Array<{ fn: string; desc: ReactNode; ret?: string }> }) {
  return (
    <div className="my-4 overflow-hidden rounded-lg border">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b bg-muted/50 text-left">
            <th className="px-4 py-2.5 font-semibold text-foreground">Function</th>
            <th className="px-4 py-2.5 font-semibold text-foreground">Description</th>
            {rows.some((r) => r.ret) && <th className="px-4 py-2.5 font-semibold text-foreground">Returns</th>}
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.fn} className="border-b last:border-0 align-top">
              <td className="whitespace-nowrap px-4 py-2.5 font-mono text-[13px]" style={{ color: 'var(--chart-2)' }}>
                {r.fn}
              </td>
              <td className="px-4 py-2.5 text-muted-foreground">{r.desc}</td>
              {rows.some((x) => x.ret) && (
                <td className="whitespace-nowrap px-4 py-2.5 font-mono text-xs text-muted-foreground">{r.ret ?? ''}</td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function Pill({ children, tone = 'default' }: { children: ReactNode; tone?: 'default' | 'h3' | 'st' }) {
  if (tone === 'default') return <Badge variant="secondary">{children}</Badge>;
  const color = tone === 'h3' ? 'var(--chart-2)' : 'var(--chart-1)';
  return (
    <span
      className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium"
      style={{ color, borderColor: `color-mix(in oklab, ${color} 40%, transparent)`, backgroundColor: `color-mix(in oklab, ${color} 12%, transparent)` }}
    >
      {children}
    </span>
  );
}

/** Two-column comparison card grid. */
export function CompareGrid({ children }: { children: ReactNode }) {
  return <div className="my-6 grid gap-4 md:grid-cols-2">{children}</div>;
}
