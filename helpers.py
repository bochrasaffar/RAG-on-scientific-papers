import re 
def get_cited_works(text):
    author = r"(?:[A-Z][A-Za-z'`-]+)"
    etal = r"(?:et al\.?)"
    additional = f"(?:,? (?:(?:and |& )?{author}|{etal}))"
    year_num = "(?:19|20)[0-9][0-9]"
    page_num = "(?:, p\.? [0-9]+)?" 
    year = fr"(?:, *{year_num}{page_num}| *\({year_num}{page_num}\))"
    regex = fr'\b{author}{additional}*{year}'
    matches = re.findall(regex,text)
    return matches
    