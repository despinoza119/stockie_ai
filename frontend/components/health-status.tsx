/**
 * Description: Async server component that fetches GET /health from the FastAPI backend
 *              and renders a status card. Handles both the success and backend-unreachable
 *              states inline so the parent never needs a client-side error boundary.
 *              Used on the Sprint 0 landing page as the end-to-end smoke-test visual.
 * Last Modified By: bvela
 * Created: 2026-05-25
 * Last Modified:
 *     2026-05-25 - File created; Sprint 0 health status card.
 */

import { apiClient } from "@/lib/api";

/**
 * Renders a card showing the current backend health status.
 * Must be used inside a <Suspense> boundary.
 */
export async function HealthStatus() {
  const { data, error } = await apiClient.GET("/health");

  if (error || !data) {
    return (
      <div className="rounded-xl border border-destructive/40 bg-destructive/5 px-6 py-4 text-sm">
        <p className="font-semibold text-destructive">Backend unreachable</p>
        <p className="mt-1 text-muted-foreground">
          Make sure the API server is running on{" "}
          <code className="rounded bg-muted px-1 py-0.5 font-mono text-xs">
            {process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}
          </code>
          .
        </p>
      </div>
    );
  }

  const formattedTimestamp = new Date(data.timestamp).toLocaleString("en-US", {
    dateStyle: "medium",
    timeStyle: "medium",
    timeZone: "UTC",
  });

  return (
    <div className="w-full max-w-sm rounded-xl border bg-card px-6 py-5 shadow-sm">
      <div className="mb-4 flex items-center gap-2">
        {/* Green pulse dot */}
        <span className="relative flex size-2.5">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-green-400 opacity-75" />
          <span className="relative inline-flex size-2.5 rounded-full bg-green-500" />
        </span>
        <span className="text-sm font-semibold uppercase tracking-widest text-muted-foreground">
          Backend Status
        </span>
      </div>

      <dl className="grid grid-cols-[auto_1fr] gap-x-6 gap-y-2 text-sm">
        <dt className="text-muted-foreground">Status</dt>
        <dd className="font-medium capitalize text-green-600 dark:text-green-400">{data.status}</dd>

        <dt className="text-muted-foreground">Version</dt>
        <dd className="font-mono font-medium">{data.version}</dd>

        <dt className="text-muted-foreground">Environment</dt>
        <dd className="font-medium capitalize">{data.environment}</dd>

        <dt className="text-muted-foreground">As of</dt>
        <dd className="text-muted-foreground">{formattedTimestamp} UTC</dd>
      </dl>
    </div>
  );
}

/** Skeleton shown by <Suspense> while the server component is resolving. */
export function HealthStatusSkeleton() {
  return (
    <div className="w-full max-w-sm animate-pulse rounded-xl border bg-card px-6 py-5 shadow-sm">
      <div className="mb-4 flex items-center gap-2">
        <span className="size-2.5 rounded-full bg-muted" />
        <span className="h-3 w-28 rounded bg-muted" />
      </div>
      <div className="grid grid-cols-[auto_1fr] gap-x-6 gap-y-3">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="contents">
            <div className="h-3 w-20 rounded bg-muted" />
            <div className="h-3 w-24 rounded bg-muted" />
          </div>
        ))}
      </div>
    </div>
  );
}
