/**
 * Description: Public barrel for the typed API layer.
 *              Consumers import from "@/lib/api" and never reach into client.ts directly.
 *              Re-exports the singleton client and generated path/component types.
 * Last Modified By: bvela
 * Created: 2026-05-25
 * Last Modified:
 *     2026-05-25 - File created; re-exported apiClient and schema types.
 */

export { apiClient } from "./client";
export type { components, paths, operations } from "./schema.d.ts";
