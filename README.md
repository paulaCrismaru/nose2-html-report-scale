# nose2-html-report-scale

### Introduction
A [nose2](https://github.com/nose-devs/nose2) plugin for generating HTML reports containing a large number of test results.
- generated test reults are grouped in one result, counting the successes and failures and showing only the failures
- when test fails the traceback will be shown in the report
- summary of results of each test is shown


### Configuration
In the `nose2.cfg` config file add the plugin in the unittests section. Plugin configuration should be placed into `report-scale` section of the configuration file. Example:
```
[unittest]
plugins = html_report_scale.report_scale

[report-scale]
always-on = true
```

#### Additional Settings to add in report-scale section
- Specify the path for the HTML report. Defaults to `report.html`
```
path = test_results/my_custom_report_file.html
```
- Specify report title. By default the title will remain `Test results`
```
report_title = my app
```
- Display the parameters passed to the tests which use test generating
```
display_test_parameters = True
```
