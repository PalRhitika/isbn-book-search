import re, requests
import isbnlib

def normalize_isbn(raw: str) -> str:
    return re.sub(r'[^0-9Xx]', '', raw or '').upper()

#open_library call
def from_openlibrary(isbn: str):
    r = requests.get(f'https://openlibrary.org/isbn/{isbn}.json', timeout=10)
    if r.status_code != 200:
        return None
    data = r.json()
    title = data.get('title')
    publishers = data.get('publishers') or []
    publish_date = data.get('publish_date')

    authors = []
    for a in data.get('authors') or []:
        key = a.get('key')
        if key:
            ar = requests.get(f'https://openlibrary.org{key}.json', timeout=10)
            if ar.status_code == 200:
                name = ar.json().get('name')
                if name:
                    authors.append(name)
    cover = None
    covers = data.get('covers') or []
    if covers:
        cover = f'https://covers.openlibrary.org/b/id/{covers[0]}-L.jpg'
    return {
        "source": "openlibrary",
        "isbn": isbn,
        "title": title,
        "authors": authors,
        "publisher": publishers[0] if publishers else None,
        "published_date": publish_date,
        "cover_image": cover,
    }


#Google books api call
def from_google(isbn: str, api_key: str | None = None):
    params = {'q': f'isbn:{isbn}'}
    if api_key:
        params['key'] = api_key
    r = requests.get('https://www.googleapis.com/books/v1/volumes', params=params, timeout=8)
    if r.status_code != 200:
        return None
    items = r.json().get('items') or []
    if not items:
        return None
    v = items[0].get('volumeInfo', {})
    links = v.get('imageLinks') or {}
    return {
        "source": "google",
        "isbn": isbn,
        "title": v.get('title'),
        "authors": v.get('authors') or [],
        "publisher": v.get('publisher'),
        "published_date": v.get('publishedDate'),
        "cover_image": links.get('thumbnail') or links.get('smallThumbnail'),
    }


#main function to fetch book information
def fetch_book(isbn_raw: str, google_key: str | None = None):
    isbn = normalize_isbn(isbn_raw)
    if not isbn:
        return None

    # Try fetching for Google Books first
    data = from_google(isbn, google_key)
    if data:
        return data

    # Fallback : Open Library
    data = from_openlibrary(isbn)
    if data:
        return data

    # Try conversion ISBN-13 -> ISBN-10 or vice versa
    try:
        if len(isbn) == 13:
            alt = isbnlib.to_isbn10(isbn)
        else:
            alt = isbnlib.to_isbn13(isbn)
        if alt:
            data = from_openlibrary(alt)
            if data:
                return data
    except Exception:
        pass

    # Finally call Google Books api
    return from_google(isbn, google_key)

