<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
<xsl:output method="html" encoding="UTF-8" indent="yes"/>
<xsl:template match="/">
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta name="robots" content="noindex,follow"/>
<title>Sitemap · PMN+</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;family=Instrument+Sans:wght@400;500;600&amp;display=swap" rel="stylesheet"/>
<style>
:root{--bg:#000;--ink:#fff;--dim:#8A8A8E;--line:#242426;--card:#0d0e12;--blue:#1E4FA0;--red:#C8102E}
*{box-sizing:border-box;margin:0}
body{background:var(--bg);color:var(--ink);font-family:'Instrument Sans',system-ui,-apple-system,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:960px;margin:0 auto;padding:2rem 16px 4rem}
header{display:flex;align-items:center;gap:1rem;padding-bottom:1.5rem;border-bottom:1px solid var(--line)}
header img{width:44px;height:auto}
.bar{height:4px;background:linear-gradient(90deg,var(--blue) 50%,var(--red) 50%);margin:0 0 2rem}
h1{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:clamp(2.6rem,8vw,4rem);line-height:.92;letter-spacing:.01em;text-transform:uppercase}
.eyebrow{font-family:'Bebas Neue',sans-serif;letter-spacing:.18em;color:var(--dim);font-size:1.05rem}
p.lead{color:var(--dim);margin:.75rem 0 2rem;max-width:60ch}
table{width:100%;border-collapse:collapse;font-size:.95rem}
th{font-family:'Bebas Neue',sans-serif;font-weight:400;letter-spacing:.12em;color:var(--dim);text-align:left;padding:.6rem .5rem;border-bottom:1px solid var(--line)}
td{padding:.7rem .5rem;border-bottom:1px solid var(--line);vertical-align:top}
td a{color:var(--ink);text-decoration:none;word-break:break-all}
td a:hover{text-decoration:underline}
td.n{color:var(--dim);white-space:nowrap}
footer{margin-top:2.5rem;color:var(--dim);font-size:.85rem}
footer a{color:var(--ink)}
@media(max-width:600px){.hide-sm{display:none}}
</style>
</head>
<body>
<div class="bar"></div>
<div class="wrap">
<header><a href="/"><img src="/shop/brand/pmn-plus-logo-white.svg" alt="PMN+ home" width="44" height="48"/></a><span class="eyebrow">Polynesian Music Network</span></header>
<h1 style="margin-top:2rem">Sitemap</h1>
<p class="lead"><xsl:value-of select="count(s:urlset/s:url)"/> pages. This is the XML sitemap search engines read; it's styled here so it's easy to browse.</p>
<table>
<thead><tr><th>Page</th><th class="hide-sm">Images</th><th>Updated</th></tr></thead>
<tbody>
<xsl:for-each select="s:urlset/s:url">
<tr>
<td><a href="{s:loc}"><xsl:value-of select="substring-after(s:loc,'polynesianmusicnetwork.com')"/><xsl:if test="substring-after(s:loc,'polynesianmusicnetwork.com')='/'"> (home)</xsl:if></a></td>
<td class="n hide-sm"><xsl:value-of select="count(image:image)"/></td>
<td class="n"><xsl:value-of select="s:lastmod"/></td>
</tr>
</xsl:for-each>
</tbody>
</table>
<footer><a href="/">Home</a> · <a href="/shop">Shop</a> · <a href="/about">About</a></footer>
</div>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
