# -*- coding: utf-8 -*-
"""Generate 130 blog posts (10 per filter category) and update blog.html cards."""
from __future__ import annotations

import html
import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog"
BLOG_HTML = ROOT / "blog.html"

# (data-category slug, display tag for card + post meta, list of (title, excerpt))
DATA: list[tuple[str, str, list[tuple[str, str]]]] = [
    (
        "moving-tips",
        "Moving Tips",
        [
            ("How to Label Moving Boxes So Your Crew Works Faster", "Clear room names and handling notes save time on load and unload—especially in Abu Dhabi towers."),
            ("Moving Day Survival Kit: What to Keep in Your Car", "Documents, chargers, snacks, and meds—pack a bag that stays off the truck."),
            ("Pet Relocation Tips for Stress-Free UAE Moves", "Routine, carriers, and vet records—how to plan pet comfort on moving day."),
            ("How to Prepare Children for a House Move", "Age-appropriate conversations, goodbye rituals, and first-night routines in the new home."),
            ("Why Elevator Reservations Matter in High-Rise Buildings", "Service lifts, time slots, and building rules—what to book before movers arrive."),
            ("Change-of-Address Checklist for Abu Dhabi Residents", "DEWA, internet, bank, and subscriptions—who to notify and when."),
            ("Moving During Ramadan: Practical Scheduling Tips", "Respectful timing, shorter days, and hydration for summer heat."),
            ("Staying Safe on Moving Day in UAE Summer Heat", "Water breaks, shade, and what crews need from you when temperatures soar."),
            ("The Night Before Movers Arrive: Last-Minute Checklist", "Fridge, beds, corridors, and parking—final tasks that prevent morning chaos."),
            ("Coordinating Security and Building Access on Move-Out Day", "Passes, loading bays, and guard desks—avoid delays at the gate."),
        ],
    ),
    (
        "moving-guide",
        "Moving Guide",
        [
            ("4-Week Moving Timeline for Abu Dhabi Families", "Week-by-week tasks so paperwork, packing, and handover stay under control."),
            ("First Night in Your New Home: Setup Essentials", "Bedding, kettle, tools, and Wi-Fi—what to unpack first."),
            ("How to Read a Moving Quote Line by Line", "Labour, truck, materials, insurance—what each line usually means."),
            ("Moving With a Baby: Room-by-Room Priorities", "Sleep space first, then feeding gear—reduce disruption for infants."),
            ("Downsizing Before a UAE Move: Where to Donate and Sell", "Furniture, clothes, and electronics—local options to lighten your load."),
            ("Utilities Handover: Chiller, DEWA, and Final Bills", "What to schedule before keys go back to the landlord."),
            ("Planning a Same-Emirate Move Without Last-Minute Stress", "Short distances still need timing, access, and parking plans."),
            ("Building a Simple Moving Inventory Spreadsheet", "Rooms, box counts, and high-value items—why lists reduce disputes."),
            ("Documents to Keep on You During Moving Day", "Passports, contracts, and keys—never pack these on the truck."),
            ("Move-Out Photos: What to Capture Before Handover", "Walls, meters, and fixtures—protect your deposit with evidence."),
        ],
    ),
    (
        "moving-cost",
        "Moving Cost",
        [
            ("Hidden Moving Fees to Ask About Before You Book", "Stairs, long carries, and after-hours—clarify what triggers extra charges."),
            ("How Truck Size Affects Your Moving Quote in the UAE", "Volume, trips, and crew size—why the right vehicle saves money."),
            ("Stairs vs Lift: When Building Access Changes the Price", "Floors matter when service elevators are not booked."),
            ("Moving Insurance Add-Ons: Are They Worth It?", "Declared value, excess, and what standard coverage usually includes."),
            ("Hourly vs Fixed-Price Moving Quotes Compared", "When each model works best for apartments and villas."),
            ("Peak Season and Weekend Pricing for UAE Moves", "Why dates move rates and how flexibility can lower your bill."),
            ("How Professional Packing Changes Your Total Moving Bill", "Materials plus labour—what to expect on the invoice."),
            ("Deposits and Payment Terms: What’s Normal for Movers?", "Percentages, balance on delivery, and cancellation windows."),
            ("Small Loads and Partial Moves: When a Van Saves Money", "Few items or single pieces—matching vehicle to job."),
            ("VAT and Moving Services: A Simple Overview for Customers", "What typically applies and how quotes should present it."),
        ],
    ),
    (
        "packing-guides",
        "Packing Guides",
        [
            ("Best Box Sizes for Books, Clothes, and Kitchenware", "Weight limits and stacking—avoid crushed boxes on the drive."),
            ("How to Pack a Mattress for Moving Day", "Bags, plastic, and orientation—keep bedding clean and dry."),
            ("Wardrobe Boxes: When They’re Worth the Extra Cost", "Suits and dresses—hang vs fold for short moves."),
            ("Packing Electronics: Screens, Cables, and Accessories", "Photos before unplugging, small bags for remotes, and original boxes if you have them."),
            ("Kitchen Packing Order: What to Pack Last", "Daily dishes vs seasonal—work back from move week meals."),
            ("Packing Lamps, Mirrors, and Odd-Shaped Items", "Disassemble bases, protect glass, and label fragile clearly."),
            ("Using Suitcases for Heavy or Valuable Items", "Books and jewellery—rolling luggage beats weak cardboard."),
            ("Color-Coding Rooms for Faster Unpacking", "Tape or stickers—help movers place boxes in the right space."),
            ("Protecting Furniture Corners With Cardboard and Blankets", "Edges take hits in doorways—simple wraps that work."),
            ("Last-Minute Packing Mistakes That Cost Time and Money", "Overfilled boxes, unlabeled mix-ups, and wet cleaning gear."),
        ],
    ),
    (
        "abu-dhabi-living",
        "Abu Dhabi Living",
        [
            ("Parking and Loading Rules for Moving Trucks in Abu Dhabi", "Municipality basics, communities, and how to avoid fines on move day."),
            ("New to Khalifa City: What Movers Wish You Knew", "Access roads, compound gates, and peak traffic patterns."),
            ("Al Reef vs Yas Island: Lifestyle Notes for New Residents", "Commute, amenities, and moving access—high-level comparison."),
            ("School Timelines and How They Affect Your Move Date", "Term breaks vs mid-year—planning around family logistics."),
            ("Service Charges and Moving: What to Budget Beyond Rent", "Community fees, chiller, and handover costs in context."),
            ("Best Times of Day to Beat Traffic on a Moving Truck", "Cross-city routes and Friday patterns—practical timing."),
            ("Saadiyat Island Moves: Building and Beach Community Tips", "Rules, routes, and coordination with security."),
            ("Mussafah and Industrial Moves: Access and Safety", "Commercial zones, loading areas, and crew coordination."),
            ("UAE Public Holidays and Your Moving Schedule", "When crews book up and when roads are quieter."),
            ("Choosing Short-Term Storage Near Your New Abu Dhabi Area", "Proximity, hours, and how it pairs with staggered handovers."),
        ],
    ),
    (
        "company-news",
        "Company News",
        [
            ("Growing Our Team: Training Abu Dhabi’s Next Moving Crews", "How we onboard staff for safe lifting and customer care."),
            ("Fleet Care: How We Service Vehicles for Reliable Moves", "Inspections, tyres, and why well-maintained trucks matter to you."),
            ("Reducing Packing Waste on Local Jobs", "Reusing materials where safe and recycling cardboard."),
            ("Behind Dispatch: Coordinating Moves on Busy Weekends", "How we schedule crews and routes across the emirate."),
            ("Customer Story: A Smooth Villa Move in Mohammed Bin Zayed", "Real timeline, challenges solved, and handover done right."),
            ("Partner Spotlight: Quality Boxes and Supplies in the UAE", "Local suppliers we trust for sturdy packing materials."),
            ("Ramadan Scheduling: Respectful Hours for Crews and Clients", "How we plan moves during the holy month."),
            ("Insurance and Accountability: What Our Customers Should Know", "Licences, coverage basics, and transparent quotes."),
            ("Thank You for Trusting Man With Van Across Abu Dhabi", "A note of gratitude as we continue to grow with families and businesses."),
            ("Safety First: Toolboxes, PPE, and Site Checks", "Standards we follow on every job site."),
        ],
    ),
    (
        "office-moving",
        "Office Moving",
        [
            ("IT Relocation Checklist for Small Abu Dhabi Offices", "Backups, labelling, and what moves before desks."),
            ("Minimising Downtime During an Office Relocation", "Phased moves, weekend slots, and communication plans."),
            ("Packing Confidential Files for Business Moves", "Seals, cartons, and chain-of-custody basics."),
            ("Aligning Fit-Out Dates With Your Office Move", "Avoid paying rent on two spaces longer than needed."),
            ("Office Furniture Disassembly and Reassembly Done Right", "Panels, cable trays, and hardware bags."),
            ("Moving Network Gear and Workstations Safely", "Monitors, docks, and static precautions."),
            ("Employee Announcements: Templates for Office Moves", "Clear timelines reduce confusion on moving week."),
            ("After-Hours vs Weekend Office Moves in the UAE", "Costs, access, and building rules compared."),
            ("Planning Desk Layout Before Boxes Arrive", "Measurements and power—sketch the new floor early."),
            ("Office Handover: Keys, Snags, and Landlord Checklists", "What to document before you return a leased unit."),
        ],
    ),
    (
        "furniture-care",
        "Furniture Care",
        [
            ("Wrapping Sofas and Fabric Furniture for Transport", "Blankets, stretch film, and avoiding compression marks."),
            ("Solid Wood in a Dry Climate: Moving and Acclimatising", "Humidity shifts and hairline checks after delivery."),
            ("Protecting Glass Tabletops and Shelving", "Corner cards, vertical carry, and never stacking heavy on glass."),
            ("When Blankets Beat Plastic for Certain Pieces", "Breathable wraps for leather and polished wood."),
            ("Disassembling Flat-Pack Beds for Safer Moves", "Hardware bags, labelled parts, and torque tips."),
            ("Marble and Stone Surfaces: Handling Without Chips", "Slings, padding, and team lifts only."),
            ("Leather Furniture: Scratches, Temperature, and Covers", "What to avoid during loading and unloading."),
            ("Standing Desks and Motorised Bases on Moving Day", "Reset heights, cable slack, and transport position."),
            ("Antiques and High-Value Pieces: Crating vs Blankets", "When to upgrade protection for irreplaceable items."),
            ("Mattress Protection: Bags, Hygiene, and Storage", "Sealed covers for trucks and short-term storage."),
        ],
    ),
    (
        "cost-saving",
        "Cost Saving",
        [
            ("Declutter Before You Quote: The Fastest Way to Pay Less", "Fewer cubic metres means smaller trucks and fewer hours."),
            ("Why Mid-Week Moves Can Cost Less Than Weekends", "Demand curves and how flexibility saves money."),
            ("Sourcing Sturdy Boxes Without Breaking the Budget", "Retail clean-outs, community groups, and when to buy new."),
            ("Hybrid Packing: Where DIY Makes Sense", "Pack non-breakables yourself; leave glass to pros."),
            ("Selling Furniture Before You Move: Extra Cash, Less Volume", "Marketplaces and timing two weeks out."),
            ("Avoiding Rush Booking Fees With Early Confirmation", "Last-minute premiums explained."),
            ("Combining Small Shipments: When Shared Loads Help", "Same building or neighbourhood—ask what’s possible."),
            ("Reviewing Your Quote for Duplicate Line Items", "Spot double charges before you sign."),
            ("Off-Peak Utility Deposits and Move-In Bills", "Staggering handovers to smooth cash flow."),
            ("Budgeting Tips for First-Time Movers in the UAE", "Hidden costs first-timers forget."),
        ],
    ),
    (
        "storage",
        "Storage",
        [
            ("Climate-Controlled Storage: Do You Need It in the UAE?", "Electronics, leather, and artwork—when humidity matters."),
            ("How to Pack a Storage Unit for Easy Access Later", "Aisles, labels, and heavy items on the bottom."),
            ("Short-Term vs Long-Term Storage: Cost Trade-offs", "Monthly rates, minimums, and exit fees to ask about."),
            ("Storing Furniture Between Villa Handover Dates", "Gap weeks and protecting upholstery."),
            ("Access Hours: Questions to Ask Your Storage Provider", "Weekends, evenings, and notice periods."),
            ("Inventory Lists for Items You Leave in Storage", "Photos and serials for insurance and peace of mind."),
            ("Insurance for Goods in Storage: What to Verify", "Inclusions, exclusions, and declared value."),
            ("Seasonal Storage After a Big Move", "Holiday decor and sports gear—rotate without clutter."),
            ("Downsizing With a Storage Unit as a Bridge", "Stagger decisions while you settle in."),
            ("Pickup and Delivery From Storage to Your New Home", "One truck, one team—planning the final mile."),
        ],
    ),
    (
        "dubai-moving",
        "Dubai Moving",
        [
            ("Abu Dhabi to Dubai: What Changes in Your Move Plan", "Distance, timing on Sheikh Zayed Road, and crew hours."),
            ("High-Rise Moves in Dubai Marina: Access Tips", "Loading docks, height limits, and bookings."),
            ("Cross-Emirate Traffic: Best Windows for Truck Moves", "Friday mornings vs weekday peaks—practical notes."),
            ("Dubai South and Logistics Zones: Planning Extra Time", "Longer distances inside the emirate affect quotes."),
            ("JLT and Business Bay: Parking and Loading Realities", "Permits, basements, and tight turns."),
            ("Hiring Abu Dhabi Movers for a Dubai Job: What to Confirm", "Licensing, insurance, and route planning."),
            ("School Moves Between Dubai and Abu Dhabi", "Term timing and reducing disruption for kids."),
            ("Smaller Dubai Loads: Van vs Truck Decisions", "When a smaller vehicle is enough."),
            ("Return Moves: Dubai Back to Abu Dhabi", "Reverse logistics and what to book early."),
            ("New Dubai Neighbourhoods: First-Week Setup After Moving", "DEWA, cooling, and service apps—quick orientation."),
        ],
    ),
    (
        "villa-moving",
        "Villa Moving",
        [
            ("Outdoor and Garden Furniture Moves for Abu Dhabi Villas", "Cleaning, disassembly, and weather-safe loading."),
            ("Measuring Gates and Driveways Before the Truck Arrives", "Avoid surprises with height bars and tight turns."),
            ("Multi-Storey Villa Moves: Stair Planning With Crews", "Heavy pieces, landings, and rest breaks."),
            ("Sheds, Pools, and Garden Equipment on Moving Day", "Drain lines, tools, and what needs special packing."),
            ("Villa Compound Rules: Timings and Noise in Abu Dhabi", "Community management and courtesy hours."),
            ("Large Dining Sets and Open-Plan Villa Layouts", "Path planning from kitchen to truck."),
            ("Maid’s Room and Storage Areas: Packing Order", "Often last-out, first-in for service quarters."),
            ("Villa Handover Cleaning vs Mover Responsibilities", "What movers do and what landlords expect."),
            ("Outdoor AC Units: Coordinating With Technicians", "Safe disconnect and reinstall timing."),
            ("Sample Timeline for a 4-Bedroom Villa Move", "Packing phases, truck day, and unpack priorities."),
        ],
    ),
    (
        "apartment-moving",
        "Apartment Moving",
        [
            ("Measuring Doorways for Bulky Furniture in Apartments", "Sofas, fridges, and when tilt-and-turn saves the day."),
            ("Booking Service Elevators: A Step-by-Step Guide", "Who to call, what to ask, and buffer time."),
            ("Balcony Furniture: Disassembly and Safety in Towers", "High floors, wind, and building rules."),
            ("Quiet Hours and Moving Rules in Residential Towers", "Avoid complaints with scheduled slots."),
            ("Studio Moves: Maximising Space and Minimising Trips", "Vertical storage and ruthless declutter."),
            ("Shared Loading Bays: Etiquette and Queueing", "Coordination with neighbours and security."),
            ("Why Compact Trucks Matter in Dense Neighbourhoods", "Tight streets and basement ramps in the city."),
            ("Storage Lockers and Cage Units in Apartment Buildings", "Emptying before handover—checklist."),
            ("High-Floor Moves: Protecting Common Areas", "Corner guards and lift padding—who provides what."),
            ("Rented Apartment Move-In Inspection: What to Note", "Snags, photos, and meter readings on arrival."),
        ],
    ),
]


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:55]


def build_body(title: str, category_label: str, excerpt: str) -> str:
    """Unique-ish body from title + category (no external facts)."""
    t = html.escape(title)
    return textwrap.dedent(
        f"""\
            <p><strong>{t}</strong> — {html.escape(excerpt)} This guide is written for families and businesses planning moves across Abu Dhabi and the wider UAE, with practical steps you can use this week.</p>

            <h2>Why this matters</h2>
            <p>Good preparation reduces damage, delays, and surprise costs. Whether you are coordinating with building security, comparing quotes, or packing room by room, a clear plan keeps everyone aligned—especially on busy days when lifts, parking, and timelines compete.</p>

            <h2>Practical steps</h2>
            <ul>
              <li><strong>Plan early:</strong> Confirm dates, access, and parking before you finalise packing.</li>
              <li><strong>Communicate:</strong> Share floor plans, fragile items, and priority rooms with your crew.</li>
              <li><strong>Protect:</strong> Use quality boxes and padding; label boxes by room and handling notes.</li>
              <li><strong>Document:</strong> Photos of high-value items and meter readings help at handover.</li>
            </ul>

            <h2>Working with professional movers</h2>
            <p>Licensed teams bring equipment, experience, and insurance appropriate to the job. Ask for a written quote, clarify what is included (materials, stairs, after-hours), and align on arrival windows. For <strong>{html.escape(category_label.lower())}</strong> topics like this, matching the right truck size and crew to your volume saves time and money.</p>

            <aside class="post-cta-minimal" aria-label="Get a quote">
              <h2>Need help with your move?</h2>
              <p>Tell us your locations, dates, and property type—we’ll reply with a clear quote.</p>
              <div class="post-cta-actions">
                <a href="../get-free-quote.html" class="btn-cta-primary">Get free quote</a>
                <a href="tel:+971508268481" class="btn-cta-outline">Call +971 50 826 8481</a>
              </div>
            </aside>

            <p><strong>Ready to move?</strong> <a href="../get-free-quote.html">Get a free quote</a> or call <a href="tel:+971508268481">+971 50 826 8481</a>. Man With Van—trusted movers across Abu Dhabi and the UAE.</p>
            """
    ).strip()


def page_html(
    slug: str,
    title: str,
    category_label: str,
    excerpt: str,
    body: str,
) -> str:
    title_esc = html.escape(title)
    excerpt_esc = html.escape(excerpt)
    meta_desc = excerpt[:155] + ("…" if len(excerpt) > 155 else "")
    meta_esc = html.escape(meta_desc)
    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": excerpt[:300],
        "author": {"@type": "Organization", "name": "Man With Van"},
        "publisher": {
            "@type": "Organization",
            "name": "Man With Van",
            "logo": {
                "@type": "ImageObject",
                "url": "https://manwithvan.ae/images/logo/logo.png",
            },
        },
        "datePublished": "2026-04-01",
        "dateModified": "2026-04-01",
    }
    ld_script = json.dumps(ld, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_esc} | Man With Van</title>
  <meta name="description" content="{meta_esc}">
  <meta name="keywords" content="movers abu dhabi, {html.escape(category_label.lower())}, moving uae">
  <link rel="icon" type="image/x-icon" href="../images/logo/favicon.ico">
  <link rel="canonical" href="https://manwithvan.ae/blog/{slug}">
  <link rel="stylesheet" href="../css/styles.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <script type="application/ld+json">{ld_script}</script>
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Man With Van - Movers Abu Dhabi">
  <meta property="og:image" content="https://manwithvan.ae/images/blog/heroes/5-essential-tips-stress-free-house-move-uae.webp">
  <meta property="og:url" content="https://manwithvan.ae/blog/{slug}">
  <meta property="og:title" content="{title_esc} | Man With Van">
  <meta property="og:description" content="{meta_esc}">
</head>
<body class="page-with-fixed-header">
  <div id="topbar"></div>
  <div id="header"></div>

  <article class="blog-post-page blog-post-page--editorial">
    <section class="post-hero" aria-labelledby="hero-title">
      <div class="post-hero-image" role="img" aria-label="{title_esc}"></div>
      <div class="post-hero-content">
        <div class="container-narrow">
          <a href="../blog.html" class="back-link">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
            <span>Back to Blog</span>
          </a>
          <div class="post-meta-top">
            <span class="post-category">{html.escape(category_label)}</span>
            <span class="post-date">April 2026</span>
          </div>
          <h1 class="post-title" id="hero-title">{title_esc}</h1>
          <p class="post-excerpt">{excerpt_esc}</p>
        </div>
      </div>
    </section>

    <section class="post-content-section">
      <div class="container-narrow">
        <div class="post-content-wrapper">
          <aside class="related-articles">
            <h3>Related</h3>
            <ul class="related-articles-list">
              <li><a href="how-to-choose-movers-abu-dhabi.html">How to Choose Movers in Abu Dhabi</a></li>
              <li><a href="cost-of-moving-abu-dhabi.html">Cost of Moving in Abu Dhabi</a></li>
              <li><a href="apartment-movers-abu-dhabi.html">Apartment Movers Abu Dhabi</a></li>
              <li><a href="../villa-movers-abu-dhabi.html">Villa Movers Abu Dhabi</a></li>
            </ul>
          </aside>
          <div class="post-main-content">
            <div class="post-body">
{body}
            </div>
            <div class="post-footer">
              <div class="post-author">
                <div class="author-avatar">
                  <svg width="32" height="32" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                </div>
                <div class="author-details">
                  <p class="author-name">Man With Van Team</p>
                  <p class="author-bio">Professional Movers in Abu Dhabi</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </article>

  <div id="footer"></div>
  <div id="wa-chat-widget"></div>
  <div id="scroll-to-top"></div>

  <script src="../js/component-loader.js" defer></script>
  <script src="../js/nav-drawer.js" defer></script>
  <script src="../js/wa-chat-widget.js" defer></script>
  <script src="../js/main.js" defer></script>
</body>
</html>
"""


def card_html(slug: str, title: str, category_key: str, tag: str, excerpt: str) -> str:
    te = html.escape(title)
    ee = html.escape(excerpt)
    return f"""              <article class="blog-card" data-category="{category_key}">
                <a href="blog/{slug}" class="blog-card__img-wrap">
                  <img src="images/blog/heroes/abu-dhabi-living-01-parking-and-loading-rules-for-moving-trucks-in-abu-dhab.webp" alt="{te}" loading="lazy">
                </a>
                <div class="blog-card__body">
                  <span class="blog-card__tag">{html.escape(tag)}</span>
                  <h2 class="blog-card__title"><a href="blog/{slug}">{te}</a></h2>
                  <p class="blog-card__excerpt">{ee}</p>
                  <a href="blog/{slug}" class="blog-card__link">Read More <span>→</span></a>
                </div>
              </article>
"""

# Kept on the listing page alongside generated posts (original URLs).
LEGACY_LISTING_CARDS = """
              <article class="blog-card" data-category="packing-guides moving-tips">
                <a href="blog/how-to-pack-fragile-items.html" class="blog-card__img-wrap">
                  <img src="images/blog/heroes/abu-dhabi-living-02-new-to-khalifa-city-what-movers-wish-you-knew.webp" alt="How to pack fragile items" loading="lazy">
                </a>
                <div class="blog-card__body">
                  <span class="blog-card__tag">Moving Tips</span>
                  <h2 class="blog-card__title"><a href="blog/how-to-pack-fragile-items.html">How to Pack Fragile Items Safely</a></h2>
                  <p class="blog-card__excerpt">Protect dishes, glass, and artwork with these packing techniques. Bubble wrap, boxes, and pro tips.</p>
                  <a href="blog/how-to-pack-fragile-items.html" class="blog-card__link">Read More <span>→</span></a>
                </div>
              </article>

              <article class="blog-card" data-category="moving-tips moving-cost">
                <a href="blog/best-months-to-move-uae.html" class="blog-card__img-wrap">
                  <img src="images/blog/heroes/abu-dhabi-living-03-al-reef-vs-yas-island-lifestyle-notes-for-new-residents.webp" alt="Best months to move in the UAE" loading="lazy">
                </a>
                <div class="blog-card__body">
                  <span class="blog-card__tag">Moving Tips</span>
                  <h2 class="blog-card__title"><a href="blog/best-months-to-move-uae.html">Best Months to Move in the UAE</a></h2>
                  <p class="blog-card__excerpt">When to schedule your move in Abu Dhabi. Weather, availability, and cost considerations.</p>
                  <a href="blog/best-months-to-move-uae.html" class="blog-card__link">Read More <span>→</span></a>
                </div>
              </article>

              <article class="blog-card" data-category="villa-moving moving-guide">
                <a href="blog/villa-moving-checklist-abu-dhabi.html" class="blog-card__img-wrap">
                  <img src="images/blog/heroes/abu-dhabi-living-04-school-timelines-and-how-they-affect-your-move-date.webp" alt="Villa moving checklist Abu Dhabi" loading="lazy">
                </a>
                <div class="blog-card__body">
                  <span class="blog-card__tag">Checklist</span>
                  <h2 class="blog-card__title"><a href="blog/villa-moving-checklist-abu-dhabi.html">Villa Moving Checklist for Abu Dhabi</a></h2>
                  <p class="blog-card__excerpt">A step-by-step checklist for villa moves. From decluttering to handover—never miss a task.</p>
                  <a href="blog/villa-moving-checklist-abu-dhabi.html" class="blog-card__link">Read More <span>→</span></a>
                </div>
              </article>

              <article class="blog-card" data-category="moving-guide">
                <a href="blog/how-to-choose-movers-abu-dhabi.html" class="blog-card__img-wrap">
                  <img src="images/blog/heroes/abu-dhabi-living-05-service-charges-and-moving-what-to-budget-beyond-rent.webp" alt="Choosing movers in Abu Dhabi" loading="lazy">
                </a>
                <div class="blog-card__body">
                  <span class="blog-card__tag">Moving Guide</span>
                  <h2 class="blog-card__title"><a href="blog/how-to-choose-movers-abu-dhabi.html">5 Questions to Ask Before Hiring Movers</a></h2>
                  <p class="blog-card__excerpt">Insurance, quotes, reviews—what to verify when choosing movers in Abu Dhabi.</p>
                  <a href="blog/how-to-choose-movers-abu-dhabi.html" class="blog-card__link">Read More <span>→</span></a>
                </div>
              </article>
"""


def main() -> None:
    cards: list[str] = []
    seen_slugs: set[str] = set()
    n = 0
    for cat_key, cat_label, posts in DATA:
        for i, (title, excerpt) in enumerate(posts):
            base = f"{cat_key}-{i + 1:02d}-{slugify(title)}"
            slug = base + ".html"
            if slug in seen_slugs:
                slug = f"{cat_key}-{i + 1:02d}-{slugify(title)}-{i}.html"
            seen_slugs.add(slug)
            body = build_body(title, cat_label, excerpt)
            body_indented = "\n".join(
                ("              " + line if line.strip() else "").rstrip() for line in body.splitlines()
            )
            out = page_html(slug, title, cat_label, excerpt, body_indented)
            (BLOG / slug).write_text(out, encoding="utf-8")
            cards.append(card_html(slug, title, cat_key, cat_label, excerpt))
            n += 1

    fragment = "\n".join(cards) + "\n" + LEGACY_LISTING_CARDS
    (BLOG / "_generated_cards_snippet.html").write_text(fragment, encoding="utf-8")

    html_text = BLOG_HTML.read_text(encoding="utf-8")
    idx_grid = html_text.find('<div class="blog-card-grid">')
    idx_aside = html_text.find('<aside class="blog-page-sidebar">')
    if idx_grid == -1 or idx_aside == -1:
        raise SystemExit("blog.html structure changed; paste blog/_generated_cards_snippet.html manually")
    before = html_text[:idx_grid]
    grid_chunk = html_text[idx_grid:idx_aside]
    after_aside = html_text[idx_aside:]
    feat_m = re.search(
        r'<article class="blog-card blog-card--featured"[\s\S]*?</article>',
        grid_chunk,
    )
    if not feat_m:
        raise SystemExit("Featured blog card not found in blog.html")
    featured = feat_m.group(0).strip()
    new_html = (
        before
        + '<div class="blog-card-grid">\n              '
        + featured
        + "\n\n"
        + fragment
        + "            </div>\n          </div>\n\n          "
        + after_aside
    )
    BLOG_HTML.write_text(new_html, encoding="utf-8")
    print(f"Wrote {n} posts under blog/ and updated blog.html")


if __name__ == "__main__":
    main()
