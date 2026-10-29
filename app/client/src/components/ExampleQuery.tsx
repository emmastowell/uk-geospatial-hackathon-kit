import { Database, FlaskConical } from 'lucide-react';
import { CodeBlock } from './CodeBlock';
import { Pill } from './content';
import type { ExampleDef } from '../data/exampleQueries';

/** Fill `:name` placeholders with the example's default values so the SQL is paste-and-run. */
function withDefaults(def: ExampleDef) {
  const values = Object.fromEntries(def.params.map((p) => [p.name, String(p.default)]));
  return def.sqlText.replace(/:([a-z_]+)/g, (m, name: string) => values[name] ?? m);
}

/** A worked SQL example: description, the table shape it expects, the parameters, and copy-ready SQL. */
export function ExampleQuery({ def }: { def: ExampleDef }) {
  return (
    <section className="my-6 overflow-hidden rounded-xl border bg-card">
      <div className="border-b bg-muted/40 p-4">
        <div className="mb-1 flex items-center gap-2">
          <FlaskConical className="h-3.5 w-3.5" style={{ color: 'var(--primary)' }} />
          <span className="text-xs font-semibold uppercase tracking-wide text-primary">Example</span>
          <Pill tone={def.concept}>{def.concept === 'h3' ? 'H3' : 'ST'}</Pill>
        </div>
        <h4 className="text-sm font-semibold text-foreground">{def.title}</h4>
        <p className="mt-1 text-sm text-muted-foreground">{def.description}</p>
        <p className="mt-1.5 flex items-start gap-1.5 text-xs text-muted-foreground">
          <Database className="mt-0.5 h-3.5 w-3.5 shrink-0" />
          <span>
            <code className="font-mono">{def.table}</code>
            {def.columns !== 'no table needed' && <> with columns: {def.columns}</>}
          </span>
        </p>
      </div>

      <div className="p-4">
        <CodeBlock title="paste into a notebook or the SQL editor" code={withDefaults(def)} />
        <p className="mt-3 text-xs font-medium text-foreground">Values to change</p>
        <ul className="mt-1 grid gap-x-6 gap-y-1 text-xs text-muted-foreground sm:grid-cols-2">
          {def.params.map((p) => (
            <li key={p.name}>
              <span className="text-foreground">{p.label}</span> (default <code className="font-mono">{p.default}</code>)
              {p.help && <>: {p.help}</>}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
