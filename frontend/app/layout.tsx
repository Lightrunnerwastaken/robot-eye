import type { Metadata } from "next";
import "../styles/globals.css";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "NeuroLearn Dashboard",
  description: "Lernziele verwalten und KI-gestützte Lernpläne erhalten"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="de">
      <body className="bg-slate-950 text-slate-100">
        <Providers>
          <main className="mx-auto flex min-h-screen max-w-5xl flex-col gap-10 px-6 py-12">
            <header className="flex flex-col gap-2">
              <h1 className="text-3xl font-bold text-primary-light">NeuroLearn v0.1</h1>
              <p className="text-slate-300">
                Erfasse Lernziele, erhalte Lernpläne und wiederhole Inhalte mit Spaced Repetition.
              </p>
            </header>
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
