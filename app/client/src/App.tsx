import { createBrowserRouter, RouterProvider, NavLink, Outlet, ScrollRestoration } from 'react-router';
import { useState } from 'react';
import {
  Button,
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  useIsMobile,
} from '@databricks/appkit-ui/react';
import { Menu, Globe2, Hexagon, Database, LayoutDashboard, BookOpen, Shapes, GitCompare } from 'lucide-react';

import { OverviewPage } from './pages/Overview';
import { FoundationsPage } from './pages/Foundations';
import { H3vsStPage } from './pages/H3vsSt';
import { DbsqlReferencePage } from './pages/DbsqlReference';
import { LakebasePage } from './pages/Lakebase';
import { VisualizePage } from './pages/Visualize';
import { AibiGeniePage } from './pages/AibiGenie';

type NavItem = { to: string; label: string; icon: React.ComponentType<{ className?: string }>; end?: boolean };
type NavGroup = { heading: string; items: NavItem[] };

const NAV: NavGroup[] = [
  {
    heading: 'Get started',
    items: [
      { to: '/', label: 'Overview', icon: Globe2, end: true },
      { to: '/foundations', label: 'Foundations: types & formats', icon: BookOpen },
    ],
  },
  {
    heading: 'SQL functions',
    items: [
      { to: '/h3-vs-st', label: 'H3 vs ST functions', icon: Hexagon },
      { to: '/dbsql', label: 'DBSQL function reference', icon: Shapes },
    ],
  },
  {
    heading: 'Beyond the lakehouse',
    items: [{ to: '/lakebase', label: 'Lakebase & PostGIS', icon: Database }],
  },
  {
    heading: 'See your data',
    items: [
      { to: '/visualize', label: 'Visualize in Databricks Apps', icon: LayoutDashboard },
      { to: '/aibi-genie', label: 'AI/BI dashboards vs Genie', icon: GitCompare },
    ],
  },
];

const linkClass = ({ isActive }: { isActive: boolean }) =>
  `flex items-center gap-2.5 rounded-md px-3 py-2 text-sm transition-colors ${
    isActive
      ? 'bg-primary/10 font-medium text-primary'
      : 'text-muted-foreground hover:bg-muted hover:text-foreground'
  }`;

function NavContent({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <nav className="space-y-6">
      {NAV.map((group) => (
        <div key={group.heading}>
          <p className="mb-1.5 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground/70">
            {group.heading}
          </p>
          <div className="space-y-0.5">
            {group.items.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink key={item.to} to={item.to} end={item.end} className={linkClass} onClick={onNavigate}>
                  <Icon className="h-4 w-4 shrink-0" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </div>
        </div>
      ))}
    </nav>
  );
}

function Brand() {
  return (
    <div className="flex items-center gap-2.5">
      <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
        <Globe2 className="h-5 w-5" />
      </span>
      <div className="leading-tight">
        <p className="text-sm font-semibold text-foreground">Geospatial on Databricks</p>
        <p className="text-xs text-muted-foreground">A hands-on learning guide</p>
      </div>
    </div>
  );
}

function Layout() {
  const isMobile = useIsMobile();
  const [open, setOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile header */}
      <header className="sticky top-0 z-20 flex items-center gap-3 border-b bg-background/95 px-4 py-3 backdrop-blur md:hidden">
        <Sheet open={open && isMobile} onOpenChange={setOpen}>
          <Button variant="ghost" size="icon" onClick={() => setOpen(true)}>
            <Menu className="h-5 w-5" />
            <span className="sr-only">Open navigation</span>
          </Button>
          <SheetContent side="left" className="w-80 overflow-y-auto">
            <SheetHeader>
              <SheetTitle className="text-left">
                <Brand />
              </SheetTitle>
            </SheetHeader>
            <div className="mt-6">
              <NavContent onNavigate={() => setOpen(false)} />
            </div>
          </SheetContent>
        </Sheet>
        <Brand />
      </header>

      <div className="mx-auto flex max-w-screen-2xl">
        {/* Desktop sidebar */}
        <aside className="sticky top-0 hidden h-screen w-72 shrink-0 overflow-y-auto border-r px-4 py-6 md:block">
          <div className="mb-6 px-2">
            <Brand />
          </div>
          <NavContent />
        </aside>

        <main className="min-w-0 flex-1">
          <div className="mx-auto max-w-4xl px-5 py-8 md:px-10 md:py-12">
            <Outlet />
          </div>
        </main>
      </div>
      <ScrollRestoration />
    </div>
  );
}

const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: '/', element: <OverviewPage /> },
      { path: '/foundations', element: <FoundationsPage /> },
      { path: '/h3-vs-st', element: <H3vsStPage /> },
      { path: '/dbsql', element: <DbsqlReferencePage /> },
      { path: '/lakebase', element: <LakebasePage /> },
      { path: '/visualize', element: <VisualizePage /> },
      { path: '/aibi-genie', element: <AibiGeniePage /> },
    ],
  },
]);

export default function App() {
  return <RouterProvider router={router} />;
}
