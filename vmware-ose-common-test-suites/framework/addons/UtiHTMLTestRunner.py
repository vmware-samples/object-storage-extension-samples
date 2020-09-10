import os

"""
A TestRunner for use with the Python unit testing framework. It
generates a HTML report to show the result at a glance.

The simplest way to use this is to invoke its main method. E.g.

    import unittest
    import HTMLTestRunner

    ... define your tests ...

    if __name__ == '__main__':
        HTMLTestRunner.main()


For more customization options, instantiates a HTMLTestRunner object.
HTMLTestRunner is a counterpart to unittest's TextTestRunner. E.g.

    # output to a file
    fp = file('my_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title='My unit test',
                description='This demonstrates the report output by HTMLTestRunner.'
                )

    # Use an external stylesheet.
    # See the Template_mixin class for more customizable options
    runner.STYLESHEET_TMPL = '<link rel="stylesheet" href="my_stylesheet.css" type="text/css">'

    # run the test
    runner.run(my_test_suite)


------------------------------------------------------------------------
Copyright (c) 2004-2007, Wai Yip Tung
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
  notice, this list of conditions and the following disclaimer in the
  documentation and/or other materials provided with the distribution.
* Neither the name Wai Yip Tung nor the names of its contributors may be
  used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# URL: http://tungwaiyip.info/software/HTMLTestRunner.html

__author__ = "Wai Yip Tung"
__version__ = "0.8.3"


"""
Change History

Version 0.8.3
* Prevent crash on class or module-level exceptions (Darren Wurf).

Version 0.8.2
* Show output inline instead of popup window (Viorel Lupu).

Version in 0.8.1
* Validated XHTML (Wolfgang Borgert).
* Added description of test classes and test cases.

Version in 0.8.0
* Define Template_mixin class for customization.
* Workaround a IE 6 bug that it does not treat <script> block as CDATA.

Version in 0.7.1
* Back port to Python 2.3 (Frank Horowitz).
* Fix missing scroll bars in detail log (Podi).
"""

# TODO: color stderr
# TODO: simplify javascript using ,ore than 1 class in the class attribute?

import datetime
import io as StringIO
import sys
import unittest
from xml.sax import saxutils
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, wait, TimeoutError
from unittest.suite import _ErrorHolder
from ansi2html import Ansi2HTMLConverter


# ------------------------------------------------------------------------
# The redirectors below are used to capture output during testing. Output
# sent to sys.stdout and sys.stderr are automatically captured. However
# in some cases sys.stdout is already cached before HTMLTestRunner is
# invoked (e.g. calling logging.basicConfig). In order to capture those
# output, use the redirectors for the cached stream.
#
# e.g.
#   >>> logging.basicConfig(stream=HTMLTestRunner.stdout_redirector)
#   >>>

def to_unicode(s):
    try:
        return str(s)
    except UnicodeDecodeError:
        # s is non ascii byte string
        return s.decode('unicode_escape')


# ----------------------------------------------------------------------
# Template

class Template_mixin(object):
    """
    Define a HTML template for report customerization and generation.

    Overall structure of an HTML report

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    STATUS = {
    0: 'pass',
    1: 'fail',
    2: 'error',
    3: 'skip',
    }

    DEFAULT_TITLE = 'Unit Test Report'
    DEFAULT_DESCRIPTION = ''

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>%(title)s</title>
    <meta name="generator" content="%(generator)s"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    %(stylesheet)s
</head>
<body>
<script language="javascript" type="text/javascript">
output_list = Array();

/* level - 0:Summary; 1:Not Passed; 2:All */
function showCase(level) {
    trs = document.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        tr = trs[i];
        id = tr.id;
        if (id.substr(0,2) == 'ft') {
            if (level < 1) {
                tr.className = 'hiddenRow';
            }
            else {
                tr.className = '';
            }
        }
        if (id.substr(0,2) == 'pt') {
            if (level > 1) {
                tr.className = '';
            }
            else {
                tr.className = 'hiddenRow';
            }
        }
    }
}


function showClassDetail(cid, count) {
    var id_list = Array(count);
    var toHide = 1;
    for (var i = 0; i < count; i++) {
        tid0 = 't' + cid.substr(1) + '.' + (i+1);
        tid = 'f' + tid0;
        tr = document.getElementById(tid);
        if (!tr) {
            tid = 'p' + tid0;
            tr = document.getElementById(tid);
        }
        id_list[i] = tid;
        if (tr.className) {
            toHide = 0;
        }
    }
    for (var i = 0; i < count; i++) {
        tid = id_list[i];
        if (toHide) {
            document.getElementById('div_'+tid).style.display = 'none'
            document.getElementById(tid).className = 'hiddenRow';
        }
        else {
            document.getElementById(tid).className = '';
        }
    }
}


function showTestDetail(div_id){
    var details_div = document.getElementById(div_id)
    var displayState = details_div.style.display
    // alert(displayState)
    if (displayState != 'block' ) {
        displayState = 'block'
        details_div.style.display = 'block'
    }
    else {
        details_div.style.display = 'none'
    }
}


function html_escape(s) {
    s = s.replace(/&/g,'&amp;');
    s = s.replace(/</g,'&lt;');
    s = s.replace(/>/g,'&gt;');
    return s;
}

function drawCircle(pass, fail, error,skip){ 
    var color = ["#6c6","#c60","#c00","#666"];  
    var data = [pass,fail,error,skip]; 
    var text_arr = ["Pass", "Fail", "Error", "Skip"];
    var canvas = document.getElementById("circle");  
    var ctx = canvas.getContext("2d");  
    var startPoint=0;
    var width = 20, height = 10;
    var posX = 100 * 2 + 20, posY = 30;
    var textX = posX + width + 5, textY = posY + 10;
    for(var i=0;i<data.length;i++){  
        ctx.fillStyle = color[i];  
        ctx.beginPath();  
        ctx.moveTo(100,65);   
        ctx.arc(100,65,60,startPoint,startPoint+Math.PI*2*(data[i]/(data[0]+data[1]+data[2]+data[3])),false);  
        ctx.fill();  
        startPoint += Math.PI*2*(data[i]/(data[0]+data[1]+data[2]+data[3]));  
        ctx.fillStyle = color[i];  
        ctx.fillRect(posX, posY + 20 * i, width, height);  
        ctx.moveTo(posX, posY + 20 * i);  
        ctx.font = 'bold 20px';
        ctx.fillStyle = color[i];
        var percent = text_arr[i] + ":"+data[i];  
        ctx.fillText(percent, textX, textY + 20 * i);  
    }
}

/* obsoleted by detail in <div>
function showOutput(id, name) {
    var w = window.open("", //url
                    name,
                    "resizable,scrollbars,status,width=800,height=450");
    d = w.document;
    d.write("<pre>");
    d.write(html_escape(output_list[id]));
    d.write("\n");
    d.write("<a href='javascript:window.close()'>close</a>\n");
    d.write("</pre>\n");
    d.close();
}
*/
</script>
<div class="piechart">
    <div>
        <canvas id="circle" width="300" height="144" </canvas>
    </div>
</div>
%(heading)s
%(report)s
%(ending)s

</body>
</html>
"""
    # variables: (title, generator, stylesheet, heading, report, ending)


    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    STYLESHEET_TMPL = """
<style type="text/css" media="screen">
body        { font-family: verdana, arial, helvetica, sans-serif; font-size: 80%; }
table       { font-size: 100%; }
pre         { }

/* -- heading ---------------------------------------------------------------------- */
h1 {
	font-size: 16pt;
	color: gray;
}
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}

.heading .attribute {
    margin-top: 1ex;
    margin-bottom: 0;
}

.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}

/* -- css div popup ------------------------------------------------------------------------ */
a.popup_link {
}

a.popup_link:hover {
    color: red;
}

.popup_window {
    display: none;
    position: relative;
    left: 0px;
    top: 0px;
    /*border: solid #627173 1px; */
    padding: 10px;
    background-color: #E6E6D6;
    font-family: "Lucida Console", "Courier New", Courier, monospace;
    text-align: left;
    font-size: 8pt;
    width: 500px;
}

}
/* -- report ------------------------------------------------------------------------ */
#show_detail_line {
    margin-top: 3ex;
    margin-bottom: 1ex;
}
#result_table {
    width: 80%;
    border-collapse: collapse;
    border: 1px solid #777;
}
#header_row {
    font-weight: bold;
    color: white;
    background-color: #777;
}
#result_table td {
    border: 1px solid #777;
    padding: 2px;
}
#total_row  { font-weight: bold; }
.passClass  { background-color: #6c6; }
.failClass  { background-color: #c60; }
.errorClass { background-color: #c00; }
.skipClass  { background-color: #ccc; }
.passCase   { color: #6c6; }
.failCase   { color: #c60; font-weight: bold; }
.errorCase  { color: #c00; font-weight: bold; }
.skipCase   { color: #666; font-weight: bold; }
tr[id^=pt]  td { background-color: rgba(73,204,144,.3) !important ; }
tr[id^=ft]  td { background-color: rgba(252,161,48,.3) !important; }
tr[id^=et]  td { background-color: rgba(249,62,62,.3) !important ; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }


/* -- ending ---------------------------------------------------------------------- */
#ending {
}
.piechart{  
   position:absolute;
   top:30px;
   left:600px;
   width: 200px;
   float: left;
   display:  inline;
}
</style>
"""



    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_TMPL = """<div class='heading'>
<h1>%(title)s</h1>
%(parameters)s
<p class='description'>%(description)s</p>
</div>

""" # variables: (title, parameters, description)

    HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>
""" # variables: (name, value)



    # ------------------------------------------------------------------------
    # Report
    #

    REPORT_TMPL = """
<p id='show_detail_line'>Show
<a href='javascript:showCase(0)'>Summary</a>
<a href='javascript:showCase(1)'>Not Passed</a>
<a href='javascript:showCase(2)'>All</a>
</p>
<table id='result_table'>
<colgroup>
<col align='left' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
<col align='right' />
</colgroup>
<tr id='header_row'>
    <td>Test Case</td>
    <td>Count</td>
    <td>Pass</td>
    <td>Fail</td>
    <td>Error</td>
    <td>Skip</td>
    <td>View</td>
</tr>
%(test_list)s
<tr id='total_row'>
    <td>Total</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td>%(skip)s</td>
    <td>&nbsp;</td>
</tr>
</table>
<script>
    showCase(1);
    drawCircle(%(Pass)s, %(fail)s, %(error)s, %(skip)s);
</script>
""" # variables: (test_list, count, Pass, fail, error)

    REPORT_CLASS_TMPL = r"""
<tr class='%(style)s'>
    <td>%(desc)s</td>
    <td>%(count)s</td>
    <td>%(Pass)s</td>
    <td>%(fail)s</td>
    <td>%(error)s</td>
    <td>%(skip)s</td>
    <td><a href="javascript:showClassDetail('%(cid)s',%(count2)s)">Detail</a></td>
</tr>
""" # variables: (style, desc, count, Pass, fail, error, skip, cid)


    REPORT_TEST_WITH_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='6' align='center'>

    <!--css div popup start-->
    <a class="popup_link" onfocus='this.blur();' href="javascript:showTestDetail('div_%(tid)s')" >
        %(status)s</a>

    <div id='div_%(tid)s' class="popup_window">
        <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_%(tid)s').style.display = 'none' " >
           [x]</a>
        </div>
        <pre>
        %(script)s
        </pre>
    </div>
    <!--css div popup end-->

    </td>
</tr>
""" # variables: (tid, Class, style, desc, status)


    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='6' align='center'>%(status)s</td>
</tr>
""" # variables: (tid, Class, style, desc, status)


    REPORT_TEST_OUTPUT_TMPL = r"""
%(id)s: %(output)s
""" # variables: (id, output)



    # ------------------------------------------------------------------------
    # ENDING
    #

    ENDING_TMPL = """<div id='ending'>&nbsp;</div>"""

# -------------------- The end of the Template class -------------------


TestResult = unittest.TestResult


def strclass(cls):
    return "%s.%s" % (cls.__module__, cls.__qualname__)


class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self, output_wrapper, verbosity=1):
        TestResult.__init__(self)
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.skip_count = 0
        self.verbosity = verbosity
        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error; 3: skip),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []
        self.threadBuffer = {}
        self.output_wrapper = output_wrapper
        self.lock = threading.Lock()

    def startTest(self, test):
        with self.lock:
            TestResult.startTest(self, test)

    def _restoreStdout(self):
        with self.lock:
            super()._restoreStdout()
            self.complete_output()

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        t = threading.get_ident()
        if t not in self.output_wrapper:
            self.output_wrapper[t] = StringIO.StringIO()
        self.threadBuffer[threading.get_ident()] = self.output_wrapper[threading.get_ident()]
        self.output_wrapper[threading.get_ident()] = StringIO.StringIO()
        return self.threadBuffer[threading.get_ident()].getvalue()

    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        with self.lock:
            self.complete_output()

    def addSuccess(self, test):
        with self.lock:
            self.success_count += 1
            TestResult.addSuccess(self, test)
            output = self.complete_output()
            groups = getattr(test, 'group_map', {}).get(getattr(test, '_testMethodName'), ['Ungrouped'])
            self.result.append((0, test, output, '', groups))
            if self.verbosity > 1:
                sys.__stderr__.write('ok ')
                sys.__stderr__.write(str(test))
                sys.__stderr__.write('\n')
            else:
                sys.__stderr__.write('.')

    def addError(self, test, err):
        with self.lock:
            cls_name = type(test).__name__
            if cls_name != '_ErrorHolder':
                self.error_count += 1
            TestResult.addError(self, test, err)
            _, _exc_str = self.errors[-1]
            output = self.complete_output()
            groups = ['Ungrouped'] if cls_name == '_ErrorHolder' else \
                getattr(test, 'group_map', {}).get(getattr(test, '_testMethodName'), ['Ungrouped'])
            self.result.append((2, test, output, _exc_str, groups))
            if self.verbosity > 1:
                sys.__stderr__.write('E  ')
                sys.__stderr__.write(str(test))
                sys.__stderr__.write('\n')
            else:
                sys.__stderr__.write('E')

    def addFailure(self, test, err):
        with self.lock:
            self.failure_count += 1
            TestResult.addFailure(self, test, err)
            _, _exc_str = self.failures[-1]
            output = self.complete_output()
            groups = getattr(test, 'group_map', {}).get(getattr(test, '_testMethodName'), ['Ungrouped'])
            self.result.append((1, test, output, _exc_str, groups))
            if self.verbosity > 1:
                sys.__stderr__.write('F  ')
                sys.__stderr__.write(str(test))
                sys.__stderr__.write('\n')
            else:
                sys.__stderr__.write('F')

    def addSkip(self, test, reason):
        with self.lock:
            self.skip_count += 1
            TestResult.addSkip(self, test, reason)
            sys.stdout.write(reason)
            output = self.complete_output()
            groups = getattr(test, 'group_map', {}).get(getattr(test, '_testMethodName'), ['Ungrouped'])
            self.result.append((3, test, output, '', groups))
            if self.verbosity > 1:
                sys.__stderr__.write('S  ')
                sys.__stderr__.write(str(test))
                sys.__stderr__.write('\n')
            else:
                sys.__stderr__.write('S')

    def __repr__(self):
        return ("<%s passes=%i errors=%i failures=%i skips=%i>" %
                (strclass(self.__class__), self.success_count, self.error_count, self.failure_count, self.skip_count))


class OutputWrapper:
    def __init__(self, fps):
        self.fps = fps

    def write(self, value):
        tid = threading.get_ident()
        if tid not in self.fps:
            self.fps[tid] = StringIO.StringIO()
        self.fps[tid].write(value)
        # sys.__stdout__.write(value)

    def flush(self):
        pass


class HTMLTestRunner(Template_mixin):
    """
    """
    def __init__(self, stream=sys.stdout, verbosity=2, title=None, description=None):
        self._cid = 0
        self.stream = stream
        self.verbosity = verbosity
        if title is None:
            self.title = self.DEFAULT_TITLE
        else:
            self.title = title
        if description is None:
            self.description = self.DEFAULT_DESCRIPTION
        else:
            self.description = description

        self.startTime = datetime.datetime.now()
        self.output_wrapper = {}
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = OutputWrapper(self.output_wrapper)
        sys.stderr = OutputWrapper(self.output_wrapper)

    @staticmethod
    def print_stage(*args, default_stage=4):
        ss = defaultdict(list)
        for suite in args:
            stage = getattr(suite, '_stage', default_stage)
            ss[stage].append(suite)
        for i in sorted(ss.keys()):
            info = ' STAGE {0}, SUITES COUNT: {1} '.format(i, len(ss[i]))
            print('+{}+'.format('-'*len(info)))
            print('|{}|'.format(info))
            print('+{}+'.format('-'*len(info)))
            for suite in ss[i]:
                print('- ' + repr(suite))
            print('\n')

    def run_stage(self, *args, default_stage=4, timeout=None, pool_size=0):
        ss = defaultdict(list)
        u = 0
        for suite in args:
            stage = getattr(suite, '_stage', default_stage)
            ss[stage].append(suite)
            u = len(ss[stage]) if len(ss[stage]) > u else u
        ll = [ss[i] for i in sorted(ss.keys())]
        fs = {}
        all_futures = []
        p = ThreadPoolExecutor(pool_size or u)
        for l in ll:
            futures = []
            for suite in l:
                suite_repr = repr(suite)
                f = p.submit(suite, _TestResult(self.output_wrapper, self.verbosity))
                futures.append(f)
                fs[f] = suite_repr
            wait(futures, timeout)
            all_futures += futures

        sys.stdout = self.stdout
        sys.stderr = self.stderr
        result = _TestResult(None)
        results = []
        timeout = False
        for f in all_futures:
            try:
                r = f.result(0)
                result.failures += r.failures
                result.errors += r.errors
                result.skipped += r.skipped
                result.testsRun += r.testsRun
                result.success_count += r.success_count
                result.failure_count += r.failure_count
                result.error_count += r.error_count
                result.skip_count += r.skip_count
                result.result += r.result
                results.append(r)
            except TimeoutError:
                timeout = True
                sys.__stderr__.write('Timed out while test is still running\n')
                result.error_count += 1
                result.result.append((2, _ErrorHolder('Suite timeout'), fs[f], fs[f], ['Ungrouped']))

        self.stopTime = datetime.datetime.now()
        self.generateReport(result)
        print('Time Elapsed: {}'.format((self.stopTime - self.startTime)), file=sys.__stderr__)
        return result, results, timeout

    def run(self, *args, timeout=None, pool_size=0):
        "Run the given test case or test suite."
        if pool_size == 0:
            pool_size = len(args)

        pool = ThreadPoolExecutor(pool_size)
        futures = []
        fsmap = {}
        for test in args:
            suite_repr = repr(test)
            f = pool.submit(test, _TestResult(self.output_wrapper, self.verbosity))
            futures.append(f)
            fsmap[f] = suite_repr

        wait(futures, timeout)
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        result = _TestResult(None)
        results = []
        timeout = False
        for f in futures:
            try:
                r = f.result(0)
                result.failures += r.failures
                result.errors += r.errors
                result.skipped += r.skipped
                result.testsRun += r.testsRun
                result.success_count += r.success_count
                result.failure_count += r.failure_count
                result.error_count += r.error_count
                result.skip_count += r.skip_count
                result.result += r.result
                results.append(r)
            except TimeoutError:
                timeout = True
                sys.__stderr__.write('Timed out while test is still running\n')
                result.error_count += 1
                result.result.append((2, _ErrorHolder('Suite timeout'), fsmap[f], fsmap[f], ['Ungrouped']))

        self.stopTime = datetime.datetime.now()
        self.generateReport(result)
        print('Time Elapsed: {}'.format((self.stopTime - self.startTime)), file=sys.__stderr__)
        return result, results, timeout

    def sortResult(self, result_list):
        # unittest does not seems to run in any particular order.
        # Here at least we want to group them together by class.
        rmap = {}
        classes = []
        for n,t,o,e,g in result_list:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n,t,o,e))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def getReportAttributes(self, result):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        """
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        ose_version = "" # os.environ['API_TEST_ENV_PROFILE']
        vendor = ""
        status = []
        if result.success_count: status.append('Pass %s'    % result.success_count)
        if result.failure_count: status.append('Failure %s' % result.failure_count)
        if result.error_count:   status.append('Error %s'   % result.error_count  )
        if result.skip_count:    status.append('Skip %s'    % result.skip_count   )
        if status:
            status = ' '.join(status)
        else:
            status = 'none'
        return [
            # ('Platform', vendor),
            # ('OSE Version', ose_version),
            ('Start Time', startTime),
            ('Duration', duration),
            ('Status', status),
        ]

    def generateReport(self, result):
        report_attrs = self.getReportAttributes(result)
        generator = 'HTMLTestRunner %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attrs)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TMPL % dict(
            title = saxutils.escape(self.title),
            generator = generator,
            stylesheet = stylesheet,
            heading = heading,
            report = report,
            ending = ending,
        )
        conv = Ansi2HTMLConverter(inline=True, escaped=False)
        output = conv.convert(output, full=False)
        self.stream.write(output.encode('utf8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                    name = saxutils.escape(name),
                    value = saxutils.escape(value),
                )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title = saxutils.escape(self.title),
            parameters = ''.join(a_lines),
            description = saxutils.escape(self.description),
        )
        return heading

    def _generate_report(self, result):
        rows = []
        sortedResult = self.sortResult(result.result)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            # subtotal for a class
            np = nf = ne = ns = 0
            for n,t,o,e in cls_results:
                if n == 0: np += 1
                elif n == 1: nf += 1
                elif n == 3: ns += 1
                else: ne += 1

            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__.split('.')[-1], cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            arg_count = np+nf+ne+ns
            arg_count2 = arg_count
            arg_pass = np
            arg_fail = nf
            arg_error = ne
            arg_skip = ns

            if cls.__name__ == '_ErrorHolder':
                arg_count = arg_pass = arg_fail = arg_error = arg_skip = '-'

            row = self.REPORT_CLASS_TMPL % dict(
                style = ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
                desc = desc,
                count = arg_count,
                count2 = arg_count2,
                Pass = arg_pass,
                fail = arg_fail,
                error = arg_error,
                skip = arg_skip,
                cid = 'c%s' % (self._cid+1),
            )
            rows.append(row)

            for tid, (n,t,o,e) in enumerate(cls_results):
                self._generate_report_test(rows, self._cid, tid, n, t, o, e)

            self._cid += 1

        report = self.REPORT_TMPL % dict(
            test_list = ''.join(rows),
            count = str(result.success_count+result.failure_count+result.error_count+result.skip_count),
            Pass = str(result.success_count),
            fail = str(result.failure_count),
            error = str(result.error_count),
            skip = str(result.skip_count),
        )
        return report

    def _generate_report_test(self, rows, cid, tid, n, t, o, e):
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(o or e)
        tid = (n == 0 and 'p' or 'f') + 't%s.%s' % (cid+1,tid+1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        desc = t.description if type(t).__name__ == '_ErrorHolder' else desc
        tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL

        # o and e should be byte string because they are collected from stdout and stderr?
        if isinstance(o,str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # uo = unicode(o.encode('string_escape'))
            uo = bytes(o, 'utf-8').decode('latin-1')
        else:
            uo = o
        if isinstance(e,str):
            # TODO: some problem with 'string_escape': it escape \n and mess up formating
            # ue = unicode(e.encode('string_escape'))
            ue = bytes(e, 'utf-8').decode('latin-1')
        else:
            ue = e

        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id = tid,
            output = saxutils.escape(uo+ue),
        )

        row = tmpl % dict(
            tid = tid,
            Class = (n == 0 and 'hiddenRow' or 'none'),
            style = n == 2 and 'errorCase' or n == 1 and 'failCase' or (n == 3 and 'skipCase' or 'none'),
            desc = desc,
            script = script,
            status = self.STATUS[n],
        )
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL


##############################################################################
# Facilities for running tests from the command line
##############################################################################

# Note: Reuse unittest.TestProgram to launch test. In the future we may
# build our own launcher to support more specific command line
# parameters like test title, CSS, etc.
class TestProgram(unittest.TestProgram):
    """
    A variation of the unittest.TestProgram. Please refer to the base
    class for command line parameters.
    """
    def runTests(self):
        # Pick HTMLTestRunner as the default test runner.
        # base class's testRunner parameter is not useful because it means
        # we have to instantiate HTMLTestRunner before we know self.verbosity.
        if self.testRunner is None:
            # TODO fix this None
            self.testRunner = HTMLTestRunner(None, verbosity=self.verbosity)
        unittest.TestProgram.runTests(self)


main = TestProgram

##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)
