import { EYEBROW, HEADLINE, TAGLINE } from '../labels'

export function Hero() {
  return (
    <section className="hero" aria-labelledby="hero-title">
      <p className="eyebrow">{EYEBROW}</p>
      <h2 id="hero-title">{HEADLINE}</h2>
      <p className="hero-text">{TAGLINE}</p>
    </section>
  )
}
