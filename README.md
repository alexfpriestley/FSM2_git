# FSM2 dataframes, plotting and conversion to netcdf 

FSM2_create_dataframes.py takes text file output from Factorial Snow Model 2 [https://www.github.com/RichardEssery/FSM2] and saves some main variables as CSV files.  
These can then be plotted with FSM2_plotting_main_variables.py as some simple plots to get an idea of your model run behaviour.  
If you want to use Meteo France's Centre d'Etude de la Neige's **Snowtools** plotting tools [https://opensource.umr-cnrm.fr/projects/snowtools_git/wiki/Graphical_User_Interface], FSM2_to_snowtools_nc.py
saves your model output in a netCDF file in the correect format for Snowtools.

