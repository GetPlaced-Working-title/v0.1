"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { isValidGithubUsername } from "@/lib/utils/validation";

interface GitHubConnectProps {
  onConnect: (username: string) => Promise<void>;
  currentUsername?: string;
}

export function GitHubConnect({ onConnect, currentUsername }: GitHubConnectProps) {
  const [username, setUsername] = useState(currentUsername || "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!isValidGithubUsername(username)) {
      setError("Invalid GitHub username");
      return;
    }
    setError("");
    setLoading(true);
    try {
      await onConnect(username);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-3">
      <div className="flex gap-2">
        <Input
          placeholder="GitHub username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <Button onClick={handleSubmit} disabled={loading || !username}>
          {loading ? "Connecting..." : "Connect"}
        </Button>
      </div>
      {error && <p className="text-sm text-destructive">{error}</p>}
      {currentUsername && (
        <p className="text-sm text-muted-foreground">
          Connected: <a href={`https://github.com/${currentUsername}`} target="_blank" rel="noreferrer" className="underline">{currentUsername}</a>
        </p>
      )}
    </div>
  );
}
