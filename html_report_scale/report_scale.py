import os
import traceback

from nose2.events import Plugin

from html_report_scale.render import render


class ScaleReport(Plugin):
    configSection = 'report-scale'
    tests_results = {}

    def __init__(self, *args, **kwargs):
        super(ScaleReport, self).__init__(*args, **kwargs)
        self.report_path = os.path.realpath(
            self.config.as_str("path", default="report.html"))
        report_title = self.config.as_str("report_title", "")
        if report_title:
            self.report_title = "Test results: {}".format(report_title)
        else:
            self.report_title = "Test results"
        self.display_test_parameters = self.config.as_str(
            "display_test_parameters", default=False)

    def testOutcome(self, event):
        test_method = event.test.__repr__().split(":")[0]
        test_name = test_method.split(".")[-1]
        if "obj" in dir(event.test):
            # TODO: add better check
            documentation = getattr(event.test.obj, test_name).__doc__
        else:
            # TODO: add better check for generator
            test_name = test_name.split(":")[0]
            test_self = event.test._testFunc.func_defaults[0]
            documentation = None
            if hasattr(test_self, "im_class"):
                test_class = test_self.im_class
                documentation = getattr(test_class, test_name).__doc__
        if test_name not in self.tests_results:
            self.tests_results[test_name] = {
                "description": documentation,
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

    def afterSummaryReport(self, event):
        tests_data = []
        for test_name, results in self.tests_results.items():
            tests_data.append((test_name, results))
        data = {
            "data": tests_data,
            "test_report_title": self.report_title,
            "display_test_parameters": self.display_test_parameters
        }
        render(self.report_path, data)
