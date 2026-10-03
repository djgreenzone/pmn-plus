# Builds /account/index.html from account/template.html with the site header (nav) and the homepage footer.
# Also copies the server functions into /api and creates /assets/pmn-config.js if it doesn't exist yet.
import os, re, shutil
HERE=os.path.dirname(os.path.abspath(__file__))
def build(root, nb):
    home=open(os.path.join(root,'index.html')).read()
    foot=home[home.index('<footer class="foot">'):home.index('</footer>')+9]
    css='\n'.join(l for l in home.split('\n') if re.match(r'(\.foot|@media \(min-width:900px\)\{\.foot)',l))
    t=open(os.path.join(HERE,'template.html')).read().replace('{{FOOTER}}',foot).replace('{{FOOTCSS}}',css)
    os.makedirs(os.path.join(root,'account'),exist_ok=True)
    out=os.path.join(root,'account','index.html');open(out,'w').write(t)
    nb.build_home(out)                                   # same header as the rest of the site
    # copy back the year script the footer uses
    s=open(out).read()
    if 'id="yr"' in s and "getElementById('yr')" not in s:
        s=s.replace('</body>',"<script>document.getElementById('yr').textContent=new Date().getFullYear()</script>\n</body>",1);open(out,'w').write(s)
    for rel in ('api/_account.js','api/account/link.js','api/account/orders.js'):
        dst=os.path.join(root,rel);os.makedirs(os.path.dirname(dst),exist_ok=True);shutil.copyfile(os.path.join(HERE,rel),dst)
    cfg=os.path.join(root,'assets','pmn-config.js')
    if not os.path.exists(cfg):
        open(cfg,'w').write('/* Public settings for the browser. Only PUBLIC values go here (never the service_role key). */\nwindow.PMN_CONFIG={\n  supabaseUrl:"",        // Supabase → Project Settings → API → Project URL\n  supabaseAnonKey:"",    // Supabase → Project Settings → API → anon / publishable key\n  google:false,          // true once Google sign-in is switched on in Supabase\n  apple:false,           // true once Apple sign-in is switched on in Supabase\n  memberGift:"",         // text shown on the account page once the Shopify member gift is set up\n  accountsLive:false     // true shows the account icon in the header\n};\n')
