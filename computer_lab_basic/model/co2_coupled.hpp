/**
 * Copyright (c) 2020, Cristina Ruiz Martin
 * ARSLab - Carleton University
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 * 1. Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */
/**
* Model developed by Hoda Khalil in Cell-DEVS CD++
* Implemented in Cadmium-cell-DEVS by Cristina Ruiz Martin
*/

#ifndef CADMIUM_CELLDEVS_CO2_COUPLED_HPP
#define CADMIUM_CELLDEVS_CO2_COUPLED_HPP

#include <nlohmann/json.hpp>
#include <cadmium/celldevs/coupled/grid_coupled.hpp>
#include "co2_lab_cell.hpp"

template <typename T>
class co2_coupled : public cadmium::celldevs::grid_coupled<T, co2, int> {
public:

    explicit co2_coupled(std::string const &id) : grid_coupled<T, co2, int>(id){}

    template <typename X>
    using cell_unordered = std::unordered_map<std::string,X>;

    void add_grid_cell_json(std::string const &cell_type, cell_map<co2, int> &map, std::string const &delay_id,
                            nlohmann::json const &config) override {
        if (cell_type == "CO2_cell") {
            auto conf = config.get<typename co2_lab_cell<T>::config_type>();
            this->template add_cell<co2_lab_cell>(map, delay_id, conf);
        } else throw std::bad_typeid();
    }
};

#endif //CADMIUM_CELLDEVS_CO2_COUPLED_HPP
