#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/3/10
# @Author  : yanxiaodong
# @File    : ppyoloe_plus_m_pipeline.py
"""
from paddleflow.pipeline import Pipeline
from paddleflow.pipeline import CacheOptions
from paddleflow.pipeline import ContainerStep
from paddleflow.pipeline import Artifact
from paddleflow.pipeline import ExtraFS

from gaea_operator.utils import DEFAULT_TRAIN_CONFIG_FILE_NAME, \
    DEFAULT_PADDLEPADDLE_MODEL_FILE_NAME, \
    ModelTemplate
# from gaea_operator.components.transform_eval import transform_eval_step
# from gaea_operator.components.package import package_step
# from gaea_operator.components.inference import inference_step


@Pipeline(
    name="change_ppyoloe_plus",
    cache_options=CacheOptions(enable=False),
)
def pipeline(accelerator: str = "T4",
             extra_fs_name: str = "vistudio",
             extra_fs_mount_path: str = "/home/paddleflow/storage/mnt/fs-root-vistudio",
             windmill_ak: str = "",
             windmill_sk: str = "",
             windmill_endpoint: str = "",
             experiment_kind: str = "",
             experiment_name: str = "",
             modelstore_name: str = "",
             tracking_uri: str = "",
             project_name: str = "",
             scene: str = "",
             train_dataset_name: str = "",
             val_dataset_name: str = "",
             base_train_dataset_name: str = "",
             base_val_dataset_name: str = "",
             train_model_name: str = "",
             train_model_display_name: str = "",
             eval_dataset_name: str = "",
             transform_model_name: str = "",
             transform_model_display_name: str = "",
             ensemble_model_name: str = "",
             ensemble_model_display_name: str = ""):
    """
    Pipeline for ppyoloe_plus_m training eval transform transform-eval package inference.
    """
    base_params = {"flavour": "c4m16gpu1",
                   "queue": "qtrain",
                   "windmill_ak": windmill_ak,
                   "windmill_sk": windmill_sk,
                   "windmill_endpoint": windmill_endpoint,
                   "experiment_name": experiment_name,
                   "experiment_kind": experiment_kind,
                   "tracking_uri": tracking_uri,
                   "project_name": project_name,
                   "model_store_name": modelstore_name,
                   "scene": scene}
    base_env = {"PF_JOB_FLAVOUR": "{{flavour}}",
                "PF_JOB_QUEUE_NAME": "{{queue}}",
                "WINDMILL_AK": "{{windmill_ak}}",
                "WINDMILL_SK": "{{windmill_sk}}",
                "WINDMILL_ENDPOINT": "{{windmill_endpoint}}",
                "EXPERIMENT_KIND": "{{experiment_kind}}",
                "EXPERIMENT_NAME": "{{experiment_name}}",
                "TRACKING_URI": "{{tracking_uri}}",
                "PROJECT_NAME": "{{project_name}}",
                "SCENE": "{{scene}}"}

    train_params = {"train_dataset_name": train_dataset_name,
                    "val_dataset_name": val_dataset_name,
                    "base_train_dataset_name": base_train_dataset_name,
                    "base_val_dataset_name": base_val_dataset_name,
                    "model_name": train_model_name,
                    "model_display_name": train_model_display_name,
                    "advanced_parameters": '{"epoch":"1",'
                                           '"LearningRate.base_lr":"0.00001",'
                                           '"worker_num":"1",'
                                           '"eval_size":"640*640",'
                                           '"TrainReader.batch_size":"8",'
                                           '"model_type":"change_ppyoloe_m"}'}
    train_env = {"TRAIN_DATASET_NAME": "{{train_dataset_name}}",
                 "VAL_DATASET_NAME": "{{val_dataset_name}}",
                 "BASE_TRAIN_DATASET_NAME": "{{base_train_dataset_name}}",
                 "BASE_VAL_DATASET_NAME": "{{base_val_dataset_name}}",
                 "MODEL_NAME": "{{model_name}}",
                 "MODEL_DISPLAY_NAME": "{{model_display_name}}",
                 "ADVANCED_PARAMETERS": "{{advanced_parameters}}",
                 "PF_EXTRA_WORK_DIR": extra_fs_mount_path}
    train_env.update(base_env)
    train_params.update(base_params)
    train = ContainerStep(name="train",
                          docker_env="iregistry.baidu-int.com/windmill-public/train/paddlepaddle:v4.1.2-dev2",
                          parameters=train_params,
                          env=train_env,
                          extra_fs=[ExtraFS(name=extra_fs_name, mount_path=extra_fs_mount_path)],
                          outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                          command=f'package_path=$(python3 -c "import site; print(site.getsitepackages()[0])") && '
                                  f'python3 -m gaea_operator.components.train.change_ppyoloe_plus '
                                  f'--output-model-uri={{{{output_model_uri}}}} '
                                  f'--output-uri={{{{output_uri}}}} '
                                  f'--log_dir={{{{output_uri}}}} '
                                  f'$package_path/paddledet/tools/train.py '
                                  f'-c {{{{output_model_uri}}}}/{DEFAULT_TRAIN_CONFIG_FILE_NAME} '
                                  f'-o save_dir={{{{output_model_uri}}}}')

    eval_params = {"dataset_name": eval_dataset_name,
                   "advanced_parameters": '{"conf_threshold":"0.5",'
                                          '"iou_threshold":"0.5"}'}
    eval_env = {"DATASET_NAME": "{{dataset_name}}",
                "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
    eval_env.update(base_env)
    eval_params.update(base_params)
    eval = ContainerStep(name="eval",
                         docker_env="iregistry.baidu-int.com/windmill-public/train/paddlepaddle:v4.1.2-dev2",
                         parameters=eval_params,
                         env=eval_env,
                         inputs={"input_model_uri": train.outputs["output_model_uri"]},
                         outputs={"output_uri": Artifact(), "output_dataset_uri": Artifact()},
                         command=f'package_path=$(python3 -c "import site; print(site.getsitepackages()[0])") && '
                                 f'python3 -m gaea_operator.components.eval.ppyoloe_plus '
                                 f'--input-model-uri={{{{input_model_uri}}}} '
                                 f'--output-uri={{{{output_uri}}}} '
                                 f'--output-dataset-uri={{{{output_dataset_uri}}}} '
                                 f'--log_dir={{{{output_uri}}}} '
                                 f'$package_path/paddledet/tools/eval.py '
                                 f'-c {{{{input_model_uri}}}}/{DEFAULT_TRAIN_CONFIG_FILE_NAME} '
                                 f'-o weights={{{{input_model_uri}}}}/{DEFAULT_PADDLEPADDLE_MODEL_FILE_NAME}')

    transform_params = {"transform_model_name": transform_model_name,
                        "transform_model_display_name": transform_model_display_name,
                        "scene": "",
                        "accelerator": "T4",
                        "advanced_parameters": '{"iou_threshold":"0.7",'
                                               '"conf_threshold":"0.01",'
                                               '"max_box_num":"30",'
                                               '"max_batch_size":"1",'
                                               '"precision":"fp16",'
                                               '"eval_size":"640*640",'
                                               '"source_framework":"paddle",'
                                               '"model_type":"change_ppyoloe_m"}'}
    transform_env = {"TRANSFORM_MODEL_NAME": "{{transform_model_name}}",
                     "TRANSFORM_MODEL_DISPLAY_NAME": "{{transform_model_display_name}}",
                     "SCENE": "{{scene}}",
                     "ACCELERATOR": "{{accelerator}}",
                     "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
    transform_env.update(base_env)
    transform_params.update(base_params)
    transform = ContainerStep(name="transform",
                              docker_env="iregistry.baidu-int.com/windmill-public/transform:v4.1.2-dev2",
                              env=transform_env,
                              parameters=transform_params,
                              inputs={"input_model_uri": train.outputs["output_model_uri"]},
                              outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                              command=f'python3 -m gaea_operator.components.transform.change_ppyoloe_plus '
                                      f'--input-model-uri={{{{input_model_uri}}}} '
                                      f'--output-uri={{{{output_uri}}}} '
                                      f'--output-model-uri={{{{output_model_uri}}}}').after(eval)

    transform_eval = transform_eval_step(algorithm=ModelTemplate.CHANGE_PPYOLOE_PLUS_NAME,
                                         windmill_ak=windmill_ak,
                                         windmill_sk=windmill_sk,
                                         windmill_endpoint=windmill_endpoint,
                                         experiment_kind=experiment_kind,
                                         experiment_name=experiment_name,
                                         tracking_uri=tracking_uri,
                                         project_name=project_name,
                                         accelerator=accelerator,
                                         eval_step=eval,
                                         transform_step=transform)

    package = package_step(algorithm=ModelTemplate.CHANGE_PPYOLOE_PLUS_NAME,
                           windmill_ak=windmill_ak,
                           windmill_sk=windmill_sk,
                           windmill_endpoint=windmill_endpoint,
                           experiment_kind=experiment_kind,
                           experiment_name=experiment_name,
                           tracking_uri=tracking_uri,
                           project_name=project_name,
                           accelerator=accelerator,
                           transform_step=transform,
                           transform_eval_step=transform_eval,
                           ensemble_model_name=ensemble_model_name,
                           ensemble_model_display_name=ensemble_model_display_name)

    inference = inference_step(windmill_ak=windmill_ak,
                               windmill_sk=windmill_sk,
                               windmill_endpoint=windmill_endpoint,
                               experiment_kind=experiment_kind,
                               experiment_name=experiment_name,
                               tracking_uri=tracking_uri,
                               project_name=project_name,
                               accelerator=accelerator,
                               eval_step=eval,
                               package_step=package)

    return inference.outputs["output_uri"]


from gaea_operator.utils import get_accelerator


def transform_eval_step(algorithm: str,
                        eval_step: ContainerStep = None,
                        transform_step: ContainerStep = None,
                        windmill_ak: str = "",
                        windmill_sk: str = "",
                        windmill_endpoint: str = "",
                        experiment_kind: str = "",
                        experiment_name: str = "",
                        modelstore_name: str = "",
                        tracking_uri: str = "",
                        project_name: str = "",
                        accelerator: str = ""):
    """
    Transform eval step
    """
    accelerator = "R200"
    algorithm = "ChangePPYOLOEPLUS/Model"
    transform_eval_params = {"flavour": "c4m16gpu1",
                             "queue": "qtrain",
                             "windmill_ak": windmill_ak,
                             "windmill_sk": windmill_sk,
                             "windmill_endpoint": windmill_endpoint,
                             "experiment_name": experiment_name,
                             "experiment_kind": experiment_kind,
                             "tracking_uri": tracking_uri,
                             "project_name": project_name,
                             "model_store_name": modelstore_name,
                             "accelerator": accelerator,
                             "advanced_parameters": '{"conf_threshold":"0.5",'
                                                    '"iou_threshold":"0.5"}'}
    transform_eval_env = {"PF_JOB_FLAVOUR": "c4m16xpu1",
                          "PF_JOB_QUEUE_NAME": "qr200",
                          "WINDMILL_AK": "{{windmill_ak}}",
                          "WINDMILL_SK": "{{windmill_sk}}",
                          "WINDMILL_ENDPOINT": "{{windmill_endpoint}}",
                          "EXPERIMENT_KIND": "{{experiment_kind}}",
                          "EXPERIMENT_NAME": "{{experiment_name}}",
                          "TRACKING_URI": "{{tracking_uri}}",
                          "PROJECT_NAME": "{{project_name}}",
                          "ACCELERATOR": "R200",
                          "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
    accelerator = get_accelerator(name=accelerator)
    env = \
        {
            "LD_LIBRARY_PATH": "/opt/tritonserver/lib",
            "XTCL_L3_SIZE": "16776192"
        }
    transform_eval_env.update(env)

    transform_eval = ContainerStep(name="transform-eval",
                                   docker_env="iregistry.baidu-int.com/windmill-public/inference/kunlun:v4.1.2-dev1",
                                   env=transform_eval_env,
                                   parameters=transform_eval_params,
                                   inputs={"input_dataset_uri": eval_step.outputs["output_dataset_uri"],
                                           "input_model_uri": transform_step.outputs["output_model_uri"]},
                                   outputs={"output_uri": Artifact()},
                                   command=f'python3 -m gaea_operator.components.transform_eval.transform_eval '
                                           f'--algorithm={algorithm} '
                                           f'--input-model-uri={{{{input_model_uri}}}} '
                                           f'--input-dataset-uri={{{{input_dataset_uri}}}} '
                                           f'--output-uri={{{{output_uri}}}}')

    return transform_eval


def inference_step(eval_step: ContainerStep = None,
                   package_step: ContainerStep = None,
                   windmill_ak: str = "",
                   windmill_sk: str = "",
                   windmill_endpoint: str = "",
                   experiment_kind: str = "",
                   experiment_name: str = "",
                   model_store_name: str = "",
                   tracking_uri: str = "",
                   project_name: str = "",
                   accelerator: str = ""):
    """
    Inference step
    """
    accelerator = "R200"
    inference_params = {"flavour": "c4m16gpu1",
                        "queue": "qtrain",
                        "windmill_ak": windmill_ak,
                        "windmill_sk": windmill_sk,
                        "windmill_endpoint": windmill_endpoint,
                        "experiment_name": experiment_name,
                        "experiment_kind": experiment_kind,
                        "tracking_uri": tracking_uri,
                        "project_name": project_name,
                        "model_store_name": model_store_name,
                        "accelerator": accelerator,
                        "advanced_parameters": '{"conf_threshold":"0.5"}'}
    inference_env = {"PF_JOB_FLAVOUR": "{{flavour}}",
                     "PF_JOB_QUEUE_NAME": "{{queue}}",
                     "WINDMILL_AK": "{{windmill_ak}}",
                     "WINDMILL_SK": "{{windmill_sk}}",
                     "WINDMILL_ENDPOINT": "{{windmill_endpoint}}",
                     "EXPERIMENT_KIND": "{{experiment_kind}}",
                     "EXPERIMENT_NAME": "{{experiment_name}}",
                     "TRACKING_URI": "{{tracking_uri}}",
                     "PROJECT_NAME": "{{project_name}}",
                     "ACCELERATOR": "R200}",
                     "ADVANCED_PARAMETERS": "{{advanced_parameters}}"}
    accelerator = get_accelerator(name=accelerator)
    inference_env.update(accelerator.suggest_env())

    inference = ContainerStep(name="inference",
                              docker_env="iregistry.baidu-int.com/windmill-public/inference/kunlun:v4.1.2-dev1",
                              env=inference_env,
                              parameters=inference_params,
                              inputs={"input_dataset_uri": eval_step.outputs["output_dataset_uri"],
                                      "input_model_uri": package_step.outputs["output_model_uri"]},
                              outputs={"output_uri": Artifact()},
                              command=f'python3 -m gaea_operator.components.inference.inference '
                                      f'--input-model-uri={{{{input_model_uri}}}} '
                                      f'--input-dataset-uri={{{{input_dataset_uri}}}} '
                                      f'--output-uri={{{{output_uri}}}}')

    return inference


def package_step(algorithm: str,
                 transform_eval_step: ContainerStep = None,
                 transform_step: ContainerStep = None,
                 windmill_ak: str = "",
                 windmill_sk: str = "",
                 windmill_endpoint: str = "",
                 experiment_kind: str = "",
                 experiment_name: str = "",
                 modelstore_name: str = "",
                 tracking_uri: str = "",
                 project_name: str = "",
                 accelerator: str = "",
                 ensemble_model_name: str = "",
                 ensemble_model_display_name: str = "",
                 sub_model_names: str = "",
                 scene: str = ""):
    """
    Package step
    """
    accelerator = "R200"
    algorithm = "ChangePPYOLOEPLUS/Model"
    package_params = {"flavour": "c4m16",
                      "queue": "qtrain",
                      "windmill_ak": windmill_ak,
                      "windmill_sk": windmill_sk,
                      "windmill_endpoint": windmill_endpoint,
                      "experiment_name": experiment_name,
                      "experiment_kind": experiment_kind,
                      "tracking_uri": tracking_uri,
                      "project_name": project_name,
                      "model_store_name": modelstore_name,
                      "accelerator": accelerator,
                      "ensemble_model_name": ensemble_model_name,
                      "ensemble_model_display_name": ensemble_model_display_name,
                      "sub_model_names": sub_model_names,
                      "scene": scene}
    package_env = {"PF_JOB_FLAVOUR": "{{flavour}}",
                   "PF_JOB_QUEUE_NAME": "{{queue}}",
                   "WINDMILL_AK": "{{windmill_ak}}",
                   "WINDMILL_SK": "{{windmill_sk}}",
                   "WINDMILL_ENDPOINT": "{{windmill_endpoint}}",
                   "EXPERIMENT_KIND": "{{experiment_kind}}",
                   "EXPERIMENT_NAME": "{{experiment_name}}",
                   "TRACKING_URI": "{{tracking_uri}}",
                   "PROJECT_NAME": "{{project_name}}",
                   "ACCELERATOR": "R200",
                   "ENSEMBLE_MODEL_NAME": "{{ensemble_model_name}}",
                   "ENSEMBLE_MODEL_DISPLAY_NAME": "{{ensemble_model_display_name}}",
                   "SUB_MODEL_NAMES": "{{sub_model_names}}",
                   "SCENE": "{{scene}}"}
    accelerator = get_accelerator(name=accelerator)

    package = ContainerStep(name="package",
                            docker_env="iregistry.baidu-int.com/windmill-public/inference/kunlun:v4.1.2-dev1",
                            env=package_env,
                            parameters=package_params,
                            inputs={"input_model_uri": transform_step.outputs["output_model_uri"]},
                            outputs={"output_model_uri": Artifact(), "output_uri": Artifact()},
                            command=f'python3 -m gaea_operator.components.package.package '
                                    f'--algorithm={algorithm} '
                                    f'--input-model-uri={{{{input_model_uri}}}} '
                                    f'--output-uri={{{{output_uri}}}} '
                                    f'--output-model-uri={{{{output_model_uri}}}}').after(transform_eval_step)

    return package


if __name__ == "__main__":
    pipeline_client = pipeline(
        accelerator="T4",
        windmill_ak="a1a9069e2b154b2aa1a83ed12316d163",
        windmill_sk="eefac23d2660404e93855197ce60efb3",
        windmill_endpoint="http://10.27.240.5:8340",
        experiment_kind="Aim",
        experiment_name="ppyoloe_plus_m",
        tracking_uri="aim://10.27.240.5:8329",
        project_name="workspaces/internal/projects/proj-o97H2oAE",
        train_dataset_name="workspaces/internal/projects/proj-o97H2oAE/datasets/ds-UCKo4LyJ/versions/1",
        val_dataset_name="workspaces/internal/projects/proj-o97H2oAE/datasets/ds-UCKo4LyJ/versions/1",
        eval_dataset_name="workspaces/internal/projects/proj-o97H2oAE/datasets/ds-UCKo4LyJ/versions/1",
        train_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/ppyoloe-plus",
        train_model_display_name="ppyoloe-plus",
        transform_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/ppyoloe-plus-t4",
        transform_model_display_name="ppyoloe-plus-t4",
        ensemble_model_name="workspaces/internal/modelstores/ms-6TDGY7Hv/models/ppyoloe-plus-ensemble",
        ensemble_model_display_name="ppyoloe-plus-ensemble")
    pipeline_client.compile(save_path="change_ppyoloe_plus_pipeline.yaml")
    _, run_id = pipeline_client.run(fs_name="vistudio")
