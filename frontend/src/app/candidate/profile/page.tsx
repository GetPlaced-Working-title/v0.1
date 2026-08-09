"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { GitHubConnect } from "@/components/candidate/github-connect";
import { ScoreRadar } from "@/components/candidate/score-radar";
import { AVAILABILITY } from "@/lib/utils/constants";

export default function CandidateProfilePage() {
  const [form, setForm] = useState({
    name: "",
    headline: "",
    location: "",
    bio: "",
    phone: "",
    current_role: "",
    current_company: "",
    availability: "",
    open_to_remote: true,
    salary_expectation_min: "",
    salary_expectation_max: "",
  });

  const handleSave = async () => {
    // Save via API
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Profile</h1>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Basic Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Full Name</label>
                  <Input
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    placeholder="John Doe"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Headline</label>
                  <Input
                    value={form.headline}
                    onChange={(e) => setForm({ ...form, headline: e.target.value })}
                    placeholder="Senior Software Engineer"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Location</label>
                  <Input
                    value={form.location}
                    onChange={(e) => setForm({ ...form, location: e.target.value })}
                    placeholder="San Francisco, CA"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Phone</label>
                  <Input
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                    placeholder="+1 555 000 0000"
                  />
                </div>
              </div>
              <div>
                <label className="text-sm font-medium">Bio</label>
                <textarea
                  className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={form.bio}
                  onChange={(e) => setForm({ ...form, bio: e.target.value })}
                  placeholder="Tell us about yourself..."
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Current Role</label>
                  <Input
                    value={form.current_role}
                    onChange={(e) => setForm({ ...form, current_role: e.target.value })}
                    placeholder="Software Engineer"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Current Company</label>
                  <Input
                    value={form.current_company}
                    onChange={(e) => setForm({ ...form, current_company: e.target.value })}
                    placeholder="Acme Corp"
                  />
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="text-sm font-medium">Availability</label>
                  <select
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    value={form.availability}
                    onChange={(e) => setForm({ ...form, availability: e.target.value })}
                  >
                    <option value="">Select...</option>
                    {AVAILABILITY.map((a) => (
                      <option key={a} value={a}>{a.replace("_", " ")}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-sm font-medium">Min Salary</label>
                  <Input
                    type="number"
                    value={form.salary_expectation_min}
                    onChange={(e) => setForm({ ...form, salary_expectation_min: e.target.value })}
                    placeholder="80000"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Max Salary</label>
                  <Input
                    type="number"
                    value={form.salary_expectation_max}
                    onChange={(e) => setForm({ ...form, salary_expectation_max: e.target.value })}
                    placeholder="150000"
                  />
                </div>
              </div>
              <Button onClick={handleSave}>Save Profile</Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Connect GitHub</CardTitle>
            </CardHeader>
            <CardContent>
              <GitHubConnect onConnect={async (username) => console.log("connect", username)} />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Add Portfolio</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2">
                <Input placeholder="https://yourportfolio.com" />
                <Button>Add</Button>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <ScoreRadar scores={{}} title="Overall Scores" />

          <Card>
            <CardHeader>
              <CardTitle>Skills</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Skills will appear here after your evidence is analyzed.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Evidence Sources</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {["Resume", "GitHub", "Portfolio", "Video", "Certificates", "LinkedIn"].map((s) => (
                  <div key={s} className="flex items-center justify-between text-sm">
                    <span>{s}</span>
                    <Badge variant="outline">Not connected</Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
