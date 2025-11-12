# Battery dispatcher program
## Strageties
Conditions of the current implemented strategy:
* Only Market 1 is considered 
* Battery behaviours are not considered

Detail:
Only buy (charge) in the daytime and sell (discharge) in the evening. In daytime, compare current price with daytime price average across the full time span provided, if it's 5% cheaper then buy 1 unit, otherwise just hold. In the evening, compare current price with evening price average across the full time span provided, if it's 5% more expensive then sell 1 unit, otherwise just hold.

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

