"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function AdminAnalyticsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Analytics</h1>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>AI Analysis Usage</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between"><span>Total AI Calls</span><span>0</span></div>
              <div className="flex justify-between"><span>Cache Hit Rate</span><span>--%</span></div>
              <div className="flex justify-between"><span>Total Tokens Used</span><span>0</span></div>
              <div className="flex justify-between"><span>Estimated Cost</span><span>$0.00</span></div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Matching Pipeline</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between"><span>Matches Run</span><span>0</span></div>
              <div className="flex justify-between"><span>Avg Candidates/Match</span><span>0</span></div>
              <div className="flex justify-between"><span>Shortlisted</span><span>0</span></div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
