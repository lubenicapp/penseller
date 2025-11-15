import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import { useEffect, useState } from "react";
import heroImage from "@/assets/hero-image.jpg";
import avatar1 from "@/assets/avatar-1.jpg";
import avatar2 from "@/assets/avatar-2.jpg";
import avatar3 from "@/assets/avatar-3.jpg";
import avatar4 from "@/assets/avatar-4.jpg";
import companyLogo1 from "@/assets/company-logo-1.jpg";
import companyLogo2 from "@/assets/company-logo-2.jpg";
import companyLogo3 from "@/assets/company-logo-3.jpg";
import companyLogo4 from "@/assets/company-logo-4.jpg";

interface PageContent {
  id: string;
  productName?: string;
  title: string;
  subtitle: string;
  description?: string;
  ctaPrimary?: string;
  ctaSecondary?: string;
  heroImageUrl?: string;
  companyLogos?: {
    logo1?: string;
    logo2?: string;
    logo3?: string;
    logo4?: string;
  };
}

const Hero = () => {
  const [content, setContent] = useState<PageContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchContent = async () => {
      try {
        // Get the 'id' query parameter from URL
        const urlParams = new URLSearchParams(window.location.search);
        const pageId = urlParams.get('id') || 'default';
        
        // Fetch content from API
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/api/content/${pageId}`);
        
        if (!response.ok) {
          throw new Error(`Failed to load content for ID: ${pageId}`);
        }
        
        const data = await response.json();
        setContent(data);
      } catch (err) {
        console.error('Error fetching content:', err);
        setError(err instanceof Error ? err.message : 'Failed to load content');
        // Use default content on error
        setContent({
          id: 'default',
          title: 'Every Pencil Deserves a Second Life',
          subtitle: 'LambdaPen extends your short pencils, giving you perfect grip and control. Write more, waste less, create endlessly.'
        });
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, []);

  // Show loading state
  if (loading) {
    return (
      <section className="relative min-h-[90vh] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading content...</p>
        </div>
      </section>
    );
  }

  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-background via-secondary/30 to-background" />
      
      <div className="container mx-auto px-4 md:px-6 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8 text-center lg:text-left">
            <div className="inline-block">
              <span className="px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium">
                Smart. Sustainable. Simple.
              </span>
            </div>
            
            <div className="flex items-center gap-4 justify-center lg:justify-start">
              <div className="flex -space-x-3">
                <img 
                  src={avatar1} 
                  alt="Happy customer" 
                  className="w-12 h-12 rounded-full border-2 border-background object-cover"
                />
                <img 
                  src={avatar2} 
                  alt="Happy customer" 
                  className="w-12 h-12 rounded-full border-2 border-background object-cover"
                />
                <img 
                  src={avatar3} 
                  alt="Happy customer" 
                  className="w-12 h-12 rounded-full border-2 border-background object-cover"
                />
                <img 
                  src={avatar4} 
                  alt="Happy customer" 
                  className="w-12 h-12 rounded-full border-2 border-background object-cover"
                />
              </div>
              <div className="text-left">
                <div className="font-bold text-lg text-foreground">10,000+</div>
                <div className="text-sm text-muted-foreground">Happy Users</div>
              </div>
              <div className="h-12 w-px bg-border" />
              <div className="text-left">
                <div className="font-bold text-lg text-foreground">50,000+</div>
                <div className="text-sm text-muted-foreground">Pencils Saved</div>
              </div>
            </div>
            
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold leading-tight">
              {error && (
                <div className="text-sm text-yellow-600 mb-2">
                  ⚠️ {error} (using default content)
                </div>
              )}
              <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                {content?.title || 'Every Pencil Deserves a Second Life'}
              </span>
            </h1>
            
            <p className="text-xl text-muted-foreground max-w-xl mx-auto lg:mx-0">
              {content?.subtitle || 'LambdaPen extends your short pencils, giving you perfect grip and control. Write more, waste less, create endlessly.'}
            </p>

            {content?.description && (
              <p className="text-lg text-muted-foreground max-w-xl mx-auto lg:mx-0 italic">
                {content.description}
              </p>
            )}

            {content?.id && (
              <div className="text-sm text-muted-foreground">
                Page ID: <span className="font-mono">{content.id}</span>
              </div>
            )}
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Button size="lg" className="text-lg h-14 px-8 shadow-md hover:shadow-lg transition-all">
                {content?.ctaPrimary || 'Get Your LambdaPen'}
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button size="lg" variant="outline" className="text-lg h-14 px-8">
                {content?.ctaSecondary || 'Learn More'}
              </Button>
            </div>
            
            <div className="pt-8">
              <p className="text-sm text-muted-foreground mb-4">Trusted by leading companies</p>
              <div className="flex items-center gap-8 justify-center lg:justify-start flex-wrap opacity-60 grayscale hover:grayscale-0 hover:opacity-100 transition-all duration-300">
                <img 
                  src={content?.companyLogos?.logo1 || companyLogo1} 
                  alt="Tech company" 
                  className="h-8 object-contain" 
                />
                <img 
                  src={content?.companyLogos?.logo2 || companyLogo2} 
                  alt="Education company" 
                  className="h-8 object-contain" 
                />
                <img 
                  src={content?.companyLogos?.logo3 || companyLogo3} 
                  alt="Design studio" 
                  className="h-8 object-contain" 
                />
                <img 
                  src={content?.companyLogos?.logo4 || companyLogo4} 
                  alt="Creative agency" 
                  className="h-8 object-contain" 
                />
              </div>
            </div>
          </div>
          
          <div className="relative">
            <div className="relative rounded-2xl overflow-hidden shadow-2xl">
              <img 
                src={content?.heroImageUrl || heroImage} 
                alt="Product in use" 
                className="w-full h-auto"
              />
            </div>
            <div className="absolute -bottom-4 -right-4 w-32 h-32 bg-primary/20 rounded-full blur-3xl" />
            <div className="absolute -top-4 -left-4 w-32 h-32 bg-accent/20 rounded-full blur-3xl" />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
