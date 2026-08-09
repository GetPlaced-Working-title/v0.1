"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { EMPLOYMENT_TYPES, WORK_MODES } from "@/lib/utils/constants";
import type { Job } from "@/lib/types/job";

interface JobFormProps {
  initialData?: Partial<Job>;
  onSubmit: (data: Partial<Job>) => Promise<void>;
  submitLabel?: string;
}

export function JobForm({ initialData, onSubmit, submitLabel = "Create Job" }: JobFormProps) {
  const [form, setForm] = useState<Partial<Job>>({
    title: "",
    description: "",
    required_skills: [],
    employment_type: "full_time",
    work_mode: "remote",
    ...initialData,
  });
  const [loading, setLoading] = useState(false);
  const [skillInput, setSkillInput] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await onSubmit(form);
    } finally {
      setLoading(false);
    }
  };

  const addSkill = () => {
    if (skillInput.trim() && !form.required_skills?.includes(skillInput.trim())) {
      setForm({
        ...form,
        required_skills: [...(form.required_skills || []), skillInput.trim()],
      });
      setSkillInput("");
    }
  };

  const removeSkill = (skill: string) => {
    setForm({
      ...form,
      required_skills: form.required_skills?.filter((s) => s !== skill),
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <div>
          <label className="text-sm font-medium">Job Title</label>
          <Input
            value={form.title || ""}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            placeholder="Senior Software Engineer"
            required
          />
        </div>

        <div>
          <label className="text-sm font-medium">Description</label>
          <textarea
            className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            value={form.description || ""}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            placeholder="Describe the role, responsibilities, and what you're looking for..."
            required
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium">Employment Type</label>
            <select
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              value={form.employment_type || ""}
              onChange={(e) => setForm({ ...form, employment_type: e.target.value })}
            >
              {EMPLOYMENT_TYPES.map((t) => (
                <option key={t} value={t}>{t.replace("_", " ")}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-sm font-medium">Work Mode</label>
            <select
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              value={form.work_mode || ""}
              onChange={(e) => setForm({ ...form, work_mode: e.target.value })}
            >
              {WORK_MODES.map((m) => (
                <option key={m} value={m}>{m}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium">Salary Min</label>
            <Input
              type="number"
              value={form.salary_min || ""}
              onChange={(e) => setForm({ ...form, salary_min: Number(e.target.value) || undefined })}
              placeholder="80000"
            />
          </div>
          <div>
            <label className="text-sm font-medium">Salary Max</label>
            <Input
              type="number"
              value={form.salary_max || ""}
              onChange={(e) => setForm({ ...form, salary_max: Number(e.target.value) || undefined })}
              placeholder="150000"
            />
          </div>
        </div>

        <div>
          <label className="text-sm font-medium">Location</label>
          <Input
            value={form.location || ""}
            onChange={(e) => setForm({ ...form, location: e.target.value })}
            placeholder="San Francisco, CA"
          />
        </div>

        <div>
          <label className="text-sm font-medium">Required Skills</label>
          <div className="flex gap-2">
            <Input
              value={skillInput}
              onChange={(e) => setSkillInput(e.target.value)}
              placeholder="Add a skill..."
              onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), addSkill())}
            />
            <Button type="button" variant="outline" onClick={addSkill}>Add</Button>
          </div>
          {form.required_skills && form.required_skills.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {form.required_skills.map((skill) => (
                <span
                  key={skill}
                  className="inline-flex items-center gap-1 rounded-full bg-secondary px-2.5 py-0.5 text-xs cursor-pointer hover:bg-destructive hover:text-destructive-foreground"
                  onClick={() => removeSkill(skill)}
                >
                  {skill} ×
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      <Button type="submit" disabled={loading} className="w-full">
        {loading ? "Saving..." : submitLabel}
      </Button>
    </form>
  );
}
