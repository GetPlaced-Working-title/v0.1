"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function CandidateCertificatesPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Certificates</h1>
        <Button>Add Certificate</Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Add Certificate</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Certificate Name</label>
              <Input placeholder="AWS Solutions Architect" />
            </div>
            <div>
              <label className="text-sm font-medium">Issuer</label>
              <Input placeholder="Amazon Web Services" />
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="text-sm font-medium">Issue Date</label>
              <Input type="date" />
            </div>
            <div>
              <label className="text-sm font-medium">Credential ID</label>
              <Input placeholder="ABC123" />
            </div>
            <div>
              <label className="text-sm font-medium">Credential URL</label>
              <Input placeholder="https://..." />
            </div>
          </div>
          <Button>Save Certificate</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Your Certificates</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">No certificates added yet.</p>
        </CardContent>
      </Card>
    </div>
  );
}
