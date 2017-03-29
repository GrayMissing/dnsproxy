from dns.name import Name, from_text

a = from_text("meta.sankuai.com")
b = from_text("www.sankuai.com")
print a.fullcompare(b)
