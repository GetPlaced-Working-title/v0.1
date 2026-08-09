import { Header } from "@/components/layout/header";
import { Sidebar } from "@/components/layout/sidebar";
import { ErrorBoundary } from "@/components/shared/error-boundary";

const links = [
  { href: "/candidate/dashboard", label: "Dashboard" },
  { href: "/candidate/profile", label: "Profile" },
  { href: "/candidate/resume", label: "Resume" },
  { href: "/candidate/projects", label: "Projects" },
  { href: "/candidate/certificates", label: "Certificates" },
  { href: "/candidate/videos", label: "Videos" },
  { href: "/candidate/settings", label: "Settings" },
];

export default function CandidateLayout({ children }: { children: React.ReactNode }) {
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
