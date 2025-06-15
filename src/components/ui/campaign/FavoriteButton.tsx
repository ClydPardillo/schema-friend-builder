
import React, { useState, useEffect } from 'react';
import { Bookmark, BookmarkPlus, BookmarkX } from 'lucide-react';
import { toast } from '@/hooks/use-toast';

interface FavoriteButtonProps {
  campaignId: string;
}

const FavoriteButton: React.FC<FavoriteButtonProps> = ({ campaignId }) => {
  const [isFavorite, setIsFavorite] = useState(false);
  const [loading, setLoading] = useState(false);

  // fetch favorites on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    fetch('/favorites', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => {
        const found = data.favorites?.some((fav: any) => fav.campaign_id === campaignId);
        setIsFavorite(!!found);
      })
      .catch(() => {});
  }, [campaignId]);

  const handleToggleFavorite = async () => {
    setLoading(true);
    const token = localStorage.getItem('access_token');
    if (!token) {
      toast({ title: "Not logged in", description: "Sign in to save campaigns", variant: "destructive" });
      setLoading(false);
      return;
    }
    try {
      if (!isFavorite) {
        const res = await fetch('/favorites', {
          method: 'POST',
          headers: {'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
          body: JSON.stringify({ campaign_id: campaignId })
        });
        if (res.ok) {
          setIsFavorite(true);
          toast({ title: "Saved", description: "Campaign added to your favorites." });
        } else {
          const d = await res.json();
          toast({ title: "Error", description: d.detail || "Unable to save.", variant: "destructive" });
        }
      } else {
        const res = await fetch(`/favorites/${campaignId}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          setIsFavorite(false);
          toast({ title: "Removed", description: "Campaign removed from favorites." });
        }
      }
    } catch (err) {
      toast({ title: "Network error", description: "Try again later.", variant: "destructive" });
    }
    setLoading(false);
  };

  return (
    <button
      className={`flex items-center gap-1 px-2 py-1 text-xs rounded 
        ${isFavorite ? "bg-clearcause-accent/30 text-clearcause-primary" : "bg-gray-100 text-gray-500"}
        ${loading ? "opacity-50" : ""}
      `}
      onClick={handleToggleFavorite}
      disabled={loading}
      aria-label={isFavorite ? "Unfavorite" : "Add to favorites"}
    >
      {isFavorite ? <BookmarkX size={16}/> : <BookmarkPlus size={16}/>}
      {isFavorite ? "Remove" : "Save"}
    </button>
  );
};

export default FavoriteButton;
