import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Header } from "@/components/layout/header";

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1">
        {/* Hero */}
        <section className="container flex flex-col items-center justify-center gap-4 py-24 text-center">
          <h1 className="text-5xl font-bold tracking-tight">
            Hiring based on <span className="text-primary">evidence</span>, not keywords
          </h1>
          <p className="max-w-2xl text-lg text-muted-foreground">
            GetPlaced analyzes resumes, GitHub profiles, portfolios, videos, certificates, and
            more to build rich candidate profiles. Recruiters describe a role — the system
            returns the best matches using vector search and AI reranking.
          </p>
          <div className="flex gap-4 pt-4">
            <Link href="/sign-up">
              <Button size="lg">Get Started</Button>
            </Link>
            <Link href="/sign-in">
              <Button variant="outline" size="lg">Sign In</Button>
            </Link>
          </div>
        </section>

        {/* Features */}
        <section className="container py-16">
          <h2 className="mb-12 text-center text-3xl font-bold">How it works</h2>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            <div className="rounded-lg border p-6">
              <h3 className="mb-2 text-lg font-semibold">1. Upload Evidence</h3>
              <p className="text-sm text-muted-foreground">
                Candidates upload resumes, connect GitHub, share portfolios, record videos,
                and add certificates. AI analyzes everything.
              </p>
            </div>
            <div className="rounded-lg border p-6">
              <h3 className="mb-2 text-lg font-semibold">2. AI Builds Your Profile</h3>
              <p className="text-sm text-muted-foreground">
                The AI creates a structured profile with verified skills, evidence confidence
                levels, and cross-source consistency checks.
              </p>
            </div>
            <div className="rounded-lg border p-6">
              <h3 className="mb-2 text-lg font-semibold">3. Smart Matching</h3>
              <p className="text-sm text-muted-foreground">
                Recruiters describe a role. Vector search finds candidates, AI reranks them
                by fit, and surfaces detailed match explanations.
              </p>
            </div>
          </div>
        </section>

        {/* Tech Stack */}
        <section className="container py-16">
          <h2 className="mb-8 text-center text-2xl font-bold">Evidence-First Analysis</h2>
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            {[
              { label: "Resume", desc: "Structured extraction + quality scoring" },
              { label: "GitHub", desc: "Code quality, patterns, contribution analysis" },
              { label: "Portfolio", desc: "Design quality and project depth" },
              { label: "Video", desc: "Communication, confidence, knowledge" },
              { label: "Certificates", desc: "Issuer verification and difficulty" },
              { label: "Work History", desc: "Achievement analysis and consistency" },
              { label: "LinkedIn", desc: "Network and activity patterns" },
              { label: "Recommendations", desc: "Credibility and specificity scoring" },
            ].map((item) => (
              <div key={item.label} className="rounded-lg border p-4">
                <h4 className="font-medium">{item.label}</h4>
                <p className="text-xs text-muted-foreground mt-1">{item.desc}</p>
              </div>
            ))}
          </div>
        </section>
      </main>

      <footer className="border-t py-8 text-center text-sm text-muted-foreground">
        <div className="container">
          GetPlaced — AI Talent Router. Built with evidence, not keywords.
        </div>
      </footer>
    </div>
  );
}
