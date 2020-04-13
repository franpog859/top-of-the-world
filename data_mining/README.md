[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/franpog859/top-of-the-world/blob/master/data_mining/calculate_tops_in_colab.ipynb)

```
backup_to_local.py
    -l --local default="local_tops.json"
    -f --file default="backup.json"
    -p --plot (plot map with tops)
update_database.py 
    -f --file default="local_tops.json"
plot_figures.py
    -d --database 
    -l --local default="local_tops.json"
calculate_tops_in_colab.ipynb
calculate_tops.py 
    -d --dummy (do not save results to the local file)
    -f --file REQUIRED
    -s --step default=1
    -m --margin (mark tops also on the map's 350 km margin)
    -p --plot (plot map and map with tops)
```

To run unit tests run:

```sh
pytest
```