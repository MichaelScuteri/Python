import requests
from bs4 import BeautifulSoup

def get_page(movie_name):
    search_url = f"https://www.justwatch.com/au/search?q={movie_name}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")

    movie = soup.find("span", class_="header-title")
    
    if movie:
        a_tag = soup.find('a', class_="title-list-row__column-header")

        if a_tag and 'href' in a_tag.attrs:
            href_value = a_tag['href']
            full_link = "https://www.justwatch.com" + href_value
            return full_link
    
    if not movie:
        print("Movie not found.")
        return None
    
def get_movie_info(full_link):
    response = requests.get(full_link)
    soup = BeautifulSoup(response.text, "html.parser")

    movie_info = {}
    movie_info['Title'] = soup.select_one("div.title-block h1").text.strip()
    movie_info['Year'] = soup.find("span", class_="text-muted").text.strip().replace("(", "").replace(")", "")
    movie_info['Director'] = soup.find("span", class_="title-credit-name").text.strip()
    movie_info['Rating'] = soup.select_one("div.jw-scoring-listing__rating span").text.strip()
    synopsis_a = soup.select_one("article.article-block p")
    synopsis_b = soup.find("p", class_="text-wrap-pre-line")
    streaming = soup.find("div", class_="buybox-row stream")
    

    if synopsis_a:
        movie_info['Synopsis'] = synopsis_a.text.strip()
    elif synopsis_b:
        movie_info['Synopsis'] = synopsis_b.text.strip()
    else:
        movie_info['Synopsis'] = "Synopsis not available"


    if streaming:
        img_tags = streaming.find_all("img", class_="offer__icon")
        services = [img['alt'] for img in img_tags if 'alt' in img.attrs]
        movie_info['Stream'] = ', '.join(services) if services else "Not available to stream"
    else:
        movie_info['Stream'] = "Not currently available to stream"


    return movie_info


if __name__ == "__main__":
    print("-"*18)
    print("Movie Lookup V1.0")
    print("-"*18)
    while True:
        movie_name = input("Enter movie name: ")
        
        if movie_name.lower() == 'q':
            break

        full_link = get_page(movie_name)
        
        if full_link:
            movie_info = get_movie_info(full_link)
            print(f"\n{movie_info['Title']}")
            print("-"*40)
            print(f"Year: {movie_info['Year']}")
            print(f"Director: {movie_info['Director']}")
            print(f"Rating: {movie_info['Rating']}")
            print(f"\nSynopsis:\n{movie_info['Synopsis']}\n")
            print(f"Available on:\n{movie_info['Stream']}\n")
