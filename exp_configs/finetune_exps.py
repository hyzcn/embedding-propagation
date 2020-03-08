 

conv4 = {
    "name": "finetuning",
    'backbone':'conv4',
    "depth": 4,
    "width": 1,
    "transform_train": "basic",
    "transform_val": "basic",
    "transform_test": "basic"
}

wrn = {
    "name": "finetuning",
    "backbone": 'wrn',
    "depth": 28,
    "width": 10,
    "transform_train": "wrn_finetune_train",
    "transform_val": "wrn_val",
    "transform_test": "wrn_val"
}

resnet12 = {
    "name": "finetuning",
    "backbone": 'resnet12',
    "depth": 12,
    "width": 1,
    "transform_train": "basic",
    "transform_val": "basic",
    "transform_test": "basic"
}

miniimagenet = {
    "dataset": "miniimagenet",
    "dataset_train": "episodic_miniimagenet",
    "dataset_val": "episodic_miniimagenet",
    "dataset_test": "episodic_miniimagenet",
    "data_root": "./data/mini-imagenet/",
    "n_classes": 64
}

tiered_imagenet = {
    "dataset": "tiered-imagenet",
    "n_classes": 351,
    "dataset_train": "episodic_tiered-imagenet",
    "dataset_val": "episodic_tiered-imagenet",
    "dataset_test": "episodic_tiered-imagenet",
    "data_root": "./data/tiered-imagenet/",
}

cub = {
    "dataset": "cub",
    "n_classes": 100,
    "dataset_train": "episodic_cub",
    "dataset_val": "episodic_cub",
    "dataset_test": "episodic_cub",
    "data_root": "./data/CUB_200_2011/"
}

EXP_GROUPS = {"finetune": []}

for dataset in [cub, miniimagenet, tiered_imagenet]:
    for backbone in [wrn, resnet12, conv4]:
        for norm_prop in [1]:
            for lr in [0.01, 0.001]:
                for shot in [1, 5]:
                    for alpha in [0.2]:
                        for seed in [42]:
                            for train_iters in [100, 600]:
                                for classification_weight in [0, 0.1, 0.5]:
                                    EXP_GROUPS['finetune'] += [{"model": backbone,
                                                                
                                                                # Hardware
                                                                "ngpu": 2,
                                                                "random_seed": seed,

                                                                # Optimization
                                                                "batch_size": 1,
                                                                "target_loss": "val_accuracy",
                                                                "lr": lr,
                                                                "min_lr_decay": 0.0001,
                                                                "weight_decay": 0.0005,
                                                                "patience": 10,
                                                                "max_epoch": 200,
                                                                "train_iters": train_iters,
                                                                "val_iters": 600,
                                                                "test_iters": 600,
                                                                "tasks_per_batch": 1,
                                                                "pretrained_weights_root": "/mnt/datasets/public/research/adaptron_laplace/logs_borgy_pretrain_haven",

                                                                # Model
                                                                "dropout": 0.1,
                                                                "avgpool": True,

                                                                # Data
                                                                'n_classes': dataset["n_classes"],
                                                                "collate_fn": "identity",
                                                                "transform_train": backbone["transform_train"],
                                                                "transform_val": backbone["transform_val"],
                                                                "transform_test": backbone["transform_test"],

                                                                "dataset_train": dataset["dataset_train"],
                                                                'dataset_train_root': dataset["data_root"],
                                                                "classes_train": 5,
                                                                "support_size_train": shot,
                                                                "query_size_train": 15,
                                                                "unlabeled_size_train": 0,

                                                                "dataset_val": dataset["dataset_val"],
                                                                'dataset_val_root': dataset["data_root"],
                                                                "classes_val": 5,
                                                                "support_size_val": shot,
                                                                "query_size_val": 15,
                                                                "unlabeled_size_val": 0,

                                                                "dataset_test": dataset["dataset_test"],
                                                                'dataset_test_root': dataset["data_root"],
                                                                "classes_test": 5,
                                                                "support_size_test": shot,
                                                                "query_size_test": 15,
                                                                "unlabeled_size_test": 0,

                                                                # Hparams
                                                                "embedding_prop" : True,
                                                                "few_shot_weight": 1,
                                                                "classification_weight": classification_weight,
                                                                "rotation_weight": 0,
                                                                "active_size": 0,
                                                                "distance_type": "labelprop",
                                                                "kernel_type": "rbf",
                                                                "kernel_standarization": "all",
                                                                "kernel_bound": "",
                                                                "labelprop_alpha": alpha, 
                                                                "labelprop_scale": 1,
                                                                "norm_prop": norm_prop,
                                                                "rotation_labels": [0],
                                                                }]