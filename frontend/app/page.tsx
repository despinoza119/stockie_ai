/**
 * Description: Sprint 0 placeholder landing page.
 *              Renders the Stockie AI wordmark and a live backend health card to confirm
 *              end-to-end connectivity. Will be replaced by the full dashboard in Sprint 8.
 * Last Modified By: bvela
 * Created: 2026-05-23
 * Last Modified:
 *     2026-05-23 - Sprint 0 placeholder; shows app name and health-check link.
 *     2026-05-25 - Wired HealthStatus server component; added Suspense skeleton.
 */

import { Suspense } from "react";

import { HealthStatus, HealthStatusSkeleton } from "@/components/health-status";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-8 p-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight">Stockie AI</h1>
        <p className="mt-2 text-lg text-muted-foreground">
          AI-powered stock analysis — coming soon.
        </p>
      </div>

      <Suspense fallback={<HealthStatusSkeleton />}>
        <HealthStatus />
      </Suspense>
    </main>
  );
}
