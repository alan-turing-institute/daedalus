import pandas as pd

from daedalus.RateTables.BaseHandler import BaseHandler
from os.path import exists
from os import remove


class ImmigrationRateTable(BaseHandler):
    def __init__(self, configuration):
        super().__init__(configuration=configuration)
        self.source_file = self.configuration.paths.path_to_immigration_file
        self.total_population_file = self.configuration.paths.path_to_total_population_file
        self.total_immigrants = None
        self.location = self.configuration.configuration.location
        self.filename = 'immigration_rate_table_'+self.location+'.csv'
        self.rate_table_path = self.rate_table_dir + self.filename


    def _build(self):
        df_immigration = pd.read_csv(self.source_file)
        df_total_population = pd.read_csv(self.total_population_file)

        df_immigration = df_immigration[df_immigration['LAD.code'].isin([self.location])]

        df_total_population = df_total_population[df_total_population['LAD'].isin([self.location])]
        print('Computing immigration rate table...')
        self.rate_table = self.compute_migration_rates(df_immigration, df_total_population,
                                                       2011,
                                                       2012,
                                                       self.configuration.population.age_start,
                                                       self.configuration.population.age_end)

    def set_total_immigrants(self):
        df_immigration = pd.read_csv(self.source_file)

        df_immigration = df_immigration[df_immigration['LAD.code'].isin([self.location])]

        print('Computing total immigration number for location '+self.location)
        self.total_immigrants = int(df_immigration[df_immigration.columns[4:]].sum().sum())
