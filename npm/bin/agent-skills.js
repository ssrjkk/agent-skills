#!/usr/bin/env node

/**
 * agent-skills CLI - Install and manage Agent Skills
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILLS_SOURCE = path.join(__dirname, '..', 'skills');
const CATALOG_PATH = path.join(__dirname, '..', 'skills_catalog.json');

function getTargetDir(agent) {
  const home = os.homedir();
  const agents = {
    'claude': path.join(home, '.claude', 'skills'),
    'opencode': path.join(home, '.opencode', 'skills'),
    'cursor': path.join(home, '.cursor', 'skills'),
    'windsurf': path.join(home, '.windsurf', 'skills'),
  };
  return agents[agent] || agents['claude'];
}

function listSkills() {
  const catalog = JSON.parse(fs.readFileSync(CATALOG_PATH, 'utf8'));
  console.log(`\nAgent Skills Library v${catalog.metadata.schema_version}`);
  console.log(`${catalog.metadata.total_skills} skills across ${catalog.metadata.domains.length} domains\n`);

  const byDomain = {};
  for (const skill of catalog.skills) {
    if (!byDomain[skill.category]) byDomain[skill.category] = [];
    byDomain[skill.category].push(skill.name);
  }

  for (const domain of Object.keys(byDomain).sort()) {
    console.log(`  ${domain}:`);
    for (const name of byDomain[domain].sort()) {
      console.log(`    - ${name}`);
    }
  }
  console.log();
}

function installSkill(name, agent = 'claude') {
  const catalog = JSON.parse(fs.readFileSync(CATALOG_PATH, 'utf8'));
  const skill = catalog.skills.find(s => s.name === name);

  if (!skill) {
    console.error(`Error: Skill '${name}' not found`);
    process.exit(1);
  }

  const sourceDir = path.join(SKILLS_SOURCE, skill.category, name);
  if (!fs.existsSync(sourceDir)) {
    console.error(`Error: Skill files not found at ${sourceDir}`);
    process.exit(1);
  }

  const targetDir = path.join(getTargetDir(agent), skill.category, name);

  // Create target directory
  fs.mkdirSync(path.dirname(targetDir), { recursive: true });

  // Copy files
  copyDir(sourceDir, targetDir);

  console.log(`\nInstalled '${name}' -> ${targetDir}`);
  console.log(`Agent: ${agent}\n`);
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function showHelp() {
  console.log(`
agent-skills - Install and manage Agent Skills

Usage:
  agent-skills list                    List all available skills
  agent-skills install <name>          Install a skill (default: claude)
  agent-skills install <name> --agent <agent>  Install for specific agent

Agents: claude, opencode, cursor, windsurf

Examples:
  agent-skills list
  agent-skills install react-19
  agent-skills install docker --agent cursor
`);
}

// CLI
const args = process.argv.slice(2);
const command = args[0];

if (!command || command === 'help' || command === '--help') {
  showHelp();
} else if (command === 'list') {
  listSkills();
} else if (command === 'install') {
  const name = args[1];
  if (!name) {
    console.error('Error: Skill name required');
    process.exit(1);
  }

  let agent = 'claude';
  const agentIdx = args.indexOf('--agent');
  if (agentIdx !== -1 && args[agentIdx + 1]) {
    agent = args[agentIdx + 1];
  }

  installSkill(name, agent);
} else {
  console.error(`Unknown command: ${command}`);
  showHelp();
  process.exit(1);
}
