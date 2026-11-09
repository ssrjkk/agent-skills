'use strict';
// Smoke test: the shipped catalog must load and look sane.
const test = require('node:test');
const assert = require('node:assert');
const lib = require('..');

test('catalog loads', () => {
  const skills = lib.listSkills();
  assert.ok(Array.isArray(skills) && skills.length >= 100, `expected 100+ skills, got ${skills.length}`);
});

test('stats shape', () => {
  const st = lib.getStats();
  assert.ok(st.totalSkills >= 100);
  assert.ok(Array.isArray(st.domains) ? true : st.domains >= 1);
});

test('search finds a known skill', () => {
  assert.ok(lib.searchSkills('fastapi').length >= 1);
});
