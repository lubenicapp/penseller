import { Card, CardContent } from "@/components/ui/card";
import { Star } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useEffect, useState } from "react";

interface Testimonial {
  name: string;
  role: string;
  content: string;
  rating: number;
  initials: string;
  avatarUrl?: string;
  profile_picture_url?: string;
}

interface PageContent {
  allTestimonials?: Testimonial[];
  testimonialsHeadline?: string;
  testimonial1?: {
    name?: string;
    role?: string;
    avatarUrl?: string;
  };
  testimonial2?: {
    name?: string;
    role?: string;
    avatarUrl?: string;
  };
}

const defaultTestimonials: Testimonial[] = [
  {
    name: "Sarah Mitchell",
    role: "Artist & Illustrator",
    content: "As an artist, I go through pencils quickly. LambdaPen has been a game-changer - I can use every pencil down to the last inch. It's saved me money and reduced waste significantly.",
    rating: 5,
    initials: "SM"
  },
  {
    name: "James Chen",
    role: "Architecture Student",
    content: "The grip is perfect for long sketching sessions. I used to throw away perfectly good pencils just because they got too short. Not anymore! This is brilliant engineering.",
    rating: 5,
    initials: "JC"
  },
  {
    name: "Emily Rodriguez",
    role: "Elementary School Teacher",
    content: "I bought these for my entire classroom. The kids love them, and we're teaching sustainability in a practical way. Parents are asking where to get them!",
    rating: 5,
    initials: "ER"
  },
  {
    name: "Michael Thompson",
    role: "Graphic Designer",
    content: "Quality craftsmanship and it actually works as advertised. The aluminum feels premium and the twist-lock mechanism is smooth. Worth every penny.",
    rating: 5,
    initials: "MT"
  },
  {
    name: "Lisa Park",
    role: "Writer & Poet",
    content: "I'm old-fashioned and love writing with pencils. LambdaPen lets me hold onto my favorites longer. Simple, elegant solution to a real problem.",
    rating: 5,
    initials: "LP"
  },
  {
    name: "David Kumar",
    role: "Engineering Student",
    content: "Perfect for technical drawing. The balance is excellent even with short pencils. My drafting work has never been more precise.",
    rating: 5,
    initials: "DK"
  }
];

const Testimonials = () => {
  const [testimonials, setTestimonials] = useState<Testimonial[]>(defaultTestimonials);
  const [headline, setHeadline] = useState<string>("Testimonials");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const urlParams = new URLSearchParams(window.location.search);
        const pageId = urlParams.get('id');
        
        // Only fetch if there's a page ID
        if (!pageId) {
          setLoading(false);
          return;
        }
        
        // Fetch content from API using relative URL (works on any domain)
        const response = await fetch(`/api/content/${pageId}`);
        
        if (!response.ok) {
          setLoading(false);
          return;
        }
        
        const data: PageContent = await response.json();
        
        // Update headline if provided
        if (data.testimonialsHeadline) {
          setHeadline(data.testimonialsHeadline);
        }
        
        // Use allTestimonials if available (from workflow with reactors)
        if (data.allTestimonials && data.allTestimonials.length > 0) {
          setTestimonials(data.allTestimonials);
        } else {
          // Fallback to updating individual testimonials
          const updatedTestimonials = [...defaultTestimonials];
          
          // Update first testimonial
          if (data.testimonial1) {
            if (data.testimonial1.name) {
              updatedTestimonials[0].name = data.testimonial1.name;
              // Generate initials from name
              const nameParts = data.testimonial1.name.split(' ');
              updatedTestimonials[0].initials = nameParts
                .map(part => part[0])
                .join('')
                .toUpperCase()
                .slice(0, 2);
            }
            if (data.testimonial1.role) {
              updatedTestimonials[0].role = data.testimonial1.role;
            }
            if (data.testimonial1.avatarUrl) {
              updatedTestimonials[0].avatarUrl = data.testimonial1.avatarUrl;
            }
          }
          
          // Update second testimonial
          if (data.testimonial2) {
            if (data.testimonial2.name) {
              updatedTestimonials[1].name = data.testimonial2.name;
              // Generate initials from name
              const nameParts = data.testimonial2.name.split(' ');
              updatedTestimonials[1].initials = nameParts
                .map(part => part[0])
                .join('')
                .toUpperCase()
                .slice(0, 2);
            }
            if (data.testimonial2.role) {
              updatedTestimonials[1].role = data.testimonial2.role;
            }
            if (data.testimonial2.avatarUrl) {
              updatedTestimonials[1].avatarUrl = data.testimonial2.avatarUrl;
            }
          }
          
          setTestimonials(updatedTestimonials);
        }
      } catch (err) {
        console.error('Error fetching testimonial data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, []);

  return (
    <section className="py-24 bg-background">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            {headline}
          </h2>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto">
          {testimonials.map((testimonial, index) => (
            <Card 
              key={index}
              className="border-none shadow-sm hover:shadow-md transition-all duration-300"
            >
              <CardContent className="p-6 space-y-4">
                <div className="flex gap-1">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star 
                      key={i} 
                      className="h-5 w-5 fill-primary text-primary" 
                    />
                  ))}
                </div>
                
                <p className="text-muted-foreground leading-relaxed">
                  "{testimonial.content}"
                </p>
                
                <div className="flex items-center gap-3 pt-4 border-t">
                  <Avatar className="h-10 w-10 bg-primary/10">
                    {(testimonial.profile_picture_url || testimonial.avatarUrl) && (
                      <AvatarImage 
                        src={testimonial.profile_picture_url || testimonial.avatarUrl} 
                        alt={testimonial.name}
                      />
                    )}
                    <AvatarFallback className="text-primary font-semibold">
                      {testimonial.initials}
                    </AvatarFallback>
                  </Avatar>
                  <div>
                    <div className="font-semibold text-sm">{testimonial.name}</div>
                    <div className="text-xs text-muted-foreground">{testimonial.role}</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
        
        <div className="text-center mt-12">
          <div className="inline-flex items-center gap-2 text-sm text-muted-foreground">
            <div className="flex">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="h-4 w-4 fill-primary text-primary" />
              ))}
            </div>
            <span className="font-semibold text-foreground">4.9/5</span>
            <span>from over 2,000 reviews</span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
