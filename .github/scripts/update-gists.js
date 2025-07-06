// const fs = require('fs');
// const fetch = require('node-fetch');
import fs from 'fs';
import fetch from 'node-fetch';

const username = 'kumarawmpapp';
const startMarker = '<!-- GIST-LIST:START -->';
const endMarker = '<!-- GIST-LIST:END -->';

async function getGists() {
  const res = await fetch(`https://api.github.com/users/${username}/gists`);
  if (!res.ok) throw new Error(`GitHub API error: ${res.status}`);
  return res.json();
}

function generateList(gists) {
  return gists.map(gist => {
    const desc = gist.description || '(no description)';
    return `-> [${desc}](${gist.html_url})`;
  }).join('\n');
}

function updateReadme(gistList) {
  const readmePath = 'README.md';
  const readme = fs.readFileSync(readmePath, 'utf8');
  const updated = readme.replace(
    new RegExp(`${startMarker}[\\s\\S]*?${endMarker}`),
    `${startMarker}\n${gistList}\n${endMarker}`
  );
  fs.writeFileSync(readmePath, updated);
}

(async () => {
  try {
    const gists = await getGists();
    const gistList = generateList(gists);
    updateReadme(gistList);
    console.log('✅ README updated with gist list.');
  } catch (err) {
    console.error('❌ Failed to update README:', err);
    process.exit(1);
  }
})();
