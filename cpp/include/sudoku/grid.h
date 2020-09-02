#pragma once

#include <array>
#include <string>

template <typename ELEM>
class Array2D_9x9 {
	public:
	Array2D_9x9()  {values.fill(0);} 
	Array2D_9x9(const ELEM& v)  {values.fill(v);}	// values.fill(v)

    ELEM& operator()(int l, int c) {
		return values[l*9+c];
	} 

    ELEM operator()(int l, int c) const {
		return values[l*9+c];
	} 

	// std::string to_string()

	private:
	std::array<ELEM, 9*9> values;
};

typedef  Array2D_9x9<short> Grid9x9;