import { useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";
import { Terminal } from "@lucasmarkes/hairline/react";
import SplitText from "./components/SplitText";
import SoffitGradient from "./components/SoffitGradient";

gsap.registerPlugin(ScrollTrigger);

/**
 * TidyLog — dev-tool landing page (dry-run #46 design leg).
 * Brief: a CLI + web viewer that turns messy service logs into searchable
 * timelines. One page: hero, three features, one terminal figure, footer.
 *
 * Palette-first inventory (GetLayers consulted FIRST):
 * - GetLayers Soffit gradient (USED) — hero ground, rebuilt as WebGL2, re-tinted ink/lime.
 * - GSAP 3.15.1 (USED) — hero entrance timeline + ScrollTrigger section reveals.
 * - React Bits SplitText-TS-TW (USED) — hero headline character rise.
 * - Hairline Terminal figure (USED) — features-section illustration, pointer-reactive.
 * Motion tokens: entrance 0.6s power2.out, stagger 0.04s, reveal 0.5s power2.out.
 * Reduced motion: GSAP tweens skipped (content visible at rest), Soffit draws
 * one static frame, SplitText renders whole.
 */
export default function App() {
  const rootRef = useRef<HTMLElement | null>(null);
  const reduced =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  useGSAP(
    () => {
      if (reduced) return; // Content is visible at rest; no entrance motion.
      const tl = gsap.timeline({ defaults: { duration: 0.6, ease: "power2.out" } });
      tl.from(".hero-kicker", { y: 16, autoAlpha: 0 })
        .from(".hero-cta", { y: 16, autoAlpha: 0 }, "-=0.35")
        .from(".hero-terminal-card", { y: 24, autoAlpha: 0 }, "-=0.35");
      gsap.utils.toArray<HTMLElement>(".reveal").forEach((el) => {
        gsap.from(el, {
          y: 28,
          autoAlpha: 0,
          duration: 0.5,
          ease: "power2.out",
          scrollTrigger: { trigger: el, start: "top 85%" },
        });
      });
    },
    { scope: rootRef },
  );

  return (
    <main ref={rootRef} className="min-h-screen bg-ink text-paper">
      {/* Hero — Soffit gradient ground, SplitText headline, GSAP entrance. */}
      <header className="relative overflow-hidden">
        <SoffitGradient className="soffit-canvas absolute inset-0 h-full w-full" />
        <div className="relative mx-auto max-w-5xl px-6 pb-24 pt-20">
          <p className="hero-kicker font-mono text-sm tracking-widest text-lime">
            TIDYLOG — LOGS, READABLE
          </p>
          <SplitText
            text="Your logs, finally in order."
            tag="h1"
            className="mt-6 text-5xl font-semibold leading-tight md:text-7xl"
            splitType="words, chars"
            effect="rise"
            delay={0.1}
            duration={0.6}
            staggerFrom="start"
          />
          <p className="mt-6 max-w-xl text-lg text-mist">
            TidyLog turns messy service logs into searchable timelines. Pipe
            stdin in, get the story out — no agents, no dashboards to babysit.
          </p>
          <div className="hero-cta mt-8 flex gap-4">
            <a
              href="#features"
              className="rounded-md bg-lime px-5 py-3 font-semibold text-ink"
            >
              Try the CLI
            </a>
            <a
              href="#figure"
              className="rounded-md border border-mist/40 px-5 py-3 font-semibold text-paper"
            >
              See it work
            </a>
          </div>
          <div className="hero-terminal-card mt-12 rounded-lg border border-white/10 bg-ink-2/80 p-5 font-mono text-sm">
            <p className="text-mist">$ tidylog tail ./api.log | tidylog timeline</p>
            <p className="mt-2 text-lime">12:04:11 GET /checkout → 200 in 41ms</p>
            <p className="text-paper">12:04:12 DB pool saturated → retry 1 of 3</p>
          </div>
        </div>
      </header>

      {/* Features — GSAP ScrollTrigger reveals. */}
      <section id="features" className="mx-auto max-w-5xl px-6 py-20">
        <h2 className="reveal text-3xl font-semibold">Three things, done well</h2>
        <div className="mt-10 grid gap-6 md:grid-cols-3">
          {[
            ["Searchable timelines", "Every line lands on a timeline you can scrub, filter, and share as a link."],
            ["Zero setup", "One binary, no server. Pipe stdin in; the story comes out."],
            ["Honest errors", "TidyLog shows the retry, the timeout, and the pool — not a green checkmark."],
          ].map(([title, body]) => (
            <article key={title} className="reveal rounded-lg border border-white/10 bg-ink-2 p-6">
              <h3 className="text-lg font-semibold text-lime">{title}</h3>
              <p className="mt-2 text-mist">{body}</p>
            </article>
          ))}
        </div>
      </section>

      {/* Hairline figure — Terminal, pointer-reactive, 5:4 aspect. */}
      <section id="figure" className="mx-auto max-w-5xl px-6 pb-20">
        <h2 className="reveal text-3xl font-semibold">It looks like the tool it is</h2>
        <p className="reveal mt-3 max-w-xl text-mist">
          The Terminal figure answers your pointer — the same way TidyLog
          answers a log line. Move across it.
        </p>
        <div className="reveal mx-auto mt-8 max-w-md">
          <Terminal className="w-full" />
        </div>
      </section>

      <footer className="border-t border-white/10 px-6 py-8 text-center font-mono text-sm text-mist">
        TidyLog — free for personal and commercial use. Built with GetLayers,
        GSAP, React Bits, and Hairline.
      </footer>
    </main>
  );
}
