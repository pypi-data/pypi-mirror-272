import yaml

import config


def config_package():
    with open('config.py', 'w') as fichier_config:
        fichier_config.write(f"""import logging
import os
from requests.auth import HTTPBasicAuth \n

username = "BillGates" 
#Api token de jira 
api_token = "TATT3xFfGF0nqgTV-RGN17B9CmizmQD0Mmr5ZY-pU0t8TjTzz0lyX0MNJ0XoNdKNy_t4eq9Is3Gw51Mta-kHF0XrEjKUANWzJM1XpRqS_-wSssC"
jira_url_base = "https://example.atlassian.net/"
jira_url_all = jira_url_base + "rest/api/3/search"
jira_url_ticket = jira_url_base + "rest/api/3/issue/"
verify_ssl_certificate = True

project_key = "90009"
key_issue_type = "10005"
s1_id_in_jira = "customfield_10054"

statusesS1 = ["status1", "status2", "status3", "status4"]
jiraStatusName = ['Pret', 'En attente', 'en cours', 'Qualifications']

module_to_use = "synch2jira.issue_S3"
class_to_use = "IssueS3"
                             
jql_query = 'project = KAN'

rate_column = 'Qualifications'

auth = HTTPBasicAuth(username, api_token)
main_directory = os.path.dirname(os.path.abspath(__file__))
config_file = main_directory + "/config.py"
workflow_database_file = "sqlite:///" + main_directory + "/database/worflow_bd.db"
workflow_file = main_directory + "/database/worflow_bd.db"
workflow_database_directory = main_directory + "/database/"
time_to_sleep = 0.1
                             
files_directory = main_directory + "/files"
csv_file = main_directory + "/workflow_time.csv"
log_directory = main_directory + "/log/"                             
log_file = main_directory + "/log/file.log"
log_format = '%(asctime)s - %(levelname)s - %(message)s'
json_issues_file = main_directory + "/files/json_issues.json"
yaml_file = main_directory + "/files/config.yaml"
csv_issue_file = main_directory + "/files/json_issues.csv"                          

fields_to_use = ["statuscategorychangedate","issuetype","timespent",
                 "project", "aggregatetimespent","resolution","resolutiondate",
                 "workratio","watches", "lastViewed", "created", "priority", 
                 "labels", "assignee", "status", "updated" ,
                 "security","description",'summary',"timeoriginalestimate",
                 "creator","subtasks","reporter","duedate","votes"]
expand_change_log = False
projectIdOrKey='KAN'
image_directory = main_directory + "/images"
use_workflow = True
workflow_status1 = "In Progress"
workflow_status2 = "Closed"
output_directory = main_directory + "/output"
""")


def config_yaml():
    data = {
        "tickets_status_par_intervalles_de_temps": [
            {
                "status": "created",
                "date_min": "2010-01-01",
                "date_max": "2011-06-30",
                "pas_de_temps": "date",
                "xtitre": "jour",
                "ytitre": "Nombre de tickets créés",
                "titre_graphe": "Tickets créés par jour",
                "type_graphe": "line"
            },
            {
                "status": "created",
                "date_min": "2010-01-01",
                "date_max": "2014-06-30",
                "pas_de_temps": "year",
                "xtitre": "année",
                "ytitre": "Nombre de tickets créés",
                "titre_graphe": "Tickets créés par année",
                "type_graphe": "points"
            },
            {
                "status": "resolutiondate",
                "date_min": "2010-01-01",
                "date_max": "2011-12-31",
                "pas_de_temps": "date",
                "xtitre": "jour",
                "ytitre": "Nombre de tickets clôturés",
                "titre_graphe": "Tickets clôturés par jour",
                "type_graphe": "line"
            },
            {
                "status": "resolutiondate",
                "date_min": "2010-01-01",
                "date_max": "2014-06-30",
                "pas_de_temps": "year",
                "xtitre": "année",
                "ytitre": "Nombre de tickets cloturés",
                "titre_graphe": "Tickets cloturés par année",
                "type_graphe": "points"

            }
        ],
        "tickets_status_par_intervalles_de_temps_par_mois": [
            {
                "status": "created",
                "date_min": "2010-01-01",
                "date_max": "2014-06-30",
                "xtitre": "Mois",
                "ytitre": "Nombre de tickets créés",
                "titre_graphe": "Tickets créés par mois"
            },
            {
                "status": "resolutiondate",
                "date_min": "2010-01-01",
                "date_max": "2014-12-31",
                "xtitre": "Mois",
                "ytitre": "Nombre de tickets clôturés",
                "titre_graphe": "Tickets clôturés par mois"

            }
        ],
        "lead_time_par_intervalles_de_temps": [
            {
                "date_min": "2010-01-01",
                "date_max": "2013-12-12",
                "pas_de_temps": "date",
                "xtitre": "jour",
                "ytitre": "Leadtime moyen (jours)",
                "titre_graphe": "Leadtime moyen par jour",
                "type_graphe": "line"
            },
            {
                "date_min": "2010-01-01",
                "date_max": "2014-06-30",
                "pas_de_temps": "year",
                "xtitre": "année",
                "ytitre": "Leadtime moyen (jours)",
                "titre_graphe": "Leadtime moyen par année",
                "type_graphe": "points"

            }
        ],
        "lead_time_par_mois": [
            {
                "date_min": "2010-01-01",
                "date_max": "2014-12-31",
                "xtitre": "Mois",
                "ytitre": "Leadtime moyen (jours)",
                "titre_graphe": "Leadtime moyen par mois"

            }
        ],
        "reliquat_par_intervalle": [
            {
                "date_min": "2010-01-01",
                "date_max": "2011-06-30",
                "pas_de_temps": "date",
                "xtitre": "jour",
                "ytitre": "Reliquat",
                "titre_graphe": "Reliquat par jour",
                "type_graphe": "line"
            },
            {
                "status": "created",
                "date_min": "2010-01-01",
                "date_max": "2014-06-30",
                "pas_de_temps": "year",
                "xtitre": "année",
                "ytitre": "Reliquat",
                "titre_graphe": "Reliquat par année",
                "type_graphe": "line"

            }
        ],
        "reliquat_par_mois": [
            {
                "date_min": "2010-01-01",
                "date_max": "2014-12-31",
                "xtitre": "Mois",
                "ytitre": "Reliquat ",
                "titre_graphe": "Reliquat par mois"
            }
        ]
    }
    with open(config.yaml_file, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True, default_flow_style=False, indent=2)


if __name__ == '__main__':
    config_yaml()
