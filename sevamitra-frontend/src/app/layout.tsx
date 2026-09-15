import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SevaMitra AI",
  description: "AI-powered government service assistant",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
