import pandas as pd
import geopandas as gpd

def configure(context):
    context.config("output_path")
    context.config("output_prefix", "ile_de_france_")

    context.stage("synthesis.locations.home.output")
    context.stage("synthesis.locations.education")
    context.stage("synthesis.locations.secondary")
    context.stage("synthesis.locations.work")

def execute(context):
    # output homes
    context.stage("synthesis.locations.home.output")

    df_education = context.stage("synthesis.locations.education")
    df_secondary = context.stage("synthesis.locations.secondary")
    df_work = context.stage("synthesis.locations.work")

    # Write dataframes into files
    for df in [df_education, df_secondary, df_work]:
        for col in df.select_dtypes(include=['category']).columns:
            df[col] = df[col].astype(str)

    df_education.to_file("%s/%seducation.gpkg" % (
        context.config("output_path"), context.config("output_prefix")
    ), layer = "education")

    df_secondary.to_file("%s/%ssecondary.gpkg" % (
        context.config("output_path"), context.config("output_prefix")
    ), layer = "secondary")

    df_work.to_file("%s/%swork.gpkg" % (
        context.config("output_path"), context.config("output_prefix")
    ), layer = "work")