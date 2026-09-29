#!/usr/bin/env node

/**
 * Post-install script - optional skill setup
 */

console.log(`
Thanks for installing agent-skills-library!

Quick start:
  npx agent-skills list              # List all skills
  npx agent-skills install <name>    # Install a skill

Or use the API:
  const skills = require('agent-skills-library');
  skills.listSkills();
  skills.searchSkills('react');

Docs: https://ssrjkk.github.io/agent-skills/
`);
