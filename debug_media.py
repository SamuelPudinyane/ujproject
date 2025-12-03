"""
Debug script to check media rendering in posts
"""
import requests
from bs4 import BeautifulSoup
import json

def debug_media_rendering():
    try:
        # Get the posts page
        response = requests.get('http://localhost:9000/post')
        
        if response.status_code != 200:
            print(f"Failed to get posts page: {response.status_code}")
            return
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for swiper slides with media
        swiper_slides = soup.find_all('div', class_='swiper-slide')
        
        print(f"Found {len(swiper_slides)} swiper slides")
        
        for i, slide in enumerate(swiper_slides):
            print(f"\n--- Slide {i+1} ---")
            
            # Check for videos
            videos = slide.find_all('video')
            for video in videos:
                source = video.find('source')
                if source and source.get('src'):
                    print(f"Video source: {source.get('src')}")
                else:
                    print("Video found but no source")
            
            # Check for images
            images = slide.find_all('img')
            for img in images:
                if img.get('src'):
                    print(f"Image source: {img.get('src')}")
                else:
                    print("Image found but no source")
        
        # Also check if there are any swiper containers at all
        swiper_containers = soup.find_all('div', class_='swiper')
        print(f"\nFound {len(swiper_containers)} swiper containers")
        
        # Check for any media-related content in the page
        if 'swiper-slide' in response.text:
            print("✓ Swiper slides are present in HTML")
        else:
            print("✗ No swiper slides found in HTML")
        
        if 'static/uploads' in response.text:
            print("✓ Static/uploads paths found in HTML")
        else:
            print("✗ No static/uploads paths found in HTML")
            
    except requests.exceptions.ConnectionError:
        print("Could not connect to localhost:9000. Make sure the app is running.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_media_rendering()