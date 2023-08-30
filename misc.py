def get_header(account_info_url: str):
    return {
        'authority'                     : 'www.binance.com',
        'accept'                        : '*/*',
        'accept-language'               : 'en-US,en;q=0.9',
        'bnc-uuid'                      : '0202c537-8c2b-463a-bdef-33761d21986a',
        'clienttype'                    : 'web',
        'csrftoken'                     : 'd41d8cd98f00b204e9800998ecf8427e',
        'device-info'                   : 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTA4MCIsImF2YWlsYWJsZV9zY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTA0MCIsInN5c3RlbV92ZXJzaW9uIjoiV2luZG93cyAxMCIsImJyYW5kX21vZGVsIjoidW5rbm93biIsInN5c3RlbV9sYW5nIjoicnUtUlUiLCJ0aW1lem9uZSI6IkdNVCszIiwidGltZXpvbmVPZmZzZXQiOi0xODAsInVzZXJfYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTAxLjAuNDk1MS42NyBTYWZhcmkvNTM3LjM2IiwibGlzdF9wbHVnaW4iOiJQREYgVmlld2VyLENocm9tZSBQREYgVmlld2VyLENocm9taXVtIFBERiBWaWV3ZXIsTWljcm9zb2Z0IEVkZ2UgUERGIFZpZXdlcixXZWJLaXQgYnVpbHQtaW4gUERGIiwiY2FudmFzX2NvZGUiOiI1ZjhkZDMyNCIsIndlYmdsX3ZlbmRvciI6Ikdvb2dsZSBJbmMuIChJbnRlbCkiLCJ3ZWJnbF9yZW5kZXJlciI6IkFOR0xFIChJbnRlbCwgSW50ZWwoUikgVUhEIEdyYXBoaWNzIDYyMCBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKSIsImF1ZGlvIjoiMTI0LjA0MzQ3NTI3NTE2MDc0IiwicGxhdGZvcm0iOiJXaW4zMiIsIndlYl90aW1lem9uZSI6IkV1cm9wZS9Nb3Njb3ciLCJkZXZpY2VfbmFtZSI6IkNocm9tZSBWMTAxLjAuNDk1MS42NyAoV2luZG93cykiLCJmaW5nZXJwcmludCI6IjE5YWFhZGNmMDI5ZTY1MzU3N2Q5OGYwMmE0NDE4Nzc5IiwiZGV2aWNlX2lkIjoiIiwicmVsYXRlZF9kZXZpY2VfaWRzIjoiMTY1MjY4OTg2NTQwMGdQNDg1VEtmWnVCeUhONDNCc2oifQ==',
        'fvideo-id'                     : '3214483f88c0abbba34e5ecf5edbeeca1e56e405',
        'lang'                          : 'en',
        'origin'                        : 'https://www.binance.com',
        'referer'                       : account_info_url,
        'sec-ch-ua'                     : '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile'              : '?0',
        'sec-ch-ua-platform'            : '"Windows"',
        'sec-fetch-dest'                : 'empty',
        'sec-fetch-mode'                : 'cors',
        'sec-fetch-site'                : 'same-origin',
        'user-agent'                    : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'x-trace-id'                    : 'e9d5223c-5d71-4834-8563-c253a1fc3ae8',
        'x-ui-request-trace'            : 'e9d5223c-5d71-4834-8563-c253a1fc3ae8',
    }

def get_json(uid: str):
    return     {
        'encryptedUid'                  : uid,
        'tradeType'                     : 'PERPETUAL',
}