add_executable(eskf_run eskf_run.cpp)
target_link_libraries(eskf_run slam_pipeline)

add_executable(deskew_scan deskew_scan.cpp)
target_link_libraries(deskew_scan slam_pipeline)

add_executable(icp_register icp_register.cpp)
target_link_libraries(icp_register slam_pipeline)

if(GTSAM_FOUND)
  add_executable(run_pipeline run_pipeline.cpp)
  target_link_libraries(run_pipeline slam_backend)
endif()
