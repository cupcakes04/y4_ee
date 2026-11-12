/**
 * katex_oracle_test.js
 * ====================
 * Authoritative KaTeX Rendering Oracle.
 * Extracts every display math ($$ ... $$) and inline math ($ ... $) block
 * across all chapters in modules/EEEE4138_aerial_robotics/chapters/
 * and runs them through the official KaTeX rendering engine (`katex.renderToString`).
 *
 * Reports verbatim parser exceptions, line numbers, and snippets.
 */

const fs = require('fs');
const path = require('path');
const katex = require('../node_modules/katex');

const chaptersDir = path.join(__dirname, '..', 'chapters');
const files = fs.readdirSync(chaptersDir)
  .filter(f => f.endsWith('.md'))
  .sort();

console.log('='.repeat(90));
console.log(' OFFICIAL KATEX RENDERING ORACLE TEST SUITE');
console.log('='.repeat(90));

let totalFiles = 0;
let totalDisplayBlocks = 0;
let totalInlineSpans = 0;
let totalFailures = 0;

const chapterResults = [];

for (const file of files) {
  totalFiles++;
  const filePath = path.join(chaptersDir, file);
  const content = fs.readFileSync(filePath, 'utf8');

  // Mask fenced code blocks with newlines to preserve exact line numbering
  const contentNoCode = content.replace(/```[\s\S]*?```/g, m => '\n'.repeat((m.match(/\n/g) || []).length));

  // 1. Extract display math blocks ($$ ... $$)
  const displayRegex = /(?<!\\)\$\$([\s\S]*?)(?<!\\)\$\$/g;
  let match;
  let fileDisplayPass = 0;
  let fileDisplayFail = 0;
  let fileInlinePass = 0;
  let fileInlineFail = 0;
  const fileErrors = [];

  while ((match = displayRegex.exec(contentNoCode)) !== null) {
    totalDisplayBlocks++;
    const mathRaw = match[1];
    const startIndex = match.index;
    const lineNumber = contentNoCode.substring(0, startIndex).split('\n').length;

    try {
      katex.renderToString(mathRaw.trim(), {
        displayMode: true,
        throwOnError: true,
        strict: false
      });
      fileDisplayPass++;
    } catch (err) {
      fileDisplayFail++;
      totalFailures++;
      fileErrors.push({
        type: 'DISPLAY_MATH',
        line: lineNumber,
        error: err.message,
        snippet: mathRaw.trim().substring(0, 100).replace(/\n/g, ' ')
      });
    }
  }

  // 2. Extract inline math spans ($ ... $)
  // First mask display blocks
  const contentNoDisplay = contentNoCode.replace(/(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$/g, m => '\n'.repeat((m.match(/\n/g) || []).length));
  const inlineRegex = /(?<!\\)\$([^\$\n]+?)(?<!\\)\$/g;
  while ((match = inlineRegex.exec(contentNoDisplay)) !== null) {
    totalInlineSpans++;
    const mathRaw = match[1];
    const startIndex = match.index;
    const lineNumber = contentNoDisplay.substring(0, startIndex).split('\n').length;

    try {
      katex.renderToString(mathRaw.trim(), {
        displayMode: false,
        throwOnError: true,
        strict: false
      });
      fileInlinePass++;
    } catch (err) {
      fileInlineFail++;
      totalFailures++;
      fileErrors.push({
        type: 'INLINE_MATH',
        line: lineNumber,
        error: err.message,
        snippet: mathRaw.trim().substring(0, 80)
      });
    }
  }

  chapterResults.push({
    file,
    displayPass: fileDisplayPass,
    displayFail: fileDisplayFail,
    inlinePass: fileInlinePass,
    inlineFail: fileInlineFail,
    errors: fileErrors
  });
}

// Print results table
console.log(`${'Chapter File'.padEnd(32)} | ${'Display Math'.padEnd(15)} | ${'Inline Math'.padEnd(15)} | ${'Status'.padEnd(8)}`);
console.log('-'.repeat(90));

for (const res of chapterResults) {
  const dispStr = `${res.displayPass} pass / ${res.displayFail} fail`;
  const inlStr = `${res.inlinePass} pass / ${res.inlineFail} fail`;
  const status = (res.displayFail === 0 && res.inlineFail === 0) ? 'PASS' : 'FAIL';
  console.log(`${res.file.padEnd(32)} | ${dispStr.padEnd(15)} | ${inlStr.padEnd(15)} | ${status.padEnd(8)}`);
}

console.log('-'.repeat(90));
console.log(`TOTALS: ${totalFiles} Files Audited`);
console.log(`Display Math Blocks Tested: ${totalDisplayBlocks} (${totalFailures} failures)`);
console.log(`Inline Math Spans Tested:   ${totalInlineSpans}`);
console.log(`Overall KaTeX Oracle Verdict: [${totalFailures === 0 ? 'APPROVE' : 'REJECT'}]`);
console.log('='.repeat(90));

if (totalFailures > 0) {
  console.log('\n--- VERBATIM KATEX PARSER FAILURES ---');
  for (const res of chapterResults) {
    if (res.errors.length > 0) {
      console.log(`\nFile: ${res.file} (${res.errors.length} errors)`);
      for (const e of res.errors) {
        console.log(`  [Line ${e.line}] [${e.type}] ${e.error}`);
        console.log(`    Snippet: ${e.snippet}`);
      }
    }
  }
  process.exit(1);
} else {
  console.log('\nAll mathematical formulas rendered cleanly with 0 exceptions.');
  process.exit(0);
}
