from google.oauth2 import service_account
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest, Dimension, FilterExpression, Filter, FilterExpressionList
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPICallError
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
        return data


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
        return sum_of_values
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
