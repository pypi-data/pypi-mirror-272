#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publish_ppl.py
"""

import os
from argparse import ArgumentParser
from gaea_operator.pipelines import category_to_ppls
from windmillclient.client.windmill_client import WindmillClient
from windmillartifactv1.client.artifact_api_artifact import ArtifactContent
from windmilltrainingv1.client.training_api_pipeline import PipelineName
from bceinternalsdk.client.paging import PagingRequest
import shutil


# python create_ppl.py --windmill-endpoint http://windmill.baidu-int.com:8340 --windmill-ak e0415220bbc94902b89fa3ceba3d4ca7 --windmill-sk 25f9ad7065b041598ce7711a2e591a2f

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--windmill-endpoint", type=str, default=os.environ.get("WINDMILL_ENDPOINT"))
    parser.add_argument("--windmill-ak", type=str, default=os.environ.get("WINDMILL_AK"))
    parser.add_argument("--windmill-sk", type=str, default=os.environ.get("WINDMILL_SK")) 

    parser.add_argument("--workspace-id", type=str, default="")
    parser.add_argument("--project-name", type=str, default="spiproject")
    args, _ = parser.parse_known_args()

    client = WindmillClient(endpoint=args.windmill_endpoint, ak=args.windmill_ak, sk=args.windmill_sk)
    workspace_id = args.workspace_id
    if workspace_id == "":
        resp = client.list_workspace(page_request=PagingRequest(order="asc", orderby="created_at"))
        print("workspace list response {}".format(resp))
        assert len(resp.results) > 0, "must have greater than one workspace id"
        workspace_id = resp.results[0]["id"]
    print("workspace id {}".format(workspace_id))

    project_name = args.project_name
    try:
        resp = client.get_project(workspace_id=workspace_id, project_name=project_name)
    except Exception as e:
        print("get project {} failed, error: {}".format(project_name, e))
        print("start create project {}".format(project_name))
        client.create_project(workspace_id=workspace_id, local_name=project_name, display_name=project_name)

    filedir = os.path.dirname(__file__)
    for cat, ppls in category_to_ppls.items():
        for p in ppls:
            print("pipeline name: {}".format(p.name))
            sub_filedir = os.path.join(filedir, "{}_pipeline".format(p.name))
            publish_filedir = os.path.join(filedir, "{}_publish_pipeline".format(p.name))
            if not os.path.exists(sub_filedir):
                os.makedirs(publish_filedir, exist_ok=True)
            filepath = os.path.join(publish_filedir, "pipeline.yaml")
            print("pipeline compile output file: {}".format(filepath))
            p.compile(save_path=filepath)
            for file in os.listdir(sub_filedir):
                if file.endswith(".yaml"):
                    source_file = os.path.join(sub_filedir, file)
                    shutil.copy(source_file, publish_filedir)

            ppl_name = PipelineName(workspace_id=workspace_id, project_name=project_name, local_name=p.name)
            location = client.create_location_with_uri(uri=publish_filedir, object_name=ppl_name.get_name())

            artifact = ArtifactContent(uri=location)
            print("pipeline artifact uri {}".format(location))

            resp = client.create_pipeline(
                workspace_id=workspace_id,
                project_name=project_name,
                local_name=p.name,
                display_name=p.name,
                category=cat,
                artifact=artifact)
            print("pipeline: {} created.".format(resp.name))

        
