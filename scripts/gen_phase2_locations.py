# Generate Phase 2 location pages — run: python scripts/gen_phase2_locations.py
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "locations"

SVGS = [
    """<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>""",
    """<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>""",
    """<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>""",
    """<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>""",
    """<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>""",
    """<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"/></svg>""",
]


def services_grid(spans):
    lines = []
    for i, text in enumerate(spans):
        lines.append(f"""        <div class="location-service-item">
          <div class="location-service-icon">{SVGS[i]}</div>
          <span>{text}</span>
        </div>""")
    return "\n".join(lines)


def render(p):
    slug = p["slug"]
    canonical = f"https://manwithvan.ae/locations/{slug}.html"
    esc = html.escape
    faq_entities = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faqs"]]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_entities}, separators=(",", ":"))
    mc = {
        "@context": "https://schema.org",
        "@type": "MovingCompany",
        "name": "Man With Van",
        "description": f"Professional movers and packers in {p['area_served']}",
        "url": "https://manwithvan.ae",
        "telephone": "+971508268481",
        "priceRange": "AED 300 – AED 2500",
        "openingHours": "Mo-Su 08:00-17:00",
        "image": "https://manwithvan.ae/images/logo/logo.png",
        "address": {"@type": "PostalAddress", "addressLocality": "Abu Dhabi", "addressRegion": "Abu Dhabi", "addressCountry": "AE"},
        "areaServed": p["area_served"],
    }
    mc_ld = json.dumps(mc, separators=(",", ":"))
    faq_html = "".join(f"        <h3>{q}</h3>\n        <p>{a}</p>\n" for q, a in p["faqs"])
    nearby = ", ".join(f'<a href="{h}">{label}</a>' for h, label in p["nearby"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(p["title"])}</title>
  <meta name="description" content="{esc(p["desc"])}">
  <meta name="keywords" content="{esc(p["keywords"])}">
  <link rel="icon" type="image/x-icon" href="/images/logo/favicon.ico">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="/css/styles.css">
  <link rel="preload" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"></noscript>
  <script type="application/ld+json">
  {mc_ld}
  </script>
  <script type="application/ld+json">
  {faq_ld}
  </script>
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Man With Van - Movers Abu Dhabi">
  <meta property="og:image" content="https://manwithvan.ae/images/blog/heroes/5-essential-tips-stress-free-house-move-uae.webp">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{esc(p["title"])}">
  <meta property="og:description" content="{esc(p["desc"])}">
</head>
<body class="page-with-fixed-header location-page">
  <div id="topbar"></div>
  <div id="header"></div>

  <section class="location-hero">
    <div class="container">
      <div class="location-hero-content">
        <h1>{p["h1"]}</h1>
        <p class="hero-subtitle">{p["subtitle"]}</p>
        <div class="hero-buttons">
          <a href="/get-free-quote.html" class="btn btn-secondary btn-lg">Get Free Quote</a>
          <a href="tel:+971508268481" class="btn btn-outline btn-lg" style="border-color: white; color: white;">Call +971 50 826 8481</a>
        </div>
      </div>
    </div>
  </section>

  <section class="location-content">
    <div class="container">
      <div class="content-intro">
        <h2>{p["intro_h2"]}</h2>
        <p>{p["intro_p1"]}</p>
        <p>{p["intro_p2"]}</p>
      </div>

      <h2>Moving Services We Offer in {p["services_h2"]}</h2>
      <div class="location-services-grid">
{services_grid(p["spans"])}
      </div>

      <div class="location-faq">
        <h2>Frequently Asked Questions</h2>
{faq_html}
      </div>

      <div class="location-cta">
        <p style="margin-bottom: 0; font-weight: 600; font-size: 1.125rem;"><strong>{p["cta_line"]}</strong></p>
        <div class="cta-buttons">
          <a href="/get-free-quote.html" class="btn btn-primary btn-lg">Get Free Quote</a>
          <a href="tel:+971508268481" class="btn btn-outline btn-lg">Call Now</a>
        </div>
      </div>

      <p class="location-links"><a href="/movers-near-me-abu-dhabi.html">Movers near me Abu Dhabi</a> — full coverage across the emirate.</p>
      <p class="location-links">Professional movers across Abu Dhabi: {nearby}</p>
    </div>
  </section>

  <div id="footer"></div>
  <div id="wa-chat-widget"></div>
  <div id="scroll-to-top"></div>

  <script src="/js/component-loader.js" defer></script>
  <script src="/js/nav-drawer.js" defer></script>
  <script src="/js/wa-chat-widget.js" defer></script>
  <script src="/js/main.js" defer></script>
</body>
</html>
"""


PAGES = [
    {
        "slug": "movers-al-bateen-abu-dhabi",
        "title": "Movers in Al Bateen Abu Dhabi | Al Bateen Moving Company UAE - Man With Van",
        "desc": "Trusted movers in Al Bateen Abu Dhabi. Villa & apartment moving, embassy district relocations. Fully insured. Free quote. Call +971 50 826 8481.",
        "keywords": "movers al bateen abu dhabi, moving company al bateen, al bateen movers",
        "area_served": "Al Bateen, Abu Dhabi",
        "h1": "Movers in Al Bateen Abu Dhabi | Al Bateen Moving Company UAE",
        "subtitle": "Upscale waterfront moving in Al Bateen—villas and apartments, embassy district access. Professional movers and packers, transparent AED pricing.",
        "intro_h2": "House Moving & Relocation Services in Al Bateen Abu Dhabi",
        "intro_p1": "Al Bateen is one of Abu Dhabi’s most prestigious waterfront districts, mixing villas, low-rise apartments and embassy-adjacent properties. As experienced movers in Al Bateen Abu Dhabi, Man With Van handles careful loading, building access and tight scheduling for this upscale community.",
        "intro_p2": "We serve Al Bateen and connect easily to Saadiyat, Al Maryah Island, the Corniche and central Abu Dhabi. Our crews know how to coordinate with security and compound rules so your relocation stays smooth from packing to placement.",
        "services_h2": "Al Bateen Abu Dhabi",
        "spans": [
            "Villa movers Al Bateen—waterfront and compound homes",
            "Apartment moving in Al Bateen towers and low-rises",
            "Office and diplomatic staff relocations across Abu Dhabi",
            "Furniture delivery, assembly and single-item moves",
            "Full packing and unpacking for Al Bateen homes",
            "Storage and removals when you need a bridge between homes",
        ],
        "faqs": [
            ("Do you cover Al Bateen villas?", "Yes. We move villas and apartments across Al Bateen, including waterfront compounds and embassy-adjacent neighbourhoods. Share your villa size and access details for a tailored quote."),
            ("What is the cost for a move in Al Bateen?", "Pricing depends on home size, distance and packing. Many apartment moves fall in the AED 400–800 range; larger villas are quoted per inventory. Call +971 50 826 8481 for a free, no-obligation estimate."),
            ("Is same-day moving available in Al Bateen?", "Same-day slots are often available subject to crew availability—contact us by phone or WhatsApp to confirm today’s dispatch."),
        ],
        "nearby": [
            ("movers-corniche-abu-dhabi.html", "Movers Corniche Abu Dhabi"),
            ("movers-al-maryah-island-abu-dhabi.html", "Movers Al Maryah Island Abu Dhabi"),
            ("movers-al-khalidiyah-abu-dhabi.html", "Movers Al Khalidiyah Abu Dhabi"),
            ("movers-saadiyat-island-abu-dhabi.html", "Movers Saadiyat Island Abu Dhabi"),
            ("movers-al-reem-island-abu-dhabi.html", "Movers Al Reem Island Abu Dhabi"),
        ],
        "cta_line": "Ready to move in Al Bateen Abu Dhabi?",
    },
    {
        "slug": "movers-al-mushrif-abu-dhabi",
        "title": "Movers in Al Mushrif Abu Dhabi | Al Mushrif Moving Company UAE - Man With Van",
        "desc": "Reliable movers in Al Mushrif Abu Dhabi. Family villas & apartments near Al Mushrif Mall. Insured moves, free quote. +971 50 826 8481.",
        "keywords": "movers al mushrif abu dhabi, moving company al mushrif, al mushrif movers",
        "area_served": "Al Mushrif, Abu Dhabi",
        "h1": "Movers in Al Mushrif Abu Dhabi | Al Mushrif Moving Company UAE",
        "subtitle": "Family-focused moving in Al Mushrif—villas and apartments near Al Mushrif Mall. Trusted movers and packers for Abu Dhabi relocations.",
        "intro_h2": "House Moving & Relocation Services in Al Mushrif Abu Dhabi",
        "intro_p1": "Al Mushrif is a well-established family area with a mix of villas and apartments, close to schools and Al Mushrif Mall. Our movers in Al Mushrif Abu Dhabi plan routes and timing around school runs, narrow streets and community access.",
        "intro_p2": "Whether you are moving within Al Mushrif or to Khalifa City, Al Reem or Mussafah, we provide insured transport, optional packing and furniture assembly so your household settles in faster.",
        "services_h2": "Al Mushrif Abu Dhabi",
        "spans": [
            "Villa movers Al Mushrif—compound and standalone homes",
            "Apartment moves in Al Mushrif residential buildings",
            "Office and small business relocation nearby",
            "Furniture moving and bulk-item delivery",
            "Packing and unpacking for busy families",
            "Storage solutions between handover dates",
        ],
        "faqs": [
            ("Do you cover all Al Mushrif streets?", "Yes. We serve Al Mushrif and surrounding residential streets, including areas near Al Mushrif Mall. Share your building or villa access so we can plan parking and loading."),
            ("What does a villa move cost in Al Mushrif?", "Villa moves are typically quoted from AED 900+ depending on bedrooms, packing and distance. We provide a written quote before you confirm your booking."),
            ("Are weekend moves available in Al Mushrif?", "Yes. We operate seven days a week including weekends and most public holidays—book early for peak weekends and end-of-month dates."),
        ],
        "nearby": [
            ("movers-al-khalidiyah-abu-dhabi.html", "Movers Al Khalidiyah Abu Dhabi"),
            ("movers-khalifa-city-abu-dhabi.html", "Movers Khalifa City Abu Dhabi"),
            ("movers-al-reem-island-abu-dhabi.html", "Movers Al Reem Island Abu Dhabi"),
            ("movers-mussafah-abu-dhabi.html", "Movers Mussafah Abu Dhabi"),
            ("movers-baniyas-abu-dhabi.html", "Movers Baniyas Abu Dhabi"),
        ],
        "cta_line": "Ready to move in Al Mushrif Abu Dhabi?",
    },
    {
        "slug": "movers-al-karamah-abu-dhabi",
        "title": "Movers in Al Karamah Abu Dhabi | Al Karamah Moving Company UAE - Man With Van",
        "desc": "Professional movers in Al Karamah Abu Dhabi. High-rise apartments near Hamdan Street. Elevator coordination & insured moves. Free quote.",
        "keywords": "movers al karamah abu dhabi, moving company al karamah",
        "area_served": "Al Karamah, Abu Dhabi",
        "h1": "Movers in Al Karamah Abu Dhabi | Al Karamah Moving Company UAE",
        "subtitle": "Central Abu Dhabi moving—tower apartments near Hamdan Street. Service lifts, loading bays and clear quotes.",
        "intro_h2": "House Moving & Relocation Services in Al Karamah Abu Dhabi",
        "intro_p1": "Al Karamah sits in the heart of Abu Dhabi with dense apartment towers and strong demand for efficient moves. As movers in Al Karamah Abu Dhabi, we coordinate service elevators, protect common areas and keep your inventory organised floor by floor.",
        "intro_p2": "We link Al Karamah with Al Khalidiyah, the Corniche, Tourist Club Area and business districts—ideal for professionals who need fast turnaround between tenancies.",
        "services_h2": "Al Karamah Abu Dhabi",
        "spans": [
            "High-rise apartment movers Al Karamah",
            "Hamdan Street and central Abu Dhabi relocations",
            "Office moves for businesses nearby",
            "Furniture delivery and assembly",
            "Packing services for compact city homes",
            "Short-term storage when dates do not align",
        ],
        "faqs": [
            ("Do you move high-rise apartments in Al Karamah?", "Yes. We coordinate service elevators, loading bays and building rules for tower moves in Al Karamah and central Abu Dhabi."),
            ("What is the typical moving cost in Al Karamah?", "Most apartment moves start from AED 400–800 depending on floor, distance and packing. We confirm a clear price band before moving day."),
            ("Do you help with elevator coordination?", "Yes. We advise on service lift booking and timing, and can align with your building management when you share your move date."),
        ],
        "nearby": [
            ("movers-tourist-club-area-abu-dhabi.html", "Movers Tourist Club Area Abu Dhabi"),
            ("movers-al-khalidiyah-abu-dhabi.html", "Movers Al Khalidiyah Abu Dhabi"),
            ("movers-corniche-abu-dhabi.html", "Movers Corniche Abu Dhabi"),
            ("movers-al-maryah-island-abu-dhabi.html", "Movers Al Maryah Island Abu Dhabi"),
            ("movers-mussafah-abu-dhabi.html", "Movers Mussafah Abu Dhabi"),
        ],
        "cta_line": "Ready to move in Al Karamah Abu Dhabi?",
    },
    {
        "slug": "movers-corniche-abu-dhabi",
        "title": "Movers on the Corniche Abu Dhabi | Corniche Moving Company UAE - Man With Van",
        "desc": "Expert movers on the Abu Dhabi Corniche. Premium waterfront towers, Tourist Club Area access. Insured high-rise moves. Free quote today.",
        "keywords": "movers corniche abu dhabi, corniche area movers abu dhabi, tourist club area movers",
        "area_served": "Abu Dhabi Corniche",
        "h1": "Movers on the Corniche Abu Dhabi | Corniche Moving Company UAE",
        "subtitle": "Premium waterfront towers along the Corniche—strict building rules, service lifts and professional crews.",
        "intro_h2": "House Moving & Relocation Services on the Abu Dhabi Corniche",
        "intro_p1": "The Corniche and adjacent districts feature some of Abu Dhabi’s most sought-after high-rises, with strict move-in windows and loading rules. Our Corniche movers understand security procedures, basement access and time slots near the Tourist Club Area.",
        "intro_p2": "We connect Corniche residents with moves across Al Maryah Island, Al Bateen, Al Khalidiyah and beyond—fully insured, with optional packing for fragile décor and artwork.",
        "services_h2": "the Abu Dhabi Corniche",
        "spans": [
            "Waterfront tower moves along the Corniche",
            "Tourist Club Area and Al Zahiyah relocations",
            "Office and executive apartment moves",
            "Fragile packing and art handling (as quoted)",
            "Furniture assembly at your new address",
            "Storage between Corniche handovers",
        ],
        "faqs": [
            ("Do Corniche towers have special move-in rules?", "Yes. Many buildings require advance notice, deposits or time slots for service lifts and loading. Share your building name—we align our crew with those rules."),
            ("What is the cost for a high-rise Corniche move?", "High-rise moves typically start from AED 400–1,200+ depending on floor, volume and packing. We quote in writing after reviewing your inventory."),
            ("How long does a Corniche apartment move take?", "Most same-building or local moves take half a day; larger inventories or long-distance legs may need a full day—we confirm timing when booking."),
        ],
        "nearby": [
            ("movers-tourist-club-area-abu-dhabi.html", "Movers Tourist Club Area Abu Dhabi"),
            ("movers-al-maryah-island-abu-dhabi.html", "Movers Al Maryah Island Abu Dhabi"),
            ("movers-al-bateen-abu-dhabi.html", "Movers Al Bateen Abu Dhabi"),
            ("movers-al-khalidiyah-abu-dhabi.html", "Movers Al Khalidiyah Abu Dhabi"),
            ("movers-al-reem-island-abu-dhabi.html", "Movers Al Reem Island Abu Dhabi"),
        ],
        "cta_line": "Ready to move on the Abu Dhabi Corniche?",
    },
    {
        "slug": "movers-al-maryah-island-abu-dhabi",
        "title": "Movers in Al Maryah Island Abu Dhabi | Al Maryah Island Moving Company - Man With Van",
        "desc": "Luxury movers in Al Maryah Island Abu Dhabi. Financial district towers, strict building protocols. Insured office & home moves. Free quote.",
        "keywords": "movers al maryah island, moving company al maryah island abu dhabi",
        "area_served": "Al Maryah Island, Abu Dhabi",
        "h1": "Movers in Al Maryah Island Abu Dhabi | Al Maryah Island Moving Company",
        "subtitle": "Abu Dhabi’s financial and lifestyle island—luxury high-rises with strict move protocols and professional crews.",
        "intro_h2": "House Moving & Relocation Services on Al Maryah Island Abu Dhabi",
        "intro_p1": "Al Maryah Island combines premium residences and commercial towers with detailed building management rules. Our movers on Al Maryah Island coordinate permits, lift bookings and after-hours slots where required.",
        "intro_p2": "We serve residents and businesses moving to or from Al Reem, the Corniche, Al Bateen and other Abu Dhabi districts—with clear pricing and insured handling throughout.",
        "services_h2": "Al Maryah Island Abu Dhabi",
        "spans": [
            "Luxury apartment movers Al Maryah Island",
            "Office and retail relocation in the financial district",
            "IT-safe packing for home offices",
            "Furniture and white-glove delivery (as agreed)",
            "Weekend and evening moves to reduce downtime",
            "Storage for staged moves between contracts",
        ],
        "faqs": [
            ("Do you coordinate move permits for Al Maryah towers?", "Yes. Requirements vary by tower—we work with your building management and security to confirm access, lift timing and any permits needed."),
            ("What does a move cost on Al Maryah Island?", "Costs depend on unit size, floor, packing and distance. Many apartment moves fall in the AED 500–1,500 range; we provide a written quote."),
            ("Are weekend moves available on Al Maryah Island?", "Yes. We offer weekend and evening slots where buildings allow—book ahead for peak periods."),
        ],
        "nearby": [
            ("movers-corniche-abu-dhabi.html", "Movers Corniche Abu Dhabi"),
            ("movers-al-bateen-abu-dhabi.html", "Movers Al Bateen Abu Dhabi"),
            ("movers-al-reem-island-abu-dhabi.html", "Movers Al Reem Island Abu Dhabi"),
            ("movers-tourist-club-area-abu-dhabi.html", "Movers Tourist Club Area Abu Dhabi"),
            ("movers-al-khalidiyah-abu-dhabi.html", "Movers Al Khalidiyah Abu Dhabi"),
        ],
        "cta_line": "Ready to move on Al Maryah Island Abu Dhabi?",
    },
    {
        "slug": "movers-masdar-city-abu-dhabi",
        "title": "Movers in Masdar City Abu Dhabi | Masdar City Moving Company UAE - Man With Van",
        "desc": "Trusted movers in Masdar City Abu Dhabi. Eco-city apartments & villas near Abu Dhabi airport. Insured moves. Free quote. +971 50 826 8481.",
        "keywords": "movers masdar city abu dhabi, moving company masdar city",
        "area_served": "Masdar City, Abu Dhabi",
        "h1": "Movers in Masdar City Abu Dhabi | Masdar City Moving Company UAE",
        "subtitle": "Sustainable community moving—apartments and villas near the airport with efficient routes into Abu Dhabi city.",
        "intro_h2": "House Moving & Relocation Services in Masdar City Abu Dhabi",
        "intro_p1": "Masdar City offers a distinctive eco-focused lifestyle with apartments and town-style homes close to Abu Dhabi International Airport. Our movers in Masdar City plan for community roads, loading areas and connections to the main highway network.",
        "intro_p2": "We move clients between Masdar City, downtown Abu Dhabi, Khalifa City, Yas Island and Dubai—always with transparent AED quotes and insured transport.",
        "services_h2": "Masdar City Abu Dhabi",
        "spans": [
            "Masdar City apartment and villa movers",
            "Moves to and from Abu Dhabi airport area",
            "Student and professional relocations",
            "Office and co-working space moves",
            "Packing and furniture assembly",
            "Inter-emirate moves including Dubai",
        ],
        "faqs": [
            ("Do you serve Masdar City apartments?", "Yes. We move apartments and villas across Masdar City, including low-rise and mid-rise buildings. Tell us your building access for accurate scheduling."),
            ("What is the move cost from Masdar to Abu Dhabi city?", "Pricing depends on volume and distance. Many local moves start from AED 400–900; we confirm after a quick inventory check."),
            ("How soon can you book availability?", "We often have same-day or next-day slots—call +971 50 826 8481 or WhatsApp to check the diary."),
        ],
        "nearby": [
            ("movers-shakhbout-city-abu-dhabi.html", "Movers Shakhbout City Abu Dhabi"),
            ("movers-khalifa-city-abu-dhabi.html", "Movers Khalifa City Abu Dhabi"),
            ("movers-al-rahba-abu-dhabi.html", "Movers Al Rahba Abu Dhabi"),
            ("movers-yas-island-abu-dhabi.html", "Movers Yas Island Abu Dhabi"),
            ("movers-mussafah-abu-dhabi.html", "Movers Mussafah Abu Dhabi"),
        ],
        "cta_line": "Ready to move in Masdar City Abu Dhabi?",
    },
    {
        "slug": "movers-shakhbout-city-abu-dhabi",
        "title": "Movers in Shakhbout City Abu Dhabi | Shakhbout City Moving Company UAE - Man With Van",
        "desc": "Professional movers in Shakhbout City Abu Dhabi. Villas & townhouses in a growing suburb. Insured relocation. Free quote today.",
        "keywords": "movers shakhbout city abu dhabi, shakhbout city movers",
        "area_served": "Shakhbout City, Abu Dhabi",
        "h1": "Movers in Shakhbout City Abu Dhabi | Shakhbout City Moving Company UAE",
        "subtitle": "Growing residential suburb—villas and townhouses with space for full truck loads and careful handling.",
        "intro_h2": "House Moving & Relocation Services in Shakhbout City Abu Dhabi",
        "intro_p1": "Shakhbout City continues to expand with villas and townhouses popular with families seeking more space. Our movers in Shakhbout City handle large furniture, garden items and multi-room inventories with the right crew size.",
        "intro_p2": "We connect Shakhbout City with MBZ, Khalifa City, Al Falah and central Abu Dhabi—planning drive times and access for smooth loading and unloading.",
        "services_h2": "Shakhbout City Abu Dhabi",
        "spans": [
            "Villa and townhouse movers Shakhbout City",
            "Full-home packing and unpacking",
            "Large-item and appliance moves",
            "Moves to and from western Abu Dhabi communities",
            "Office and home business relocations",
            "Storage when your new home is not ready",
        ],
        "faqs": [
            ("Do you cover all Shakhbout City phases?", "Yes. We serve current and new phases across Shakhbout City. Share your phase and street so we can plan vehicle access."),
            ("What is the villa move cost in Shakhbout City?", "Villa moves typically start from AED 900+ depending on rooms, packing and distance. We provide a detailed quote before you book."),
            ("Can you move large items like pianos or gym equipment?", "Heavy items may need extra crew or equipment—tell us when booking so we quote and schedule safely."),
        ],
        "nearby": [
            ("movers-masdar-city-abu-dhabi.html", "Movers Masdar City Abu Dhabi"),
            ("movers-mohammed-bin-zayed-city-abu-dhabi.html", "Movers Mohammed Bin Zayed City Abu Dhabi"),
            ("movers-al-falah-abu-dhabi.html", "Movers Al Falah Abu Dhabi"),
            ("movers-khalifa-city-abu-dhabi.html", "Movers Khalifa City Abu Dhabi"),
            ("movers-al-shamkha-abu-dhabi.html", "Movers Al Shamkha Abu Dhabi"),
        ],
        "cta_line": "Ready to move in Shakhbout City Abu Dhabi?",
    },
    {
        "slug": "movers-madinat-zayed-abu-dhabi",
        "title": "Movers in Madinat Zayed Abu Dhabi | Madinat Zayed Moving Company UAE - Man With Van",
        "desc": "Reliable movers in Madinat Zayed Abu Dhabi. Western region residential moves. Long-distance & local quotes. Insured. +971 50 826 8481.",
        "keywords": "movers madinat zayed abu dhabi, madinat zayed movers",
        "area_served": "Madinat Zayed, Abu Dhabi",
        "h1": "Movers in Madinat Zayed Abu Dhabi | Madinat Zayed Moving Company UAE",
        "subtitle": "Western Abu Dhabi region—residential moves with routes planned for distance and drive time.",
        "intro_h2": "House Moving & Relocation Services in Madinat Zayed Abu Dhabi",
        "intro_p1": "Madinat Zayed serves as a key residential hub in the western region of Abu Dhabi emirate. Our movers in Madinat Zayed support families and businesses with longer drive times factored into quotes and scheduling.",
        "intro_p2": "Whether you are moving locally within Madinat Zayed or to Abu Dhabi city, Al Ain or Dubai, we provide insured transport, optional packing and clear communication on arrival windows.",
        "services_h2": "Madinat Zayed Abu Dhabi",
        "spans": [
            "Residential movers Madinat Zayed and western region",
            "Long-distance moves to Abu Dhabi city and other emirates",
            "Villa and apartment relocations",
            "Furniture and appliance transport",
            "Packing services for remote moves",
            "Commercial and office moves on request",
        ],
        "faqs": [
            ("Do you travel to Madinat Zayed?", "Yes. We serve Madinat Zayed and surrounding western communities. Distance affects pricing—we quote upfront."),
            ("What is the cost for a long-distance move from Madinat Zayed?", "Longer drives add fuel and time; typical home moves are quoted from AED 800+ depending on inventory. Contact us for a fixed estimate."),
            ("How long does a move to Abu Dhabi city take?", "Drive time plus loading usually means a full-day job for larger homes; we confirm start times and crew size when you book."),
        ],
        "nearby": [
            ("movers-al-shamkha-abu-dhabi.html", "Movers Al Shamkha Abu Dhabi"),
            ("movers-al-rahba-abu-dhabi.html", "Movers Al Rahba Abu Dhabi"),
            ("movers-al-falah-abu-dhabi.html", "Movers Al Falah Abu Dhabi"),
            ("movers-mussafah-abu-dhabi.html", "Movers Mussafah Abu Dhabi"),
            ("movers-khalifa-city-abu-dhabi.html", "Movers Khalifa City Abu Dhabi"),
        ],
        "cta_line": "Ready to move in Madinat Zayed Abu Dhabi?",
    },
    {
        "slug": "movers-al-falah-abu-dhabi",
        "title": "Movers in Al Falah Abu Dhabi | Al Falah City Moving Company UAE - Man With Van",
        "desc": "Affordable movers in Al Falah Abu Dhabi. Villas & apartments in Al Falah City. Insured moves, same-day options. Free quote. +971 50 826 8481.",
        "keywords": "movers al falah abu dhabi, al falah city movers abu dhabi",
        "area_served": "Al Falah, Abu Dhabi",
        "h1": "Movers in Al Falah Abu Dhabi | Al Falah City Moving Company UAE",
        "subtitle": "Affordable residential community moving—villas and apartments with clear AED pricing.",
        "intro_h2": "House Moving & Relocation Services in Al Falah Abu Dhabi",
        "intro_p1": "Al Falah City offers value-focused housing with villas and apartments popular with growing families. Our movers in Al Falah Abu Dhabi deliver reliable packing, loading and delivery without hidden fees.",
        "intro_p2": "We connect Al Falah with Khalifa City, MBZ, Shakhbout City and Abu Dhabi island—handling everything from studio moves to full villa relocations.",
        "services_h2": "Al Falah Abu Dhabi",
        "spans": [
            "Al Falah City villa and apartment movers",
            "Budget-friendly packing options",
            "Furniture and appliance moves",
            "Same-day and next-day slots when available",
            "Moves to Abu Dhabi city and other emirates",
            "Storage between handovers",
        ],
        "faqs": [
            ("Do you cover Al Falah City?", "Yes. We move homes across Al Falah City including villas and apartments. Share your unit type for an accurate quote."),
            ("What is the move cost from Al Falah to Abu Dhabi city?", "Pricing depends on volume and distance. Many moves start from AED 400–1,200; long-distance trips are quoted individually."),
            ("Is same-day moving available in Al Falah?", "Same-day moves are often possible subject to crew availability—call or WhatsApp +971 50 826 8481 to check."),
        ],
        "nearby": [
            ("movers-shakhbout-city-abu-dhabi.html", "Movers Shakhbout City Abu Dhabi"),
            ("movers-mohammed-bin-zayed-city-abu-dhabi.html", "Movers Mohammed Bin Zayed City Abu Dhabi"),
            ("movers-khalifa-city-abu-dhabi.html", "Movers Khalifa City Abu Dhabi"),
            ("movers-masdar-city-abu-dhabi.html", "Movers Masdar City Abu Dhabi"),
            ("movers-al-rahba-abu-dhabi.html", "Movers Al Rahba Abu Dhabi"),
        ],
        "cta_line": "Ready to move in Al Falah Abu Dhabi?",
    },
    {
        "slug": "movers-al-rahba-abu-dhabi",
        "title": "Movers in Al Rahba Abu Dhabi | Al Rahba Moving Company UAE - Man With Van",
        "desc": "Trusted movers in Al Rahba Abu Dhabi. Near Abu Dhabi–Dubai border. Local & Dubai moves. Insured. Free quote. Call +971 50 826 8481.",
        "keywords": "movers al rahba abu dhabi, al rahba movers",
        "area_served": "Al Rahba, Abu Dhabi",
        "h1": "Movers in Al Rahba Abu Dhabi | Al Rahba Moving Company UAE",
        "subtitle": "Residential suburb near the Abu Dhabi–Dubai corridor—ideal for cross-emirate relocations.",
        "intro_h2": "House Moving & Relocation Services in Al Rahba Abu Dhabi",
        "intro_p1": "Al Rahba offers suburban living with quick access toward Dubai and the main highway network. Our movers in Al Rahba plan routes for border-area traffic and longer-distance jobs.",
        "intro_p2": "We handle moves within Al Rahba and to Khalifa City, Dubai, Abu Dhabi island and western communities—with inter-emirate pricing explained clearly upfront.",
        "services_h2": "Al Rahba Abu Dhabi",
        "spans": [
            "Al Rahba villa and apartment movers",
            "Abu Dhabi to Dubai relocations",
            "Furniture and full-home moves",
            "Packing and unpacking services",
            "Office and small business moves",
            "Storage and staging solutions",
        ],
        "faqs": [
            ("Do you cover Al Rahba?", "Yes. We serve Al Rahba and nearby residential communities. Share your exact location for routing and timing."),
            ("What is the typical move cost from Al Rahba?", "Costs depend on home size and destination. Local moves often start from AED 500+; Dubai moves are quoted per distance and volume."),
            ("Can you move to Dubai from Al Rahba?", "Yes. We regularly handle Abu Dhabi–Dubai moves including from Al Rahba—ask for an inter-emirate quote."),
        ],
        "nearby": [
            ("movers-shakhbout-city-abu-dhabi.html", "Movers Shakhbout City Abu Dhabi"),
            ("movers-masdar-city-abu-dhabi.html", "Movers Masdar City Abu Dhabi"),
            ("movers-al-shamkha-abu-dhabi.html", "Movers Al Shamkha Abu Dhabi"),
            ("movers-khalifa-city-abu-dhabi.html", "Movers Khalifa City Abu Dhabi"),
            ("movers-yas-island-abu-dhabi.html", "Movers Yas Island Abu Dhabi"),
        ],
        "cta_line": "Ready to move in Al Rahba Abu Dhabi?",
    },
    {
        "slug": "movers-al-shamkha-abu-dhabi",
        "title": "Movers in Al Shamkha Abu Dhabi | Al Shamkha Moving Company UAE - Man With Van",
        "desc": "Expert movers in Al Shamkha Abu Dhabi. Western villas & expanding communities. Insured moves. Weekend slots. Free quote +971 50 826 8481.",
        "keywords": "movers al shamkha abu dhabi, al shamkha movers",
        "area_served": "Al Shamkha, Abu Dhabi",
        "h1": "Movers in Al Shamkha Abu Dhabi | Al Shamkha Moving Company UAE",
        "subtitle": "Western residential area—villa districts and new phases with flexible scheduling.",
        "intro_h2": "House Moving & Relocation Services in Al Shamkha Abu Dhabi",
        "intro_p1": "Al Shamkha continues to grow with villa communities and new infrastructure across western Abu Dhabi. Our movers in Al Shamkha handle large gardens, multi-bedroom homes and long driveways with the right equipment.",
        "intro_p2": "We link Al Shamkha with Madinat Zayed, Khalifa City, MBZ and Abu Dhabi city—always with insured loads and optional full packing.",
        "services_h2": "Al Shamkha Abu Dhabi",
        "spans": [
            "Villa movers Al Shamkha and western Abu Dhabi",
            "New phase and off-plan handover moves",
            "Heavy furniture and outdoor items",
            "Weekend and public holiday bookings",
            "Long-distance moves across the UAE",
            "Storage when your villa is not ready",
        ],
        "faqs": [
            ("Do you cover Al Shamkha?", "Yes. We serve Al Shamkha including newer phases. Tell us your community name for access planning."),
            ("What is the move cost for a villa in Al Shamkha?", "Villa moves typically start from AED 900+ depending on size, packing and destination. We provide a written quote."),
            ("Is weekend availability good in Al Shamkha?", "Yes. We operate weekends—book early for month-end peaks."),
        ],
        "nearby": [
            ("movers-madinat-zayed-abu-dhabi.html", "Movers Madinat Zayed Abu Dhabi"),
            ("movers-al-falah-abu-dhabi.html", "Movers Al Falah Abu Dhabi"),
            ("movers-shakhbout-city-abu-dhabi.html", "Movers Shakhbout City Abu Dhabi"),
            ("movers-mohammed-bin-zayed-city-abu-dhabi.html", "Movers Mohammed Bin Zayed City Abu Dhabi"),
            ("movers-al-reef-abu-dhabi.html", "Movers Al Reef Abu Dhabi"),
        ],
        "cta_line": "Ready to move in Al Shamkha Abu Dhabi?",
    },
    {
        "slug": "movers-tourist-club-area-abu-dhabi",
        "title": "Movers in Tourist Club Area Abu Dhabi | TCA Moving Company UAE - Man With Van",
        "desc": "Dense apartment movers in Tourist Club Area Abu Dhabi (Al Zahiyah). City-centre towers, parking coordination. Insured. Free quote today.",
        "keywords": "movers tourist club area abu dhabi, TCA movers abu dhabi, al zahiyah movers",
        "area_served": "Tourist Club Area, Abu Dhabi",
        "h1": "Movers in Tourist Club Area Abu Dhabi | TCA Moving Company UAE",
        "subtitle": "City-centre apartments—also known as Al Zahiyah—with busy streets and structured building access.",
        "intro_h2": "House Moving & Relocation Services in Tourist Club Area Abu Dhabi",
        "intro_p1": "The Tourist Club Area (TCA), overlapping Al Zahiyah, is one of Abu Dhabi’s densest apartment districts. Our TCA movers coordinate parking, service elevators and tight loading windows for high-rise residents.",
        "intro_p2": "We connect TCA with the Corniche, Al Maryah Island, Al Karamah and Khalidiyah—ideal for professionals and families upgrading within the city core.",
        "services_h2": "Tourist Club Area Abu Dhabi",
        "spans": [
            "Tourist Club Area / Al Zahiyah apartment movers",
            "High-rise packing and elevator coordination",
            "Small-office and home-office moves",
            "Furniture-only and single-item jobs",
            "After-hours moves where buildings allow",
            "Storage for city-centre handover gaps",
        ],
        "faqs": [
            ("Do you move apartments in Tourist Club Area?", "Yes. We regularly move apartments throughout TCA and Al Zahiyah, including older and newer towers."),
            ("What is the typical moving cost in TCA?", "Most apartment moves start from AED 400–900 depending on floor, volume and packing. We quote before we start."),
            ("How do you handle parking for a moving truck?", "We work with your building’s loading bay rules and street parking where permitted—share building guidelines when you book."),
        ],
        "nearby": [
            ("movers-al-zahiyah-abu-dhabi.html", "Movers Al Zahiyah Abu Dhabi"),
            ("movers-corniche-abu-dhabi.html", "Movers Corniche Abu Dhabi"),
            ("movers-al-karamah-abu-dhabi.html", "Movers Al Karamah Abu Dhabi"),
            ("movers-al-khalidiyah-abu-dhabi.html", "Movers Al Khalidiyah Abu Dhabi"),
            ("movers-al-maryah-island-abu-dhabi.html", "Movers Al Maryah Island Abu Dhabi"),
        ],
        "cta_line": "Ready to move in Tourist Club Area Abu Dhabi?",
    },
]


def main():
    assert len(PAGES) == 12
    OUT.mkdir(parents=True, exist_ok=True)
    for p in PAGES:
        path = OUT / f"{p['slug']}.html"
        path.write_text(render(p), encoding="utf-8")
        print("Wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
