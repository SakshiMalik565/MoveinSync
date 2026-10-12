"""
Professional Presentation Generator for MoveInSync FDE Candidate Assignment
Generates a 16:9 executive slide deck using python-pptx.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_filename="MoveInSync_FDE_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank layout

    # Color Palette
    C_NAVY = RGBColor(13, 32, 64)       # Primary Dark
    C_TEAL = RGBColor(0, 163, 196)      # Primary Accent
    C_BLUE = RGBColor(30, 136, 229)     # Secondary Accent
    C_RED = RGBColor(229, 57, 53)       # Alert / P0
    C_BG_LIGHT = RGBColor(245, 247, 250)# Card Background
    C_WHITE = RGBColor(255, 255, 255)
    C_TEXT_DARK = RGBColor(30, 41, 59)
    C_TEXT_MUTED = RGBColor(100, 116, 139)
    C_GREEN = RGBColor(46, 125, 50)
    C_CARD_BORDER = RGBColor(226, 232, 240)

    def add_header(slide, title_text, category_text="MOVEINSYNC • FORWARD DEPLOYED ENGINEER ASSIGNMENT"):
        # Header background banner line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = C_TEAL
        line.line.color.rgb = C_TEAL

        # Category Tracker
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(11.733), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(9.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_TEAL

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.733), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY

    def add_card(slide, left, top, width, height, bg_color=C_BG_LIGHT, border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Executive Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.color.rgb = C_NAVY

    # Decorative Accent Stripe
    stripe = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.8), Inches(0.12), Inches(3.6))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = C_TEAL
    stripe.line.color.rgb = C_TEAL

    tbox1 = s1.shapes.add_textbox(Inches(1.3), Inches(1.6), Inches(10.8), Inches(3.8))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "FORWARD DEPLOYED ENGINEER ASSIGNMENT"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = C_TEAL
    p0.space_after = Pt(12)

    p1 = tf1.add_paragraph()
    p1.text = "MoveInSync Play Store Rating Intelligence & Strategic Action Plan"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p1.space_after = Pt(12)

    p2 = tf1.add_paragraph()
    p2.text = "Diagnosing Rating Degradation, Engineering Next-Day Fixes, and Building a Reusable Pulse Monitor"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_after = Pt(28)

    p3 = tf1.add_paragraph()
    p3.text = "Candidate: Sakshi  •  Target App: MoveInSync (com.moveinsync.ets)  •  Scale: 1.5M+ Commuters / 430+ Enterprises"
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_TEAL

    # =========================================================================
    # SLIDE 2: Executive Summary & The Problem Statement
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Challenge: 'Why Are Our Play Store Ratings Lower Than They Should Be?'")

    # 3 Stat Cards on top
    stat_configs = [
        ("Current Rating", "4.32 ★", "114,880 Lifetime Ratings", C_BLUE),
        ("Daily Scale", "1.5M+", "Daily Commutes Across 430+ Enterprises", C_TEAL),
        ("Negative Review Sample", "46.8%", "1★ & 2★ Reviews Analyzed (42 P0 Blockers)", C_RED)
    ]
    for i, (label, val, sub, col) in enumerate(stat_configs):
        c_left = Inches(0.8 + i * 4.0)
        card = add_card(s2, c_left, Inches(1.5), Inches(3.733), Inches(1.4), C_BG_LIGHT)
        tb = s2.shapes.add_textbox(c_left + Inches(0.2), Inches(1.6), Inches(3.333), Inches(1.2))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = label.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_MUTED
        
        p_val = tf.add_paragraph()
        p_val.text = val
        p_val.font.size = Pt(26)
        p_val.font.bold = True
        p_val.font.color.rgb = col
        
        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(9.5)
        p_sub.font.color.rgb = C_TEXT_DARK

    # Bottom 2 columns: The Core Mandate & Key Takeaway
    # Left Card: Mandate
    add_card(s2, Inches(0.8), Inches(3.1), Inches(5.7), Inches(3.8))
    tb_m = s2.shapes.add_textbox(Inches(1.0), Inches(3.25), Inches(5.3), Inches(3.5))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    p = tf_m.paragraphs[0]
    p.text = "THE FDE PROBLEM BRIEF"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    bullets_m = [
        "Core Question: Work out why ratings are where they are, and tell us exactly what to fix first.",
        "Engineering Readiness: Recommendations must be specific enough that product and engineering can start the next day.",
        "Recurring Capability: 'How are our ratings?' is a recurring leadership ask, requiring a reusable automated pipeline, not a one-off report.",
        "Enterprise Stakes: Enterprise commuters rely on MoveInSync for shift-critical daily transport; app failures immediately disrupt office operations."
    ]
    for b in bullets_m:
        p_b = tf_m.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_TEXT_DARK
        p_b.space_after = Pt(8)

    # Right Card: Core Discovery
    add_card(s2, Inches(6.8), Inches(3.1), Inches(5.733), Inches(3.8))
    tb_d = s2.shapes.add_textbox(Inches(7.0), Inches(3.25), Inches(5.333), Inches(3.5))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True
    p = tf_d.paragraphs[0]
    p.text = "THE ROOT CAUSE DISCOVERY"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    bullets_d = [
        "1. Mobile App Crashes (48.2%): Room DB schema migration errors freeze splash screens on app updates, forcing uninstalls.",
        "2. Tracking & ETA Drift (24.6%): Map viewport auto-zooms out every 3s; ETAs diverge drastically from live traffic.",
        "3. OTP Gatekeeper Friction: Safety popups block the 'View OTP' button, delaying cab boarding under tight morning rosters.",
        "4. The Spite Review Loop (5.4%): An unskippable post-trip feedback dialog blocks commuters, driving angry users to Play Store for 1-star revenge reviews."
    ]
    for b in bullets_d:
        p_b = tf_d.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = C_TEXT_DARK
        p_b.space_after = Pt(8)

    # =========================================================================
    # SLIDE 3: Engineering Approach & System Architecture
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Our Engineering Approach: End-to-End Intelligence Pipeline")

    steps = [
        ("1. Data Ingestion Engine", "• Scraped com.moveinsync.ets\n• Dual-strategy harvesting (NEWEST + MOST_RELEVANT)\n• Extracted 756 reviews, version tags, timestamps & upvotes\n• Saved to raw JSON/CSV", C_BLUE),
        ("2. Multi-Axis Classifier", "• Categorized into 6 functional groups\n• Mapped across 7 journey stages\n• Separated Tech Bugs vs Ground Ops vs Policy vs UX\n• Assigned Severity (P0, P1, P2)", C_TEAL),
        ("3. Impact & Drag Scoring", "• Formula: Drag = (5 - Rating) × (1 + 0.5×ThumbsUp) × Severity\n• Detected version regressions\n• Isolated high-impact community blockers", C_NAVY),
        ("4. Reusable Outputs", "• Jira-ready user stories & PRDs\n• Interactive Streamlit Dashboard\n• Play Store Rating Growth Hack\n• Weekly cron-ready architecture", C_GREEN)
    ]

    for i, (title, details, col) in enumerate(steps):
        left = Inches(0.8 + i * 2.98)
        add_card(s3, left, Inches(1.6), Inches(2.8), Inches(5.1))
        
        # Color bar top
        cbar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.6), Inches(2.8), Inches(0.1))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = col
        cbar.line.color.rgb = col
        
        tb = s3.shapes.add_textbox(left + Inches(0.15), Inches(1.85), Inches(2.5), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(12)
        
        for line in details.split("\n"):
            p_line = tf.add_paragraph()
            p_line.text = line
            p_line.font.size = Pt(10.5)
            p_line.font.color.rgb = C_TEXT_DARK
            p_line.space_after = Pt(6)

    # =========================================================================
    # SLIDE 4: Root Cause Taxonomy: Separating Tech vs Ops vs Policy
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Data Analysis: The 4 Failure Dimensions of MoveInSync")

    dims = [
        ("Mobile & Software Tech Bugs", "48.2% of Negative Reviews", "Mobile Android & Backend Infra",
         "• App update crashes & infinite splash screen freeze\n• Map camera viewport auto-zoom reset bug\n• Session auth token drops / unexpected logouts\n• Push notification sync failures", C_RED),
        ("Routing & ETA Tracking Engine", "24.6% of Negative Reviews", "Routing Algorithm & Maps Team",
         "• Massive ETA divergence from Google Maps traffic\n• Excessive multi-passenger pooling detours ('Bharat Darshan')\n• GPS car marker jumping & freezing on routes\n• Static transit speeds failing during rush hours", C_BLUE),
        ("Ground Fleet & Driver Ops", "21.8% of Negative Reviews", "Fleet Operations & Transport Desk",
         "• Driver tardiness and unauthorized cancellations\n• Driver phone bridge / VoIP number masking failures\n• AC turned off / vehicle cleanliness disputes\n• Transport desk escalation resolution delays", C_NAVY),
        ("UX Friction & Policy Gates", "5.4% of Negative Reviews", "Product Design & UX",
         "• Unskippable post-trip feedback dialog blocks app\n• Seatbelt safety modal blocks 'View OTP' button\n• Unclear waitlist status vs confirmed booking\n• Inability to edit drop location during active trip", C_TEAL)
    ]

    for i, (title, sub, owner, pts, col) in enumerate(dims):
        col_idx = i % 2
        row_idx = i // 2
        left = Inches(0.8 + col_idx * 5.95)
        top = Inches(1.6 + row_idx * 2.7)
        
        add_card(s4, left, top, Inches(5.75), Inches(2.5))
        
        # Header strip
        tb = s4.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.35), Inches(2.2))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title.upper()
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col
        
        p_sub = tf.add_paragraph()
        p_sub.text = f"{sub}  |  Owner: {owner}"
        p_sub.font.size = Pt(9.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = C_TEXT_MUTED
        p_sub.space_after = Pt(6)
        
        for pt in pts.split("\n"):
            p_pt = tf.add_paragraph()
            p_pt.text = pt
            p_pt.font.size = Pt(10)
            p_pt.font.color.rgb = C_TEXT_DARK
            p_pt.space_after = Pt(3)

    # =========================================================================
    # SLIDE 5: Commuter Journey Lifecycle Audit
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Journey Touchpoint Audit: Where Commuters Experience Friction")

    stages_data = [
        ("1. Roster & Login", "50 Issues", "Splash freeze on launch, session auth logout", C_BLUE),
        ("2. Ride Booking", "79 Issues", "Waitlist ambiguity, strict cutoff locks", C_BLUE),
        ("3. Cab Allocation", "18 Issues", "Long detours, suboptimal pooling logic", C_TEAL),
        ("4. Live Tracking", "82 Issues", "Map auto-zoom out, GPS drift, ETA inaccurate", C_RED),
        ("5. Boarding & OTP", "18 Issues", "Safety popup blocks OTP, SMS delay", C_RED),
        ("6. In-Transit", "7 Issues", "Driver route disputes, AC issues, SOS checks", C_NAVY),
        ("7. Post-Trip", "20 Issues", "Forced unskippable rating modal", C_RED)
    ]

    for i, (stg, count, desc, col) in enumerate(stages_data):
        left = Inches(0.8 + (i % 4) * 2.95)
        top = Inches(1.6 + (i // 4) * 2.65)
        width = Inches(2.78)
        height = Inches(2.4)
        
        if i == 6: # Make 7th card span width or fit nicely
            width = Inches(5.73)
            
        add_card(s5, left, top, width, height)
        tb = s5.shapes.add_textbox(left + Inches(0.15), top + Inches(0.15), width - Inches(0.3), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = stg
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        
        p_c = tf.add_paragraph()
        p_c.text = count
        p_c.font.size = Pt(16)
        p_c.font.bold = True
        p_c.font.color.rgb = col
        p_c.space_after = Pt(4)
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 6: App Version Regression Audit
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Release Regression Audit: Pinpointing Faulty App Updates")

    # Left: Table / Breakdown
    add_card(s6, Inches(0.8), Inches(1.6), Inches(6.8), Inches(5.1))
    tb_tab = s6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(6.4), Inches(4.7))
    tf_tab = tb_tab.text_frame
    tf_tab.word_wrap = True
    
    p = tf_tab.paragraphs[0]
    p.text = "APP VERSION PERFORMANCE & REGRESSIONS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    regressions = [
        ("v11.4.13 (1.14 ★)", "Severe map regression: Viewport resets and zooms out every 3s."),
        ("v12.11.2 (1.96 ★)", "Authentication regression: Invalids session token on app relaunch."),
        ("v12.16.1 (1.92 ★)", "Room DB schema migration crash: App freezes on splash screen."),
        ("v12.17.0 (3.54 ★)", "False-positive update prompt: Urges update when already latest."),
        ("v12.19.0 (3.62 ★)", "UX regression: Added seatbelt popup directly over View OTP button.")
    ]
    for v_title, v_desc in regressions:
        p_v = tf_tab.add_paragraph()
        p_v.text = f"{v_title} — {v_desc}"
        p_v.font.size = Pt(10.5)
        p_v.font.color.rgb = C_TEXT_DARK
        p_v.space_after = Pt(8)

    # Right: Key Architectural Lessons
    add_card(s6, Inches(7.8), Inches(1.6), Inches(4.733), Inches(5.1), bg_color=C_BG_LIGHT)
    tb_les = s6.shapes.add_textbox(Inches(8.0), Inches(1.8), Inches(4.333), Inches(4.7))
    tf_les = tb_les.text_frame
    tf_les.word_wrap = True
    
    p = tf_les.paragraphs[0]
    p.text = "ARCHITECTURAL TAKEAWAYS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(10)

    lessons = [
        "1. Schema Migration Fallbacks: Local Room SQLite upgrades must never fail uncaught; implement graceful fallback clearing non-auth cache.",
        "2. Viewport Gesture Latching: Never re-center maps automatically when user touch gestures are detected.",
        "3. Decouple Safety from Core Tasks: Safety prompts should be passive banners, never blocking modals over critical buttons (OTP).",
        "4. Staged Rollouts & Crash Gate: Halt releases on Play Console if launch crashes exceed 0.25% in the first 48 hours."
    ]
    for les in lessons:
        p_l = tf_les.add_paragraph()
        p_l.text = les
        p_l.font.size = Pt(10)
        p_l.font.color.rgb = C_TEXT_DARK
        p_l.space_after = Pt(8)

    # =========================================================================
    # SLIDE 7: Prioritized Engineering Backlog (Start Tomorrow)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Prioritized Action Plan: Jira-Ready Engineering Backlog")

    tickets = [
        ("MIS-TECH-P0-01", "P0 - BLOCKER", "Mobile Android",
         "Fix App Crash & Splash Freeze on Update",
         "Root Cause: Room DB migration exception on Application.onCreate().\nFix: Fallback migration handler + soft cache reset.", C_RED),
        ("MIS-TECH-P0-02", "P0 - BLOCKER", "Mobile & Backend",
         "Decouple Boarding OTP from Blocking Modals",
         "Root Cause: Safety modal blocks OTP; SMS fallback delays.\nFix: Home-card OTP display + offline local token caching.", C_RED),
        ("MIS-PROD-P1-01", "P1 - HIGH", "Product Design UX",
         "Deprecate Unskippable Post-Trip Rating Modal",
         "Root Cause: Forced gate drives commuters to Play Store for spite reviews.\nFix: Add prominent 'Skip' / 'Later' button.", C_BLUE),
        ("MIS-TECH-P1-02", "P1 - HIGH", "Mobile Android (Maps)",
         "Fix Map Viewport Camera State Reset Bug",
         "Root Cause: Map bounding box animates on every WebSocket packet.\nFix: Latch user gesture touch listener; add 'Re-center' button.", C_BLUE),
        ("MIS-ALGO-P1-03", "P1 - HIGH", "Routing Algorithm",
         "Cap Multi-Passenger Pooling Detour Ratios",
         "Root Cause: Optimization ignores individual trip detour limits.\nFix: Enforce Max Detour <= 1.35x direct travel time + live traffic feeds.", C_NAVY),
        ("MIS-TECH-P2-01", "P2 - MEDIUM", "Mobile Android",
         "Fix False-Positive 'Update Required' Nag Screen",
         "Root Cause: Faulty string comparison against remote config.\nFix: Standardize on Google Play In-App Updates SDK (versionCode).", C_TEAL)
    ]

    for i, (tid, prio, team, title, desc, col) in enumerate(tickets):
        c_idx = i % 3
        r_idx = i // 3
        left = Inches(0.8 + c_idx * 3.98)
        top = Inches(1.6 + r_idx * 2.65)
        
        add_card(s7, left, top, Inches(3.8), Inches(2.45))
        tb = s7.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), Inches(3.5), Inches(2.2))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = f"[{tid}] {prio}"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col
        
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(11.5)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY
        p_t.space_after = Pt(4)
        
        p_team = tf.add_paragraph()
        p_team.text = f"Team: {team}"
        p_team.font.size = Pt(9.5)
        p_team.font.color.rgb = C_TEXT_MUTED
        p_team.space_after = Pt(4)
        
        for d in desc.split("\n"):
            p_d = tf.add_paragraph()
            p_d.text = d
            p_d.font.size = Pt(9.5)
            p_d.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 8: 30-60-90 Day Execution Roadmap
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Roadmap: 'What to Do First' Across 30 - 60 - 90 Days")

    phases = [
        ("Sprint 1: Days 1-14", "Stop the Bleeding (P0 Blockers)",
         "• Deploy hotfix for SQLite Room DB update crash\n• Decouple View OTP button from safety modal\n• Add 'Skip' button to post-trip rating modal\n• Halt spite review creation immediately\n• Target: Stabilize crash-free rate at >99.7%", C_RED),
        ("Sprint 2: Days 15-45", "Core Experience & Growth Engine",
         "• Fix Map camera auto-zoom gesture latching\n• Cap pooling detour ratios at 1.35x in routing algo\n• Integrate Google Play In-App Review API\n• Launch internal escalation hotline for delayed trips\n• Target: Lift store rating from 4.32 to 4.50★", C_BLUE),
        ("Sprint 3: Days 46-90", "Operational Maturity & Scale",
         "• Roll out in-app driver chat & VoIP bridge fallback\n• Deploy automated Play Store developer response bot\n• Implement offline Dynamic QR Code boarding passes\n• Target: Achieve 4.70★ sustained store rating", C_GREEN)
    ]

    for i, (p_title, p_sub, p_desc, col) in enumerate(phases):
        left = Inches(0.8 + i * 3.98)
        add_card(s8, left, Inches(1.6), Inches(3.8), Inches(5.1))
        
        # Color accent banner
        cbar = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.6), Inches(3.8), Inches(0.1))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = col
        cbar.line.color.rgb = col
        
        tb = s8.shapes.add_textbox(left + Inches(0.2), Inches(1.85), Inches(3.4), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        
        p_sub_t = tf.add_paragraph()
        p_sub_t.text = p_sub
        p_sub_t.font.size = Pt(11)
        p_sub_t.font.bold = True
        p_sub_t.font.color.rgb = C_NAVY
        p_sub_t.space_after = Pt(14)
        
        for line in p_desc.split("\n"):
            p_l = tf.add_paragraph()
            p_l.text = line
            p_l.font.size = Pt(10.5)
            p_l.font.color.rgb = C_TEXT_DARK
            p_l.space_after = Pt(8)

    # =========================================================================
    # SLIDE 9: The Reputation Growth Hack (4.32★ to 4.70★+)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "The Rating Intercept Engine: Mathematical Path to 4.7★")

    # Left Card: The Math & Mechanism
    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.8), Inches(5.1))
    tb_math = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.4), Inches(4.7))
    tf_math = tb_math.text_frame
    tf_math.word_wrap = True
    
    p = tf_math.paragraphs[0]
    p.text = "THE ASYMMETRIC BIAS OF ENTERPRISE COMMUTES"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)

    math_bullets = [
        "Negativity Bias: 1.5M commuters ride MoveInSync daily. When rides go smoothly, commuters never rate the app. When a cab is late, they vent on Play Store.",
        "The In-App Review API: Google allows prompting native 5-star reviews directly within the app without navigating to Play Store.",
        "Qualification Criteria: Trigger prompt ONLY when an employee completes >= 5 on-time rides with 5-star internal driver ratings.",
        "The Conversion Math: Capturing just 0.5% of satisfied daily commuters = ~7,500 organic 5-star reviews per month.",
        "Outcome: Dilutes historical negative reviews and lifts rating to 4.65-4.70★ within 60 days."
    ]
    for b in math_bullets:
        p_b = tf_math.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = C_TEXT_DARK
        p_b.space_after = Pt(8)

    # Right Card: The Deflection Gate
    add_card(s9, Inches(6.9), Inches(1.6), Inches(5.633), Inches(5.1))
    tb_def = s9.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.233), Inches(4.7))
    tf_def = tb_def.text_frame
    tf_def.word_wrap = True
    
    p = tf_def.paragraphs[0]
    p.text = "THE NEGATIVE REVIEW DEFLECTION GATE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.space_after = Pt(8)

    def_bullets = [
        "Catch Delays Before Play Store: If a cab is >15 minutes late or cancelled, pop an instant 'Connect to Transport Desk' hotline.",
        "Internal Resolution: Resolve the employee's transportation problem in real time (instant alternate cab dispatch or manager note).",
        "Kill the Rating Modal Gate: Never lock the user out of the app with mandatory rating screens.",
        "Automated Developer Reply SLA: Respond to 1★ reviews on Play Console within 4 hours with direct corporate escalation links."
    ]
    for b in def_bullets:
        p_b = tf_def.add_paragraph()
        p_b.text = "• " + b
        p_b.font.size = Pt(10.5)
        p_b.font.color.rgb = C_TEXT_DARK
        p_b.space_after = Pt(8)

    # =========================================================================
    # SLIDE 10: The Reusable Capability & Demo Dashboard
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Recurring Capability: Answering 'How Are Our Play Store Ratings?'")

    cards10 = [
        ("Continuous Ingestion Pipeline", "• Modular python scraper in src/scraper.py\n• Scheduled via GitHub Actions / weekly cron\n• Automated de-duplication on reviewId\n• Exports clean JSON and CSV datasets", C_BLUE),
        ("Multi-Axis NLP Classifier", "• Evaluates incoming reviews automatically\n• Categorizes by team ownership & touchpoint\n• Computes Rating Drag Score\n• Detects version regressions in real time", C_TEAL),
        ("Interactive Executive Dashboard", "• Built in Streamlit (app.py)\n• Dynamic filters: Rating, Category, Version, Team\n• Visual regression timeline & sentiment charts\n• Jira ticket viewer with user quotes & solutions", C_NAVY),
        ("Turnkey Production Deliverables", "• RECOMMENDATION_REPORT.md (C-Level doc)\n• ARCHITECTURE.md (Technical system design)\n• Complete codebase pushed to GitHub\n• Ready for team adoption tomorrow", C_GREEN)
    ]

    for i, (title, desc, col) in enumerate(cards10):
        left = Inches(0.8 + i * 2.98)
        add_card(s10, left, Inches(1.6), Inches(2.8), Inches(5.1))
        
        cbar = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.6), Inches(2.8), Inches(0.1))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = col
        cbar.line.color.rgb = col
        
        tb = s10.shapes.add_textbox(left + Inches(0.15), Inches(1.85), Inches(2.5), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(12)
        
        for line in desc.split("\n"):
            p_l = tf.add_paragraph()
            p_l.text = line
            p_l.font.size = Pt(10.5)
            p_l.font.color.rgb = C_TEXT_DARK
            p_l.space_after = Pt(6)

    # =========================================================================
    # SLIDE 11: Conclusion & Next Steps (Dark Theme)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    bg11 = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg11.fill.solid()
    bg11.fill.fore_color.rgb = C_NAVY
    bg11.line.color.rgb = C_NAVY

    tb11 = s11.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(10.9), Inches(4.5))
    tf11 = tb11.text_frame
    tf11.word_wrap = True

    p = tf11.paragraphs[0]
    p.text = "FORWARD DEPLOYED ENGINEERING MANDATE"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    p.space_after = Pt(12)

    p_t = tf11.add_paragraph()
    p_t.text = "Summary: Turning Customer Feedback into Reusable Platform Excellence"
    p_t.font.size = Pt(28)
    p_t.font.bold = True
    p_t.font.color.rgb = C_WHITE
    p_t.space_after = Pt(20)

    recap_pts = [
        "1. Grounded in Real Data: 756 real Play Store reviews audited, identifying 42 P0 critical blockers.",
        "2. Ready for Tomorrow: 6 detailed Jira tickets with technical root causes, code solutions, and acceptance criteria.",
        "3. Not a One-Time Ask: Full automated pipeline and interactive dashboard ready for continuous monitoring.",
        "4. Mathematical Path to 4.7★: Google In-App Review API strategy tapping into 1.5M daily satisfied commuters.",
        "5. Codebase & Deliverables: Live on GitHub at https://github.com/SakshiMalik565/MoveinSync.git"
    ]
    for r in recap_pts:
        p_r = tf11.add_paragraph()
        p_r.text = r
        p_r.font.size = Pt(13)
        p_r.font.color.rgb = RGBColor(226, 232, 240)
        p_r.space_after = Pt(10)

    # Save
    prs.save(output_filename)
    print(f"Presentation saved successfully to {output_filename}")

if __name__ == "__main__":
    create_deck()
