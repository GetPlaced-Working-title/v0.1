"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function AdminUsersPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Users</h1>

      <Card>
        <CardHeader>
          <CardTitle>All Users</CardTitle>
        </CardHeader>
        <CardContent>
          <table className="w-full text-sm">
            <thead className="border-b">
              <tr>
                <th className="pb-3 text-left font-medium text-muted-foreground">Email</th>
                <th className="pb-3 text-left font-medium text-muted-foreground">Role</th>
                <th className="pb-3 text-left font-medium text-muted-foreground">Status</th>
                <th className="pb-3 text-left font-medium text-muted-foreground">Joined</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td colSpan={4} className="py-4 text-center text-muted-foreground">
                  No users yet
                </td>
              </tr>
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
}
