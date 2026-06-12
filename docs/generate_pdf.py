
#!/usr/bin/env python3
"""Generate a marketing-style PDF from the OPCP OpenStack First Steps content."""

from weasyprint import HTML

html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
@page {
    size: A4;
    margin: 0;
}

body {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    margin: 0;
    padding: 0;
    color: #2c3e50;
    line-height: 1.6;
}

/* Cover Page */
.cover {
    height: 297mm;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: white;
    padding: 60px;
    page-break-after: always;
}

.cover h1 {
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 20px;
    letter-spacing: -0.5px;
}

.cover .subtitle {
    font-size: 22px;
    font-weight: 300;
    opacity: 0.9;
    margin-bottom: 40px;
}

.cover .tagline {
    font-size: 16px;
    font-weight: 300;
    opacity: 0.7;
    border-top: 1px solid rgba(255,255,255,0.3);
    padding-top: 30px;
    margin-top: 40px;
}

.cover .brand {
    font-size: 18px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 60px;
    opacity: 0.8;
}

/* Content Pages */
.page {
    padding: 50px 60px;
    page-break-after: always;
}

.page:last-child {
    page-break-after: avoid;
}

h2 {
    font-size: 28px;
    color: #0f3460;
    font-weight: 700;
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 3px solid #e94560;
}

h3 {
    font-size: 20px;
    color: #16213e;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 15px;
}

p {
    font-size: 14px;
    margin-bottom: 15px;
    color: #444;
}

.intro-text {
    font-size: 16px;
    color: #555;
    line-height: 1.8;
    margin-bottom: 30px;
}

/* Feature Cards */
.features {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin: 30px 0;
}

.feature-card {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 25px;
    width: 45%;
    border-left: 4px solid #e94560;
}

.feature-card h4 {
    font-size: 16px;
    color: #0f3460;
    margin: 0 0 10px 0;
    font-weight: 600;
}

.feature-card p {
    font-size: 13px;
    color: #666;
    margin: 0;
}

/* Benefits List */
.benefits {
    list-style: none;
    padding: 0;
}

.benefits li {
    font-size: 15px;
    padding: 12px 0 12px 35px;
    position: relative;
    border-bottom: 1px solid #eee;
}

.benefits li::before {
    content: "✓";
    position: absolute;
    left: 0;
    color: #e94560;
    font-weight: 700;
    font-size: 18px;
}

/* Timeline */
.timeline {
    margin: 30px 0;
}

.timeline-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 20px;
}

.timeline-badge {
    background: #0f3460;
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
    margin-right: 20px;
    flex-shrink: 0;
}

.timeline-content {
    flex: 1;
}

.timeline-content h4 {
    margin: 0 0 5px 0;
    font-size: 16px;
    color: #16213e;
}

.timeline-content p {
    margin: 0;
    font-size: 13px;
    color: #666;
}

/* Modules Grid */
.modules-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin: 25px 0;
}

.module-card {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    border-radius: 10px;
    padding: 20px;
    width: 44%;
    text-align: center;
}

.module-card .module-number {
    background: #e94560;
    color: white;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 10px;
}

.module-card h4 {
    font-size: 15px;
    color: #0f3460;
    margin: 8px 0;
}

.module-card p {
    font-size: 12px;
    color: #666;
    margin: 0;
}

/* CTA Section */
.cta {
    background: linear-gradient(135deg, #0f3460, #16213e);
    border-radius: 15px;
    padding: 40px;
    text-align: center;
    color: white;
    margin-top: 40px;
}

.cta h3 {
    color: white;
    font-size: 24px;
    margin: 0 0 15px 0;
}

.cta p {
    color: rgba(255,255,255,0.8);
    font-size: 15px;
    margin-bottom: 25px;
}

.cta .contact {
    font-size: 18px;
    font-weight: 600;
    color: #e94560;
}

/* Highlight Box */
.highlight-box {
    background: linear-gradient(135deg, #fff3f5, #ffeef0);
    border: 1px solid #e94560;
    border-radius: 12px;
    padding: 25px;
    margin: 25px 0;
}

.highlight-box h4 {
    color: #e94560;
    margin: 0 0 10px 0;
    font-size: 16px;
}

/* Environment section */
.env-cards {
    display: flex;
    gap: 20px;
    margin: 25px 0;
}

.env-card {
    flex: 1;
    background: white;
    border: 2px solid #e9ecef;
    border-radius: 12px;
    padding: 25px;
    text-align: center;
}

.env-card h4 {
    color: #0f3460;
    font-size: 16px;
    margin: 0 0 15px 0;
}

.env-card ul {
    text-align: left;
    padding-left: 20px;
    font-size: 13px;
    color: #666;
}

.env-card ul li {
    margin-bottom: 8px;
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    font-size: 11px;
    color: #999;
    margin-top: 40px;
}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover">
    <h1>OPCP OpenStack<br>First Steps</h1>
    <div class="subtitle">Votre parcours de découverte<br>de l'infrastructure Cloud</div>
    <div class="tagline">Une journée pour maîtriser les fondamentaux d'OpenStack<br>dans un environnement sécurisé et accompagné</div>
    <div class="brand">PSMC OVHcloud</div>
</div>

<!-- PAGE 2: INTRODUCTION & VALUE PROPOSITION -->
<div class="page">
    <h2>Accélérez votre montée en compétences Cloud</h2>
    <p class="intro-text">
        Découvrez les fondamentaux de l'infrastructure Cloud OPCP OpenStack chez OVHcloud.
        Notre programme immersif vous permet de pratiquer dans un environnement réel,
        sécurisé et accompagné — de la théorie à la maîtrise opérationnelle en une seule journée.
    </p>

    <h3>Ce que vous allez accomplir</h3>
    <ul class="benefits">
        <li>Maîtriser les concepts fondamentaux d'OpenStack et son écosystème</li>
        <li>Créer et gérer des instances, réseaux et volumes en toute autonomie</li>
        <li>Pratiquer sur un environnement Cloud réel avec des exercices guidés</li>
        <li>Appliquer les bonnes pratiques d'authentification et de sécurité</li>
    </ul>

    <div class="highlight-box">
        <h4>⏱ Format optimisé : 1 journée</h4>
        <p style="margin:0; font-size: 14px; color: #555;">
            Un programme intensif mais progressif, conçu pour vous rendre opérationnel
            rapidement sans sacrifier la compréhension des fondamentaux.
        </p>
    </div>
</div>

<!-- PAGE 3: PROGRAMME & TIMELINE -->
<div class="page">
    <h2>Un parcours structuré et progressif</h2>

    <div class="timeline">
        <div class="timeline-item">
            <div class="timeline-badge">1</div>
            <div class="timeline-content">
                <h4>Introduction et Prérequis — ~1h</h4>
                <p>Mise en place de votre environnement, présentation de l'architecture OpenStack et des concepts clés.</p>
            </div>
        </div>
        <div class="timeline-item">
            <div class="timeline-badge">2</div>
            <div class="timeline-content">
                <h4>Concepts Fondamentaux — ~1h</h4>
                <p>Découverte des services principaux : Compute (Nova), Réseau (Neutron), Stockage (Cinder) et authentification.</p>
            </div>
        </div>
        <div class="timeline-item">
            <div class="timeline-badge">3</div>
            <div class="timeline-content">
                <h4>Exercices Pratiques — ~2 à 3h</h4>
                <p>Mise en pratique sur un environnement réel : création d'instances, configuration réseau, gestion du stockage.</p>
            </div>
        </div>
        <div class="timeline-item">
            <div class="timeline-badge">4</div>
            <div class="timeline-content">
                <h4>Résumé et Prochaines Étapes — ~1h</h4>
                <p>Bilan des acquis, conseils pour la suite et ressources complémentaires.</p>
            </div>
        </div>
    </div>

    <h3>Votre environnement de formation</h3>
    <div class="env-cards">
        <div class="env-card">
            <h4>🌐 SkillHub</h4>
            <ul>
                <li>Interface web interactive</li>
                <li>Contenu multilingue (FR/EN)</li>
                <li>Modules pédagogiques structurés</li>
                <li>Validation des connaissances</li>
            </ul>
        </div>
        <div class="env-card">
            <h4>🔬 Labs</h4>
            <ul>
                <li>Environnement OpenStack réel</li>
                <li>Exercices avec validation auto</li>
                <li>Gestion sécurisée des ressources</li>
                <li>Option Docker disponible</li>
            </ul>
        </div>
    </div>
</div>

<!-- PAGE 4: MODULES -->
<div class="page">
    <h2>5 modules pour une maîtrise complète</h2>
    <p class="intro-text">Chaque module est conçu pour vous faire progresser étape par étape, de la création de votre première instance à la configuration réseau avancée.</p>

    <div class="modules-grid">
        <div class="module-card">
            <div class="module-number">1</div>
            <h4>Premiers Pas</h4>
            <p>Création d'instances, configuration réseau de base, volumes</p>
        </div>
        <div class="module-card">
            <div class="module-number">2</div>
            <h4>Compute (Nova)</h4>
            <p>Lancement, redimensionnement et snapshots d'instances</p>
        </div>
        <div class="module-card">
            <div class="module-number">3</div>
            <h4>Réseau (Neutron)</h4>
            <p>Réseaux, sous-réseaux et routeurs</p>
        </div>
        <div class="module-card">
            <div class="module-number">4</div>
            <h4>Stockage (Cinder)</h4>
            <p>Création, attachement et gestion de volumes</p>
        </div>
        <div class="module-card">
            <div class="module-number">5</div>
            <h4>Configuration LACP</h4>
            <p>Agrégation de liens et bonds réseau</p>
        </div>
    </div>

    <h3>À qui s'adresse ce programme ?</h3>
    <div class="features">
        <div class="feature-card">
            <h4>👨‍💻 Administrateurs Système</h4>
            <p>Vous gérez déjà des infrastructures et souhaitez ajouter OpenStack à vos compétences.</p>
        </div>
        <div class="feature-card">
            <h4>🚀 Développeurs & Ingénieurs IT</h4>
            <p>Vous voulez comprendre l'infrastructure cloud qui héberge vos applications.</p>
        </div>
        <div class="feature-card">
            <h4>📊 Professionnels IT</h4>
            <p>Vous souhaitez maîtriser les bases de l'architecture cloud moderne.</p>
        </div>
    </div>
</div>

<!-- PAGE 5: RESULTS & CTA -->
<div class="page">
    <h2>Vos acquis à l'issue de la formation</h2>

    <ul class="benefits">
        <li>Compréhension des services OpenStack principaux et de leur interaction</li>
        <li>Autonomie dans la création et la gestion de ressources cloud</li>
        <li>Maîtrise des concepts d'authentification et de sécurité</li>
        <li>Exercices validés et documentés comme référence pratique</li>
        <li>Bases solides pour aller plus loin avec OpenStack</li>
    </ul>

    <div class="highlight-box">
        <h4>🎯 Prérequis simples</h4>
        <p style="margin:0; font-size: 14px; color: #555;">
            Connaissance de base du cloud computing, capacité à utiliser un terminal,
            et familiarité avec les outils de développement. Nous fournissons tout le reste.
        </p>
    </div>

    <div class="cta">
        <h3>Prêt à démarrer ?</h3>
        <p>Contactez notre équipe pour planifier votre session de découverte OpenStack.</p>
        <div class="contact">psmc@ovhcloud.com</div>
    </div>

    <div class="footer">
        <p>© PSMC OVHcloud — Programme OPCP OpenStack First Steps</p>
    </div>
</div>

</body>
</html>
"""

output_path = "/home/slepetre/workspace/github/opcp-openstack-first-steps/docs/OPCP-OpenStack-First-Steps-Marketing.pdf"
HTML(string=html_content).write_pdf(output_path)
print(f"PDF generated: {output_path}")
