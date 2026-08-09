import { Header } from "@/components/layout/header";
import { Sidebar } from "@/components/layout/sidebar";
import { ErrorBoundary } from "@/components/shared/error-boundary";

const links = [
  { href: "/recruiter/dashboard", label: "Dashboard" },
  { href: "/recruiter/jobs", label: "Jobs" },
  { href: "/recruiter/candidates", label: "Candidates" },
  { href: "/recruiter/search", label: "Search" },
  { href: "/recruiter/matches", label: "Matches" },
  { href: "/recruiter/settings", label: "Settings" },
];

export default function RecruiterLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <div className="flex flex-1">
        <Sidebar links={links} />
        <main className="flex-1 p-4 md:p-6">
          <ErrorBoundary>{children}</ErrorBoundary>
        </main>
      </div>
    </div>
  );
}
