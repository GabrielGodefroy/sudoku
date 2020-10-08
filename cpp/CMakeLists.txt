cmake_minimum_required(VERSION 3.5)

project (sudoku)

set (CMAKE_CXX_STANDARD 11)
set (CMAKE_CXX_FLAGS "-Wall -Werror")
set (CMAKE_CXX_FLAGS "-o3")


set(CMAKE_INCLUDE_CURRENT_DIR ON)

find_package(Qt5 COMPONENTS Widgets REQUIRED)

include_directories(include)

add_library (
	sudoku-lib
    src/sudoku/grid.cpp
	src/sudoku/solver.cpp
)


# remove if unused
function(compileExec execname)
	add_executable(${execname}  src/sudoku/${execname}.cpp)
	target_link_libraries (${execname} sudoku-lib)
endfunction()

add_executable(cli src/sudoku/cli.cpp)
target_link_libraries (cli sudoku-lib)



add_library (
	sudoku-test
    tests/t_grid.cpp
	tests/t_sudoku.cpp
	tests/t_solver.cpp
)
add_executable(catch_test  tests/t_main.cpp)
target_link_libraries (catch_test sudoku-test sudoku-lib)




set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

add_executable(qt src/sudoku/qt.cpp)
target_link_libraries (qt sudoku-lib Qt5::Widgets)
