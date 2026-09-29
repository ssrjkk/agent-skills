/**
 * agent-skills-library - Node.js API
 */

const fs = require('fs');
const path = require('path');

const CATALOG_PATH = path.join(__dirname, 'skills_catalog.json');

let catalogCache = null;

function getCatalog() {
  if (!catalogCache) {
    catalogCache = JSON.parse(fs.readFileSync(CATALOG_PATH, 'utf8'));
  }
  return catalogCache;
}

function listSkills() {
  return getCatalog().skills;
}

function getSkill(name) {
  return getCatalog().skills.find(s => s.name === name);
}

function searchSkills(query) {
  const q = query.toLowerCase();
  return getCatalog().skills.filter(skill =>
    skill.name.toLowerCase().includes(q) ||
    skill.description.toLowerCase().includes(q) ||
    skill.tags.some(tag => tag.toLowerCase().includes(q))
  );
}

function getSkillsByDomain(domain) {
  return getCatalog().skills.filter(s => s.category === domain);
}

function getDomains() {
  return getCatalog().metadata.domains;
}

function getStats() {
  const meta = getCatalog().metadata;
  return {
    totalSkills: meta.total_skills,
    totalRu: meta.total_ru,
    domains: meta.domains.length,
    schemaVersion: meta.schema_version,
  };
}

module.exports = {
  listSkills,
  getSkill,
  searchSkills,
  getSkillsByDomain,
  getDomains,
  getStats,
};
