cmake_minimum_required(VERSION 3.8)

project(GatewayService)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

option(ENABLE_TESTING "Build the tests" OFF)

file(GLOB APP_SOURCE_FILES "src/*.cpp")

macro(add_grpc_proto_files OUT_SRC)
  set(OUT_SRC_TMP)
  foreach(name ${ARGN})
    list(APPEND OUT_SRC_TMP "${CMAKE_CURRENT_SOURCE_DIR}/protos/${name}.pb.cc")
    list(APPEND OUT_SRC_TMP "${CMAKE_CURRENT_SOURCE_DIR}/protos/${name}.grpc.pb.cc")
  endforeach()
  set(${OUT_SRC} ${OUT_SRC_TMP})
endmacro()

set(GRPC_PROTO_FILES)
add_grpc_proto_files(GRPC_PROTO_FILES "todo/todo" "user/user")
add_executable(${PROJECT_NAME} ${APP_SOURCE_FILES} ${GRPC_PROTO_FILES})

set_target_properties(
  ${PROJECT_NAME}
  PROPERTIES
  CXX_STANDARD 17
  CXX_STANDARD_REQUIRED YES
  CXX_EXTENSIONS NO
)
target_compile_options(
  ${PROJECT_NAME}
  PUBLIC
  -Wall
  -Werror
  -Wextra
  -Wpedantic
  -pedantic-errors
)

find_package(OpenSSL REQUIRED)

target_include_directories(
  ${PROJECT_NAME}
  PRIVATE
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/protos>"
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/inc>"
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/third_party/jwt-cpp/include>"
    ${OPENSSL_INCLUDE_DIR}
)

set(LIBPROTOBUF "/usr/lib/x86_64-linux-gnu/libprotobuf.so")
set(LIBGRPC "/usr/lib/x86_64-linux-gnu/libgrpc++.so")

target_link_libraries(
  ${PROJECT_NAME}
  ${LIBPROTOBUF}
  ${LIBGRPC}
  ${OPENSSL_LIBRARIES}
)
