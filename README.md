# Catfish Heads Blog: AI Proxy

Welcome to the AI proxy for the Catfish Heads blog! This service powers SEO-driven blogging using generative AI with robust security, including seamless integration with OpenAI and Hugging Face models. It enables smarter and broader content creation, covering every page and post to maximize engagement and outreach.

## Key Features

- **AI-Powered SEO Content Generation:**
  - Automatically generates high-quality, SEO-optimized blog posts and pages to boost organic traffic.
  - Customizes headlines, keywords, and meta descriptions for each article, improving discoverability and ranking.
  - Provides suggestions and generates content ideas tailored to your blog’s audience and trending topics.

- **OpenAI Key Security:**
  - Uses a secure proxy system to interact with OpenAI APIs.
  - OpenAI API keys are never exposed to the end user or front-end code—managed exclusively server-side.
  - Supports environment variable-based key handling, rotation, and monitoring for best-practice security.

- **Hugging Face Integration:**
  - Connects seamlessly to Hugging Face's `google/flan-t5-small` model for diverse generative tasks:
    - Headline generation
    - Summaries
    - Content rewriting
    - Contextual Q&A
  - Efficient failover: If the OpenAI API is unavailable, content generation continues with Hugging Face models.

- **Full Blog & Page Coverage:**
  - Every blog post and static page can be enhanced or generated using the AI proxy.
  - Supports batch updating of existing posts or pages with improved SEO and new content sections.
  - Integrates with your CMS or markdown file structure.

## Technical Details

- **Tech Stack:** Node.js proxy (Express), OpenAI API, Hugging Face `transformers` library
- **Security:** Environment variable management, secure server routes, and best practices for secrets
- **Deployment:** Deployable on any Node.js-compatible host supporting environment variables and outbound HTTPS

## Getting Started

1. **Clone the Repository**
   ```bash
   git clone https://github.com/joe345-str/Jomoto.git
   ```

2. **Install Dependencies**
   ```bash
   cd Jomoto
   npm install
   ```

3. **Configure API Keys**
   - Add your OpenAI key and Hugging Face token to environment variables (`.env` file):
     ```env
     OPENAI_API_KEY=your-openai-key
     HF_TOKEN=your-huggingface-token
     ```

4. **Start the Proxy Service**
   ```bash
   npm run start:ai-proxy
   ```

## Usage Examples

- **Generate a new SEO blog post:**
  ```bash
  curl -X POST /api/generate-post -d '{"topic": "catfish habitat"}'
  ```
- **Rewrite or summarize an existing page:**
 ```bash
 curl -X POST /api/ai-enhance -d '{"pageId": "about-me"}'
 ```

## CLI

- Requires Node.js 20+ (built-in `fetch` support).
- Install dependencies: `npm install`
- View help: `npm test` (runs `jomoto --help`)
- Generate a post: `npx jomoto generate "catfish habitat" --keywords "catfish,river"` (defaults to `http://localhost:3000`; override with `--base-url` or `JOMOTO_BASE_URL`)
- Enhance a page: `npx jomoto enhance about-me --prompt "Keep the playful tone"`
- Inspect configured proxy target: `npx jomoto inspect`

## License
MIT License

---

For feedback, contribution, or issues, please open an issue or PR!
