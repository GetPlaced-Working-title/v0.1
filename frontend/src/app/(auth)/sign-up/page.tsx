"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import Link from "next/link";

export default function SignUpPage() {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("candidate");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      router.push(role === "recruiter" ? "/recruiter/dashboard" : "/candidate/dashboard");
    }, 500);
  };

  return (
    <div className="flex min-h-screen items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Create your account</CardTitle>
          <CardDescription>Join GetPlaced — evidence-based hiring</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSignUp} className="space-y-4">
            <div>
              <label className="text-sm font-medium">Email</label>
              <Input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="text-sm font-medium">I am a...</label>
              <div className="flex gap-3 mt-2">
                <button
                  type="button"
                  onClick={() => setRole("candidate")}
                  className={`flex-1 rounded-lg border p-3 text-center text-sm transition-colors ${
                    role === "candidate"
                      ? "border-primary bg-primary/5 text-primary"
                      : "border-muted hover:border-primary/50"
                  }`}
                >
                  Candidate
                </button>
                <button
                  type="button"
                  onClick={() => setRole("recruiter")}
                  className={`flex-1 rounded-lg border p-3 text-center text-sm transition-colors ${
                    role === "recruiter"
                      ? "border-primary bg-primary/5 text-primary"
                      : "border-muted hover:border-primary/50"
                  }`}
                >
                  Recruiter
                </button>
              </div>
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Creating account..." : "Sign Up"}
            </Button>
            <p className="text-center text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link href="/sign-in" className="underline text-primary">Sign in</Link>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
