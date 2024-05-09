from .CoreATASApi import CoreATASApi


def init(endpoints, token, launch_name, executor, job_execution_id):
    return CoreATASApi.init_result(endpoints, token, launch_name, executor, job_execution_id)


def upload_result(endpoints, token, execution_id, case_name, step_desc, step_status, case_status, executor, path,
                  screenshot,
                  attachment, start_time, end_time, test_plan_case_id, run_id):
    data = {'caseName': case_name,
            'path': path,
            'stepStatus': step_status,
            'stepDescription': step_desc,
            'caseStatus': case_status,
            'executor': executor,
            'screen_path': screenshot,
            'attachment_path': attachment,
            'executionId': execution_id,
            'startTime': start_time,
            'endTime': end_time,
            'testCaseId': test_plan_case_id,
            'unionKey': run_id}
    CoreATASApi.save_result(endpoints, token, data)


def complete(endpoints, token, execution_id, case_status):
    CoreATASApi.run_complete(endpoints, token, execution_id, case_status)


def get_run_case(endpoints, token, id):
    CoreATASApi.get_run_cases(endpoints, token, id)


def bulk_upload_result(endpoints, token, execution_id, job_execution_id, launch_name, description, executor, completed,
                       case_info):
    data = {'launchName': launch_name, 'description': description, 'jobExecutionId': job_execution_id,
            'executionId': execution_id, 'executor': executor, 'completed': completed, 'list': case_info}
    CoreATASApi.bulk_save_result(endpoints, token, data)


def upload_attachment(endpoints, token, file_path):
    return CoreATASApi.upload_attachment(endpoints, token, file_path)
