"""
Intelligent Taxonomy & Root Cause Analyzer for MoveInSync Reviews
Performs multi-dimensional classification across:
1. Category (Tech Bug, Tracking/ETA, Ground Ops/Driver, UX/Policy, Communication/OTP, Positive)
2. Employee Journey Stage (Roster/Auth -> Booking -> Routing -> Tracking -> Boarding/OTP -> In-Transit -> Post-Trip)
3. Severity / Priority Level (P0 Critical, P1 High, P2 Medium, P3 Low)
4. Engineering Team Ownership (Android Eng, Backend Eng, Algorithm Team, UX, Ground Ops)
"""

import os
import re
import json
import logging
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Keyword Rule Sets for High-Fidelity Classification
CATEGORY_KEYWORDS = {
    "TECH_BUG": [
        "crash", "crashes", "freeze", "freezing", "stuck", "blank screen", "opening screen",
        "splash", "white screen", "not opening", "uninstall", "reinstall", "logout", "logged out",
        "logs out", "bug", "bugs", "glitch", "error", "failed", "update made it worse",
        "update is worse", "older version", "zoom out", "zooming", "slow", "hang"
    ],
    "TRACKING_NAVIGATION": [
        "tracking", "track", "live tracking", "gps", "eta", "location", "map", "miles",
        "route", "routing", "detour", "delay", "jumping", "accuracy", "zoom", "bharat darshan",
        "google maps", "calculator", "estimated time"
    ],
    "COMMUNICATION_OTP": [
        "otp", "otps", "password", "verification", "sms", "notification", "notifications",
        "call driver", "calling", "connect to the driver", "dialing", "masking", "chat"
    ],
    "UX_POLICY": [
        "forcing", "force", "mandatory", "no skip", "rating after every ride", "rate",
        "feedback form", "waitlist", "confusing", "multiple clicks", "complex",
        "cut off", "cutoff", "rule", "manager", "policy"
    ],
    "GROUND_OPS_DRIVER": [
        "driver", "cab", "driver behavior", "rash", "rude", "cleanliness", "ac",
        "air conditioner", "late", "cancelled", "refused", "no show", "vendor", "vehicle"
    ]
}

JOURNEY_STAGES = {
    "Roster_&_Authentication": [
        "login", "logout", "logged out", "logs out", "password", "opening screen",
        "splash", "not opening", "open the app", "register", "roster", "sso"
    ],
    "Ride_Booking_&_Scheduling": [
        "booking", "book", "booked", "schedule", "self booking", "waitlist",
        "calendar", "shift", "cutoff", "cancel booking", "monthly view", "day view"
    ],
    "Cab_Allocation_&_Routing": [
        "route", "routing", "detour", "algorithm", "allocation", "pooling",
        "cross-country", "long route", "drop order", "pickup order"
    ],
    "Live_Tracking_&_ETA": [
        "tracking", "track", "gps", "eta", "map", "location", "zoom",
        "van location", "cab location", "live location", "google map"
    ],
    "Boarding_&_OTP_Verification": [
        "otp", "board", "boarding", "verification", "start trip", "end otp",
        "driver verification", "qr code", "passengers list", "passenger picked"
    ],
    "Driver_Communication_&_Transit": [
        "call driver", "driver number", "calling", "driver behavior", "rash",
        "speed", "safety", "sos", "ac", "driver refused", "in-cab"
    ],
    "Post_Trip_&_Feedback_Support": [
        "rating after every ride", "feedback", "transport desk", "support",
        "help desk", "escalate", "customer care", "complaint"
    ]
}

TEAM_OWNERSHIP = {
    "Mobile_Android_Eng": [
        "crash", "freeze", "blank screen", "opening screen", "splash", "zoom out",
        "zooming", "update", "push notification", "multiple clicks", "ui"
    ],
    "Backend_Infra_Eng": [
        "otp", "sms", "server", "sync", "desync", "logged out", "token", "auth",
        "database", "network", "api"
    ],
    "Routing_Algorithm_Team": [
        "route", "routing", "detour", "algorithm", "pooling", "allocation",
        "eta calculator", "eta"
    ],
    "Product_Design_UX": [
        "forcing", "no skip", "rating after every ride", "confusing", "feedback form",
        "waitlist status", "interface", "design"
    ],
    "Fleet_Operations_Desk": [
        "driver", "cab late", "driver behavior", "rude", "cleanliness", "ac off",
        "vendor", "cab cancelled"
    ]
}

def classify_text_rules(text: str, rating: int) -> dict:
    """Classify a single review text into category, journey stage, severity, and team."""
    text_lower = text.lower() if isinstance(text, str) else ""
    
    # Check for pure positive
    if rating >= 4 and not any(kw in text_lower for kw in ["worst", "bad", "bug", "crash", "stuck", "terrible", "issue", "forcing"]):
        return {
            "category": "POSITIVE_EXPERIENCE",
            "journey_stage": "Overall_Experience",
            "severity": "P3_LOW",
            "team": "Product_Leadership",
            "is_tech_issue": False,
            "root_cause_summary": "Satisfied employee praise"
        }

    # Match Category
    category_scores = {cat: 0 for cat in CATEGORY_KEYWORDS}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                category_scores[cat] += 1
    
    best_cat = max(category_scores, key=category_scores.get)
    if category_scores[best_cat] == 0:
        best_cat = "GENERAL_FEEDBACK" if rating >= 3 else "TECH_BUG"

    # Match Journey Stage
    journey_scores = {stage: 0 for stage in JOURNEY_STAGES}
    for stage, keywords in JOURNEY_STAGES.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                journey_scores[stage] += 1
                
    best_stage = max(journey_scores, key=journey_scores.get)
    if journey_scores[best_stage] == 0:
        best_stage = "Live_Tracking_&_ETA" if "track" in text_lower or "eta" in text_lower else "Overall_Experience"

    # Match Team
    team_scores = {team: 0 for team in TEAM_OWNERSHIP}
    for team, keywords in TEAM_OWNERSHIP.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                team_scores[team] += 1
                
    best_team = max(team_scores, key=team_scores.get)
    if team_scores[best_team] == 0:
        best_team = "Mobile_Android_Eng" if best_cat == "TECH_BUG" else "Fleet_Operations_Desk"

    # Determine Severity
    # P0: App won't open, crash on launch, OTP failure (can't board trip), safety
    p0_triggers = ["not able to open", "not opening", "splash", "crash", "otp", "not sending otp", "sos", "safety", "medical"]
    p1_triggers = ["stuck", "tracking", "eta", "forcing me to give rating", "no skip", "logout every time", "worst"]
    
    if rating <= 2 and any(t in text_lower for t in p0_triggers):
        severity = "P0_CRITICAL"
    elif rating <= 2 and any(t in text_lower for t in p1_triggers):
        severity = "P1_HIGH"
    elif rating <= 3:
        severity = "P2_MEDIUM"
    else:
        severity = "P3_LOW"

    is_tech = best_cat in ["TECH_BUG", "TRACKING_NAVIGATION", "COMMUNICATION_OTP"]

    # Generate Root Cause Summary Snippet
    root_cause = "General user friction"
    if "update" in text_lower and ("crash" in text_lower or "open" in text_lower or "worse" in text_lower):
        root_cause = "App update crash / cache migration failure"
    elif "zoom" in text_lower:
        root_cause = "Map camera reset during live tracking refresh cycle"
    elif "otp" in text_lower:
        root_cause = "SMS/Push OTP delivery latency or state desynchronization"
    elif "forcing" in text_lower and "rating" in text_lower:
        root_cause = "Unskippable post-trip in-app rating modal frustrating users"
    elif "eta" in text_lower:
        root_cause = "ETA divergence from real road traffic conditions"
    elif "logout" in text_lower or "logged out" in text_lower:
        root_cause = "Authentication token expiry / session loss bug"
    elif "driver" in text_lower and "call" in text_lower:
        root_cause = "Driver calling / number masking VoIP bridge failure"
    elif "routing" in text_lower or "detour" in text_lower:
        root_cause = "Suboptimal pooling routing causing lengthy commutes"

    return {
        "category": best_cat,
        "journey_stage": best_stage,
        "severity": severity,
        "team": best_team,
        "is_tech_issue": is_tech,
        "root_cause_summary": root_cause
    }

def analyze_all_reviews(input_path: str = "data/raw_reviews.json", output_dir: str = "data") -> pd.DataFrame:
    """Run taxonomy classification and scoring on the complete raw review dataset."""
    logger.info(f"Loading raw reviews from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        reviews_data = json.load(f)

    analyzed_list = []
    for r in reviews_data:
        classification = classify_text_rules(r.get("content", ""), r.get("rating", 3))
        
        # Calculate Drag Impact Score
        # Higher score = more damage to public rating
        rating_penalty = max(1, 5 - r.get("rating", 3))
        upvotes = r.get("thumbs_up", 0)
        severity_mult = {"P0_CRITICAL": 3.0, "P1_HIGH": 2.0, "P2_MEDIUM": 1.2, "P3_LOW": 0.5}.get(classification["severity"], 1.0)
        
        drag_score = round(rating_penalty * (1 + (upvotes * 0.5)) * severity_mult, 2)
        
        merged_record = {
            **r,
            **classification,
            "drag_score": drag_score
        }
        analyzed_list.append(merged_record)

    df = pd.DataFrame(analyzed_list)
    
    # Save analyzed results
    os.makedirs(output_dir, exist_ok=True)
    json_out = os.path.join(output_dir, "analyzed_reviews.json")
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(analyzed_list, f, indent=2)
    
    csv_out = os.path.join(output_dir, "analyzed_reviews.csv")
    df.to_csv(csv_out, index=False, encoding="utf-8")
    
    logger.info(f"Analyzed {len(df)} reviews and saved to {json_out} and {csv_out}.")
    return df

if __name__ == "__main__":
    analyze_all_reviews()
