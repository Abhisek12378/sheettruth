import { ADAPTER_URL, GITHUB_URL, PRODUCT_NAME } from '../labels'

export function Footer() {
  return (
    <footer className="footer">
      <span>{PRODUCT_NAME}. Every finding is checked against the workbook before it is reported.</span>
      <nav aria-label="Project links">
        {GITHUB_URL && (
          <a href={GITHUB_URL} target="_blank" rel="noreferrer">
            Source on GitHub
          </a>
        )}
        {ADAPTER_URL && (
          <a href={ADAPTER_URL} target="_blank" rel="noreferrer">
            Model adapter on Hugging Face
          </a>
        )}
      </nav>
    </footer>
  )
}
