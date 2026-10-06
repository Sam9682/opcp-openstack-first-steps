/**
 * SkillHub — Lesson Catalog Data Module
 *
 * Defines the lesson catalog used by navigation.js and main.js.
 * The catalog is project-specific: update the LESSONS array below when pages
 * are added, removed, or reordered.
 *
 * Each entry: { id, slug, titleEN, titleFR, difficulty, estimatedMinutes, prerequisites }
 *   - slug must match the HTML filename without extension (e.g. "networking" → networking.html).
 *   - The special slug "index" maps to the locale landing page (en/index.html, fr/index.html).
 *
 * Shared via the window.SkillHub namespace (no build tools).
 */
(function () {
  'use strict';

  /* Ensure namespace exists */
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
      estimatedMinutes: 10,
      prerequisites: ['intro']
    },
    {
      id: 'core-concepts',
      slug: 'core-concepts',
      titleEN: 'Core Concepts',
      titleFR: 'Concepts Fondamentaux',
      difficulty: 'beginner',
      estimatedMinutes: 15,
      prerequisites: ['prerequisites']
    },
    {
      id: 'user-management',
      slug: 'user-management',
      titleEN: 'User Management',
      titleFR: 'Gestion des utilisateurs',
      difficulty: 'beginner',
      estimatedMinutes: 20,
      prerequisites: ['core-concepts']
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
      id: 'networking',
      slug: 'networking',
      titleEN: 'Networking',
      titleFR: 'Réseau',
      difficulty: 'intermediate',
      estimatedMinutes: 20,
      prerequisites: ['auth']
    },
    {
      id: 'compute',
      slug: 'compute',
      titleEN: 'Compute',
      titleFR: 'Compute',
      difficulty: 'intermediate',
      estimatedMinutes: 25,
      prerequisites: ['networking']
    },
    {
      id: 'lacp',
      slug: 'lacp',
      titleEN: 'LACP Configuration',
      titleFR: 'Configuration LACP',
      difficulty: 'advanced',
      estimatedMinutes: 25,
      prerequisites: ['networking']
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
      id: 'appendix',
      slug: 'appendix',
      titleEN: 'Appendix — Accessing OpenStack',
      titleFR: 'Annexe — Accès à OpenStack',
      difficulty: 'beginner',
      estimatedMinutes: 10,
      prerequisites: []
    },
    {
      id: 'appendix-trunk-setup',
      slug: 'appendix-trunk-setup',
      titleEN: 'Appendix — Neutron Trunk Setup',
      titleFR: 'Configuration des ports Trunk Neutron',
      difficulty: 'advanced',
      estimatedMinutes: 20,
      prerequisites: ['networking']
    },
    {
      id: 'software-raid',
      slug: 'software-raid',
      titleEN: 'Appendix — Software RAID',
      titleFR: 'Configuration RAID Logiciel',
      difficulty: 'intermediate',
      estimatedMinutes: 20,
      prerequisites: ['compute']
    },
    {
      id: 'cheat-sheet',
      slug: 'cheat-sheet',
      titleEN: 'CLI & API Cheat Sheet',
      titleFR: 'Aide-mémoire CLI & API',
      difficulty: 'beginner',
      estimatedMinutes: 10,
      prerequisites: []
    },
    {
      id: 'glossary',
      slug: 'glossary',
      titleEN: 'Glossary',
      titleFR: 'Glossaire',
      difficulty: 'beginner',
      estimatedMinutes: 10,
      prerequisites: []
    }
  ];

  /* Expose on namespace */
  window.SkillHub.lessons = LESSONS;
})();
