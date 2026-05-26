/**
 * Description: Ambient module declarations for CSS files.
 *              Silences the IDE false-positive on side-effect CSS imports in Next.js
 *              (e.g. `import "./globals.css"` in layout.tsx). The compiler and bundler
 *              handle these correctly; this file only satisfies the language server.
 * Last Modified By: bvela
 * Created: 2026-05-25
 * Last Modified:
 *     2026-05-25 - File created.
 */

declare module "*.css" {
  const styles: Record<string, string>;
  export default styles;
}
