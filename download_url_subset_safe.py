# download_url_subset_safe.py
from datasets import load_dataset
import csv
import os

# Create data directory if not exists
os.makedirs('data/raw/url', exist_ok=True)

print("Downloading 20,000 URLs (safe batch size)...")
ds = load_dataset('phreshphish/phreshphish', split='train', streaming=True)

# Save to CSV in batches of 1000
csv_file = 'data/raw/url/url_subset_20k.csv'
count = 0
batch_size = 20000  # Total to download

with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['url', 'label'])  # header
    for i, sample in enumerate(ds):
        if i >= batch_size:
            break
        writer.writerow([sample['url'], sample['label']])
        if (i+1) % 5000 == 0:
            print(f"Downloaded {i+1} URLs...")

print(f"✅ Saved {batch_size} URLs to {csv_file}")