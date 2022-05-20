# Master-Thesis: Carbon Footprints of European Central Bank (ECB)

The market-neutral approach followed by the European Central Bank (ECB) for its asset portfolio undermines the EU goal of transitioning to a low carbon economy. This
thesis investigates the extent of carbon emissions taken into account while purchasing bonds to suggest greener pathways. 
The thesis is divided into two parts: 
a) Creating database for Corporate Bond Purchases Program (CSPP) holdings, industry classification, revenue and emissions information.
b) Estimating the carbon intensity using different metrics.

## Instructions for the code
Follow the intructions to use the code:

### 1. Download the code from git
In the code section, click the green button with "code" written on it and download the zip.

### 2. Clone the environment

conda env create -f environment_file.yml 

Run the above command in the terminal to create a virtual environment with the required dependencies.

### 3. Replicating the end-to-end process
In the "Master_Thesis" folder, go to "3. Code" folder and run the python files according to the number written on them. Specific instructions or requiremenrs are mentioned in the file itself.

##### Note:
For downloading the CSPP holdings published by the ECB, (Python file: 1a. CSPP holdings - download portfolio data.ipynb) , the version requirement for Chrome 100.0.4896.127 and make sure to delete the files in the folder Downloaded_Data - Web Scrapping (Master_Thesis > 2. Data >  1. ECB Data). The files are already downloaded, the rest of the code can also be used without running this file as it will require some time to run.

### 4. Replicating the dashboard
The code for creating dashboard is in folder "5. Carbon footprint - dashboard". The required dependencies are available in the requirements file and should be imported before running the code. The interactive dashboard has also been deployed on Heroku for the ease of the reader. (https://carbon-footprint-ecb.herokuapp.com/)

### 5. Network Analysis






