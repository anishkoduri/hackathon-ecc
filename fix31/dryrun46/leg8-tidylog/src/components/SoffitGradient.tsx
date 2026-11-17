import { useEffect, useRef } from "react";

/**
 * Soffit — GetLayers gradient layer, rebuilt from its published description.
 * Source (live, fetched 2026-11-17): https://www.getlayers.ai/layer/soffit
 * Category: Gradients (Free, Shadow family). llms.txt: gradients are pure
 * WebGL2, pointer-interactive, ~1 KB each.
 *
 * Published description: "The underside of an overhang: one long fall from
 * the opening into the shade, and a bounce coming back the other way so the
 * deep end lifts off the floor instead of dying flat — the hand turns the
 * light and walks it along the opening."
 *
 * Rebuild (this file, our own code — no GetLayers source vendored):
 * a fullscreen WebGL2 fragment shader — one long vertical fall from a lit
 * opening at the top into shade at the bottom, a bounce term that lifts the
 * deep end back up, and a pointer-driven light that walks along the opening.
 * Re-tinted to the TidyLog palette (ink navy ground, lime signal) per the
 * foundation rule: the layer's composition and motion are kept, its palette
 * is the brief's, not the stock layer's.
 *
 * Reduced motion: a single static frame is drawn once and the loop never
 * starts, so the hero is a complete static design at rest.
 */
const VERT = `#version 300 es
layout(location = 0) in vec2 a_pos;
void main() { gl_Position = vec4(a_pos, 0.0, 1.0); }
`;

const FRAG = `#version 300 es
precision highp float;
uniform vec2 u_res;
uniform float u_time;
uniform vec2 u_mouse; // 0..1, y up
out vec4 outColor;

void main() {
  vec2 uv = gl_FragCoord.xy / u_res;
  // One long fall: light at the opening (top) into shade (bottom).
  float fall = smoothstep(1.0, 0.0, uv.y);
  // Bounce coming back the other way: the deep end lifts off the floor.
  float bounce = 0.35 * pow(sin(uv.y * 3.14159), 2.0) * (0.5 + 0.5 * sin(u_time * 0.6));
  // The hand walks the light along the opening: pointer-driven glow.
  float d = distance(uv, vec2(u_mouse.x, 0.92));
  float lamp = 0.9 * exp(-d * d * 6.0);
  // TidyLog palette: ink navy ground, lime signal.
  vec3 deep = vec3(0.043, 0.063, 0.125);   // #0b1020
  vec3 mid  = vec3(0.078, 0.102, 0.200);   // #141a33
  vec3 lime = vec3(0.722, 0.945, 0.208);   // #b8f135
  vec3 col = mix(deep, mid, fall);
  col += lime * (lamp * 0.55 + bounce * 0.18 * fall);
  // Soft vignette so the opening reads as an overhang, not a flat wash.
  col *= 0.85 + 0.15 * (1.0 - length(uv - vec2(0.5, 0.55)));
  outColor = vec4(col, 1.0);
}
`;

export default function SoffitGradient({ className }: { className?: string }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const gl = canvas.getContext("webgl2");
    if (!gl) return; // No WebGL2: the CSS ink ground behind the canvas is the fallback.
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const compile = (type: number, src: string) => {
      const sh = gl.createShader(type)!;
      gl.shaderSource(sh, src);
      gl.compileShader(sh);
      return sh;
    };
    const prog = gl.createProgram()!;
    gl.attachShader(prog, compile(gl.VERTEX_SHADER, VERT));
    gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, FRAG));
    gl.linkProgram(prog);
    gl.useProgram(prog);

    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(
      gl.ARRAY_BUFFER,
      new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]),
      gl.STATIC_DRAW,
    );
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);

    const uRes = gl.getUniformLocation(prog, "u_res");
    const uTime = gl.getUniformLocation(prog, "u_time");
    const uMouse = gl.getUniformLocation(prog, "u_mouse");
    const mouse = { x: 0.5, y: 0.92 };

    const resize = () => {
      const r = canvas.getBoundingClientRect();
      canvas.width = Math.max(1, Math.floor(r.width * window.devicePixelRatio));
      canvas.height = Math.max(1, Math.floor(r.height * window.devicePixelRatio));
      gl.viewport(0, 0, canvas.width, canvas.height);
    };
    resize();
    window.addEventListener("resize", resize);
    const onMove = (e: PointerEvent) => {
      const r = canvas.getBoundingClientRect();
      mouse.x = (e.clientX - r.left) / Math.max(1, r.width);
      mouse.y = 1 - (e.clientY - r.top) / Math.max(1, r.height);
    };
    window.addEventListener("pointermove", onMove);

    const draw = (t: number) => {
      gl.uniform2f(uRes, canvas.width, canvas.height);
      gl.uniform1f(uTime, t / 1000);
      gl.uniform2f(uMouse, mouse.x, Math.max(0.5, mouse.y));
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    };

    if (reduced) {
      draw(0); // One static frame; no loop.
      return () => {
        window.removeEventListener("resize", resize);
        window.removeEventListener("pointermove", onMove);
      };
    }
    let raf = 0;
    const loop = (t: number) => {
      draw(t);
      raf = requestAnimationFrame(loop);
    };
    raf = requestAnimationFrame(loop);
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
      window.removeEventListener("pointermove", onMove);
    };
  }, []);

  return <canvas ref={canvasRef} className={className} aria-hidden="true" />;
}
