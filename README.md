To generate predictions, run populate, then run baseballDB.

Note that the program uses the baseball_scraper library, which may be outdated.
If it fails to run, a "fixed" version can be found in the "fixes" folder.

Due to baseball-reference.com's anti-scraping measures, the scraper has a builtin delay of 10 seconds per team.
This can be reduced, but at the risk of a temporary or permanent IP ban.

Currently, the program does not support season before 2012, due to the hardcoded nature of the divisions and teams.
This will be fixed in a future update, mostly because of the Athletics.
