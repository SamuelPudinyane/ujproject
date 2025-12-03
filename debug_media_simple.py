"""
Simple debug script to check media content in posts
"""
import requests

def debug_media():
    try:
        # Test the post route
        response = requests.get('http://localhost:9000/post')
        
        if response.status_code != 200:
            print(f"Failed to get posts page: {response.status_code}")
            return
        
        html_content = response.text
        
        print("=== DEBUGGING MEDIA CONTENT ===")
        print(f"Response status: {response.status_code}")
        print(f"Content length: {len(html_content)}")
        
        # Check for swiper elements
        if 'swiper-slide' in html_content:
            print("✓ Swiper slides found in HTML")
            
            # Count swiper slides
            slide_count = html_content.count('swiper-slide')
            print(f"Number of swiper-slide occurrences: {slide_count}")
        else:
            print("✗ No swiper slides found in HTML")
        
        # Check for media sources
        if 'static/uploads' in html_content:
            print("✓ Static uploads paths found")
            
            # Extract some media paths
            import re
            video_matches = re.findall(r'src="([^"]*\.mp4[^"]*)"', html_content)
            img_matches = re.findall(r'src="([^"]*\.jpg[^"]*)"', html_content)
            
            print(f"Video sources found: {video_matches}")
            print(f"Image sources found: {img_matches}")
        else:
            print("✗ No static/uploads paths found")
        
        # Check for the media data in JavaScript or template variables
        if 'data.media' in html_content:
            print("✓ data.media template variable found")
        else:
            print("✗ data.media template variable not found")
            
        # Look for any media file extensions
        media_extensions = ['.mp4', '.jpg', '.png', '.jpeg', '.gif']
        found_media = []
        for ext in media_extensions:
            if ext in html_content:
                found_media.append(ext)
        
        if found_media:
            print(f"Media file extensions found: {found_media}")
        else:
            print("No media file extensions found in HTML")
        
        # Check a small sample of the HTML around swiper
        if 'swiper' in html_content.lower():
            # Find swiper section
            swiper_start = html_content.lower().find('swiper')
            if swiper_start != -1:
                sample = html_content[max(0, swiper_start-100):swiper_start+500]
                print(f"\nHTML sample around swiper:\n{sample}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_media()