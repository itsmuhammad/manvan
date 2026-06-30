const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const today = '2026-05-10';
const phone = '+971 50 826 8481';
const phoneCompact = '+971508268481';

const pages = [
  {
    file: 'house-shifting-abu-dhabi.html',
    title: 'House Shifting Services in Abu Dhabi | Man With Van',
    description: 'Book house shifting in Abu Dhabi with packing, furniture care and carefully handled movers. Call +971 50 826 8481 for a fast written quote from local experts today.',
    keyword: 'house shifting abu dhabi',
    h1: 'House Shifting Abu Dhabi',
    type: 'service',
    intro: 'House shifting in Abu Dhabi needs a mover who understands building access, villa communities, apartment towers and the pressure families feel on handover day.',
    audience: 'families moving between apartments, villas and townhouses across Abu Dhabi',
    areas: ['Khalifa City', 'Al Reem Island', 'Yas Island', 'Saadiyat Island', 'Mussafah'],
    related: ['villa-movers-abu-dhabi.html', 'packing-services-abu-dhabi.html', 'furniture-movers-abu-dhabi.html'],
    faq: [
      ['How much does house shifting cost in Abu Dhabi?', 'Most local house shifting jobs start from AED 700 for smaller homes and increase by property size, access, packing volume and distance. We confirm a written quote before moving day.'],
      ['Do you provide packing for house shifting?', 'Yes. We can provide boxes, wrap, blankets and labelled packing for rooms, fragile items and furniture.'],
      ['Can you move villas and apartments?', 'Yes. We handle apartment tower moves, villa moves and townhouse relocations across Abu Dhabi.'],
      ['Do you disassemble and reassemble furniture?', 'Yes. Beds, wardrobes, tables and modular furniture can be disassembled, protected, transported and reassembled.'],
      ['Can you help with urgent house shifting?', 'Yes, subject to crew availability. For urgent moves, WhatsApp us with both locations, date and inventory.']
    ]
  },
  {
    file: 'apartment-movers-abu-dhabi.html',
    title: 'Apartment Movers and Packers Abu Dhabi | Man With Van',
    description: 'Hire apartment movers in Abu Dhabi for tower moves, service lifts and careful packing. Call +971 50 826 8481 for a quick quote from local experts today.',
    keyword: 'apartment movers abu dhabi',
    h1: 'Apartment Movers Abu Dhabi',
    type: 'service',
    intro: 'Apartment movers in Abu Dhabi must work around service elevators, loading bays, security approvals, narrow corridors and strict move-in timings.',
    audience: 'tenants and owners moving studios, 1 BHK, 2 BHK and family apartments',
    areas: ['Al Reem Island', 'Corniche', 'Al Khalidiyah', 'Tourist Club Area', 'Al Raha Beach'],
    related: ['studio-movers-abu-dhabi.html', '1-bhk-movers-abu-dhabi.html', '2-bhk-movers-abu-dhabi.html'],
    faq: [
      ['Do you handle high-rise apartment moves?', 'Yes. We coordinate service lift timing, protect common areas and move furniture safely through corridors and loading bays.'],
      ['How early should I book apartment movers?', 'Book at least 3-7 days ahead when your building requires elevator approval. Same-day moves may be possible for smaller apartments.'],
      ['Can you move a studio apartment in one trip?', 'Often yes, depending on furniture volume, boxes and building access. We choose the right vehicle after reviewing your inventory.'],
      ['Do you protect lifts and corridors?', 'Yes. We use blankets and Careful handling practices to reduce scratches and building complaints.'],
      ['Can you pack fragile kitchen items?', 'Yes. We pack glassware, dishes, small appliances and fragile home items with protective material.']
    ]
  },
  {
    file: 'piano-movers-abu-dhabi.html',
    title: 'Piano Movers and Handlers Abu Dhabi | Man With Van',
    description: 'Need piano movers in Abu Dhabi? Get Careful handling, padding and planned access for upright pianos. Call +971 50 826 8481 for a careful quote today.',
    keyword: 'piano movers abu dhabi',
    h1: 'Piano Movers Abu Dhabi',
    type: 'service',
    intro: 'Piano movers in Abu Dhabi need planning, manpower and protective handling because one wrong angle can damage flooring, walls or the instrument finish.',
    audience: 'families, schools, studios and villas moving upright pianos and heavy musical items',
    areas: ['Khalifa City', 'Saadiyat Island', 'Yas Island', 'Al Bateen', 'Al Mushrif'],
    related: ['single-furniture-movers-abu-dhabi.html', 'villa-movers-abu-dhabi.html', 'furniture-movers-abu-dhabi.html'],
    faq: [
      ['Do you move all piano types?', 'We handle upright pianos and similar heavy musical items after access review. Grand pianos may require specialist equipment and a separate survey.'],
      ['Do you protect floors and walls?', 'Yes. We plan the route, use padding and move carefully around doorways, stairs and lift areas.'],
      ['Can you move a piano from a villa?', 'Yes. Villas are common piano move locations, especially where access through gates and stairs must be checked first.'],
      ['How do I prepare a piano for moving?', 'Clear the route, remove nearby furniture and share photos of stairs, lifts and entrances before quoting.'],
      ['Is piano moving carefully handled?', 'We review access, handling needs, and high-value instruments before booking.']
    ]
  },
  {
    file: 'single-furniture-movers-abu-dhabi.html',
    title: 'Single Furniture Movers in Abu Dhabi | Man With Van',
    description: 'Move one sofa, bed, table or wardrobe in Abu Dhabi with careful furniture movers. Call +971 50 826 8481 for a quick single-item quote from local experts.',
    keyword: 'single furniture movers abu dhabi',
    h1: 'Single Furniture Movers Abu Dhabi',
    type: 'service',
    intro: 'Single furniture movers in Abu Dhabi are useful when you do not need a full relocation but still need trained hands, the right vehicle and careful delivery.',
    audience: 'customers moving one sofa, wardrobe, bed, dining table, fridge or marketplace purchase',
    areas: ['Al Reem Island', 'Khalifa City', 'Mussafah', 'Al Raha', 'Baniyas'],
    related: ['furniture-movers-abu-dhabi.html', 'same-day-movers-abu-dhabi.html', 'packing-services-abu-dhabi.html'],
    faq: [
      ['Can you move just one item?', 'Yes. We move single sofas, wardrobes, beds, appliances, tables and marketplace purchases across Abu Dhabi.'],
      ['Can you collect furniture from a seller?', 'Yes. Share pickup and drop-off details, item photos and timing so we can quote accurately.'],
      ['Do you disassemble a wardrobe or bed?', 'Yes, if required for safe movement through doors, lifts or staircases.'],
      ['Can you do same-day single furniture delivery?', 'Often yes, depending on location and crew availability. WhatsApp us for the fastest slot.'],
      ['How is single furniture moving priced?', 'Pricing depends on item size, manpower, access, distance and whether disassembly or packing is neeservice.']
    ]
  },
  {
    file: 'appliances-movers-abu-dhabi.html',
    title: 'Appliance Movers and Packers Abu Dhabi | Man With Van',
    description: 'Move fridges, washing machines and appliances in Abu Dhabi with Careful handling. Call +971 50 826 8481 for a fast appliance moving quote from experts.',
    keyword: 'appliance movers abu dhabi',
    h1: 'Appliance Movers Abu Dhabi',
    type: 'service',
    intro: 'Appliance movers in Abu Dhabi help when refrigerators, washing machines, dryers and large home appliances need upright transport and Careful handling.',
    audience: 'residents moving bulky appliances between apartments, villas, storage units and second-hand purchases',
    areas: ['Khalifa City', 'Al Reem Island', 'Al Raha Beach', 'Mussafah', 'MBZ City'],
    related: ['single-furniture-movers-abu-dhabi.html', 'furniture-movers-abu-dhabi.html', 'house-shifting-abu-dhabi.html'],
    faq: [
      ['Do you move refrigerators in Abu Dhabi?', 'Yes. We move refrigerators with upright handling where possible and careful loading to reduce damage risk.'],
      ['Can you move washing machines?', 'Yes. Drain and disconnect the machine before collection, or confirm if you need handyman support.'],
      ['Do you install appliances?', 'We move appliances; connection and installation should be handled by a qualified technician where required.'],
      ['Can you collect appliances from a seller?', 'Yes. We can collect appliances from homes, stores or marketplace sellers when access is confirmed.'],
      ['How should I prepare appliances for moving?', 'Empty, clean and disconnect appliances before pickup. Secure loose shelves, hoses and accessories.']
    ]
  },
  {
    file: 'locations/movers-al-ain.html',
    title: 'Reliable Movers in Al Ain Abu Dhabi | Man With Van',
    description: 'Book movers in Al Ain for villas, apartments and Abu Dhabi relocations with carefully handled crews. Call +971 50 826 8481 for moving support today from experts.',
    keyword: 'movers al ain',
    h1: 'Movers in Al Ain Abu Dhabi',
    type: 'location',
    intro: 'Movers in Al Ain need to plan longer travel windows, villa access, family homes and intercity timing between Al Ain and Abu Dhabi.',
    audience: 'families, students and businesses moving within Al Ain or between Al Ain and Abu Dhabi',
    areas: ['Al Jimi', 'Al Muwaiji', 'Al Towayya', 'Al Ain Oasis', 'Abu Dhabi city'],
    related: ['house-shifting-abu-dhabi.html', 'villa-movers-abu-dhabi.html', 'movers-abu-dhabi-to-dubai.html'],
    faq: [
      ['Do you move homes in Al Ain?', 'Yes. We handle Al Ain villa, apartment and intercity moves with planned crew timing.'],
      ['Can you move from Al Ain to Abu Dhabi?', 'Yes. We plan the route, truck size and loading schedule for Al Ain to Abu Dhabi moves.'],
      ['Do you provide packing in Al Ain?', 'Yes. Packing can be included for fragile items, furniture and full homes.'],
      ['How much does an Al Ain move cost?', 'Pricing depends on distance, inventory, packing and access. Share both locations for a written quote.'],
      ['Can you move offices in Al Ain?', 'Yes. We can support small office moves, files, desks and equipment with prior planning.']
    ]
  },
  {
    file: 'locations/movers-al-ruwais-abu-dhabi.html',
    title: 'Reliable Movers in Al Ruwais Abu Dhabi | Man With Van',
    description: 'Moving to or from Al Ruwais Abu Dhabi? Book carefully handled long-distance movers with planned timing. Call +971 50 826 8481 for a clear quote today from experts.',
    keyword: 'movers al ruwais abu dhabi',
    h1: 'Movers in Al Ruwais Abu Dhabi',
    type: 'location',
    intro: 'Movers in Al Ruwais Abu Dhabi must plan distance, timing, fuel stops, loading access and family handover windows before the truck leaves.',
    audience: 'families and employees relocating between Al Ruwais, Abu Dhabi city and western region communities',
    areas: ['Al Ruwais', 'Madinat Zayed', 'Ghayathi', 'Abu Dhabi city', 'Mussafah'],
    related: ['movers-abu-dhabi-to-dubai.html', 'house-shifting-abu-dhabi.html', 'storage-abu-dhabi.html'],
    faq: [
      ['Do you move from Abu Dhabi to Al Ruwais?', 'Yes. We handle long-distance moves between Abu Dhabi and Al Ruwais with planned truck timing.'],
      ['Can you pack before an Al Ruwais move?', 'Yes. Packing can be scheduled before departure so loading is faster and safer.'],
      ['Do you move company accommodation?', 'Yes. We can support staff accommodation and family relocations when inventory is confirmed.'],
      ['How is Al Ruwais moving priced?', 'Pricing depends on distance, truck size, manpower, packing and whether storage is required.'],
      ['Can you do same-day Al Ruwais moves?', 'Some smaller moves may be possible, but long-distance moves should be booked early.']
    ]
  },
  {
    file: 'locations/movers-mohammed-bin-zayed-city.html',
    title: 'Movers in Mohammed Bin Zayed City Abu Dhabi | Man With Van',
    description: 'Book movers in Mohammed Bin Zayed City for villa and apartment relocation with packing. Call +971 50 826 8481 for an carefully handled moving quote today now.',
    keyword: 'movers mohammed bin zayed city',
    h1: 'Movers in Mohammed Bin Zayed City',
    type: 'location',
    intro: 'Movers in Mohammed Bin Zayed City handle family villas, townhouse communities, apartment blocks and moves toward Mussafah, Khalifa City and Abu Dhabi island.',
    audience: 'families moving in MBZ City villas, staff accommodation and nearby apartment buildings',
    areas: ['MBZ City', 'Mussafah', 'Khalifa City', 'Baniyas', 'Shakhbout City'],
    related: ['villa-movers-abu-dhabi.html', 'house-shifting-abu-dhabi.html', 'packing-services-abu-dhabi.html'],
    faq: [
      ['Do you move villas in Mohammed Bin Zayed City?', 'Yes. MBZ City villa moves are common for our team, including packing, furniture protection and reassembly.'],
      ['Can you move from MBZ City to Abu Dhabi island?', 'Yes. We plan truck timing and routes between MBZ City, Mussafah, Khalifa City and Abu Dhabi island.'],
      ['Do you provide packing materials?', 'Yes. Boxes, wrap, blankets and labels can be included in your moving quote.'],
      ['Can you move staff accommodation?', 'Yes. We can move rooms, shared accommodation and small company housing when inventory is clear.'],
      ['How early should I book MBZ City movers?', 'Book several days ahead for villas or full homes. Same-day moves may be possible for smaller jobs.']
    ]
  }
];

function esc(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function urlFor(file) {
  return `https://manwithvan.ae/${file.replace(/\\/g, '/')}`;
}

function linkTo(file, label) {
  const prefix = file.startsWith('locations/') ? '../' : '';
  return `<a href="${prefix}${label.href}">${esc(label.text)}</a>`;
}

function pageHtml(page) {
  const canonical = urlFor(page.file);
  const depth = page.file.startsWith('locations/') ? '../' : '';
  const relatedLinks = page.related.map(href => ({ href, text: href.replace(/\.html$/, '').replace(/\//g, ' ').replace(/-/g, ' ') }));
  const areaList = page.areas.map(a => `<li>${esc(a)} moves with route and access planning</li>`).join('\n              ');
  const faqHtml = page.faq.map(([q, a]) => `<div class="post-faq-item">\n                <h3>${esc(q)}</h3>\n                <p>${esc(a)}</p>\n              </div>`).join('\n              ');
  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: page.faq.map(([q, a]) => ({
      '@type': 'Question',
      name: q,
      acceptedAnswer: {'@type': 'Answer', text: a}
    }))
  };
  const serviceSchema = {
    '@context': 'https://schema.org',
    '@type': page.type === 'location' ? ['MovingCompany', 'LocalBusiness'] : ['Service', 'MovingCompany', 'LocalBusiness'],
    name: page.h1,
    serviceType: page.keyword,
    description: page.description,
    url: canonical,
    telephone: phoneCompact,
    priceRange: 'AED 300 - AED 5000',
    openingHours: 'Mo-Su 07:00-21:00',
    image: 'https://manwithvan.ae/images/logo/logo.png',
    address: {'@type': 'PostalAddress', addressLocality: 'Abu Dhabi', addressRegion: 'Abu Dhabi', addressCountry: 'AE'},
    areaServed: ['Abu Dhabi', ...page.areas]
  };
  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {'@type': 'ListItem', position: 1, name: 'Home', item: 'https://manwithvan.ae/'},
      {'@type': 'ListItem', position: 2, name: page.type === 'location' ? 'Locations' : 'Services', item: page.type === 'location' ? 'https://manwithvan.ae/locations/' : 'https://manwithvan.ae/services.html'},
      {'@type': 'ListItem', position: 3, name: page.h1, item: canonical}
    ]
  };
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- SEO target keyword: ${esc(page.keyword)} -->
  <title>${esc(page.title)}</title>
  <meta name="description" content="${esc(page.description)}">
  <meta name="keywords" content="${esc(page.keyword)}, movers abu dhabi, man with van abu dhabi, moving company abu dhabi">
  <link rel="icon" type="image/x-icon" href="${depth}images/logo/favicon.ico">
  <link rel="canonical" href="${canonical}">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
  <link rel="stylesheet" href="${depth}css/styles.css">
  <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"></noscript>
  <script type="application/ld+json">${JSON.stringify(serviceSchema)}</script>
  <script type="application/ld+json">${JSON.stringify(faqSchema)}</script>
  <script type="application/ld+json">${JSON.stringify(breadcrumbSchema)}</script>
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Man With Van - Movers Abu Dhabi">
  <meta property="og:url" content="${canonical}">
  <meta property="og:title" content="${esc(page.title)}">
  <meta property="og:description" content="${esc(page.description)}">
  <meta property="og:image" content="https://manwithvan.ae/images/logo/logo.png">
</head>
<body class="page-with-fixed-header">
  <div id="topbar"></div>
  <div id="header"></div>
  <main>
    <section class="hero-section">
      <div class="hero-bg"></div>
      <div class="container">
        <div class="hero-content">
          <div class="hero-text">
            <h1>${esc(page.h1)}</h1>
            <p>${esc(page.intro)} We help ${esc(page.audience)} with clear pricing, careful packing and responsive WhatsApp support.</p>
            <div class="hero-buttons" style="margin-top:1.25rem;display:flex;flex-wrap:wrap;gap:.75rem;">
              <a href="${depth}get-free-quote.html" class="btn btn-secondary btn-lg">Get Free Quote</a>
              <a href="https://wa.me/971508268481?text=Hi%2C%20I%20need%20${encodeURIComponent(page.keyword)}." class="btn btn-lg" style="background:#25D366;color:#fff;border:none;" target="_blank" rel="noopener noreferrer">WhatsApp ${phone}</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Local ${esc(page.keyword)} support built for Abu Dhabi</h2>
        <p>Abu Dhabi moves are rarely simple copy-and-paste jobs. Towers may require service lift bookings, villas may have gate and driveway limits, and communities often need security approval before a truck can load. Man With Van plans these details before the crew arrives, so moving day is calmer and faster.</p>
        <p>Our team focuses on practical coordination: inventory review, route planning, packing priorities, loading sequence and handover timing. For ${esc(page.audience)}, that means fewer surprises and better control over cost, timing and building requirements.</p>
        <p>We serve ${esc(page.areas.join(', '))} and nearby Abu Dhabi communities. If your move crosses areas, we plan the truck route and crew timing around traffic, building access and your preferred arrival window.</p>
      </div>
    </section>

    <section class="section" style="background:#f8fafc;">
      <div class="container">
        <h2>What is included</h2>
        <p>Every job starts with a practical quote. Share photos, inventory, both locations and access notes over WhatsApp. We confirm the right vehicle, crew size and packing level before you approve the booking.</p>
        <ul>
          <li>Careful loading, transport and unloading by trained Abu Dhabi movers</li>
          <li>Furniture blankets, wrap and room-by-room handling notes where neeservice</li>
          <li>Optional packing support for fragile, bulky or high-priority items</li>
          <li>Disassembly and reassembly guidance for beds, tables, wardrobes and similar items</li>
          <li>Clear communication by phone or WhatsApp before and during the move</li>
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Areas and access planning</h2>
        <p>Good movers do more than arrive with a truck. We check whether the route needs a compact vehicle, whether the building needs a loading permit, and whether fragile or heavy items should be loaded first or last. This is especially important in Abu Dhabi towers, villa communities and long-distance moves.</p>
        <ul>
          ${areaList}
        </ul>
        <p>For related services, see ${relatedLinks.map(l => linkTo(page.file, l)).join(', ')}. These internal links help you compare the right service before booking and give Google clearer context about our Abu Dhabi moving coverage.</p>
        <p>Before quoting, we ask for practical details competitors often miss: building name, floor, lift access, parking distance, fragile pieces, bulky items and whether your move needs after-hours timing. These details help us avoid underquoting, delays and last-minute crew changes. The result is a calmer move with clearer expectations from the first message.</p>
      </div>
    </section>

    <section class="section" style="background:#f8fafc;">
      <div class="container">
        <h2>Why Man With Van</h2>
        <p>Competitors often sell generic UAE moving pages. This page is written for Abu Dhabi customers who need local timing, building access awareness and straightforward quotes. We keep communication simple: send the details, get a response, confirm the slot and know what is included.</p>
        <p>Our advantage is local focus. We know the difference between a quick apartment transfer, a villa handover, a single-item delivery and a long-distance move to another Abu Dhabi region. That focus lets us quote realistically and assign the right crew.</p>
        <aside class="post-cta-minimal" aria-label="Get a quote">
          <h2>Need a mover in Abu Dhabi?</h2>
          <p>WhatsApp ${phone} with pickup, drop-off, date and photos for a fast quote.</p>
          <div class="post-cta-actions">
            <a href="${depth}get-free-quote.html" class="btn-cta-primary">Get free quote</a>
            <a href="tel:${phoneCompact}" class="btn-cta-outline">Call ${phone}</a>
          </div>
        </aside>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <h2>Frequently asked questions</h2>
        <div class="post-faq-list">
          ${faqHtml}
        </div>
      </div>
    </section>
  </main>
  <div id="footer"></div>
  <div id="wa-chat-widget"></div>
  <div id="scroll-to-top"></div>
  <script src="${depth}js/component-loader.js" defer></script>
  <script src="${depth}js/nav-drawer.js" defer></script>
  <script src="${depth}js/wa-chat-widget.js" defer></script>
  <script src="${depth}js/main.js" defer></script>
</body>
</html>
`;
}

for (const page of pages) {
  const target = path.join(root, page.file);
  fs.mkdirSync(path.dirname(target), {recursive: true});
  fs.writeFileSync(target, pageHtml(page), 'utf8');
}

const sitemapPath = path.join(root, 'sitemap.xml');
let sitemap = fs.readFileSync(sitemapPath, 'utf8');
for (const page of pages) {
  const loc = urlFor(page.file);
  if (!sitemap.includes(`<loc>${loc}</loc>`)) {
    sitemap = sitemap.replace('</urlset>', `  <url><loc>${loc}</loc><lastmod>${today}</lastmod><changefreq>monthly</changefreq><priority>${page.type === 'location' ? '0.72' : '0.82'}</priority></url>\n</urlset>`);
  }
}
fs.writeFileSync(sitemapPath, sitemap, 'utf8');

const htaccessPath = path.join(root, '.htaccess');
let htaccess = fs.readFileSync(htaccessPath, 'utf8');
const rules = [
  'RewriteRule ^apartment-movers-abu-dhabi/?$ apartment-movers-abu-dhabi.html [L]',
  'RewriteRule ^house-shifting-abu-dhabi/?$ house-shifting-abu-dhabi.html [L]',
  'RewriteRule ^piano-movers-abu-dhabi/?$ piano-movers-abu-dhabi.html [L]',
  'RewriteRule ^single-furniture-movers-abu-dhabi/?$ single-furniture-movers-abu-dhabi.html [L]',
  'RewriteRule ^appliances-movers-abu-dhabi/?$ appliances-movers-abu-dhabi.html [L]',
  'RewriteRule ^locations/movers-al-ain/?$ locations/movers-al-ain.html [L]',
  'RewriteRule ^locations/movers-al-ruwais-abu-dhabi/?$ locations/movers-al-ruwais-abu-dhabi.html [L]',
  'RewriteRule ^locations/movers-mohammed-bin-zayed-city/?$ locations/movers-mohammed-bin-zayed-city.html [L]'
];
for (const rule of rules) {
  if (!htaccess.includes(rule)) {
    htaccess = htaccess.replace('</IfModule>', `${rule}\n</IfModule>`);
  }
}
fs.writeFileSync(htaccessPath, htaccess, 'utf8');

const logPath = path.join(root, 'action_log.txt');
const logLines = pages.map(page => `${today} - [DONE] ${page.file} — created 700+ word ${page.type} page targeting "${page.keyword}" with canonical, LocalBusiness/Service, FAQ and Breadcrumb schema.`);
fs.appendFileSync(logPath, `\n${logLines.join('\n')}\n${today} - [DONE] sitemap.xml and .htaccess — adservice new page URLs and clean URL rewrite rules for the new SEO gap pages.\n`, 'utf8');

console.log(JSON.stringify({created: pages.map(p => p.file)}, null, 2));
