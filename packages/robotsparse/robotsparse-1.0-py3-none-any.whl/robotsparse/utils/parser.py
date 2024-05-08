import re
from .exceptions import *
from ._regex import searchForGroup

def getRobotsInfo(robotsContent: str) -> dict:
    robotsContent = re.sub(r"\n{1,}", "\n", robotsContent)
    robots = {}
    userAgents = {}
    userAgentIter = re.finditer(
        r"^user-agent: (?P<ua>.*?)(?:$|\s?#)\n(?P<rules>.*?)(?=user-agent|\Z)",
        robotsContent,
        flags=(re.MULTILINE | re.DOTALL | re.IGNORECASE),
    )
    for uaIter in userAgentIter:
        ua = uaIter.group("ua")
        rules = {}
        for ruleIter in uaIter.group("rules").splitlines():
            ruleIter = ruleIter.lower()
            try:
                _rule, _value = re.search(r"^(.*?)\s*:\s*(.*?)(?:$|\s?#)", ruleIter).groups()
            except:
                continue
            if _rule != None and _value != None:
                if _rule in rules:
                    rules[_rule].append(_value)
                else:
                    rules[_rule] = [_value]
        userAgents[ua] = rules
    sitemaps = re.findall(
        r"^(?:sitemap: )(.*?)(?:$|\s?#)",
        robotsContent,
        flags=(re.MULTILINE | re.DOTALL | re.IGNORECASE),
    )
    if userAgents != {}: robots["user-agents"] = userAgents
    if sitemaps != []: robots["sitemaps"] = list(set(sitemaps))
    return robots if robots != {} else None

def getXmlSitemapInfo(sitemapContent: str) -> dict:
    sitemapContent = re.sub(r"\n{1,}", "", sitemapContent, flags=(re.DOTALL | re.MULTILINE))
    innerUrls = re.findall(
        r"<\s*(sitemap|url).*?>(.*?)<\s*/\s*\1\s*>",
        sitemapContent,
        re.DOTALL | re.MULTILINE
    )
    sitemapInfo = []
    for i in innerUrls:
        loc = searchForGroup(
            r"<\s*loc\s*>(.*?)<\s*/\s*loc\s*>",
            i[1],
            1
        )
        lastmod = searchForGroup(
            r"<\s*lastmod\s*>(.*?)<\s*/\s*lastmod\s*>",
            i[1],
            1
        )
        sitemapInfo.append({"url": loc, "lastModified": lastmod})
    return sitemapInfo if bool(sitemapInfo) else None

class Robots:
    """Contains parsed robots information."""
    def __init__(self, fileContents: str):
        self.robots = getRobotsInfo(fileContents)
        if self.robots == None:
            return
        self.user_agents = list(self.robots.get("user-agents"))
        self.sitemaps = self.robots.get("sitemaps")
        if self.user_agents != None:
            keysToSearch = ["allow", "disallow", "crawl-delay"]
            for ua in self.user_agents:
                for key in keysToSearch:
                    keyAttribute = key.replace("-", "_")
                    currentKeyValue = self.robots["user-agents"][ua].get(key)
                    if currentKeyValue == None:
                        setattr(self, keyAttribute, None)
                        continue
                    try:
                        currentKeyAttributeValue = getattr(self, keyAttribute)
                    except:
                        currentKeyAttributeValue = {}
                    currentKeyAttributeValue[ua] = currentKeyValue
                    setattr(self, keyAttribute, currentKeyAttributeValue)


