/**
 * Description: Root page — placeholder landing page for Sprint 0.
 *              Will be replaced by the full dashboard in Sprint 8.
 *              Calls the backend /health endpoint to verify connectivity.
 * Last Modified By: bvela
 * Created: 2026-05-23
 * Last Modified:
 *     2026-05-23 - Sprint 0 placeholder; shows app name and health-check link.
 */

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 p-8">
      <h1 className="text-4xl font-bold tracking-tight">Stockie AI</h1>
      <p className="text-lg text-foreground/60">
        AI-powered stock analysis — coming soon.
      </p>
    </main>
  );
}
