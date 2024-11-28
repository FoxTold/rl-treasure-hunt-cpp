cmake_minimum_required(VERSION 3.7.2)

project(rl_env)

add_subdirectory(deps)

add_executable(rl_env
    src/main.cpp
    src/Game.cpp
    src/Game.h)
target_link_libraries(rl_env PRIVATE sfml-graphics )
target_compile_features(rl_env PRIVATE cxx_std_20)
message(${CMAKE_BINARY_DIR}/deps/SFML/lib/${CMAKE_BUILD_TYPE} )

add_custom_command(
    TARGET rl_env POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
    ${CMAKE_BINARY_DIR}/deps/SFML/lib/${CMAKE_BUILD_TYPE}
    ${CMAKE_BINARY_DIR}   
)