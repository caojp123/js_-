import re
import requests
import execjs

headers = {
    'authority': 'fanyi.baidu.com',
    'method': 'POST',
    'path': '/v2transapi?from=en&to=zh',
    'scheme': 'https',
    'accept': '*/*',
   'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'content-length': '137',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'BIDUPSID=728D4BAE985AFCF3B59C78EC98999013; PSTM=1590676199; BAIDUID=1D6AA99EB40EFA5D5EDBF44AFDD92AB4:FG=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=32192_1456_31671_32139_31253_32046_32230_26350_31640; delPer=0; PSINO=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1591773709,1592358459,1592358476,1593738525; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1593738525; __yjsv5_shitong=1.0_7_ad59d5ac1e2bca17570765813bb9ee47704f_300_1593738525310_60.10.17.186_1d496b21; yjs_js_security_passport=e44e9effeedb8ab8dff4869af5151a89ac029bb1_1593738555_js',
    'origin': 'https://fanyi.baidu.com',
    'referer': 'https://fanyi.baidu.com/translate?aldtype=16047&query=apple%0D%0A&keyfrom=baidu&smartresult=dict&lang=auto2zh',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

js = """
function n(r, o) {
        for (var t = 0; t < o.length - 2; t += 3) {
            var a = o.charAt(t + 2);
            a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
            a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
            r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
        }
        return r
    }
var i=null;
function e(r) {
        var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
        if (null === o) {
            var t = r.length;
            t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
        } else {
            for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)
                "" !== e[C] && f.push.apply(f, a(e[C].split(""))),
                C !== h - 1 && f.push(o[C]);
            var g = f.length;
            g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
        }
        var u = void 0
          , l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
        u = null !== i ? i : (i = "320305.131321201" || "") || "";
        for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
            var A = r.charCodeAt(v);
            128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
            S[c++] = A >> 18 | 240,
            S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
            S[c++] = A >> 6 & 63 | 128),
            S[c++] = 63 & A | 128)
        }
        for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
            p += S[b],
            p = n(p, F);
        return p = n(p, D),
        p ^= s,
        0 > p && (p = (2147483647 & p) + 2147483648),
        p %= 1e6,
        p.toString() + "." + (p ^ m)
    }
"""
js = execjs.compile(js)
params = {
    'transtype': 'translang',
    'simple_means_flag': '3',
    # 'sign': '704513.926512',
    'token': '3cf6f25a4606f584d7b56292563b20ae',
    'domain': 'common'
}
url = 'https://fanyi.baidu.com/v2transapi'
item_list = ['apple', '苹果', '香蕉', '菠萝']
for item in item_list:

    # 正则检测是否存在汉字
    if re.findall('[\\u4E00-\\u9FA5]', item):
        params['from'] = 'zh'
        params['to'] = 'en'
    else:
        params['from'] = 'en'
        params['to'] = 'zh'
    params['query'] = item
    params['sign'] = js.call('e', item)
    url = url + '?from=' + params['from'] + 'to=' + params['to']
    response = requests.post(url=url, headers=headers, data=params).json()
    print(response)

