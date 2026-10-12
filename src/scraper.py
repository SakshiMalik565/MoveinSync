"""
Automated Play Store Review Ingestion Engine for MoveInSync
Fetches app metadata and comprehensive review datasets across ratings and versions.
"""

import os
import json
import logging
from datetime import datetime
import pandas as pd
from google_play_scraper import app, reviews, Sort

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_APP_ID = "com.moveinsync.ets"

def fetch_app_metadata(app_id: str = DEFAULT_APP_ID) -> dict:
    """Fetch high-level Play Store app metadata."""
    logger.info(f"Fetching app metadata for {app_id}...")
    try:
        app_data = app(app_id)
        metadata = {
            "app_id": app_id,
            "title": app_data.get("title"),
            "score": app_data.get("score"),
            "ratings_count": app_data.get("ratings"),
            "reviews_count": app_data.get("reviews"),
            "histogram": app_data.get("histogram"),
            "installs": app_data.get("installs"),
            "current_version": app_data.get("version"),
            "last_updated": str(app_data.get("updated")),
            "developer": app_data.get("developer"),
            "fetched_at": datetime.utcnow().isoformat()
        }
        logger.info(f"App Metadata: {metadata['title']} | Rating: {metadata['score']}★ | Ratings Count: {metadata['ratings_count']}")
        return metadata
    except Exception as e:
        logger.error(f"Error fetching metadata for {app_id}: {e}")
        return {}

def fetch_reviews(app_id: str = DEFAULT_APP_ID, count_per_sort: int = 400) -> list:
    """
    Fetch reviews using multiple sorting strategies to capture:
    1. Sort.NEWEST: Latest release regressions & recent user sentiment.
    2. Sort.MOST_RELEVANT: High-impact, highly upvoted reviews affecting public brand perception.
    """
    logger.info(f"Fetching reviews for {app_id} (batch count: {count_per_sort} per strategy)...")
    all_reviews_dict = {}

    strategies = [
        ("NEWEST", Sort.NEWEST),
        ("MOST_RELEVANT", Sort.MOST_RELEVANT)
    ]

    for strat_name, sort_order in strategies:
        try:
            logger.info(f"Fetching reviews using strategy: {strat_name}...")
            result, _ = reviews(
                app_id,
                lang="en",
                country="in",
                sort=sort_order,
                count=count_per_sort
            )
            for r in result:
                r_id = r.get("reviewId")
                if r_id and r_id not in all_reviews_dict:
                    # Clean datetime for serialization
                    review_date = r.get("at")
                    review_date_str = review_date.isoformat() if review_date else None
                    
                    all_reviews_dict[r_id] = {
                        "review_id": r_id,
                        "user_name": r.get("userName"),
                        "rating": r.get("score"),
                        "content": r.get("content", "").strip(),
                        "thumbs_up": r.get("thumbsUpCount", 0),
                        "app_version": r.get("reviewCreatedVersion") or "Unknown",
                        "date": review_date_str,
                        "developer_response": r.get("replyContent"),
                        "developer_response_date": str(r.get("repliedAt")) if r.get("repliedAt") else None,
                        "fetch_strategy": strat_name
                    }
        except Exception as e:
            logger.error(f"Failed to fetch reviews with strategy {strat_name}: {e}")

    reviews_list = list(all_reviews_dict.values())
    logger.info(f"Successfully collected {len(reviews_list)} unique reviews.")
    return reviews_list

def save_raw_data(metadata: dict, reviews_list: list, output_dir: str = "data") -> None:
    """Save metadata and raw review data to JSON and CSV formats."""
    os.makedirs(output_dir, exist_ok=True)
    
    metadata_path = os.path.join(output_dir, "app_metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Saved metadata to {metadata_path}")

    json_path = os.path.join(output_dir, "raw_reviews.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(reviews_list, f, indent=2)
    logger.info(f"Saved {len(reviews_list)} raw reviews to {json_path}")

    df = pd.DataFrame(reviews_list)
    csv_path = os.path.join(output_dir, "raw_reviews.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")
    logger.info(f"Saved raw reviews CSV to {csv_path}")

def run_scraper(app_id: str = DEFAULT_APP_ID, count: int = 500) -> tuple:
    """End-to-end scraper execution."""
    meta = fetch_app_metadata(app_id)
    revs = fetch_reviews(app_id, count_per_sort=count)
    save_raw_data(meta, revs)
    return meta, revs

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MoveInSync Play Store Review Scraper")
    parser.add_argument("--app_id", default=DEFAULT_APP_ID, help="Google Play Store package ID")
    parser.add_argument("--count", type=int, default=400, help="Number of reviews per strategy")
    args = parser.parse_args()
    
    run_scraper(app_id=args.app_id, count=args.count)
