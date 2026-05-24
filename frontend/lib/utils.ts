/**
 * Description: Utility helpers shared across all components.
 *              `cn` merges Tailwind class strings safely, resolving conflicts via tailwind-merge.
 * Last Modified By: bvela
 * Created: 2026-05-24
 * Last Modified:
 *     2026-05-24 - File created; added cn helper (shadcn/ui init).
 */

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
