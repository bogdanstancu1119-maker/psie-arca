// HYDRA PUBLIC WORKER — generat de meta-creierul Hydrei, copiat de Arhitect
// (invocare 6ac117f41ecab4f30d159e18). Deploy: wrangler deploy --temporary.
// API gratuit de traducere, zero cost, organism PSIE public.

export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (request.method === 'GET' && url.pathname === '/') {
      return new Response('<h1>Hydra</h1><p>Organism PSIE. API: POST /traduce {text, spre}</p>', {headers:{'content-type':'text/html'}});
    }
    if (request.method === 'POST' && url.pathname === '/traduce') {
      const {text, spre='en'} = await request.json();
      const r = await fetch('https://api.mymemory.translated.net/get?q=' + encodeURIComponent(text) + '&langpair=auto|' + spre);
      const d = await r.json();
      return Response.json({tradus: d?.responseData?.translatedText||'', sursa:'MyMemory gratuit'});
    }
    return new Response('Not found', {status:404});
  }
};
