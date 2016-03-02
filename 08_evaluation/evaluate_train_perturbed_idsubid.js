var Evaluator = require('./Evaluator.js');
var evaluator = new Evaluator({truthFile: '/home/yangyan/SHREC2016/dataset_shape_retrieval/train.csv'});
evaluator.evaluate('/home/yangyan/SHREC2016/dataset_shape_retrieval/pooling/train_perturbed/train_perturbed_idsubid/');
