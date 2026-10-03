/* Public settings for the browser. Only PUBLIC values go here (never the service_role key). */
window.PMN_CONFIG={
  supabaseUrl:"https://zacfssfjlmixnqhjuoed.supabase.co",
  supabaseAnonKey:"sb_publishable__o1QyHHm3--jPJ2iz61m8A_ssXrOmWk",   // Supabase publishable key (safe to be public)
  google:true,           // Google sign-in (Supabase provider on, Google Cloud project pmn-plus)
  apple:false,           // true once Apple sign-in is switched on in Supabase
  memberGift:"A surprise from the PMN+ vault in every order. What\u2019s inside changes with each drop.",
  accountsLive:true,      // shows the account icon in the header
  analytics:{ga4:"G-KEQ8HPTH9W", meta:"1983591485663494", tiktok:"", clarity:"ys5h8s9j8m"}  // GA4 G-…, Meta Pixel ID, TikTok Pixel ID, Clarity project ID; blank = off
};
