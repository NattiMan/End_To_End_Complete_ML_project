from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer



num_cols = ["math_score","reading_score"]
cat_cols = ["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
obj2 = DataTransformation("data\studs.csv","data\studs.csv",num_cols,cat_cols)
train_array, test_array, _= obj2.initiate_data_transformation('writing_score')
obj_trainer = ModelTrainer()
error = obj_trainer.initiate_model_trainer(train_array=train_array, test_array=test_array)






print(error)


