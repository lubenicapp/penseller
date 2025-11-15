const steps = [
  {
    number: "01",
    title: "Insert Your Pencil",
    description: "Simply slide your short pencil into the LambdaPen holder until it reaches the bottom."
  },
  {
    number: "02",
    title: "Twist to Lock",
    description: "Give the extension a gentle twist to securely lock your pencil in place."
  },
  {
    number: "03",
    title: "Write Away",
    description: "Enjoy comfortable, extended use with perfect balance and grip. Write as if it's a new pencil!"
  }
];

const HowItWorks = () => {
  return (
    <section className="py-24">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            Simple as 1-2-3
          </h2>
          <p className="text-xl text-muted-foreground">
            Getting started with LambdaPen takes seconds. No tools, no mess, no fuss.
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {steps.map((step, index) => (
            <div key={index} className="relative text-center">
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-12 left-[60%] w-[80%] h-0.5 bg-gradient-to-r from-primary/50 to-transparent" />
              )}
              
              <div className="relative">
                <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg">
                  <span className="text-3xl font-bold text-primary-foreground">
                    {step.number}
                  </span>
                </div>
                
                <h3 className="text-2xl font-semibold mb-3">{step.title}</h3>
                <p className="text-muted-foreground">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
