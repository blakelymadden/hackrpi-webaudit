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

import re

class HTMLTagContentAggregator:
    def __init__(self, html_file, tags, content):
        self.html_file = html_file
        self.tags = tags
        self.content = content

    def retrieve_content_inside_all_tags(self, tag):
        tag_re = r"<%s[^>]*?>([\s\S]*?)</%s?>" % (tag, tag)
        tag_contents_list = re.findall(tag_re, self.html_file)
        return tag_contents_list

    def map_links_to_tags(self):
        links_to_contents = {}
        for tag in self.tags:
            tag_contents_list = self.retrieve_content_inside_all_tags(tag)
            for block in tag_contents_list:
                links = re.findall(self.content, block)
                for link in links:
                    previous = links_to_contents.get(link)
                    if previous:
                        links_to_contents[link] = previous.append(block)
                    else:
                        links_to_contents[link] = [block]
        return links_to_contents
