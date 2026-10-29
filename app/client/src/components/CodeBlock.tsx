import { useState } from 'react';
import { Check, Copy } from 'lucide-react';

const KEYWORDS = new Set([
  'select', 'from', 'where', 'join', 'inner', 'left', 'right', 'outer', 'on', 'group',
  'by', 'order', 'as', 'create', 'or', 'replace', 'table', 'insert', 'into', 'values',
  'with', 'recursive', 'and', 'or', 'not', 'in', 'is', 'null', 'distinct', 'cross',
  'limit', 'catalog', 'schema', 'default', 'collation', 'collate', 'use', 'add', 'column',
  'alter', 'set', 'case', 'when', 'then', 'else', 'end', 'union', 'all', 'having',
  'between', 'like', 'exists', 'explode', 'array', 'struct', 'map', 'using', 'desc', 'asc',
  'begin', 'declare', 'if', 'while', 'for', 'return', 'returns', 'index', 'extension',
  'materialized', 'view', 'cluster', 'schedule', 'every', 'comment', 'primary', 'key',
  'foreign', 'references', 'constraint', 'generated', 'always', 'identity',
]);

const TYPES = new Set([
  'string', 'int', 'integer', 'bigint', 'double', 'float', 'decimal', 'boolean', 'date',
  'timestamp', 'geometry', 'geography', 'binary', 'variant', 'ge'
]);

const TOKEN_RE = /(--[^\n]*|\/\*[\s\S]*?\*\/)|('(?:[^']|'')*')|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)/g;

type Seg = { text: string; color?: string; style?: 'italic' };

function tokenize(code: string): Seg[] {
  const segs: Seg[] = [];
  let last = 0;
  let m: RegExpExecArray | null;
  TOKEN_RE.lastIndex = 0;
  while ((m = TOKEN_RE.exec(code)) !== null) {
    if (m.index > last) segs.push({ text: code.slice(last, m.index) });
    const [full, comment, str, num, ident] = m;
    if (comment !== undefined) {
      segs.push({ text: full, color: 'var(--muted-foreground)', style: 'italic' });
    } else if (str !== undefined) {
      segs.push({ text: full, color: 'var(--chart-4)' });
    } else if (num !== undefined) {
      segs.push({ text: full, color: 'var(--chart-5)' });
    } else if (ident !== undefined) {
      const low = ident.toLowerCase();
      if (/^(st_|h3_)/.test(low)) {
        segs.push({ text: full, color: 'var(--chart-2)' });
      } else if (KEYWORDS.has(low)) {
        segs.push({ text: full, color: 'var(--chart-1)' });
      } else if (TYPES.has(low)) {
        segs.push({ text: full, color: 'var(--chart-3)' });
      } else {
        segs.push({ text: full });
      }
    }
    last = m.index + full.length;
  }
  if (last < code.length) segs.push({ text: code.slice(last) });
  return segs;
}

export function CodeBlock({ code, lang = 'sql', title }: { code: string; lang?: string; title?: string }) {
  const [copied, setCopied] = useState(false);
  const trimmed = code.replace(/^\n/, '').replace(/\s+$/, '');
  const segs = lang === 'sql' ? tokenize(trimmed) : [{ text: trimmed }];

  const onCopy = () => {
    navigator.clipboard?.writeText(trimmed).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    });
  };

  return (
    <div className="rounded-lg border bg-muted/40 overflow-hidden my-1">
      <div className="flex items-center justify-between border-b bg-muted/60 px-3 py-1.5">
        <span className="font-mono text-xs uppercase tracking-wide text-muted-foreground">{title ?? lang}</span>
        <button
          onClick={onCopy}
          className="inline-flex items-center gap-1.5 rounded px-2 py-1 text-xs text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
        >
          {copied ? <Check className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
          {copied ? 'Copied' : 'Copy'}
        </button>
      </div>
      <pre className="overflow-x-auto p-4 text-[13px] leading-relaxed">
        <code className="font-mono">
          {segs.map((s, i) => (
            <span key={i} style={{ color: s.color, fontStyle: s.style }}>
              {s.text}
            </span>
          ))}
        </code>
      </pre>
    </div>
  );
}
