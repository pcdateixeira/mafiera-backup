# Fix nested tags
# Fix internal links

import re

def validateText(text):
    # Removes XML tags that surround the text block
    text = text[67:-56:1]
    text = validateQuote(text)
    text = validateImg(text)
    text = validateUrl(text)
    text = validateFormatting(text)

    return text

# Fixes quote tags
def validateQuote(text):
    text = re.sub(r'<div class=\"bbCodeBlock bbCodeQuote\" data-author=\"(.+?)\">\n<aside>\n<div class=\"attribution type\">', "[quote=\"author:", text)
    text = text.replace(" said:\n<a href=\"goto/post?id=", ", post:")
    text = re.sub(r' onclick=\"return scrollToId\(\'\#post-(.+?)\'\)\">↑</a>\n</div>\n<blockquote class=\"quoteContainer\"><div class=\"quote\">', "]", text)
    text = re.sub(r'#post-[0-9]+\"\]', "\"]", text)
    text = text.replace("</div><div class=\"quoteExpand\">Click to expand...</div></blockquote>\n</aside>\n</div>\n<script>\nfunction scrollToId(selector, offset = 60) {\n  window.scroll(0, document.querySelector(selector).offsetTop - offset);\n  return false\n}\n</script>\n", "[\quote]\n")

    return text

# Fixes img tags
def validateImg(text):
    url = re.search(r'<img alt=\"\[​IMG\]\" class=\"bbCodeImage LbImage\" data-url=\"(.+?) src=(.+?)/>', text)
    if url:
        text = re.sub(r'<img alt=\"\[​IMG\]\" class=\"bbCodeImage LbImage\" data-url=\"(.+?) src=(.+?)/>', "[img]" + url.group(2)[1:-1:1] + "[/img]", text)

    return text

# Fixes url tags
def validateUrl(text):
    url = re.search(r'<a class=\"externalLink\" href=(.+?) rel=\"nofollow\" target=\"_blank\">(.+?)</a>', text)
    if url:
        text = re.sub(r'<a class=\"externalLink\" href=(.+?) rel=', "[url='" + url.group(1)[1:-1:1] + "'] rel=", text)
        text = re.sub(r' rel=\"nofollow\" target=\"_blank\">(.+?)</a>', url.group(2) + "[/url]", text)


    return text

# Fixes formatting tags
def validateFormatting(text):
    text = text.replace("<br/>", "")

    text = text.replace("<i>", "[i]")
    text = text.replace("</i>", "[\i]")

    text = text.replace("<b>", "[b]")
    text = text.replace("</b>", "[\b]")

    text = text.replace("<span style=\"text-decoration: underline\">", "[u]")
    underline = re.search(r'\[u\](.+?)</span>', text)
    if underline:
        text = re.sub(r'\[u\](.+?)</span>', "[u]" + underline.group(1) + "[/u]", text)

    text = text.replace("<span style=\"text-decoration: line-through\">", "[s]")
    strike = re.search(r'\[s\](.+?)</span>', text)
    if strike:
        text = re.sub(r'\[s\](.+?)</span>', "[s]" + strike.group(1) + "[/s]", text)

    text = text.replace("<span style=\"font-size: ", "[size]")
    size = re.search(r'\[size\](.+?)px\">(.+?)</span>', text)
    if size:
        text = re.sub(r'\[size\](.+?)px\">', "[size=" + size.group(1) + "px]", text)
        text = re.sub(r'px\](.+?)</span>', "px]" + size.group(2) + "[/size]", text)

    return text
