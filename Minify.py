import sublime
import sublime_plugin
import http.client
import urllib

class ClosureBase(sublime_plugin.TextCommand):
       
    def exec_request(self, js_code, compilation_level):
        connection = http.client.HTTPSConnection('closure-compiler.appspot.com')
        headers = { "Content-type": "application/x-www-form-urlencoded" }
        params = urllib.parse.urlencode({
            'js_code': js_code.encode('utf-8'),
            'compilation_level': compilation_level,
            'output_format': "text",
            'output_info': "compiled_code" })
        connection.request('POST', '/compile', params, headers)
        response = connection.getresponse()
        resText = response.read().decode('utf-8')
        return resText

class Minify(ClosureBase):

    def run(self, edit):
        for selection in self.view.sel():
            result = self.exec_request(self.view.substr(selection), "WHITESPACE_ONLY")
            self.view.replace(edit, selection, result)

class Obfuscate(ClosureBase):

    def run(self, edit):
        for selection in self.view.sel():
            result = self.exec_request(self.view.substr(selection), "ADVANCED_OPTIMIZATIONS")
            self.view.replace(edit, selection, result)