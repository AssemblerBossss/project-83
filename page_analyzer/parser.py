from bs4 import BeautifulSoup


def get_seo_information(content) -> dict[str, str]:
    soup = BeautifulSoup(content, 'html.parser')
    data = {
        'h1': '',
        'title': '',
        'description': '',
    }
    if soup.h1:
        data['h1'] = soup.h1.text
    if soup.title:
        data['title'] = soup.title.text
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    if meta_tag:
        data['description'] = meta_tag['content']
    return data
