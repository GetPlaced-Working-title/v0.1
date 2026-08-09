"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Loading } from "@/components/shared/loading";

export default function CandidateDashboard() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <Link href="/candidate/profile">
          <Button>Edit Profile</Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Profile Completeness
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">--%</div>
            <p className="text-xs text-muted-foreground">Upload more evidence to improve</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Evidence Confidence
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Badge variant="outline" className="text-lg">--</Badge>
            <p className="text-xs text-muted-foreground mt-2">Add GitHub, portfolio, videos</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Verified Skills
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">--</div>
            <p className="text-xs text-muted-foreground">Skills verified through evidence</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <Link href="/candidate/resume">
              <Button variant="outline" className="w-full justify-start">Upload Resume</Button>
            </Link>
            <Link href="/candidate/profile">
              <Button variant="outline" className="w-full justify-start">Connect GitHub</Button>
            </Link>
            <Link href="/candidate/projects">
              <Button variant="outline" className="w-full justify-start">Add Projects</Button>
            </Link>
            <Link href="/candidate/videos">
              <Button variant="outline" className="w-full justify-start">Upload Video</Button>
            </Link>
            <Link href="/candidate/certificates">
              <Button variant="outline" className="w-full justify-start">Add Certificates</Button>
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">No recent activity. Start by uploading your resume.</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
