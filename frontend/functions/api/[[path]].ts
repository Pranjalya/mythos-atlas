const BACKEND_URL = "https://mythos-atlas-three.vercel.app";

export async function onRequest(context: {
  request: Request;
  params: { path: string[] };
}): Promise<Response> {
  const { request, params } = context;

  // Reconstruct the target URL: strip the CF Pages origin, keep /api/...
  const url = new URL(request.url);
  const targetUrl = `${BACKEND_URL}/api/${params.path.join("/")}${url.search}`;

  // Forward the request verbatim
  const proxyRequest = new Request(targetUrl, {
    method: request.method,
    headers: request.headers,
    body: request.method !== "GET" && request.method !== "HEAD"
      ? request.body
      : undefined,
    redirect: "follow",
  });

  const response = await fetch(proxyRequest);

  // Pass response back, adding CORS headers in case the backend omits them
  const newHeaders = new Headers(response.headers);
  newHeaders.set("Access-Control-Allow-Origin", "*");
  newHeaders.set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
  newHeaders.set("Access-Control-Allow-Headers", "Content-Type, Authorization");

  // Handle CORS preflight
  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: newHeaders });
  }

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders,
  });
}
