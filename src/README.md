# Technical Overview
This folder contains the notebook that can was used in the experimentation phase and the code for API and frontend static site.

# License
This project is licensed under the terms of the MIT license.  

See LICENSE file in the root folder for more information.

# Notebook folder
The folder contains the final notebook that can be used for
* Replication of the results
* Changing the configs to create new models.

The output of a single run will produce the following files.

`config.json` - Current config along with  
`examples.png` - 5 examples from the Fliker8k dataset along with original and predicted outputs  
`graph.png` - Accuracy and loss curve of the model during training  
`latest_model.h5` - Serialized model weights  
`model.png` - Current model architecture  
`model_summary.txt` - Current model architecture in text format  
`tokenizer.pickle` - Pickled tokenizer  
`train_validate_features.pkl` - Pickled fetures of training and validation images  
`training_history.log` - Training history for the current config  

`experiment_results.csv` - The output of model evaluation. Contains the configuration values along with the BLEU scored.


Please update the GDrive path for drive integration.

# Running the project

1. Replicate or create new `config.json`, `latest_model.h5`, `tokenizer.pickle` files
2. Update `api.env` to set your private Azure Storage Account details
3. Upload the files to Azure container  

**To run the services locally**  
1. Run `pip install -r requirements.txt` in the `api` directory
2. Run `run_local.bat` in the `api/app` folder
3. Run `run_local.bat` in the `server/html_files` folder
4. Navigate to http://localhost

**To build and run Docker locally**  
1. Make sure you have docker installed.
2. Run `docker-compose -p aiml_project1 up --build`

**To build and run Docker on Azure**  

Follow the commands listed in the `commands.txt` in Powershell for Windows

On Linux the commands should remian the same if the paths for Azure CLI and Docker are set correctly.
