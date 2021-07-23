from enum import Enum


class CSVColumns(Enum):
    TCID = 'TCID'
    CaseTitle = 'CaseTitle'
    Catalog = 'Catalog'
    Priority = 'Priority'
    PreCondition = 'PreCondition'
    Variables = 'Variables'
    Role = 'Role'
    ClientType = 'ClientType'
    AuthSettings = 'AuthSettings'
    Action = 'Action'
    Parameter = 'Parameter'
    ExpectResponseCode = 'ExpectResponseCode'
    ExpectResponseHeader = 'ExpectResponseHeader'
    ExpectResponseBody = 'ExpectResponseBody'
    ExpectResponseBodySchema = 'ExpectResponseBodySchema'
    PostValidation = 'PostValidation'
    CleanUp = 'Cleanup'
    Description = 'Description'
    Comment = 'Comment'


class CaseResults(Enum):
    PASS = 'PASS'
    FAIL = 'FAIL'
    ERROR = 'ERROR'
    NO_RUN = 'NO_RUN'


if __name__ == '__main__':
    pass

