# CMakeLists.txt for potential desktop cross-compilation and testing
# This enables compilation of firmware components on desktop for unit testing

cmake_minimum_required(VERSION 3.16)
project(SwarmbotFirmware)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable testing
enable_testing()

# Project structure
set(FIRMWARE_SRC_DIR ${CMAKE_SOURCE_DIR}/firmware/src)
set(FIRMWARE_INCLUDE_DIR ${CMAKE_SOURCE_DIR}/firmware/include)
set(TEST_DIR ${CMAKE_SOURCE_DIR}/testing)

# Add firmware libraries (platform-agnostic components)
add_library(firmware_core
    ${FIRMWARE_SRC_DIR}/utils/crc.cpp
    ${FIRMWARE_SRC_DIR}/utils/logger.cpp
)
target_include_directories(firmware_core PUBLIC ${FIRMWARE_INCLUDE_DIR})

# Add unit tests
add_subdirectory(testing/unit)

# Print configuration
message(STATUS "Firmware Source: ${FIRMWARE_SRC_DIR}")
message(STATUS "Firmware Include: ${FIRMWARE_INCLUDE_DIR}")
message(STATUS "Test Directory: ${TEST_DIR}")
