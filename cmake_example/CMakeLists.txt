cmake_minimum_required(VERSION 3.5)
project(example)

# If Clava CMake plugin is not installed (e.g., sudo clava-update), the path to the plugin
# can be manually specified by setting the variable Clava_DIR
# The Clava CMake plugin can be found here: https://github.com/specs-feup/clava/tree/master/CMake
set(Clava_DIR ./clava)

set(CMAKE_C_STANDARD 99)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -g -Wall -O3 -mcmodel=medium")

set(SOURCE_FILES
	example.c
)


add_executable(example ${SOURCE_FILES})

#target_link_libraries(example m)
	
# Clava section

find_package(Clava REQUIRED)

# Call AutoPar
#clava_weave(example SeparateFunctions.mjs)
clava_weave(example ExtractSymbols.mjs)
