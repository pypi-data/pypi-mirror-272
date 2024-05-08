
# Version 1.0.1 

+ Add "evaluate" function to all Estimators (RbfRegressor, RbfClassifier, MhaRbfRegressor, MhaRbfClassifier)
+ **Add new module "scaler"**
+ Our scaler can be utilized with multiple methods.
+ Add "save_loss_train" and "save_metrics" functions to all Estimators
+ Add "save_model" and "load_model" functions to all Estimators
+ Add "save_y_predicted" function to all Estimators
+ Update all examples and documents

---------------------------------------------------------------------


# Version 1.0.0 

+ Add supported information for each classes.
+ Restructure evorbf module to based_elm module and model subpackage that includes mha_elm and standard_elm modules.
+ Add traditional/standard RBF models (RbfRegressor and RbfClassifier classes) to standard_elm module.
+ Add examples and tests for traditional models
+ Add score and scores functions to all classes.
+ Fix bug calculate metrics and objective in RBF-based models.
+ Add examples with real-world datasets and examples with GridsearchCV to tune hyper-parameters of RBF-based models.
+ Add documents

---------------------------------------------------------------------

# Version 0.1.0 (First version)

+ Add infors (CODE_OF_CONDUCT.md, MANIFEST.in, LICENSE, README.md, requirements.txt, CITATION.cff)
+ Add helpers modules (`metrics`, `scaler`, `validator`, and `preprocessor`)
+ Add InaRbfRegressor class
+ Add examples and tests folders
