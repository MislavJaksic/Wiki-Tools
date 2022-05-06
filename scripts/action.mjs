import fetch from "node-fetch";

export class WikiActionPayload {
    constructor(url, options) {
        this.url = url;
        this.options = options;
    }

    setReferer(referer) {
        this.options.headers.Referer = referer;
    }

    setBody(body) {
        this.options.body = body;
    }

    checkIntegrity() {
        if (this.options.headers.Referer === null) {
            throw new ReferenceError("Header's Referer is not set.");
        } else if (this.options.body === null) {
            throw new ReferenceError("Option's body is not set.");
        }
    }
}

export class WikiAction {
    constructor(payload) {
        payload.checkIntegrity();
        this.payload = payload;
    }

    async do() {
        const reponse = await fetch(this.payload.url, this.payload.options);
        console.log(reponse.ok);
        console.log(reponse.redirected);
        console.log(reponse.status);
        console.log(reponse.type);
        console.log(reponse.url);
    }
  }
