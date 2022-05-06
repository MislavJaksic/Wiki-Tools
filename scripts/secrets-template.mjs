/*
mediaWikiUrl is the base URL.
XUrl, XOptions and XBody are generated by:
* open `Network` tab in Chrome Developer Tools (F12)
* generate a POST request by submiting an action you are trying to script
* right-click on the generated POST request, `Copy`, `Copy as Node.js fetch`
* you will get a `fetch()` function made up of a URL and options (made up of a header, body, method, ...)
*/

const mediaWikiUrl = "";
const cookie = "";
const bodyEditToken = "";

export let curlyOptions = {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": cookie,
    "Referer": null,
    "Referrer-Policy": "strict-origin-when-cross-origin"
  },
  "body": null,
  "method": "POST"
}

export const mergeUsersUrl = mediaWikiUrl + "Special:UserMerge";
export let curlyMergeUsersReferer = null;
export let curlyMergeUsersBody = null;

export const movePagesUrl = mediaWikiUrl + "index.php?title=Special:MovePage&action=submit";
export let curlyMovePagesReferer = mediaWikiUrl + "Special:MovePage/{}";
export let curlyMovePagesBody = "wpNewTitleNs={}&wpNewTitleMain={}&wpReason={}&wpMovetalk=1&wpLeaveRedirect={}&wpMove=Move+page&wpOldTitle={}&wpEditToken=" + bodyEditToken;
