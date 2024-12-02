import os
from better_bing_image_downloader import downloader

def extract_image_urls(keyword, limit=100):
    """
    Extract image URLs from Bing image search
    
    Args:
    keyword (str): Search term for images
    limit (int): Maximum number of URLs to extract
    
    Returns:
    list: List of image URLs
    """
    # Create output directory
    output_dir = 'dataset'
    os.makedirs(output_dir, exist_ok=True)
    
    # Perform image search and URL extraction
    downloader(
        keyword, 
        limit=limit, 
        output_dir=output_dir, 
        adult_filter_off=True, 
        force_replace=False, 
        timeout=60, 
        filter="photo", 
        verbose=True, 
        badsites=[],
        name='Image'
    )
    
    # Path to the links file
    links_path = os.path.join(output_dir, f'{keyword}_Image_links.txt')
    
    # Read URLs
    try:
        with open(links_path, 'r') as f:
            urls = f.read().splitlines()
        
        # Remove empty lines and duplicates
        urls = list(dict.fromkeys(filter(bool, urls)))
        
        print(f"Extracted {len(urls)} URLs for {keyword}")
        return urls
    
    except FileNotFoundError:
        print(f"No URLs found for {keyword}")
        return []

# List of keywords to search
keywords = ['Aloo paratha', 'Khakhra', 'Palak Panner']

# Extract URLs for each keyword
all_urls = {}
for keyword in keywords:
    urls = extract_image_urls(keyword)
    all_urls[keyword] = urls

# Print extracted URLs
for keyword, urls in all_urls.items():
    print(f"\nURLs for {keyword}:")
    for url in urls:
        print(url)

# Optionally, save URLs to individual text files
output_dir = 'dataset'
for keyword, urls in all_urls.items():
    with open(os.path.join(output_dir, f'{keyword}_urls.txt'), 'w') as f:
        for url in urls:
            f.write(url + '\n')