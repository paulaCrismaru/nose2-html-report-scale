import logging
import os
import traceback

from nose2.events import Plugin

from render import render

FILE_PATH = os.path.realpath('report.html')


class ScaleReport(Plugin):
    configSection = 'report-scale'
    tests_results = {}

    def __init__(self,*args,**kwargs):
        super(ScaleReport, self).__init__(*args, **kwargs)
        config_file = os.path.realpath(self.config.as_str("path", default="report.html"))

    def testOutcome(self, event):
        test_name = event.test.__repr__().split('.')[-1]
        if "obj" in dir(event.test):
            # TODO: add better check
            documentation = getattr(event.test.obj, test_name).__doc__
            self.tests_results[test_name] = {
                "description": documentation,
                "True": 0,
                "False": 0,
                "failures": []
            }
        else:
            # TODO: add better check for generator
            test_name = test_name.split(":")[0]
            # print "*"
            # print event.test
            if test_name not in self.tests_results:
                self.tests_results[test_name] = {
                    "description": "bla",
                    "True": 0,
                    "False": 0,
                    "failures": []
                }
        if "passed" not in event.outcome:
            exception_type = event.exc_info[0]
            exception_message = event.exc_info[1]
            exception_traceback = event.exc_info[2]
            formatted_traceback = ''.join(traceback.format_exception(
                exception_type, exception_message, exception_traceback))
            passed_parameters = None
            if len(event.test.__repr__().split('\n')) > 1:
                passed_parameters = event.test.__repr__().split('\n')[1]
                self.tests_results[test_name]["failures"].append(
                    (passed_parameters, formatted_traceback)
                )
            else:
                self.tests_results[test_name]["failures"].append(
                    (passed_parameters, formatted_traceback)
                )
        key = "False" if "passed" not in event.outcome else "True"
        self.tests_results[test_name][key] += 1

    def afterTestRun(self, *args, **kwargs):
        print "afterTestRun"

    def afterSummaryReport(self, event):
        print "after summary report"
        # import pdb; pdb.set_trace()
        tests_data = []
        for test_name, results in self.tests_results.items():
            tests_data.append((test_name, results))
            # if "failures" in results:
                # data += "Input values of failures:\n"
                # for value, traceback in results["failures"]:
                #     data += '{}\n{}'.format(value, traceback)
                    # print traceback
        render(FILE_PATH, {"data": tests_data,
                           "test_report_title": "my title"})