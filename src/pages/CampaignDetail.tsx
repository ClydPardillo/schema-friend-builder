import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { Droplet, Home, Users } from 'lucide-react';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';
import CampaignBanner from '@/components/ui/campaign/CampaignBanner';
import CampaignHeader from '@/components/ui/campaign/CampaignHeader';
import DonationCard from '@/components/ui/campaign/DonationCard';
import TabNavigation from '@/components/ui/campaign/TabNavigation';
import TabContent from '@/components/ui/campaign/TabContent';
import FavoriteButton from '@/components/ui/campaign/FavoriteButton';

const SAMPLE_CAMPAIGN = {
  id: "1",
  title: "Build Clean Water Wells in Rural Villages",
  imageUrl: "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
  bannerUrl: "https://images.unsplash.com/photo-1503387837-b154d5074bd2?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80",
  charity: "Water For All Foundation",
  description: "Help us build 10 clean water wells that will provide safe drinking water to over 5,000 people in rural communities. Access to clean water is a fundamental human right, yet millions still lack this basic necessity. Your donation will help us construct durable wells that will serve these communities for decades to come.\n\nThis project focuses on rural villages where residents currently walk miles each day to collect water from contaminated sources, leading to waterborne diseases and other health issues. By building these wells, we not only provide clean water but also give back time to families, allowing children to attend school and adults to focus on productive activities.\n\nOur implementation partner has over 15 years of experience in well construction and community water management training. Each well location has been carefully selected based on hydrogeological surveys to ensure sustainability.",
  raised: 850000,
  goal: 1000000,
  daysLeft: 15,
  verified: true,
  category: "Clean Water",
  donors: 432,
  location: "Multiple Rural Communities, Central Philippines",
  charityLogo: "https://randomuser.me/api/portraits/men/32.jpg",
  transparency: 98,
  efficiency: 95,
};

const MILESTONES = [
  {
    id: "1",
    title: "Site Selection and Community Engagement",
    description: "Complete hydrogeological surveys, select optimal well locations, and conduct community meetings to ensure local buy-in and support.",
    status: "released" as const,
    date: "January 15, 2024",
    amount: 200000,
    evidence: "Completed surveys for all 10 sites, with community meeting attendance logs and signed MOUs from village leaders attached.",
  },
  {
    id: "2",
    title: "Initial Construction - First 3 Wells",
    description: "Begin construction of the first 3 wells, including drilling, casing installation, and platform construction.",
    status: "verified" as const,
    date: "March 1, 2024",
    amount: 300000,
    evidence: "Construction completed on wells 1-3. Photo documentation and engineering certification provided as verification.",
  },
  {
    id: "3",
    title: "Mid-Project Extension - 4 More Wells",
    description: "Construction of wells 4-7, following the same quality standards and community involvement processes.",
    status: "pending" as const,
    date: "April 30, 2024",
    amount: 400000,
    evidence: "Construction in progress. Preliminary photos submitted showing work on wells 4 and 5.",
  },
  {
    id: "4",
    title: "Final Construction & Water Quality Testing",
    description: "Complete the final 3 wells, conduct comprehensive water quality testing on all wells, and train community members on maintenance.",
    status: "upcoming" as const,
    date: "June 15, 2024",
    amount: 100000,
  },
];

const IMPACT_METRICS = [
  {
    id: "1",
    title: "People with Clean Water",
    value: "2,175",
    icon: <Droplet className="h-6 w-6 text-clearcause-primary" />,
    trend: 15,
  },
  {
    id: "2",
    title: "Wells Completed",
    value: "3",
    icon: <Home className="h-6 w-6 text-clearcause-primary" />,
    trend: 0,
  },
  {
    id: "3",
    title: "Villages Served",
    value: "3",
    icon: <Users className="h-6 w-6 text-clearcause-primary" />,
    trend: 0,
  },
  {
    id: "4",
    title: "Water Quality (Purity)",
    value: "98%",
    icon: <Droplet className="h-6 w-6 text-clearcause-primary" />,
    trend: 2,
  },
];

const RECENT_ACTIVITIES = [
  {
    id: "1",
    title: "Well #3 Construction Completed",
    timestamp: "2 days ago",
    description: "Construction team has finished the third well installation in Barangay San Isidro. Water quality testing shows 98% purity levels.",
  },
  {
    id: "2",
    title: "Community Training Session",
    timestamp: "1 week ago",
    description: "30 community members trained in basic well maintenance and water safety protocols to ensure long-term sustainability.",
  },
  {
    id: "3",
    title: "Well #4 Construction Started",
    timestamp: "1 week ago",
    description: "Ground broken for fourth well in Barangay Mabini. Expected completion in 2 weeks if weather permits.",
  },
];

const CampaignDetail: React.FC = () => {
  const { campaignId } = useParams();
  const [activeTab, setActiveTab] = useState('about');

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-grow">
        <CampaignBanner 
          bannerUrl={SAMPLE_CAMPAIGN.bannerUrl}
          title={SAMPLE_CAMPAIGN.title}
        />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-16 relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column - Campaign Info */}
            <div className="lg:col-span-2 space-y-6">
              <CampaignHeader
                category={SAMPLE_CAMPAIGN.category}
                verified={SAMPLE_CAMPAIGN.verified}
                title={SAMPLE_CAMPAIGN.title}
                charityLogo={SAMPLE_CAMPAIGN.charityLogo}
                charity={SAMPLE_CAMPAIGN.charity}
                daysLeft={SAMPLE_CAMPAIGN.daysLeft}
              />
              {/* Add Favorite Button */}
              <div className="flex justify-end pr-4 pb-2">
                <FavoriteButton campaignId={SAMPLE_CAMPAIGN.id} />
              </div>
              {/* Tab Navigation and Content */}
              <div className="bg-white rounded-xl shadow-md">
                <TabNavigation 
                  activeTab={activeTab}
                  onTabChange={setActiveTab}
                />

                <div className="p-6">
                  <TabContent
                    activeTab={activeTab}
                    description={SAMPLE_CAMPAIGN.description}
                    location={SAMPLE_CAMPAIGN.location}
                    milestones={MILESTONES}
                    impactMetrics={IMPACT_METRICS}
                    recentActivities={RECENT_ACTIVITIES}
                    campaignId={campaignId || ''}
                  />
                </div>
              </div>
            </div>

            {/* Right Column - Donation Box */}
            <div className="lg:col-span-1 space-y-6">
              <DonationCard campaign={SAMPLE_CAMPAIGN} />
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default CampaignDetail;
