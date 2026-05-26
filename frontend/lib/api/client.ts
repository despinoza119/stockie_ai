/**
 * Description: Singleton openapi-fetch client typed against the FastAPI OpenAPI schema.
 *              Import `apiClient` (or the convenience helpers from `lib/api`) anywhere in
 *              the app to make fully type-safe HTTP calls to the backend.
 *              Base URL is read from NEXT_PUBLIC_API_URL (defaults to localhost:8000 for dev).
 * Last Modified By: bvela
 * Created: 2026-05-25
 * Last Modified:
 *     2026-05-25 - File created; wired openapi-fetch to generated schema.
 */

import createClient from "openapi-fetch";

import type { paths } from "./schema.d.ts";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

/**
 * Pre-configured HTTP client typed against the Stockie AI backend OpenAPI spec.
 *
 * @example
 *   const { data, error } = await apiClient.GET("/health");
 *   // data is typed as components["schemas"]["HealthResponse"]
 */
export const apiClient = createClient<paths>({ baseUrl: BASE_URL });
