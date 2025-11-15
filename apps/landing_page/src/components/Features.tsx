import { Recycle, Grip, Wrench, Sparkles, Leaf, Heart, Globe } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { useEffect, useState } from "react";

const defaultFeatures = [
  {
    icon: "Recycle",
    title: "Eco-Friendly",
    description: "Reduce waste by extending the life of your pencils. Each LambdaPen saves dozens of pencils from the trash."
  },
  {
    icon: "Grip",
    title: "Perfect Grip",
    description: "Ergonomic design provides comfortable writing experience, even with the shortest pencils."
  },
  {
    icon: "Wrench",
    title: "Universal Fit",
    description: "Works with all standard pencils. Simple twist mechanism locks your pencil securely in place."
  },
  {
    icon: "Sparkles",
    title: "Premium Quality",
    description: "Crafted from durable aluminum with a smooth finish. Built to last for years of daily use."
  }
];

const iconMap: Record<string, any> = {
  Recycle,
  Grip,
  Wrench,
  Sparkles,
  Leaf,
  Heart,
  Globe
};

interface PageContent {
  featuresHeadline?: string;
  features?: Array<{
    icon: string;
    title: string;
    description: string;
  }>;
}

const Features = () => {
  const [content, setContent] = useState<PageContent | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const pageId = urlParams.get('id');
        
        if (!pageId) {
          setLoading(false);
          return;
        }
        
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/api/content/${pageId}`);
        
        if (!response.ok) {
          setLoading(false);
          return;
        }
        
        const data = await response.json();
        setContent(data);
      } catch (err) {
        console.error('Error fetching features data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, []);

  const headline = content?.featuresHeadline || "Why Choose LambdaPen?";
  const features = content?.features || defaultFeatures;

  return (
    <section className="py-24 bg-secondary/50">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            {headline}
          </h2>
          <p className="text-xl text-muted-foreground">
            The smart solution for pencil lovers, artists, students, and anyone who values sustainability.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => {
            const IconComponent = iconMap[feature.icon] || Sparkles;
            return (
              <Card 
                key={index}
                className="border-none shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1"
              >
                <CardContent className="p-6 space-y-4">
                  <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center">
                    <IconComponent className="h-7 w-7 text-primary" />
                  </div>
                  <h3 className="text-xl font-semibold">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Features;
