# Module 7 STARTER: runtime image for the pipeline (used by the Argo workflow).
# TODO(m7): start from the pinned dev image (never :latest), copy the repository, build the C++ apps in
# Release mode, put run_pipeline / eskf_run / icp_register on the PATH, install slampipe, and set a
# non-root user. Keep the build reproducible (pinned base, pinned requirements, no network at runtime).
FROM TODO
