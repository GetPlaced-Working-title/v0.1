"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/hooks/use-auth";

export function Header() {
  const { user, isLoading } = useAuth();

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <Link href="/" className="me-6 flex items-center space-x-2">
          <span className="font-bold text-xl">GetPlaced</span>
        </Link>

        <nav className="flex items-center space-x-6 text-sm font-medium">
          {user?.role === "candidate" && (
            <>
              <Link href="/candidate/dashboard" className="transition-colors hover:text-foreground/80">Dashboard</Link>
              <Link href="/candidate/profile" className="transition-colors hover:text-foreground/80">Profile</Link>
            </>
          )}
          {user?.role === "recruiter" && (
            <>
              <Link href="/recruiter/dashboard" className="transition-colors hover:text-foreground/80">Dashboard</Link>
              <Link href="/recruiter/jobs" className="transition-colors hover:text-foreground/80">Jobs</Link>
              <Link href="/recruiter/search" className="transition-colors hover:text-foreground/80">Search</Link>
            </>
          )}
          {user?.role === "admin" && (
            <Link href="/admin/dashboard" className="transition-colors hover:text-foreground/80">Admin</Link>
          )}
        </nav>

        <div className="ms-auto flex items-center space-x-4">
          {!isLoading && (
            user ? (
              <div className="flex items-center space-x-3">
                <span className="text-sm text-muted-foreground">{user.email}</span>
                <Button variant="outline" size="sm">Sign Out</Button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link href="/sign-in">
                  <Button variant="ghost" size="sm">Sign In</Button>
                </Link>
                <Link href="/sign-up">
                  <Button size="sm">Sign Up</Button>
                </Link>
              </div>
            )
          )}
        </div>
      </div>
    </header>
  );
}
