import numpy as np

from Datasets import BaseDataset
from DataSamplers import DataSamplers
from DataTools import set_random_states, get_random_states, reset_random_states
from ResultHandler import ResultHandler
from Classifiers import Classifiers

from imblearn.pipeline import make_pipeline

from sdv.metadata import SingleTableMetadata

np.set_printoptions(precision=2)


# This function uses an ImbLearn Pipeline. Each Oversampling/Under-sampling method MUST support the fit_resample method
# To use plug-and-play implementations that do not implement fit_resample, please use eval_resampling.
# This method has been used in the experiments of the paper:
# L. Aritidis, P. Bozanis, "A Clustering-Based Resampling Technique with Cluster Structure Analysis for Software Defect
# Detection in Imbalanced Datasets", Information Sciences, 2024.
def eval_oversampling_efficacy(datasets, num_threads, random_state):
    """Test the ability of a Generator to improve the performance of a classifier by balancing an imbalanced dataset.
    The Generator performs over-sampling on the minority classes and equalizes the number of samples per class.
    This function uses an ImbLearn Pipeline. Each Oversampling/Under-sampling method MUST support the fit_resample method
    To use plug-and-play implementations that do not implement fit_resample, please use eval_resampling.
    This method has been used in the experiments of the paper:
    L. Aritidis, P. Bozanis, "A Clustering-Based Resampling Technique with Cluster Structure Analysis for Software Defect
    Detection in Imbalanced Datasets", Information Sciences, 2024.

    Algorithm:

      1. For each dataset d, for each classifier c, for each sampler s
      2. Fit s
      3. d_balanced <--- over-sample(d with s)
      4. Test classification performance of c on d_balanced
      5. Steps 2-4 are embedded in a pipe-line; the pipe-line is cross validated with 5 folds.
    """
    set_random_states(random_state)
    np_random_state, torch_random_state, cuda_random_state = get_random_states()

    classifiers = Classifiers(random_state=random_state)

    results_list = []

    order = 0
    # For each input dataset
    x = 0
    for key in datasets.keys():
        x += 1
        # if x > 1:
        #     break
        print("\n=================================\n Evaluating dataset", key, "\n=================================\n")
        reset_random_states(np_random_state, torch_random_state, cuda_random_state)
        ds = datasets[key]
        original_dataset = BaseDataset(ds['name'], random_state=random_state)
        original_dataset.load_from_csv(path=ds['path'], feature_cols=ds['features_cols'], class_col=ds['class_col'])

        dataset_results_list = []

        # Convert all columns to numerical
        metadata = SingleTableMetadata()
        metadata.detect_from_dataframe(original_dataset.df_)
        for k in metadata.columns.keys():
            metadata.columns[k] = {'sdtype': 'numerical'}
        metadata.columns[original_dataset.get_class_column() - 1] = {'sdtype': 'categorical'}

        # For each classifier
        for clf in classifiers.models_:
            samplers = DataSamplers(metadata, sampling_strategy='auto', random_state=random_state)

            # For each over-sampler, balance the input dataset. The fit_resample method of each sampler is called
            # internally by the `imblearn` pipeline and the cross validator.
            for s in samplers.over_samplers_:
                reset_random_states(np_random_state, torch_random_state, cuda_random_state)
                order += 1

                print("Testing", clf.name_, "with", s.name_)

                #pipe_line = make_pipeline(s.sampler_, StandardScaler(), clf.model_)
                pipe_line = make_pipeline(s.sampler_, clf.model_)
                r, _ = original_dataset.cross_val(estimator=pipe_line, num_folds=5, num_threads=num_threads,
                                                  classifier_str=clf.name_, sampler_str=s.name_, order=order)

                for e in range(len(r)):
                    results_list.append(r[e])
                    dataset_results_list.append(r[e])

        # Record the results for this dataset
        drh = ResultHandler("Oversampling", dataset_results_list)
        drh.record_results(key + "_oversampling")

    # Record the results for all datasets
    rh = ResultHandler("Oversampling", results_list)
    rh.record_results("oversampling")
