#!/usr/bin/env python3

import sys
import importlib
from pathlib import Path
import time
import numpy as np
import pandas as pd
import daedalus.static as Static
import daedalus.utils as utils

from vivarium import InteractiveContext
from vivarium_public_health.population import FertilityAgeSpecificRates
from vivarium_public_health.population import Mortality
from vivarium_public_health.population import Emigration
from vivarium_public_health.population import ImmigrationDeterministic as Immigration
from vivarium_public_health.population.spenser_population import TestPopulation
from vivarium_public_health.population.spenser_population import transform_rate_table
from vivarium_public_health.population.spenser_population import compute_migration_rates

from vivarium_public_health.utilities import read_config_file

def main(config):
    """ Run the daedalus Microsimulation """

    # Set up the components using the configuration.

    # TODO: test population initialisation with all West Yorkshire regions.

    # TODO: If regions already exist in the cache then no need to run initialisation.

    components = [TestPopulation(),
                  FertilityAgeSpecificRates(),
                  Mortality(),
                  Emigration(),
                  Immigration()]
    # Dev: limit to population. Need to Rename TestPopulation.
    components = [TestPopulation()]

    simulation = InteractiveContext(components=components,
                                    configuration=config,
                                    plugin_configuration=utils.base_plugins(),
                                    setup=False)

    start_population_size = len(pd.read_csv(config.paths.path_to_pop_file))
    print('Start Population Size: {}'.format(start_population_size))
    num_days = 365 * 2
    #
    # # setup mortality rates
    # mortality_rate_df = pd.read_csv(config.paths.path_to_mortality_file)
    # asfr_data = transform_rate_table(mortality_rate_df, 2011, 2012, config.configuration.population.age_start,
    #                                  config.configuration.population.age_end)
    # simulation._data.write("cause.all_causes.cause_specific_mortality_rate", asfr_data)
    #
    # # setup fertility rates
    # fertility_rate_df = pd.read_csv(config.paths.path_to_fertility_file)
    # asfr_data_fertility = transform_rate_table(fertility_rate_df, 2011, 2012, 10, 50, [2])
    # simulation._data.write("covariate.age_specific_fertility_rate.estimate", asfr_data_fertility)
    #
    # # setup emigration rates
    # df_emigration = pd.read_csv(config.paths.path_to_emigration_file)
    # df_total_population = pd.read_csv(config.paths.path_to_total_population_file)
    # asfr_data_emigration = compute_migration_rates(df_emigration, df_total_population, 2011, 2012,
    #                                                config.configuration.population.age_start, config.configuration.population.age_end)
    # simulation._data.write("covariate.age_specific_migration_rate.estimate", asfr_data_emigration)
    #
    # # setup immigration rates
    # df_immigration = pd.read_csv(config.paths.path_to_immigration_file)
    # asfr_data_immigration = compute_migration_rates(df_immigration, df_total_population,
    #                                                 2011,
    #                                                 2012,
    #                                                 config.configuration.population.age_start,
    #                                                 config.configuration.population.age_end,
    #                                                 normalize=False
    #                                                 )
    #
    # # read total immigrants from the file
    # total_immigrants = int(df_immigration[df_immigration.columns[4:]].sum().sum())
    #
    # simulation._data.write("cause.all_causes.cause_specific_immigration_rate", asfr_data_immigration)
    # simulation._data.write("cause.all_causes.cause_specific_total_immigrants_per_year", total_immigrants)

    simulation.setup()
    simulation.run_for(duration=pd.Timedelta(days=num_days))
    pop = simulation.get_population()

if __name__ == "__main__":
    main(config=utils.get_config())