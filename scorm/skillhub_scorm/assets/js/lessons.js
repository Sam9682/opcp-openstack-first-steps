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
      id: 'prerequisites',
      slug: 'prerequisites',
      titleEN: 'Prerequisites',
      titleFR: 'Prérequis',
      difficulty: 'beginner',
      estimatedMinutes: 15,
      prerequisites: []
    },
    {
      id: 'intro',
      slug: 'index',
      titleEN: 'Introduction',
      titleFR: 'Introduction',
      difficulty: 'beginner',
      estimatedMinutes: 5,
      prerequisites: ['prerequisites']
    },
    {
      id: 'core-concepts',
      slug: 'core-concepts',
      titleEN: 'Core Concepts',
      titleFR: 'Concepts Fondamentaux',
      difficulty: 'beginner',
      estimatedMinutes: 15,
      prerequisites: ['intro']
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
      id: 'network',
      slug: 'networking',
      titleEN: 'Networking',
      titleFR: 'Réseau',
      difficulty: 'intermediate',
      estimatedMinutes: 20,
      prerequisites: ['user-management']
    },
    {
      id: 'compute',
      slug: 'compute',
      titleEN: 'Compute',
      titleFR: 'Compute',
      difficulty: 'intermediate',
      estimatedMinutes: 25,
      prerequisites: ['network']
    },
    {
      id: 'summary',
      slug: 'summary',
      titleEN: 'Summary & Next Steps',
      titleFR: 'Résumé & Prochaines étapes',
      difficulty: 'beginner',
      estimatedMinutes: 5,
      prerequisites: ['network']
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
    },
    {
      id: 'first-steps',
      slug: 'appendix',
      titleEN: 'Appendix A - Accessing OpenStack',
      titleFR: 'Annexe A - Accès à OpenStack',
      difficulty: 'beginner',
      estimatedMinutes: 20,
      prerequisites: ['core-concepts']
    },
    {
      id: 'trunk-setup',
      slug: 'appendix-trunk-setup',
      titleEN: 'Appendix - Setup Neutron Trunk',
      titleFR: 'Annexe - Configuration des ports Trunk Neutron',
      difficulty: 'advanced',
      estimatedMinutes: 30,
      prerequisites: ['network']
    },
    {
      id: 'storage',
      slug: 'software-raid',
      titleEN: 'Appendix - Software RAID',
      titleFR: 'Annexe - RAID Logiciel',
      difficulty: 'advanced',
      estimatedMinutes: 25,
      prerequisites: ['network']
    },
    {
      id: 'lacp',
      slug: 'lacp',
      titleEN: 'Appendix - LACP Configuration',
      titleFR: 'Annexe - Configuration LACP',
      difficulty: 'advanced',
      estimatedMinutes: 30,
      prerequisites: ['network']
    },
    {
      id: 'glossary',
      slug: 'glossary',
      titleEN: 'Glossary',
      titleFR: 'Glossaire',
      estimatedMinutes: 10,
      prerequisites: []
    }
  ];

  window.SkillHub.lessons = LESSONS;
})();