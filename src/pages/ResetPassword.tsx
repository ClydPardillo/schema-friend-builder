
import React, { useState } from "react";
import { toast } from "@/hooks/use-toast";
import { useSearchParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";

const ResetPassword: React.FC = () => {
  const [params] = useSearchParams();
  const token = params.get("token") || "";
  const [pw, setPw] = useState("");
  const [confirm, setConfirm] = useState("");
  const [done, setDone] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!pw || pw !== confirm) {
      toast({ title: "Error", description: "Passwords do not match", variant: "destructive" });
      return;
    }
    const res = await fetch("/users/reset-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token, new_password: pw }),
    });
    const data = await res.json();
    if (data.success) {
      setDone(true);
      toast({ title: "Reset successful!" });
      setTimeout(() => navigate("/login"), 1500);
    } else {
      toast({ title: "Error", description: data.message, variant: "destructive" });
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="max-w-xs w-full space-y-4 bg-white p-6 rounded shadow">
        <h2 className="text-lg font-semibold mb-2">Reset Password</h2>
        {done ? (
          <div className="text-green-700">Password has been reset! Redirecting…</div>
        ) : (
          <>
            <input
              type="password"
              className="w-full border px-3 py-2 rounded"
              required
              placeholder="New password"
              value={pw}
              onChange={e => setPw(e.target.value)}
            />
            <input
              type="password"
              className="w-full border px-3 py-2 rounded"
              required
              placeholder="Confirm password"
              value={confirm}
              onChange={e => setConfirm(e.target.value)}
            />
            <Button type="submit" className="w-full">Reset Password</Button>
          </>
        )}
      </form>
    </div>
  );
};

export default ResetPassword;
