# from backend.database import repository
# from backend.jmeter.runner import JMeterRunner
# from backend.orchestrator import status_manager


# runner = JMeterRunner()

# result = runner.execute(
#     run_name="Smoke_Test"
# )

# if not result.success:

#     status_manager.failed(
#         result.error_message
#     )

#     return

# summary = runner.parse_result(result)

# repository.update_status(

#     run_id,

#     "JMeter Completed",

#     "Reading CSV"
# )

# csv_parser.parse(
#     result.jtl_file
# )