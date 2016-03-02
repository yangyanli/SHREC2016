var Evaluator = require('./Evaluator.js');
var evaluator = new Evaluator({truthFile: '/home/yangyan/SHREC2016/dataset_shape_retrieval/train.csv'});
evaluator.evaluate('/home/yangyan/SHREC2016/dataset_shape_retrieval/concatenate/train/train_idsubid/');
