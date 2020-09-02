cmake_minimum_required(VERSION 3.5)

project (sudoku)

set (CMAKE_CXX_STANDARD 11)
set (CMAKE_CXX_FLAGS "-Wall -Werror")
set (CMAKE_CXX_FLAGS "-o3")

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Widgets REQUIRED)


include_directories(include)

add_library (
	sudoku-lib
	src/sudoku/solver.cpp
)





# remove is unused
function(compileExec execname)
	add_executable(${execname}  src/sudoku/${execname}.cpp)
	target_link_libraries (${execname} sudoku-lib)
endfunction()

compileExec(cli)
#compileExec(qt)

add_executable(qt src/sudoku/qt.cpp)
target_link_libraries (qt sudoku-lib Qt5::Widgets)




enable_testing()

function(compileTest testname)
	add_executable(${testname}  tests/${testname}.cpp)
	target_link_libraries (${testname} sudoku-lib)
	add_test(${testname} ${testname})
endfunction()

compileTest(grid)
#compileTest(event-manager)
#compileTest(room-manager)
#compileTest(dyn-room-manager)
