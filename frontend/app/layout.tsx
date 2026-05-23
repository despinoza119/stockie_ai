/**
 * Description: Root layout for the Stockie AI Next.js application.
 *              Applies global fonts, Tailwind base styles, and shared metadata.
 *              Every page in the app/ directory is wrapped by this layout.
 * Last Modified By: bvela
 * Created: 2026-05-23
 * Last Modified:
 *     2026-05-23 - Replaced create-next-app boilerplate with project metadata.
 */

import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});

const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: {
    default: "Stockie AI",
    template: "%s | Stockie AI",
  },
  description:
    "AI-powered stock analysis and recommendations for US equities and ETFs.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
