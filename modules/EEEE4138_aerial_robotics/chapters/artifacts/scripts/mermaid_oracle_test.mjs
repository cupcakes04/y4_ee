/**
 * mermaid_oracle_test.mjs
 * =======================
 * Official Mermaid Diagram Parser Oracle.
 * Extracts every single ```mermaid ... ``` block across all 7 chapter files
 * and tests parsing with the official Mermaid API (`mermaid.parse`).
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const chaptersDir = path.join(__dirname, '..', 'chapters');
const files = fs.readdirSync(chaptersDir)
  .filter(f => f.endsWith('.md'))
  .sort();

// Mock minimal browser environment for Mermaid in Node.js
global.window = {
  DOMPurify: { addHook: () => {}, sanitize: s => s },
  addEventListener: () => {}
};
global.document = {
  createElement: () => ({ getContext: () => null }),
  getElementsByTagName: () => []
};

const mermaidModule = await import('../node_modules/mermaid/dist/mermaid.core.mjs');
const mermaid = mermaidModule.default;
mermaid.initialize({ startOnLoad: false, suppressErrorRendering: true });

let totalDiagrams = 0;
let totalFailures = 0;
const results = [];

for (const file of files) {
  const filePath = path.join(chaptersDir, file);
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');

  let inMermaid = false;
  let diagStart = 0;
  let currentDiag = [];
  let fileDiagrams = 0;
  let fileFailures = 0;
  const fileErrors = [];

  for (let idx = 0; idx < lines.length; idx++) {
    const rawLine = lines[idx];
    const stripped = rawLine.trim();

    if (stripped.startsWith('```mermaid')) {
      inMermaid = true;
      diagStart = idx + 1;
      currentDiag = [];
      continue;
    } else if (inMermaid && (stripped.startsWith('```') || stripped.startsWith('~~~'))) {
      inMermaid = false;
      fileDiagrams++;
      totalDiagrams++;
      const diagCode = currentDiag.join('\n').trim();

      try {
        await mermaid.parse(diagCode);
      } catch (err) {
        fileFailures++;
        totalFailures++;
        fileErrors.push({
          line: diagStart,
          error: err.message || String(err),
          snippet: currentDiag.slice(0, 3).join(' ')
        });
      }
      currentDiag = [];
      continue;
    } else if (inMermaid) {
      currentDiag.push(rawLine);
    }
  }

  results.push({
    file,
    diagrams: fileDiagrams,
    failures: fileFailures,
    errors: fileErrors
  });
}

console.log(`${'Chapter File'.padEnd(32)} | ${'Total Diagrams'.padEnd(16)} | ${'Passed'.padEnd(10)} | ${'Status'.padEnd(8)}`);
console.log('-'.repeat(90));

for (const r of results) {
  const passed = r.diagrams - r.failures;
  const status = r.failures === 0 ? 'PASS' : 'FAIL';
  console.log(`${r.file.padEnd(32)} | ${String(r.diagrams).padEnd(16)} | ${String(passed).padEnd(10)} | ${status.padEnd(8)}`);
}

console.log('-'.repeat(90));
console.log(`TOTALS: ${totalDiagrams} Mermaid Diagrams Tested across ${files.length} Chapters`);
console.log(`Total Parser Failures: ${totalFailures}`);
console.log(`Overall Mermaid Oracle Verdict: [${totalFailures === 0 ? 'APPROVE' : 'REJECT'}]`);
console.log('='.repeat(90));

if (totalFailures > 0) {
  console.log('\n--- VERBATIM MERMAID PARSER FAILURES ---');
  for (const r of results) {
    if (r.errors.length > 0) {
      console.log(`\nFile: ${r.file} (${r.errors.length} failed diagrams):`);
      for (const e of r.errors) {
        console.log(`  [Line ${e.line}] Parser Error: ${e.error}`);
        console.log(`    Snippet: ${e.snippet}`);
      }
    }
  }
  process.exit(1);
} else {
  console.log('\nAll Mermaid diagrams parsed cleanly with 0 syntax errors.');
  process.exit(0);
}
