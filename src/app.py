from . import Scrapper


# ----------------------------------------------------------------------------
""" -----------USE THE SCRIPT AS A COMMAND-LINE INTERFACE------------------"""
# ----------------------------------------------------------------------------
console = argparse.ArgumentParser(description="Web scraping tool for job search", epilog="Good luck with the search!")
console.add_argument("-keyword", metavar="'keyword'", type=str, help="A keyword to look for the desired job")
console.add_argument("-location", metavar="'location'", type=str, help="The location of the job")
console.add_argument("-site", metavar="'site'", type=str, help="The site of the job")

args = console.parse_args()
keyword, location, site = args.job, args.location


scrapper = Scrapper(site, keyword, location)
scrapper.start()