import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from statistics import mean

import config
from synch2jira.log import new_log
from synch2jira.issue_S2 import IssueS2
from synch2jira.issue_workflow import IssueWorkflow


@dataclass
class WorkFlow:
    issueKey: str

    @staticmethod
    def get_duration_between_two_state(issue_key, state1, state2):
        if IssueWorkflow.did_issue_have_state(issue_key, state1) and IssueWorkflow.did_issue_have_state(issue_key,
                                                                                                      state2):
            worflow1 = IssueWorkflow.find_by(issueKey=issue_key, status=state1)[0]
            worflow2 = IssueWorkflow.find_by(issueKey=issue_key, status=state2)[0]
            #print(f' workflow1 {worflow1.to_time} workflow2 {worflow2.to_time}')
            if worflow1.from_time is not None and worflow2.from_time is not None:
                date1 = WorkFlow.convert_str_time_to_unix(worflow1.from_time)
                date2 = WorkFlow.convert_str_time_to_unix(worflow2.from_time)
                timestamp_to_jour = WorkFlow.convert_timestamp_to_days(date1 - date2)
                return [issue_key, worflow2.from_time, worflow1.from_time, timestamp_to_jour,
                        worflow1.updated if date1 > date2 else worflow2.updated]

    @staticmethod
    def get_all_duration_between_to_state(state1, state2, issue_list):
        return [WorkFlow.get_duration_between_two_state(issue, state1, state2) for issue in issue_list]

    @staticmethod
    def get_all_workflow(state1, state2):
        issue_list = [issue.key for issue in IssueS2.all_lite()]  # S2 qui renvoit les clés
        workFlow_list = WorkFlow.get_all_duration_between_to_state(state1, state2, issue_list)
        return [workflow for workflow in workFlow_list if workflow]

    @staticmethod
    def get_all_workflow_in_csv(state1, state2):
        if not os.path.exists(config.workflow_database_directory) :
            os.makedirs(config.workflow_database_directory)
            new_log("INFO",f"Dossier BDD créé à l'emplacement : {config.workflow_database_directory}")
        else:
            new_log("WARNING","Le dossier BDD existe déjà.")

        if not(os.path.exists(config.files_directory)) : 
            new_log("WARNING","Le ficier issue json existe pas ")
            os.makedirs(config.files_directory)
            with open(config.json_issues_file,'x') as file:
                pass
        if not os.path.exists(config.workflow_file) : # or IssueWorkflow.length() == 0 :
            new_log("WARNING","La BDD n'existe pas ou bien elle est vide")
            new_log("INFO","Tentative de creation de la BDD")
            IssueWorkflow.fill_issue_workflow_bdd()  
            new_log("INFO","La BDD a été rempli avec success")
        result = WorkFlow.get_all_workflow(state1, state2)
        for elt in result: 
            if elt[1] != elt[2]:
                print("HELLO mon petir")
        print(result[-1])
        entete = ["Issue", f"{state1}_last_date", f"{state2}_last_date", "Duration", "Last_update"]
        IssueWorkflow.save_result_in_csv(result, entete)

    @staticmethod
    def get_all_workflow_from_jira_in_csv(state1, state2):
        debut = time.time()
        issue_key_list = IssueS2.all_key()
        worflow_list = []
        for key in issue_key_list:
            _, time1 = IssueWorkflow.get_workflow(key, state1)
            _, time2 = IssueWorkflow.get_workflow(key, state2)
            date1 = WorkFlow.convert_str_time_to_unix(time1) if time1 else time1
            date2 = WorkFlow.convert_str_time_to_unix(time2) if time2 else time2
            timestamp_to_jour = WorkFlow.convert_timestamp_to_days(date1 - date2) if (date1 and date2) else 'oo'
            worflow_list.append([key, time1, time2, timestamp_to_jour])
        entete = ["Issue", f"{state1}_last_date", f"{state2}_last_date", "Duration", "Last_update"]
        worflow_list = [workflow for workflow in worflow_list if workflow[3] != 'oo']
        IssueWorkflow.save_result_in_csv(worflow_list, entete)
        fin = time.time()
        print(f'fin de lexecution en {fin - debut}')

    @staticmethod
    def get_mean_duration(state1, state2, issue_list):
        return mean(WorkFlow.get_duration_between_two_state(state1, state2, issue_list))

    @staticmethod
    def is_in_state(state):
        return False

    @staticmethod
    def get_all_issues_with_state(cls, state):
        return []

    @staticmethod
    def get_rate(begin_time, end_time):
        try : 
            workflow_list = IssueWorkflow.find_by(status="Qualifications")  # config
            print(f'before filtering {len(workflow_list)}')
            workflow_list = [workflow for workflow in workflow_list if workflow.to_time]
            print(f'after filtering {len(workflow_list)}')
            workflow_list = [workflow for workflow in workflow_list if
                             WorkFlow.is_time_in_period(WorkFlow.convert_jira_date_to_datime(workflow.to_time), begin_time,
                                                  end_time)]
            return len(workflow_list)
        except Exception as e:
            new_log("ERROR",f'Erreur lors de lexecution de get_rate : {e}')

    @staticmethod
    def is_time_in_period(time, begin_time, end_time):
        return begin_time <= time <= end_time

    @staticmethod
    def compare_date_with_str_date(date1, date2):
        date1 = date1.replace(tzinfo=timezone.utc)
        date2 = WorkFlow.convert_jira_date_to_datime(date2)
        print(f'date 1 {date1} , date 2 {date2}')
        if date1 > date2:
            # KAN-17 2024-03-05 09:13:40.998417 2024-03-05T11:27:28.959+0100
            # KAN-99 2024-03-05 11:06:19.485890 2024-03-05T11:27:29.733+0100
            return True

        return False

    @staticmethod
    def convert_jira_date_to_datime(date):
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=timezone.utc)

    @staticmethod
    def get_worflow_history():
        pass

    @staticmethod
    def csv_file():
        return config.csv_file

    @staticmethod
    def convert_date_str_to_date(date_str):
        datetime_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        return datetime_obj.strftime('%Y-%m-%d')

    @staticmethod
    def convert_str_time_to_unix(time):
        timestamp_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        element = datetime.strptime(time, timestamp_format)
        timestamp = datetime.timestamp(element)
        return timestamp

    @staticmethod
    def convert_timestamp_to_days(timestamp):
        return round(timestamp / (24 * 3600))
