import type { Feature } from "../types";
import { NamedIcon } from "./Icons";

export default function FeatureGrid({ features }: { features: Feature[] }) {
  return (
    <section className="container features">
      {features.map((feature) => (
        <article key={feature.id} className="feature-card">
          <div className="icon-wrap">
            <NamedIcon name={feature.icon} />
          </div>
          <h3>{feature.title}</h3>
          <p>{feature.description}</p>
        </article>
      ))}
    </section>
  );
}
