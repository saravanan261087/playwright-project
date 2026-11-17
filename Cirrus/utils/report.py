class ReportManager:

    @staticmethod
    def write_result(
            log_file,
            operation,
            result):

        text = f"""
====================================================
Result - {operation}
====================================================

GUID : {result['guid']}
Transaction : {result['name']}
Transaction ID : {result['id']}
Timestamp : {result['timestamp']}
Status : {result['status']}
Result : {result['result']}

"""

        log_file.write(text)
        log_file.flush()