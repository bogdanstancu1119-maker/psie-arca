#!/bin/bash
scalingo login --api-token $SCALINGO_TOKEN
scalingo create hydra-psi-node --region osc-fr1
scalingo env-set HYDRA_MODE=active NODE_ID=001
scalingo deploy --source ./deploy_package.tar.gz