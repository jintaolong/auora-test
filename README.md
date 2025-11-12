# Battery dispatcher program
## Strageties
Conditions of the current implemented strategy:
* Only Market 1 is considered 
* Battery behaviours are not considered
* Current price is randonly generated between 0 to 80
* Trading interval is reduce to 2 second for demonstration

Detail:
Only buy (charge) during off-peak hours and sell (discharge) in the peak hours (4pm to 8pm daily). During off-peak hours, compare current price with off-peak price average across the full time span provided, if it's 5% cheaper then buy 1 unit, otherwise just hold. In peak time, compare current price with peak-time price average across the full time span provided, if it's 5% more expensive then sell 1 unit, otherwise just hold.

## How to use it
### Env setup

The following needs to be installed 

* poetry=2.1
* conda/miniforge

Once the above are installed, run the following:

    $ conda env create -f environment.yml
    $ conda activate aurora-test
    $ poetry install -vv 

After this the virtual environment is setup.

### Run battery dispatcher model

To Run the program:
    
    $ conda activate aurora-test
    $ python src/main.py 

