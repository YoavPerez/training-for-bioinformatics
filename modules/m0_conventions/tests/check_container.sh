#!/usr/bin/env bash
# Module 0: checks that the dev image builds and that the sample sequence loads inside it.
# Run from the repository root after `python data/download.py --sample`.
# If the build stalls on downloads (WSL/VPN, network MTU < 1500), run it as: DOCKER_NET=host bash <this script>
set -euo pipefail
docker build --network "${DOCKER_NET:-default}" -t slam-onboarding-dev -f infra/docker/Dockerfile .
docker run --rm -v "$PWD":/workspace -w /workspace slam-onboarding-dev \
  python -c "import sys; sys.path.insert(0, 'pipeline/python'); from slampipe import kitti; \
d = kitti.Drive('data/samples/kitti/2011_09_26/2011_09_26_drive_0002_sync'); \
print('scans:', len(d.scan_paths()), 'oxts:', len(d.oxts()))"
echo "container OK"
