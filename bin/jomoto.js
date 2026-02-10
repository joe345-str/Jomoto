#!/usr/bin/env node

const { Command } = require('commander');
const pkg = require('../package.json');

const program = new Command();
const defaultBaseUrl = process.env.JOMOTO_BASE_URL || 'http://localhost:3000';

program
  .name('jomoto')
  .description('CLI for the Catfish Heads AI proxy')
  .version(pkg.version)
  .option('-b, --base-url <url>', 'AI proxy base URL', defaultBaseUrl);

program
  .command('generate <topic>')
  .description('Generate a new SEO blog post via the AI proxy')
  .option('-k, --keywords <keywords>', 'Comma-separated keywords to guide generation')
  .option('-m, --meta <meta>', 'Optional meta description hint')
  .action(async (topic, options) => {
    const payload = {
      topic,
    };

    if (options.keywords) {
      payload.keywords = options.keywords
        .split(',')
        .map((keyword) => keyword.trim())
        .filter(Boolean);
    }

    if (options.meta) {
      payload.meta = options.meta;
    }

    const baseUrl = program.opts().baseUrl;
    await handleRequest(baseUrl, '/api/generate-post', payload);
  });

program
  .command('enhance <pageId>')
  .description('Enhance or rewrite an existing page via the AI proxy')
  .option('-p, --prompt <prompt>', 'Additional guidance for the model')
  .action(async (pageId, options) => {
    const payload = { pageId };

    if (options.prompt) {
      payload.prompt = options.prompt;
    }

    const baseUrl = program.opts().baseUrl;
    await handleRequest(baseUrl, '/api/ai-enhance', payload);
  });

program
  .command('inspect')
  .description('Show the current configuration source for the AI proxy base URL')
  .action(() => {
    console.log(`Base URL: ${program.opts().baseUrl}`);
  });

async function handleRequest(baseUrl, endpoint, payload) {
  try {
    const result = await postJson(baseUrl, endpoint, payload);

    if (typeof result === 'string') {
      console.log(result);
      return;
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}

async function postJson(baseUrl, endpoint, payload) {
  const url = new URL(endpoint, baseUrl);
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const text = await response.text();
  const data = parseMaybeJson(text);

  if (!response.ok) {
    const errorMessage =
      (data && (data.error || data.message)) ||
      text ||
      `Request failed with status ${response.status}`;

    throw new Error(errorMessage);
  }

  return data ?? text;
}

function parseMaybeJson(text) {
  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

program.parseAsync(process.argv);
