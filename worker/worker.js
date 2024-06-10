addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const loadedData = await fetchMetadata()
  // Replace it with real values
  const keyLoads = {
    "code": "",
    "access_token": "",
    "refresh_token": "",
    "user_bookmarks_illust": "",
    "proxy_url": "i.pixiv.re"
  }  

  const apiFormat = new URL(request.url).searchParams.get("format")
  const apiNsfw = new URL(request.url).searchParams.get("r18") || "0"

  const randomIndex = Math.floor(Math.random() * loadedData.length)
  const randomData = loadedData[randomIndex]

  const imageUrl = randomData.url
  const imageProxyUrl = imageUrl.replace(/i\.pximg\.net/, keyLoads.proxy_url)

  const data = {
    data: {
      id: randomData.id,
      title: randomData.title,
      image_url: imageUrl,
      proxy_url: imageProxyUrl,
      user: {
        name: randomData.user.name,
        id: randomData.user.id,
        account: randomData.user.account,
      },
      tags: randomData.tags,
      r18: randomData.r18,
    },
    code: 200,
    index: randomIndex
  }

  // Filter r18 tag
  if ((apiNsfw === "0" && randomData.r18 === 1) || (apiNsfw === "1" && randomData.r18 === 0)) {
    return handleRequest(request) // Retry to get a suitable image
  }

  // Return different formats
  if (apiFormat === "json") {
    return new Response(JSON.stringify(data), {
      headers: { "Content-Type": "application/json" },
    })
  } else if (apiFormat === "image") {
    return Response.redirect(imageProxyUrl, 302)
  } else {
    return new Response(JSON.stringify(data), {
      headers: { "Content-Type": "application/json" },
    })
  }
}

async function fetchMetadata() {
  const metadata = await CLOUDFLARE_KV_NAMESPACE.get('metadata')
  return JSON.parse(metadata)
}