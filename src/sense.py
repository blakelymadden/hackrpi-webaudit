# Web Audit profiles a website to show a user what third party actions
# occur when they connect to that website.
# 
# Copyright (C) 2014 Blake Madden, Anders Dahl
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import html_parser
import re
import subprocess

def validate_web_url(url):
    perfect_url_re = r"https?://[\w.-]*\.[A-Za-z]{2,}?/"
    basic_url_re = r"[\w.-]*\.[\w]{2,}/"
    url = url if url[-1] == '/' else url + '/'
    if re.match(perfect_url_re, url):
        return url
    if not re.match(basic_url_re, url):
        return None
    if "http" not in url and "://" not in url:
        return "http://" + url
    return None

def url_callback_ga(url):
    se = SenseEngine(["script"], "(google-analytics)", url)
    return se.analyze()

class SenseEngine:
    def __init__(self, tags, content, url):
        self.tags = tags
        self.content = content
        self.url = validate_web_url(url)
        if self.url is None:
            raise Exception("Bad URL: " + url)
        self.site_to_cookies = None
        self.page_data = ""

    def poke_website(self):
        out = self.url.split('/')[-1]
        # should change this so that what is currently "a.html" is cached
        # for return visits... TODO
        out += '.html' if not out == "" else "a.html"
        out_cookies = out + ".cookies"
        self.site_to_cookies = (out, out_cookies)
        curl_args = ['curl', '-o', out, '-c', out_cookies, '-L', self.url]
        subprocess.check_call(curl_args)

    def pull_tag_content(self):
        self.poke_website()
        fdata = open(self.site_to_cookies[0], 'r')
        fcookies = open(self.site_to_cookies[1], 'r')
        self.data = fdata.read()
        cookies = fcookies.read()
        fdata.flush()
        fcookies.flush()
        fdata.close()
        fcookies.close()
        aggregator = html_parser.HTMLTagContentAggregator(self.data,
                                                          self.tags,
                                                          self.content)
        return aggregator.map_content_to_data()

    def analyze_ga(self, ga_block):
        capture_ga_var = r"var[\s]*?([\w]+)[\s]*?="
        raw_ga_var = re.findall(capture_ga_var, ga_block.pop())[0]
        ga_var = "(" + raw_ga_var + ")"
        aggregator = html_parser.HTMLTagContentAggregator(self.data, ["script"],
                                                          ga_var)
        ga_to_blocks = aggregator.map_content_to_data()
        ga_tracking = ga_to_blocks.get(raw_ga_var)
        ga_var_push_re = "%s\.push\(([\s\S]*?)\);" % raw_ga_var
        ret = []
        for track in ga_tracking:
            ret.extend(re.findall(ga_var_push_re, track))
        return ret

    def analyze(self):
        content_to_data = self.pull_tag_content()
        for content in content_to_data:
            block = content_to_data.get(content)
            if content == "google-analytics":
                return self.analyze_ga(block)
