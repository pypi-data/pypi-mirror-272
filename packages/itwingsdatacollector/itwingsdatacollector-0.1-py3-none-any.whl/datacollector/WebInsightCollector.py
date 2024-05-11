from google.oauth2 import service_account
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest, Dimension, FilterExpression, Filter, FilterExpressionList
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPICallError
from mymodule.config import *
from mymodule.raw_data_to_csv import raw_data_to_csv
import requests
import os
import shutil
import subprocess

# Define needed variables
SCOPES = ['https://www.googleapis.com/auth/webmasters',
          'https://www.googleapis.com/auth/webmasters.readonly']


def GAC(credentials, parameters):
    try:
        webmasters_service = initialize_service(credentials)
        if webmasters_service is None:
            return None
    except Exception as e:
        print(f"Error initializing service: {e}")
        return None
    start_row = 0
    request = {
        'startDate': parameters['start_date'],
        'endDate': parameters['end_date'],
        # Assign dimensions from parameters
        'dimensions': parameters['dimensions'],
        'rowLimit': parameters['max_rows'],
        'startRow': start_row
    }
    response = webmasters_service.searchanalytics().query(
        siteUrl=parameters['url'], body=request).execute()

    if 'rows' in response and response['rows'] and all(key in response['rows'][0] for key in ['impressions', 'clicks', 'position']):
        data = {
            'url': parameters['url'],
            'GSC Impressions': response['rows'][0]['impressions'],
            'GSC Clicks': response['rows'][0]['clicks'],
            'GSC CTR': "{:.2%}".format(response['rows'][0]['clicks'] / response['rows'][0]['impressions']),
            'GSC Average Position': round(response['rows'][0]['position']),
        }
        # Add dimensions dynamically to the data dictionary
        for dim in parameters.get('dimensions', []):
            data[f'GSC {dim.capitalize()}'] = response['rows'][0]['keys'][parameters['dimensions'].index(
                dim)]
    raw_data_to_csv("gsc", data, append=True)


def initialize_service(gsc_credentials):
    credentials = service_account.Credentials.from_service_account_info(
        gsc_credentials, scopes=SCOPES)
    service = build('webmasters', 'v3', credentials=credentials)
    return service


def GA4(GA4parameters, credentials_json, dimensionss, metricss):
    try:

        credentials = service_account.Credentials.from_service_account_info(
            credentials_json)
        client = BetaAnalyticsDataClient(credentials=credentials)

        request = RunReportRequest(
            property=f"properties/{GA4parameters['ga4_property_id']}",
            dimensions=[Dimension(name=dimension)
                        for dimension in dimensionss],
            metrics=[Metric(name=metric) for metric in metricss],
            date_ranges=[{"start_date": GA4parameters['start_date'],
                          "end_date": GA4parameters['end_date']}],
        )
        response = client.run_report(request)
        # Process the response
        # Add URL parameter at the first position
        sum_of_values = {'URL': GA4parameters['url']}
        for metric in metricss:
            sum_of_values[metric] = 0
        for entry in response.rows:
            metric_values = [float(metric.value)
                             for metric in entry.metric_values]
            for i, metric_value in enumerate(metric_values):
                metric_name = metricss[i]
                sum_of_values[metric_name] += metric_value
        raw_data_to_csv("ga4", sum_of_values, append=True)
        # Process response to calculate metrics
        # for row in response.rows:
        #     sessions = int(row.metric_values[1].value)
        #     total_sessions += sessions
        #     total_users += int(row.metric_values[0].value)
        #     bounce_rate_sum += float(row.metric_values[2].value)
        #     avg_session_duration_sum += float(
        #         row.metric_values[3].value)
        #     engagement_rate_sum += float(
        #         row.metric_values[4].value)
    except GoogleAPICallError as e:
        print(f"Error: {e}")


def generate_export_tabs(tabs):
    return ','.join(tabs)


def crawl_website(parameters):

    try:
        export_tabs = generate_export_tabs(parameters["tabs"])
        temp_directory = parameters["temp_folder"]
        os.makedirs(temp_directory, exist_ok=True)

        # Define the command to crawl the website using Screaming Frog SEO Spider and export issues data to a CSV file
        command = (
            f'screamingfrogseospider '
            f'--crawl {parameters["crawl_parameters"]["url"]} '
            # Use user-provided config file path
            f'--config "{parameters["config_file_path"]}" '
            # Use user-provided temp folder
            f'--output-folder {temp_directory} '
            f'--headless '
            f'--export-tabs "{export_tabs}" '  # Pass tabs dynamically
            f'--save-crawl '  # Corrected option
        )
        # Execute the command using subprocess
        subprocess.run(command, shell=True, check=True)
        print(f"CSV file downloaded successfully.")
    except Exception as e:
        print("Error:", e)


def get_pagespeed_report(pagespeed_parameters):
    # Initial data dictionary setup
    data = {
        "url": pagespeed_parameters['url']
    }
    # Setup the initial data structure with default "" values
    def setup_no_data():
        data.update(
            {f"{strategy}_evaluation_result": "-" for strategy in pagespeed_parameters["strategies"]})

    try:
        for strategy in pagespeed_parameters["strategies"]:
            # API request
            response = requests.get(
                f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={pagespeed_parameters["url"]}&strategy={strategy}')
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Processing response
            report = response.json()

            if ("LARGEST_CONTENTFUL_PAINT_MS" in report.get("loadingExperience", {}).get("metrics", {}) and
                "INTERACTION_TO_NEXT_PAINT" in report.get("loadingExperience", {}).get("metrics", {}) and
                    "CUMULATIVE_LAYOUT_SHIFT_SCORE" in report.get("loadingExperience", {}).get("metrics", {})):

                if (report["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"] > ps_config["thresholds"]["LCP"] or
                    report["loadingExperience"]["metrics"]["INTERACTION_TO_NEXT_PAINT"]["percentile"] > ps_config["thresholds"]["INP"] or
                        report["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]/100 > ps_config["thresholds"]["CLS"]):
                    result = "failed"
                else:
                    result = "passed"

                data[f"{strategy}_evaluation_result"] = result
                # We commented out this part because the client currently does not need the metrics of pagespeed but might want to add them to the report later.
                # if strategy == "mobile":
                #     for metric_key, metric_name in config["metrics"].items():
                #         if metric_name in report["loadingExperience"]["metrics"]:
                #             data[f"{metric_key}_category"] = report["loadingExperience"]["metrics"][metric_name]["category"]
                #             if metric_name == "CUMULATIVE_LAYOUT_SHIFT_SCORE":
                #                 data[f"{metric_key}_percentile"] = report["loadingExperience"]["metrics"][metric_name]["percentile"] / 100
                #             else:
                #                 data[f"{metric_key}_percentile"] = report["loadingExperience"]["metrics"][metric_name]["percentile"]
                #         else:
                #             data[metric_key] = 'N/A'
            else:
                setup_no_data()

        raw_data_to_csv("pagespeed", data, append=True)

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving pagespeed report: {e}")
        # If there is an error, setup data dictionary with ""
        setup_no_data()
        # Then save or log the error data as needed
        raw_data_to_csv("pagespeed", data, append=True)
