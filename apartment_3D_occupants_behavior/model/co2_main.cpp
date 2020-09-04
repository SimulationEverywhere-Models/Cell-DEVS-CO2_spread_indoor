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

#include <fstream>
#include <cadmium/modeling/dynamic_coupled.hpp>
#include <cadmium/engine/pdevs_dynamic_runner.hpp>
#include <cadmium/logger/common_loggers.hpp>
#include "co2_coupled.hpp"

using namespace std;
using namespace cadmium;
using namespace cadmium::celldevs;

using TIME = float;

/*************** Loggers *******************/
static ofstream out_messages("results/output_messages.txt");
struct oss_sink_messages{
    static ostream& sink(){
        return out_messages;
    }
};
static ofstream out_state("results/state.txt");
struct oss_sink_state{
    static ostream& sink(){
        return out_state;
    }
};

using state=logger::logger<logger::logger_state, dynamic::logger::formatter<TIME>, oss_sink_state>;
using log_messages=logger::logger<logger::logger_messages, dynamic::logger::formatter<TIME>, oss_sink_messages>;
using global_time_mes=logger::logger<logger::logger_global_time, dynamic::logger::formatter<TIME>, oss_sink_messages>;
using global_time_sta=logger::logger<logger::logger_global_time, dynamic::logger::formatter<TIME>, oss_sink_state>;

using logger_top=logger::multilogger<state, log_messages, global_time_mes, global_time_sta>;


int main(int argc, char ** argv) {
	//sets the seed for the random number generator
    srand(time(NULL));

    if (argc < 2) {
        cout << "Program used with wrong parameters. The program must be invoked as follows:";
        cout << argv[0] << " SCENARIO_CONFIG.json [MAX_SIMULATION_TIME (default: 500)]" << endl;
        return -1;
    }

    co2_coupled<TIME> test = co2_coupled<TIME>("co2_lab");
    std::string scenario_config_file_path = argv[1];
    test.add_lattice_json(scenario_config_file_path);
    test.couple_cells();

    std::shared_ptr<cadmium::dynamic::modeling::coupled<TIME>> t = std::make_shared<co2_coupled<TIME>>(test);

    cadmium::dynamic::engine::runner<TIME, logger_top> r(t, {0});
    cout<<"Model started"<<endl;
    float sim_time = (argc > 2)? atof(argv[2]) : 500;
    r.run_until(sim_time);
    cout<<"Simulation finished"<<endl;
    return 0;
}