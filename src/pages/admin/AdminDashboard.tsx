import React from 'react';
import AdminStatsGrid from '@/components/admin/AdminStatsGrid';
import AdminQuickActions from '@/components/admin/AdminQuickActions';
import AdminRecentActivity from '@/components/admin/AdminRecentActivity';
import { toast } from '@/hooks/use-toast';

const AdminDashboard = () => {
  // Example campaign IDs (replace with fetched list in a real app):
  const campaigns = [{ id: "1", title: "Clean Water Project" }];
  
  const handleApprove = async (campaignId: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) return toast({ title: "Auth error" });
    const res = await fetch(`/admin/campaigns/${campaignId}/approve`, {
      method: "POST",
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) {
      toast({ title: "Campaign Approved" });
      // Optionally refresh data
    } else {
      toast({ title: "Error", description: "Approval failed", variant: "destructive" });
    }
  };

  const handleReject = async (campaignId: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) return toast({ title: "Auth error" });
    const res = await fetch(`/admin/campaigns/${campaignId}/reject`, {
      method: "POST",
      headers: { 'Authorization': `Bearer ${token}` }
    });
    if (res.ok) {
      toast({ title: "Campaign Rejected" });
    } else {
      toast({ title: "Error", description: "Rejection failed", variant: "destructive" });
    }
  };

  return (
    <div className="space-y-8 p-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">ClearCause Admin Dashboard</h1>
        <p className="text-muted-foreground">
          Monitor platform activity and manage verification processes
        </p>
      </div>

      {/* Stats Grid */}
      <AdminStatsGrid />

      <div className="grid gap-6 md:grid-cols-2">
        {/* Quick Actions */}
        <AdminQuickActions />

        {/* Recent Activity */}
        <AdminRecentActivity />
      </div>

      <div>
        <h2 className="font-bold mb-2">Pending Campaign Approvals</h2>
        <ul>
          {campaigns.map(c => (
            <li key={c.id} className="flex items-center gap-2 mb-2">
              <span>{c.title}</span>
              <button className="bg-green-200 px-2 py-1 rounded text-xs" onClick={() => handleApprove(c.id)}>Approve</button>
              <button className="bg-red-200 px-2 py-1 rounded text-xs" onClick={() => handleReject(c.id)}>Reject</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AdminDashboard;
