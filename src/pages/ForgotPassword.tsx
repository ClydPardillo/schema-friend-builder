
import React, { useState } from "react";
import { toast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";

const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [token, setToken] = useState(""); // For demonstration only

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch("/users/forgot-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });
    const data = await res.json();
    if (data.success) {
      setSent(true);
      setToken(data.data?.reset_token || "");
      toast({ title: "If your email exists, a link was sent." });
    } else {
      toast({ title: "Failed", description: data.message, variant: "destructive" });
    }
  };
  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="max-w-xs w-full space-y-4 bg-white p-6 rounded shadow">
        <h2 className="text-lg font-semibold mb-2">Forgot Password?</h2>
        {sent ? (
          <div>
            <p className="text-green-700">Check your email for a reset link.</p>
            {token && (
              <div className="mt-2 text-xs text-gray-500">
                For demo: <Link to={`/reset-password?token=${token}`} className="underline">Reset with token</Link>
              </div>
            )}
          </div>
        ) : (
          <>
            <input
              className="w-full border px-3 py-2 rounded"
              type="email"
              required
              placeholder="Your email"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
            <Button type="submit" className="w-full">Send Reset Link</Button>
          </>
        )}
      </form>
    </div>
  );
};

export default ForgotPassword;
