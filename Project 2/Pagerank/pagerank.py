import os
import random
import re
import copy
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    transition = dict()
    
    for pages in corpus:
        transition[pages] = 0

    if len(corpus[page]) > 0:
        for i_page in corpus:
            if i_page not in corpus[page]:
                transition[i_page] = (1 - damping_factor) / len(corpus)
            else:
                transition[i_page] = (damping_factor / len(corpus[page])) + ((1 - damping_factor) / len(corpus))

    else:
        for i_page in corpus: 
            transition[i_page] = 1 / len(corpus)
            
    return transition
    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict()
    dic = dict()
    for page in corpus:
        pagerank[page] = 0
        dic[page] = 0

    # n = 1
    current_page = random.choice(list(corpus.keys()))

    for i in range(1, n):
        if current_page:
            pagerank[current_page] += 1
            dic = transition_model(corpus, current_page, damping_factor)
            current_page = random.choices(list(dic.keys()), list(dic.values()), k=1)[0]
    

    for page in pagerank:
        pagerank[page] /= n
    
    return pagerank
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    p_iterate = dict()
    i_iterate = dict()
    N = len(corpus)
    d = damping_factor

    for page in corpus:
        i_iterate[page] = 1/N
    

    while True:
        for p_page in corpus:
            p_iterate[p_page] = 0 

            for i_page in corpus:
                if p_page in corpus[i_page]: # if page is linked
                    p_iterate[p_page] += i_iterate[i_page] / len(corpus[i_page])

                if len(corpus[i_page]) == 0: # if page is not linked with p in any way
                    p_iterate[p_page] += (i_iterate[i_page]) / len(corpus)

            p_iterate[p_page] *= d # damping 
            p_iterate[p_page] += (1-d)/N # first condition

        diff = max([abs(p_iterate[pg] - i_iterate[pg]) for pg in i_iterate])
        if diff < 0.001:
            break
        else:
            i_iterate = p_iterate.copy()
            

    return i_iterate


if __name__ == "__main__":
    main()
