/**
 * SkillHub — Lesson Catalog Data Module
 *
 * Defines the 8-lesson catalog for opcp-openstack-first-steps.
 * Shared via the window.SkillHub namespace (no build tools).
 */
(function () {
  'use strict';

  window.SkillHub = window.SkillHub || {};

  var LESSONS = [
    {
      id: 'intro',
      slug: 'index',
      titleEN: 'Introduction',
      titleFR: 'Introduction',
      difficulty: 'beginner',
      estimatedMinutes: 5,
      prerequisites: []
    },
    {
      id: 'prerequisites',
      slug: 'prerequisites',
      titleEN: 'Prerequisites',
      titleFR: 'Prérequis',
      difficulty: 'beginner',
      estimatedMinutes: 15,
      prerequisites: ['intro']
    },
    {
      id: 'first-steps',
      slug: 'first-steps',
      titleEN: 'First Steps',
      titleFR: 'Premiers pas',
      difficulty: 'beginner',
      estimatedMinutes: 20,
      prerequisites: ['prerequisites']
    },
    {
      id: 'user-management',
      slug: 'user-management',
      titleEN: 'User Management',
      titleFR: 'Gestion des utilisateurs',
      difficulty: 'beginner',
      estimatedMinutes: 20,
      prerequisites: ['first-steps']
    },
    {
      id: 'auth',
      slug: 'authentication',
      titleEN: 'Authentication',
      titleFR: 'Authentification',
      difficulty: 'beginner',
      estimatedMinutes: 15,
      prerequisites: ['user-management']
    },
    {
      id: 'network',
      slug: 'networking',
      titleEN: 'Networking',
      titleFR: 'Réseau',
      difficulty: 'intermediate',
      estimatedMinutes: 20,
      prerequisites: ['auth']
    },
    {
      id: 'storage',
      slug: 'storage',
      titleEN: 'Storage',
      titleFR: 'Stockage',
      difficulty: 'intermediate',
      estimatedMinutes: 20,
      prerequisites: ['network']
    },
    {
      id: 'compute',
      slug: 'compute',
      titleEN: 'Compute',
      titleFR: 'Calcul',
      difficulty: 'intermediate',
      estimatedMinutes: 25,
      prerequisites: ['storage']
    },
    {
      id: 'lacp',
      slug: 'lacp',
      titleEN: 'LACP Configuration',
      titleFR: 'Configuration LACP',
      difficulty: 'advanced',
      estimatedMinutes: 30,
      prerequisites: ['network']
    },
    {
      id: 'summary',
      slug: 'summary',
      titleEN: 'Summary & Next Steps',
      titleFR: 'Résumé & Prochaines étapes',
      difficulty: 'beginner',
      estimatedMinutes: 5,
      prerequisites: ['compute']
    },
    {
      id: 'cleanup',
      slug: 'cleanup',
      titleEN: 'Cleanup Resources',
      titleFR: 'Nettoyage des ressources',
      difficulty: 'beginner',
      estimatedMinutes: 10,
      prerequisites: ['summary']
    },
    {
      id: 'cheat-sheet',
      slug: 'cheat-sheet',
      titleEN: 'CLI & API Cheat Sheet',
      titleFR: 'Aide-mémoire CLI & API',
      difficulty: 'beginner',
      estimatedMinutes: 10,
      prerequisites: ['cleanup']
    }
  ];

  window.SkillHub.lessons = LESSONS;
})();
