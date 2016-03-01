var Evaluator = require('./Evaluator.js');
var evaluator = new Evaluator({truthFile: '/home/yangyan/SHREC2016/dataset_shape_retrieval/val.csv'});
evaluator.evaluate('/home/yangyan/SHREC2016/dataset_shape_retrieval/pooling/val_perturbed/val_perturbed_feature/');
