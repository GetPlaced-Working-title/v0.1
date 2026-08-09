"use client";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useSearchStore } from "@/lib/stores/search-store";

interface SearchFiltersProps {
  onSearch: () => void;
  type: "candidates" | "jobs";
}

export function SearchFilters({ onSearch, type }: SearchFiltersProps) {
  const { filters, setFilters, resetFilters } = useSearchStore();

  return (
    <div className="space-y-4 rounded-lg border bg-card p-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Input
          placeholder="Search..."
          value={filters.query}
          onChange={(e) => setFilters({ query: e.target.value })}
          onKeyDown={(e) => e.key === "Enter" && onSearch()}
        />
        <Input
          placeholder="Location"
          value={filters.location}
          onChange={(e) => setFilters({ location: e.target.value })}
        />
        {type === "candidates" ? (
          <Input
            type="number"
            placeholder="Min experience (years)"
            value={filters.minExperience || ""}
            onChange={(e) => setFilters({ minExperience: Number(e.target.value) || null })}
          />
        ) : (
          <select
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            value={filters.employmentType}
            onChange={(e) => setFilters({ employmentType: e.target.value })}
          >
            <option value="">All types</option>
            <option value="full_time">Full Time</option>
            <option value="part_time">Part Time</option>
            <option value="contract">Contract</option>
            <option value="internship">Internship</option>
          </select>
        )}
      </div>

      <div className="flex items-center gap-2">
        <Button onClick={onSearch}>Search</Button>
        <Button variant="outline" onClick={() => { resetFilters(); onSearch(); }}>
          Clear
        </Button>
      </div>
    </div>
  );
}
