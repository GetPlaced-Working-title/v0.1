"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

interface SidebarLink {
  href: string;
  label: string;
}

interface SidebarProps {
  links: SidebarLink[];
}

export function Sidebar({ links }: SidebarProps) {
  const pathname = usePathname();

  return (
    <aside className="hidden w-64 shrink-0 border-e bg-muted/30 md:block">
      <nav className="flex flex-col gap-1 p-4 sticky top-14">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={cn(
              "flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
              pathname === link.href
                ? "bg-accent text-accent-foreground"
                : "text-muted-foreground"
            )}
          >
            {link.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
