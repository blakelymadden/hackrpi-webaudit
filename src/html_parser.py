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

    def map_content_to_data(self):
        contents_to_data = {}
        for tag in self.tags:
            tag_contents_list = self.retrieve_content_inside_all_tags(tag)
            for block in tag_contents_list:
                blocks_with_content = re.findall(self.content, block)
                for content_match in blocks_with_content:
                    previous = contents_to_data.get(content_match)
                    if previous:
                        contents_to_data[content_match] = previous.append(block)
                    else:
                        contents_to_data[content_match] = [block]
        return contents_to_data
