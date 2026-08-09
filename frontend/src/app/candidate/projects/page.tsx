"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

export default function CandidateProjectsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Projects</h1>
        <Button>Add Project</Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Add New Project</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Project Title</label>
              <Input placeholder="My Awesome Project" />
            </div>
            <div>
              <label className="text-sm font-medium">Your Role</label>
              <Input placeholder="Lead Developer" />
            </div>
          </div>
          <div>
            <label className="text-sm font-medium">Description</label>
            <textarea className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm" placeholder="What did you build?" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">GitHub URL</label>
              <Input placeholder="https://github.com/..." />
            </div>
            <div>
              <label className="text-sm font-medium">Live URL</label>
              <Input placeholder="https://..." />
            </div>
          </div>
          <Button>Save Project</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Your Projects</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">No projects added yet. Add your best work above.</p>
        </CardContent>
      </Card>
    </div>
  );
}
