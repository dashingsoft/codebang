// import i18n from 'gettext.js'
let i18n = require('gettext.js').default( {
    domain: 'codebang',
    locale: 'zh-cn'
} )

let locales = [
    {
        "": {
            "language": "zh-cn",
            "plural-forms": "nplurals=2; plural=n>1;"
        },
        "CodeBang": "代码帮",
        "Code": "代码",
        "Build": "编译",
        "Launch": "运行",
        "Please input search text": "请输入搜索内容",
        "Signed in as %1": "登陆为 %1",
        "Sign in": "登陆",
        "Sign out": "注销",
        "Settings": "设置",
    }
]

locales.forEach( data => i18n.loadJSON( data, 'codebang' ) )

const I18nPlugin = {
    
    install( Vue ) {
        Vue.setLocale = function ( lang ) {
            i18n.setLocale( lang )
        },
        Vue.prototype.$t = function () {
            return i18n.gettext.apply( i18n, arguments )
        }
    }
    
}

function gettext () {
    return i18n.gettext.apply( i18n, arguments )
}

export { I18nPlugin as default, gettext as _t }
