var Evaluator = require('./Evaluator.js');
var evaluator = new Evaluator({truthFile: '/home/yangyan/SHREC2016/dataset_shape_retrieval/val.csv'});
evaluator.evaluate('/home/yangyan/SHREC2016/dataset_shape_retrieval/concatenate/val/val_idsubid_2/');
