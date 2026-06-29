import { useEffect, useRef } from "react";
import mermaid from "mermaid";

mermaid.initialize({
  startOnLoad: false
});

type MermaidProps = {
  chart: string;
};

export function Mermaid({ chart }: MermaidProps) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;

    const id = `mermaid-${Math.random().toString(36).slice(2)}`;

    mermaid.render(id, chart).then(({ svg }) => {
      if (ref.current) {
        ref.current.innerHTML = svg;
      }
    });
  }, [chart]);

  return <div ref={ref} />;
}