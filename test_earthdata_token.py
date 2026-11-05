
import getpass
import asf_search as asf

print("DHARA - Earthdata Token Test")

token = getpass.getpass("Paste your Earthdata token: ")

session = asf.ASFSession()

try:
    session.auth_with_token(token)
    print("eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6InNoaWtoaWx5YWRhdiIsInN1YiI6InNoaWtoaWx5YWRhdiIsImV4cCI6MTc5OTA3NzM3OCwiaWF0IjoxNzkzODkzMzc4LCJpc3MiOiJodHRwczovL3Vycy5lYXJ0aGRhdGEubmFzYS5nb3YiLCJpZGVudGl0eV9wcm92aWRlciI6ImVkbF9vcHMiLCJhY3IiOiJlZGwiLCJhc3N1cmFuY2VfbGV2ZWwiOjN9.uG-s0vQVXAh7Y53cNIVwmBSuU-bqbu9UjsHmsbyOcrTa4bMGgSuwDbn3rpv0jd7wfnBn1dN_aXZWNekohkxkhqSCrP5SlCffHnxdRrE3NaHDbDEuLaBnr5W9Pq7yQQ3Gg9h2wqRyFHBZzvPJ_NlkMcF5Pqr3y32eT5tUOdzEsO1zSz2dR9Owh_phfuvkB-E1ifzVQQW6kYF5LpHMVnuo8akqQNmuQ4Dda-MzRxt2vpHKr7Oo5emCp17LYobXzdjNEwwhfu0QMoJs3YFi1BdrW3JxF66Lqwu9VLbxRwrkeWdOctabJbZbaG822oMw4OvGXjQ85GPyabP9ZfMEeRt8aQ")

except Exception as error:
    print("\nAuthentication failed:", error)

finally:
    token = None
    session.close()
