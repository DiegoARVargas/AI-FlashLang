import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import Features from "@/components/Features";
import CardShowcase from "@/components/CardShowcase";
import CallToAction from "@/components/CallToAction";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white font-sans">
      <Navbar />
      <Hero />
      <Features />
      <CardShowcase />
      <CallToAction />
      <Footer />
    </main>
  );
}
