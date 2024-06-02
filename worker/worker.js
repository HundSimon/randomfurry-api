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
    "proxy_url": ""
  }  

  const apiFormat = new URL(request.url).searchParams.get("format")
  const apiNsfw = new URL(request.url).searchParams.get("r18") || "0"

  const randomData = loadedData[Math.floor(Math.random() * loadedData.length)]

  // Image URL with different sizes
  let imageUrl
  if (randomData.meta_single_page === {}) {
    imageUrl = randomData.image_urls.large
  } else if (randomData.meta_pages.length > 0) {
    imageUrl = randomData.meta_pages[0].image_urls.large
  } else {
    imageUrl = randomData.meta_single_page.original_image_url
  }

  const imageProxyUrl = imageUrl.replace(/i\.pximg\.net/, keyLoads.proxy_url)

  const data = {
    data: {
      id: randomData.id,
      title: randomData.title,
      image_url: imageUrl,
      image_url_proxy: imageProxyUrl,
      user: {
        name: randomData.user.name,
        id: randomData.user.id,
        account: randomData.user.account,
      },
      tags: randomData.tags,
      r18: randomData.x_restrict,
    },
  }

  // Filter r18 tag
  if ((apiNsfw === "0" && randomData.x_restrict === 1) || (apiNsfw === "1" && randomData.x_restrict === 0)) {
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