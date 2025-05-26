# pga_data_scrapers
This repo was created and works as of May 25, 2025. 

This repo contains three files, one Jupyter notebook and two python scripts. 

'statistic_scraping.py' and 'dataset_generation.ipynb' work together. The nuts and bolts are contatined in the python script, while the actual generation with specifications is in the notebook. All you need to do is find your API key, insert it into the script and save, then run the code in the dataset_generation notebook. 

If you are unsure how to find your API key, follow these steps:
1) In Chrome or Firefox: right-click anywhere on the PGA Tour stats (pga tour stats)[https://www.pgatour.com/stats] page and choose Inspect, then switch to the Network tab.
2) Reload the page then in the Network list, type “graphql” to find the POST calls that drive the statDetails endpoint.
3) Click on one of the graphql entries. Under Headers ▶ Request Headers, look for the line: x-api-key: da2-XXXXXXXXXXXXXXXXXXXXXXXX
4) Copy and paste the da2-XXXXXXXXXXXXXXXXXXXXXXXX into both scripts.


